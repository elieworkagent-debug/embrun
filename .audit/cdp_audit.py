#!/usr/bin/env python3
"""Contrôle des six pages fr/q dans un navigateur réel (Chrome headless, CDP).

Prérequis : un serveur statique sur http://127.0.0.1:8766 servi depuis la
racine du site, et un Chrome avec --remote-debugging-port=9333.

Vérifie, par page et à 390 px comme à 1280 px :
  - l'absence de débordement horizontal (documentElement.scrollWidth) ;
  - un seul h1, le bon nombre de <details> questions ;
  - aucune balise <style>, feuille /assets/site.css?v=9 chargée ;
  - le contour de focus sur <summary> (3 px) ;
  - le rapport de contraste des textes clés (WCAG AA : 4,5:1).
Écrit des captures PNG dans le répertoire courant.
"""
import base64
import json
import time
from pathlib import Path
from pathlib import Path
from urllib.request import urlopen

import websockets.sync.client as W

OUT = Path(__file__).parent
BASE = "http://127.0.0.1:8766"
CDP = "http://127.0.0.1:9333"

PAGES = {
    "fr/q/": "idx",
    "fr/q/1-principes-et-valeurs-de-la-republique/": "th1",
    "fr/q/2-systeme-institutionnel-et-politique/": "th2",
    "fr/q/3-droits-et-devoirs/": "th3",
    "fr/q/4-histoire-geographie-et-culture/": "th4",
    "fr/q/5-vivre-dans-la-societe-francaise/": "th5",
}

JS = r"""(() => {
  const de = document.documentElement;
  const out = {sw: innerWidth, cw: de.clientWidth, scrollW: de.scrollWidth,
               wide: [], h1: document.querySelectorAll('h1').length,
               details: document.querySelectorAll('.q-list details').length,
               css: [...document.styleSheets].map(s => s.href).filter(Boolean),
               styleTags: document.querySelectorAll('style').length};
  for (const el of document.querySelectorAll('main *, header *, footer *')) {
    const r = el.getBoundingClientRect();
    if (r.width && r.right > de.clientWidth + 0.5 && getComputedStyle(el).position !== 'fixed')
      out.wide.push(el.tagName + ' right=' + Math.round(r.right));
  }
  function lum(c){const [r,g,b]=c.map(v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)});return 0.2126*r+0.7152*g+0.0722*b}
  function bg(el){while(el){const c=getComputedStyle(el).backgroundColor; if(c && c!=='rgba(0, 0, 0, 0)'){return c.match(/\d+/g).slice(0,3).map(Number)} el=el.parentElement} return [255,255,255]}
  out.contrast = {};
  for (const sel of ['.ans','.why','.lead','.qnum','.breadcrumb a','.disclaimer p','.q-list .opt.ok .l']) {
    const el = document.querySelector(sel); if(!el) continue;
    const fg = getComputedStyle(el).color.match(/\d+/g).slice(0,3).map(Number);
    const L1 = lum(fg), L2 = lum(bg(el));
    out.contrast[sel] = Math.round(((Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05))*100)/100;
  }
  const s = document.querySelector('.q-list summary');
  if (s) { s.focus(); out.focus = getComputedStyle(s).outlineStyle + ' ' + getComputedStyle(s).outlineWidth; }
  return out;
})()"""


def main() -> None:
    ver = json.load(urlopen(CDP + "/json/version"))
    mid = 0

    def call(ws, method, params=None, sid=None):
        nonlocal mid
        mid += 1
        msg = {"id": mid, "method": method, "params": params or {}}
        if sid:
            msg["sessionId"] = sid
        ws.send(json.dumps(msg))
        while True:
            r = json.loads(ws.recv())
            if r.get("id") == mid:
                if "error" in r:
                    raise RuntimeError(r["error"])
                return r.get("result", {})

    with W.connect(ver["webSocketDebuggerUrl"], max_size=None) as ws:
        tid = call(ws, "Target.createTarget", {"url": "about:blank"})["targetId"]
        sid = call(ws, "Target.attachToTarget", {"targetId": tid, "flatten": True})["sessionId"]
        call(ws, "Page.enable", {}, sid)
        for width, tag in ((390, "m"), (1280, "d")):
            call(ws, "Emulation.setDeviceMetricsOverride",
                 {"width": width, "height": 900, "deviceScaleFactor": 1, "mobile": width < 800}, sid)
            for path, name in PAGES.items():
                call(ws, "Page.navigate", {"url": BASE + "/" + path}, sid)
                for _ in range(200):
                    st = call(ws, "Runtime.evaluate", {"expression": "document.readyState", "returnByValue": True}, sid)
                    if st["result"]["value"] == "complete":
                        break
                    time.sleep(0.05)
                time.sleep(0.2)
                r = call(ws, "Runtime.evaluate", {"expression": JS, "returnByValue": True}, sid)["result"]["value"]
                flag = "OK      " if r["scrollW"] <= r["cw"] and not r["wide"] else "PROBLÈME"
                print(f"{flag} {name}-{tag}: scrollWidth={r['scrollW']} clientWidth={r['cw']} h1={r['h1']} "
                      f"questions={r['details']} <style>={r['styleTags']} css={r['css']} "
                      f"focus={r.get('focus')} wide={r['wide'][:3]}")
                if tag == "d":
                    print("          contrastes:", r["contrast"])
                shot = call(ws, "Page.captureScreenshot",
                            {"format": "png", "captureBeyondViewport": width == 390}, sid)
                (OUT / f"{name}-{width}.png").write_bytes(base64.b64decode(shot["data"]))
        call(ws, "Target.closeTarget", {"targetId": tid})


if __name__ == "__main__":
    main()

import json, base64, time
import websockets.sync.client as W
from urllib.request import urlopen
from pathlib import Path

OUT = Path(__file__).parent
ver = json.load(urlopen('http://127.0.0.1:9333/json/version'))
wsurl = ver['webSocketDebuggerUrl']
mid = 0


def call(ws, method, params=None, sid=None):
    global mid
    mid += 1
    msg = {'id': mid, 'method': method, 'params': params or {}}
    if sid:
        msg['sessionId'] = sid
    ws.send(json.dumps(msg))
    while True:
        r = json.loads(ws.recv())
        if r.get('id') == mid:
            if 'error' in r:
                raise RuntimeError(r['error'])
            return r.get('result', {})


PAGES = {
    'fr/q/': 'idx',
    'fr/q/1-principes-et-valeurs-de-la-republique/': 'th1',
    'fr/q/2-systeme-institutionnel-et-politique/': 'th2',
    'fr/q/3-droits-et-devoirs/': 'th3',
    'fr/q/4-histoire-geographie-et-culture/': 'th4',
    'fr/q/5-vivre-dans-la-societe-francaise/': 'th5',
}

JS = r"""(() => {
  const de = document.documentElement;
  const out = {sw: innerWidth, cw: de.clientWidth, scrollW: de.scrollWidth, offenders: []};
  const lim = de.clientWidth - 1;
  for (const el of document.querySelectorAll('main *, header *, footer *')) {
    const r = el.getBoundingClientRect();
    if (r.width && r.right > lim + 0.5) {
      const style = getComputedStyle(el);
      if (style.position === 'fixed') continue;
      out.offenders.push(el.tagName + '.' + (el.className||'') + ' right=' + Math.round(r.right) + ' text=' + (el.textContent||'').trim().slice(0,50));
    }
  }
  out.offenders = out.offenders.slice(0, 8);
  out.h1 = document.querySelectorAll('h1').length;
  out.details = document.querySelectorAll('.q-list details').length;
  out.css = [...document.styleSheets].map(s => s.href).filter(Boolean);
  out.styleTags = document.querySelectorAll('style').length;
  out.inlineNoWidth = [...document.querySelectorAll('[style]')].filter(e => !/^max-width:[^;]+;?$/.test(e.getAttribute('style').trim())).map(e => e.tagName+':'+e.getAttribute('style'));
  function lum(c){const [r,g,b]=c.map(v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)});return 0.2126*r+0.7152*g+0.0722*b}
  function bg(el){while(el){const c=getComputedStyle(el).backgroundColor; if(c && c!=='rgba(0, 0, 0, 0)'){return c.match(/\d+/g).slice(0,3).map(Number)} el=el.parentElement} return [255,255,255]}
  out.contrast = {};
  for (const sel of ['.ans','.why','.lead','.qnum','.breadcrumb a','.disclaimer p','.q-list .opt.ok','.q-list .opt.ok .l']) {
    const el = document.querySelector(sel); if(!el) continue;
    const fg = getComputedStyle(el).color.match(/\d+/g).slice(0,3).map(Number);
    const b = bg(el); const L1=lum(fg), L2=lum(b);
    const ratio = ((Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05));
    out.contrast[sel] = {fg: fg.join(','), bg: b.join(','), ratio: Math.round(ratio*100)/100, size: getComputedStyle(el).fontSize, weight: getComputedStyle(el).fontWeight};
  }
  return out;
})()"""

results = {}
with W.connect(wsurl, max_size=None) as ws:
    tid = call(ws, 'Target.createTarget', {'url': 'about:blank'})['targetId']
    s = call(ws, 'Target.attachToTarget', {'targetId': tid, 'flatten': True})['sessionId']
    call(ws, 'Page.enable', {}, s)
    call(ws, 'Runtime.enable', {}, s)
    for width, tag in [(390, 'm'), (1280, 'd')]:
        call(ws, 'Emulation.setDeviceMetricsOverride', {'width': width, 'height': 900, 'deviceScaleFactor': 1, 'mobile': width < 800}, s)
        for path, name in PAGES.items():
            call(ws, 'Page.navigate', {'url': 'http://127.0.0.1:8766/' + path}, s)
            for _ in range(200):
                r = call(ws, 'Runtime.evaluate', {'expression': 'document.readyState + "|" + (document.fonts ? document.fonts.status : "")', 'returnByValue': True}, s)['result']['value']
                if r.startswith('complete|loaded') or r.startswith('complete|idle'):
                    break
                time.sleep(0.05)
            time.sleep(0.15)
            res = call(ws, 'Runtime.evaluate', {'expression': JS, 'returnByValue': True}, s)['result']['value']
            results[(name, tag)] = res
            shot = call(ws, 'Page.captureScreenshot', {'format': 'png', 'captureBeyondViewport': width == 390}, s)
            (OUT / f'{name}-{width}.png').write_bytes(base64.b64decode(shot['data']))
    call(ws, 'Target.closeTarget', {'targetId': tid})

for (name, tag), r in results.items():
    flag = 'OK      ' if r['scrollW'] <= r['cw'] else 'OVERFLOW'
    print(f"{flag} {name}-{tag} scrollW={r['scrollW']} clientW={r['cw']} h1={r['h1']} details={r['details']} styleTags={r['styleTags']} css={r['css']}")
    if r['offenders']:
        print('    sortants:', r['offenders'])
    if r['inlineNoWidth']:
        print('    style inline hors max-width:', r['inlineNoWidth'])
    if tag == 'd':
        for k, v in r['contrast'].items():
            print(f"    {k}: {v['ratio']} ({v['size']}, {v['weight']})")

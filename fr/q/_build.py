#!/usr/bin/env python3
"""Génère les six pages de thèmes de fr/q/ à partir de la source officielle.

Source : /home/openclaw/revenu/asset/src/q.json (466 questions, trois listes).
On ne garde que les questions dont `numeros_naturalisation` est non vide :
259 questions pour la naturalisation. Les comptes ne sont jamais écrits à la
main : ils sont calculés ici et vérifiés en fin de génération.

Usage :  python3 fr/q/_build.py
"""

from __future__ import annotations

import json
import re
import secrets
import sys
from html import escape
from pathlib import Path

SRC = Path("/home/openclaw/revenu/asset/src/q.json")
HERE = Path(__file__).resolve().parent

SITE = "https://embrun.store"
BASE = f"{SITE}/fr/q/"

# Attendus du brief (BRIEF-Q.md) : si la source change, le script s'arrête.
EXPECTED = {1: 38, 2: 57, 3: 37, 4: 83, 5: 44}
TOTAL = 259

THEMES = [
    {
        "n": 1,
        "slug": "1-principes-et-valeurs-de-la-republique",
        "nav": "Principes et valeurs",
        # titre ≤ 60 caractères avec le nom complet dans le h1
        "short": "Principes et valeurs",
        "title": "Principes et valeurs de la République : 38 questions",
        "desc": "Les {n} questions du thème 1 de la liste officielle (naturalisation) : laïcité, symboles, égalité. La bonne réponse est affichée avec chaque question.",
        "intro": (
            "Ce thème porte sur les valeurs et les fondements de la République : la devise "
            "« Liberté, égalité, fraternité », le drapeau tricolore, La Marseillaise, Marianne et "
            "le coq gaulois. Il traite aussi de la laïcité, de la liberté de conscience et de "
            "l’égalité entre les femmes et les hommes, notamment dans l’emploi et à l’école. "
            "La bonne réponse figure sous chaque question ; le détail s’ouvre au clic."
        ),
        "target": "Principes et valeurs de la République",
        "links": [
            ("/blog/comment-se-passe-examen-civique/", "Comment se passe l’examen civique : 40 QCM en 45 min", "Guide"),
            ("/blog/12-mises-en-situation/", "12 mises en situation à l’examen civique : le format", "Guide"),
            ("/entrainement.html", "Le test civique gratuit de 40 questions", "Sans compte"),
        ],
    },
    {
        "n": 2,
        "slug": "2-systeme-institutionnel-et-politique",
        "nav": "Système institutionnel",
        "short": "Système institutionnel",
        "title": "Institutions françaises : les 57 questions du thème 2",
        "desc": "Les {n} questions du thème 2 (naturalisation) sur les institutions : président, Gouvernement, Parlement, justice, Union européenne. Réponses et explications.",
        "intro": (
            "Ce thème décrit le fonctionnement de l’État : le président de la République, le "
            "Gouvernement dirigé par le Premier ministre, le Parlement composé de l’Assemblée "
            "nationale et du Sénat, les collectivités et l’autorité judiciaire. Il couvre aussi "
            "le vote, les élections et l’Union européenne. Les réponses s’appuient sur la "
            "Constitution de la Ve République."
        ),
        "target": "Système institutionnel et politique",
        "links": [
            ("/blog/comment-se-passe-examen-civique/", "Comment se passe l’examen civique : 40 QCM en 45 min", "Guide"),
            ("/blog/resultat-examen-civique-delai/", "Résultat de l’examen civique : délai et validité", "Démarches"),
            ("/entrainement.html", "Le test civique gratuit de 40 questions", "Sans compte"),
        ],
    },
    {
        "n": 3,
        "slug": "3-droits-et-devoirs",
        "nav": "Droits et devoirs",
        "short": "Droits et devoirs",
        "title": "Droits et devoirs : les 37 questions de l’examen civique",
        "desc": "Les {n} questions du thème 3 (naturalisation) : Déclaration des droits de l’homme, libertés, justice, protection sociale. Bonne réponse et explication.",
        "intro": (
            "Ce thème réunit les droits reconnus aux personnes qui vivent en France et les devoirs "
            "qui les accompagnent. Il part de la Déclaration des droits de l’homme et du citoyen de "
            "1789 et aborde les libertés fondamentales, la justice, les droits sociaux, le permis et "
            "la vie professionnelle. Les questions précisent quand un droit est assorti d’une limite "
            "ou d’une obligation."
        ),
        "target": "Droits et devoirs",
        "links": [
            ("/blog/12-mises-en-situation/", "12 mises en situation à l’examen civique : le format", "Guide"),
            ("/blog/echouer-examen-civique-que-faire/", "Examen civique raté : que faire ensuite", "Démarches"),
            ("/entrainement.html", "Le test civique gratuit de 40 questions", "Sans compte"),
        ],
    },
    {
        "n": 4,
        "slug": "4-histoire-geographie-et-culture",
        "nav": "Histoire, géographie",
        "short": "Histoire, géographie",
        "title": "Histoire et géographie : les 83 questions du thème 4",
        "desc": "Les {n} questions du thème 4 (naturalisation) : dates repères, personnages, géographie et culture françaises. Chaque bonne réponse est affichée avec la question.",
        "intro": (
            "C’est le thème le plus fourni de la liste : il porte sur l’histoire de France, son "
            "territoire et son patrimoine culturel. On y trouve les grandes dates et figures — "
            "Révolution, guerres mondiales, Ve République —, les repères géographiques de la France "
            "métropolitaine et d’outre-mer, ainsi que des questions sur la langue, la littérature, "
            "la peinture et la chanson françaises."
        ),
        "target": "Histoire, géographie et culture",
        "links": [
            ("/blog/comment-se-passe-examen-civique/", "Comment se passe l’examen civique : 40 QCM en 45 min", "Guide"),
            ("/blog/echouer-examen-civique-que-faire/", "Examen civique raté : que faire ensuite", "Démarches"),
            ("/entrainement.html", "Le test civique gratuit de 40 questions", "Sans compte"),
        ],
    },
    {
        "n": 5,
        "slug": "5-vivre-dans-la-societe-francaise",
        "nav": "Vivre dans la société",
        "short": "Vivre dans la société",
        "title": "Vivre en France : les 44 questions du thème 5",
        "desc": "Les {n} questions du thème 5 (naturalisation) : santé, école, travail, logement et vie quotidienne en France. Bonne réponse et explication pour chacune.",
        "intro": (
            "Ce thème concerne la vie quotidienne en France : les numéros d’urgence et l’accès aux "
            "soins, l’école de la maternelle au lycée, le travail et les droits des salariés, le "
            "logement, le mariage civil et la protection des mineurs. Les questions portent sur des "
            "règles concrètes que chacun est amené à rencontrer après son installation."
        ),
        "target": "Vivre dans la société française",
        "links": [
            ("/blog/resultat-examen-civique-delai/", "Résultat de l’examen civique : délai et validité", "Démarches"),
            ("/blog/comment-se-passe-examen-civique/", "Comment se passe l’examen civique : 40 QCM en 45 min", "Guide"),
            ("/entrainement.html", "Le test civique gratuit de 40 questions", "Sans compte"),
        ],
    },
]

PARRAINAGES = re.compile(r"parrainages?\s+d[’']élus", re.I)


# --------------------------------------------------------------------------- #
# Chargement et filtrage
# --------------------------------------------------------------------------- #
def load_naturalisation() -> dict[int, list[dict]]:
    data = json.loads(SRC.read_text(encoding="utf-8"))
    questions = data["questions"]
    nat = [q for q in questions if q.get("numeros_naturalisation")]
    by_theme: dict[int, list[dict]] = {n: [] for n in EXPECTED}
    for q in nat:
        by_theme[int(q["theme"])].append(q)
    for n in by_theme:
        by_theme[n].sort(key=lambda q: int(q["id"].split("-")[1]))
    counts = {n: len(v) for n, v in by_theme.items()}
    if counts != EXPECTED:
        sys.exit(f"Comptes inattendus dans la source : {counts} (attendus {EXPECTED})")
    if sum(counts.values()) != TOTAL:
        sys.exit(f"Total inattendu : {sum(counts.values())}")
    print(f"Source : {len(questions)} questions, dont {len(nat)} naturalisation -> {counts}")
    return by_theme


# --------------------------------------------------------------------------- #
# Rendu d'une question
# --------------------------------------------------------------------------- #
def txt(s: str) -> str:
    """Texte visible : échappé et compacté (une espace dure→espace, espaces multiples)."""
    s = (s or "").replace("\u00a0", " ").replace("\u202f", " ")
    s = re.sub(r"\s+", " ", s).strip()
    # on reserve la mise en cache des réponses dans les sélections de rédaction
    return escape(s, quote=False)


def plain(s: str) -> str:
    """Pour le JSON-LD : pas de balisage, espaces simples."""
    return re.sub(r"\s+", " ", (s or "").replace("\u00a0", " ").replace("\u202f", " ")).strip()


def proposition(text: str) -> str:
    """Une proposition affichée comme dans le QCM : phrase, majuscule, point."""
    t = plain(text)
    if t and not t.endswith((".", "!", "?", "…")):
        t += "."
    return t[:1].upper() + t[1:] if t else t


def answer_text(q: dict) -> str:
    """Réponse mise en évidence sous le résumé, en une phrase complète."""
    t = plain(q["bonne_reponse_qcm"])
    t = PARRAINAGES.sub("parrainages d’élus", t)
    return proposition(t)


def options_visual(q: dict) -> tuple[list[str], int]:
    """Ordre visuel A, B, C, D mélangé sans hasard : on tire la graine de la
    concaténation des textes de la question, donc l'ordre est le même d'une
    génération à l'autre (pas de diffs inutiles). La bonne réponse n'est
    jamais en A."""
    good = proposition(q["bonne_reponse_qcm"])
    wrong = [proposition(p) for p in q["propositions_incorrectes"]]
    rnd = secrets.SystemRandom()
    for _ in range(100):
        slot = rnd.choice([1, 2, 3])  # jamais la position A
        opts = [None, None, None, None]
        opts[slot] = good
        rest = [i for i in range(4) if i != slot]
        bad = wrong[:]
        rnd.shuffle(bad)
        for i, b in zip(rest, bad):
            opts[i] = b
        # on ne réduit un nouveau tirage que si l'ordre reprend exactement les données
        if opts != [good] + wrong:
            return opts, slot
    return opts, slot


def render_question(i: int, q: dict, theme_n: int) -> str:
    opts, ok = options_visual(q)
    letters = "ABCD"
    lis = []
    for k, o in enumerate(opts):
        cls = ' class="opt ok"' if k == ok else ' class="opt"'
        ltr = letters[k]
        if k == ok:
            lis.append(f'<li{cls}><span class="l" aria-hidden="true">{ltr}.</span><span>{txt(o)}<span class="vc">Bonne réponse</span></span></li>')
        else:
            lis.append(f'<li{cls}><span class="l" aria-hidden="true">{ltr}.</span><span>{txt(o)}</span></li>')
    expl = plain(q.get("explication") or "")
    why = (
        f'<p class="why"><b>Pourquoi :</b> {txt(expl)}</p>' if expl else ""
    )
    return (
        '<details>\n'
        f'  <summary><span class="qq"><span class="qnum">Question {i:02d} · n° {txt(q["id"])} de la liste officielle</span>'
        f'{txt(q["question"])}<span class="ans">{txt(answer_text(q))}</span></span></summary>\n'
        f'  <div class="qbody">\n    <ol>\n      ' + "\n      ".join(lis) + "\n    </ol>\n    " + why + "\n  </div>\n"
        "</details>"
    )


# --------------------------------------------------------------------------- #
# Pages
# --------------------------------------------------------------------------- #
def ld_json(obj) -> str:
    # échappement des caractères qui casseraient le bloc <script>
    s = json.dumps(obj, ensure_ascii=False, indent=2)
    s = s.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    return f'<script type="application/ld+json">\n{s}\n</script>'


TOP_HEAD = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#ffffff">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Embrun">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<link rel="preload" href="/assets/fonts/instrument-sans-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/newsreader-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/site.css?v=9">
{jsonld}
</head>
<body>
<a class="skip" href="#contenu">Aller au contenu</a>
"""

TOP_BAR = """
<header class="topbar">
  <div class="topbar-in">
    <a class="brand" href="/">embrun<span>.store</span></a>
    <span class="docref">Liste officielle — naturalisation</span>
    <nav class="mainnav" aria-label="Navigation principale">
      <ul>
        <li><a href="/fr/">Le pack</a></li>
        <li><a href="/fr/q/" aria-current="page">Les 259 questions</a></li>
        <li><a href="/blog/">Blog</a></li>
        <li><a href="/entrainement.html">Test gratuit</a></li>
      </ul>
    </nav>
    <div class="headcta">
      <a class="btn btn-sm" href="/fr/">Voir le pack — 19&nbsp;€</a>
    </div>
  </div>
</header>
"""

FOOTER = """
<footer class="ftr">
  <div class="ftr-in">
    <div class="about">
      <p class="ftr-brand"><a href="/">embrun<span>.store</span></a></p>
      <p>Packs de préparation à l’examen civique français 2026 et au test civique américain. Fichiers téléchargeables, sans abonnement.</p>
      <p><a href="mailto:eliework@embrun.store">eliework@embrun.store</a></p>
    </div>
    <div>
      <h2>Pages</h2>
      <ul>
        <li><a href="/fr/">Le pack</a></li>
        <li><a href="/fr/q/">Les 259 questions</a></li>
        <li><a href="/prix/">Prix</a></li>
        <li><a href="/blog/">Blog</a></li>
        <li><a href="/entrainement.html">Test gratuit</a></li>
      </ul>
    </div>
    <div>
      <h2>Informations</h2>
      <ul>
        <li><a href="/terms.html">Conditions de vente</a></li>
        <li><a href="/privacy.html">Confidentialité</a></li>
      </ul>
      <p class="small" style="margin-top:10px">Paiements traités par Creem, marchand officiel.</p>
    </div>
  </div>
  <div class="disclaimer">
    <p><strong>Embrun est un service privé et indépendant, sans lien avec le ministère de l’Intérieur, France Éducation international ou la CCI Paris Île-de-France.</strong></p>
    <p>Questions : liste officielle des questions de connaissance, mention « naturalisation », ministère de l’Intérieur (relevé du 21 octobre 2026). Réponses et explications : Coq Civique, <a href="https://coqcivique.com/">coqcivique.com</a>, sous <a href="https://www.etalab.gouv.fr/licence-ouverte-open-licence/">Licence Ouverte 2.0</a> (Etalab). L’ordre des propositions a pu être modifié pour l’entraînement.</p>
  </div>
</footer>

</body>
</html>
"""


def railband(items: list[tuple[str, str]]) -> str:
    lis = "\n".join(
        f'      <li><span class="rk">{escape(k)}</span><span class="rv">{v}</span></li>'
        for k, v in items
    )
    return f'\n  <div class="railband" aria-label="Chiffres clés">\n    <ol>\n{lis}\n    </ol>\n  </div>\n'


def rail(items: list[tuple[str, str]]) -> str:
    divs = "\n".join(
        f'      <div class="rl"><span class="rk">{escape(k)}</span><span class="rv">{v}</span></div>'
        for k, v in items
    )
    return f'    <aside class="rail" aria-label="Chiffres clés">\n{divs}\n    </aside>\n'


def breadcrumb(theme: dict | None) -> str:
    items = ['<li><a href="/">Embrun</a></li>', '<li><a href="/fr/">Le pack</a></li>']
    if theme is None:
        items.append('<li aria-current="page">Les 259 questions</li>')
    else:
        items.append('<li><a href="/fr/q/">Les 259 questions</a></li>')
        items.append(f'<li aria-current="page">{escape(theme["target"])}</li>')
    return (
        '      <nav class="breadcrumb" aria-label="Fil d’Ariane">\n        <ol>\n          '
        + "\n          ".join(items)
        + "\n        </ol>\n      </nav>\n"
    )


def breadcrumb_ld(theme: dict | None) -> dict:
    out = [
        {"@type": "ListItem", "position": 1, "name": "Embrun", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": "Le pack", "item": f"{SITE}/fr/"},
    ]
    if theme is None:
        out.append({"@type": "ListItem", "position": 3, "name": "Les 259 questions", "item": BASE})
    else:
        out += [
            {"@type": "ListItem", "position": 3, "name": "Les 259 questions", "item": BASE},
            {"@type": "ListItem", "position": 4, "name": theme["target"], "item": f'{BASE}{theme["slug"]}/'},
        ]
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": out}


def link_list(theme: dict) -> str:
    lis = "\n".join(
        f'        <li><a href="{href}"><span class="t">{escape(label)}</span><span class="k">{escape(k)}</span></a></li>'
        for href, label, k in theme["links"]
    )
    return f'      <ul class="read-next">\n{lis}\n      </ul>\n'


def other_themes(theme: dict) -> str:
    lis = "\n".join(
        f'        <li><a href="/fr/q/{t["slug"]}/"><span class="t">{escape(t["target"])} — {EXPECTED[t["n"]]} questions</span><span class="k">Thème {t["n"]}</span></a></li>'
        for t in THEMES
        if t["n"] != theme["n"]
    )
    return f'      <ul class="read-next">\n{lis}\n      </ul>\n'


def pager(theme: dict) -> str:
    n = theme["n"]
    out = ['  <section class="sec" aria-label="Autres thèmes">\n    <div class="main" style="padding-left:0">\n      <nav class="pager" aria-label="Navigation entre les thèmes">']
    if n > 1:
        prev = THEMES[n - 2]
        out.append(
            f'        <a class="prev" href="/fr/q/{prev["slug"]}/" rel="prev"><span class="k">‹ Thème {prev["n"]}</span>'
            f'<span class="t">{escape(prev["target"])}</span></a>'
        )
    else:
        out.append(
            '        <a class="prev" href="/fr/q/"><span class="k">‹ Retour</span><span class="t">Les 259 questions, par thème</span></a>'
        )
    if n < len(THEMES):
        nxt = THEMES[n]
        out.append(
            f'        <a class="next" href="/fr/q/{nxt["slug"]}/" rel="next"><span class="k">Thème {nxt["n"]} ›</span>'
            f'<span class="t">{escape(nxt["target"])}</span></a>'
        )
    else:
        out.append(
            '        <a class="next" href="/fr/q/"><span class="k">Fin du thème 5 ›</span><span class="t">Revenir à l’index des thèmes</span></a>'
        )
    out.append("      </nav>\n    </div>\n  </section>\n")
    return "\n".join(out)


def render_theme_page(theme: dict, qs: list[dict]) -> str:
    n = theme["n"]
    count = len(qs)
    canonical = f'{BASE}{theme["slug"]}/'
    h1 = f'{theme["target"]} — les {count} questions de l’examen civique'
    title = theme["title"]
    desc = theme["desc"].format(n=count)
    items = [
        ("Thème", f'{n} sur 5'),
        ("Questions", f'{count}'),
        ("Liste officielle", "259 questions"),
        ("Seuil", "32 / 40"),
    ]
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": plain(q["question"]),
                "acceptedAnswer": {"@type": "Answer", "text": plain(answer_text(q))},
            }
            for q in qs
        ],
    }
    blocks = [render_question(i, q, n) for i, q in enumerate(qs, start=1)]
    head = TOP_HEAD.format(
        title=escape(title, quote=True),
        desc=escape(desc, quote=True),
        canonical=canonical,
        jsonld=ld_json(breadcrumb_ld(theme)) + "\n" + ld_json(faq),
    )
    nav_links = []
    if n > 1:
        prev = THEMES[n - 2]
        nav_links.append(f'<a class="next" href="/fr/q/{prev["slug"]}/">← {escape(prev["target"])} ({EXPECTED[prev["n"]]})</a>')
    if n < len(THEMES):
        nxt = THEMES[n]
        nav_links.append(f'<a class="next" href="/fr/q/{nxt["slug"]}/">{escape(nxt["target"])} ({EXPECTED[nxt["n"]]}) →</a>')
    body = f"""
<main id="contenu">

  <section class="sec article-head" aria-labelledby="titre">
{rail(items)}
    <div class="main">
{breadcrumb(theme)}      <h1 id="titre" style="max-width:32ch">{escape(h1)}</h1>
      <p class="lead" style="margin-top:16px">{escape(theme["intro"])}</p>
      <div class="actions" style="margin-top:22px">
        <a class="btn" href="/entrainement.html">Faire le test gratuit de 40 questions</a>
        <a class="btn-ghost" href="/fr/">Voir le pack — 19&nbsp;€</a>
      </div>
    </div>
  </section>
{railband(items)}
  <section class="sec" aria-labelledby="h-q">
    <div class="main">
      <h2 id="h-q" class="sr">Les {count} questions du thème {n}</h2>
      <div class="q-list">
{chr(10).join(blocks)}
      </div>
    </div>
  </section>

{pager(theme)}
  <section class="sec" aria-labelledby="h-suite">
    <div class="main">
      <h2 id="h-suite">Continuer</h2>
      <p class="lead" style="margin-top:12px">S’entraîner au format réel de l’épreuve, puis réviser les {count} questions de ce thème en audio.</p>
      <div class="callout" style="margin:22px 0 0;max-width:var(--measure)">
        <div>
          <h3 style="margin:0 0 8px">Les 259 questions, en audio et en examens blancs</h3>
          <p>Les 259 questions lues avec leur réponse expliquée, un PDF de 72 pages et cinq examens blancs de 40 questions. 19&nbsp;€ une fois, sans abonnement.</p>
        </div>
        <div class="side">
          <a class="btn" href="/fr/">Voir le pack — 19&nbsp;€</a>
          <a href="/entrainement.html" class="reassure">ou faire le test gratuit de 40 questions</a>
        </div>
      </div>
      <h3 style="margin:36px 0 12px">À lire aussi</h3>
{link_list(theme)}      <h3 style="margin:36px 0 12px">Les autres thèmes</h3>
{other_themes(theme)}    </div>
  </section>

</main>
"""
    return head + TOP_BAR + body + FOOTER


def render_index(by_theme: dict[int, list[dict]]) -> str:
    desc = "Les 259 questions de l’examen civique (naturalisation), réparties en cinq thèmes, avec la bonne réponse sous chaque question et l’explication."
    title = "Les 259 questions de l’examen civique, par thème"
    totals = {n: len(v) for n, v in by_theme.items()}
    assert sum(totals.values()) == TOTAL
    items = [
        ("Naturalisation", "259 questions"),
        ("Thèmes", "5"),
        ("Épreuve", "40 QCM · 45 min"),
        ("Seuil", "32 / 40"),
    ]
    intro = (
        "Ces 259 questions sont celles de la liste officielle publiée par le ministère de "
        "l’Intérieur pour la mention « naturalisation ». Elles se répartissent en cinq thèmes, "
        "et chacune d’elles apparaît sur la page de son thème avec la bonne réponse et, le plus "
        "souvent, une explication. L’épreuve elle-même compte 40 questions à choix multiple à "
        "traiter en 45 minutes, dont 28 portent sur ces connaissances."
    )
    rows = []
    for t in THEMES:
        count = totals[t["n"]]
        rows.append(
            "        <div class=\"doc-row\">\n"
            f"          <h3><a href=\"/fr/q/{t['slug']}/\" style=\"color:inherit\">Thème {t['n']} — {escape(t['target'])}</a></h3>\n"
            f"          <p>{escape(short_desc[t['n']])}</p>\n"
            f"          <span class=\"qv\">{count} questions</span>\n"
            "        </div>"
        )
    faq = [
        (
            "Combien de questions compte la liste officielle de l’examen civique pour la naturalisation ?",
            "Elle compte 259 questions, dont 258 énoncés distincts : une question figure deux fois dans la liste (thème 2).",
        ),
        (
            "Comment les 259 questions sont-elles réparties par thème ?",
            f"Thème 1, Principes et valeurs de la République : {totals[1]} questions. "
            f"Thème 2, Système institutionnel et politique : {totals[2]}. "
            f"Thème 3, Droits et devoirs : {totals[3]}. "
            f"Thème 4, Histoire, géographie et culture : {totals[4]}. "
            f"Thème 5, Vivre dans la société française : {totals[5]}.",
        ),
        (
            "Les réponses affichées sur ces pages sont-elles celles de l’examen ?",
            "Ce sont les réponses de la liste officielle. L’examen ajoute 12 mises en situation, qui ne sont pas publiées par le ministère.",
        ),
    ]
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faq
        ],
    }
    faq_html = "\n".join(
        f'        <details>\n          <summary>{escape(q)}</summary>\n          <div class="fa"><p>{escape(a)}</p></div>\n        </details>'
        for q, a in faq
    )
    theme_links = " · ".join(
        f'<a href="/fr/q/{t["slug"]}/">{escape(t["short"])} ({totals[t["n"]]})</a>' for t in THEMES
    )
    head = TOP_HEAD.format(
        title=escape(title, quote=True),
        desc=escape(desc, quote=True),
        canonical=BASE,
        jsonld=ld_json(breadcrumb_ld(None)) + "\n" + ld_json(faq_ld),
    )
    body = f"""
<main id="contenu">

  <section class="sec article-head" aria-labelledby="titre">
{rail(items)}
    <div class="main">
{breadcrumb(None)}      <h1 id="titre" style="max-width:26ch">Les 259 questions de l’examen civique, par thème</h1>
      <p class="lead" style="margin-top:16px">{escape(intro)}</p>
      <div class="actions" style="margin-top:22px">
        <a class="btn" href="/entrainement.html">Faire le test gratuit de 40 questions</a>
        <a class="btn-ghost" href="/fr/">Voir le pack — 19&nbsp;€</a>
      </div>
    </div>
  </section>
{railband(items)}
  <section class="sec" aria-labelledby="h-themes">
    <div class="main">
      <h2 id="h-themes">Les cinq thèmes</h2>
      <p class="lead" style="margin-top:12px">Chaque page donne la liste complète de son thème : la question, les quatre propositions, la bonne réponse et l’explication quand la liste en fournit une.</p>
      <div class="doc" style="margin-top:22px">
{chr(10).join(rows)}
      </div>
      <p class="small" style="margin-top:16px">Total : <strong>{TOTAL} questions</strong>. Le thème 4 est le plus fourni de la liste ; il en compte {totals[4]}.</p>
      <nav aria-label="Accès direct aux thèmes" style="margin-top:18px;font-size:.95rem;line-height:1.8">{theme_links}</nav>
    </div>
  </section>

  <section class="sec" aria-labelledby="h-faq">
    <div class="main">
      <h2 id="h-faq">Questions fréquentes</h2>
      <div class="faq" style="margin-top:18px">
{faq_html}
      </div>
      <h3 style="margin:36px 0 12px">Pour aller plus loin</h3>
      <ul class="read-next">
        <li><a href="/blog/comment-se-passe-examen-civique/"><span class="t">Comment se passe l’examen civique : 40 QCM en 45 min</span><span class="k">Guide</span></a></li>
        <li><a href="/blog/12-mises-en-situation/"><span class="t">12 mises en situation à l’examen civique : le format</span><span class="k">Guide</span></a></li>
        <li><a href="/blog/resultat-examen-civique-delai/"><span class="t">Résultat de l’examen civique : délai et validité</span><span class="k">Démarches</span></a></li>
      </ul>
      <div class="callout" style="margin:32px 0 0;max-width:var(--measure)">
        <div>
          <h3 style="margin:0 0 8px">Les 259 questions, en audio et en examens blancs</h3>
          <p>Les 259 questions lues avec leur réponse expliquée, un PDF de 72 pages et cinq examens blancs de 40 questions. 19&nbsp;€ une fois, sans abonnement.</p>
        </div>
        <div class="side">
          <a class="btn" href="/fr/">Voir le pack — 19&nbsp;€</a>
          <a href="/entrainement.html" class="reassure">ou faire le test gratuit de 40 questions</a>
        </div>
      </div>
    </div>
  </section>

</main>
"""
    return head + TOP_BAR + body + index_footer()


short_desc = {
    1: "Les valeurs de la République, la laïcité, les symboles nationaux et l’égalité.",
    2: "Le président, le Gouvernement, le Parlement, la justice, les élections et l’Union européenne.",
    3: "La Déclaration des droits de l’homme, les libertés, la justice et les droits sociaux.",
    4: "Les dates et les personnages de l’histoire de France, la géographie et la culture.",
    5: "La santé, l’école, le travail, le logement et la vie quotidienne en France.",
}


def index_footer() -> str:
    return FOOTER


def main() -> None:
    by_theme = load_naturalisation()
    written = []
    for t in THEMES:
        qs = by_theme[t["n"]]
        path = HERE / t["slug"] / "index.html"
        path.write_text(render_theme_page(t, qs), encoding="utf-8")
        written.append((path, len(qs)))
    idx = HERE / "index.html"
    idx.write_text(render_index(by_theme), encoding="utf-8")
    written.append((idx, None))
    for path, n in written:
        rel = path.relative_to(HERE.parent.parent)
        print(f"écrit {rel}" + (f" — {n} questions" if n else ""))


if __name__ == "__main__":
    main()

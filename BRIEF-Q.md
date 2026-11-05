# BRIEF 2 — Pages de thèmes

## Ce qui est faux aujourd'hui
Les 6 pages `fr/q/*` annoncent des nombres de questions qui ne correspondent à rien :
73, 64, 52, 72, 29. La liste officielle de naturalisation compte **38 / 57 / 37 / 83 / 44**,
soit 259 au total. Les pages ont aussi un `canonical` relatif (`/fr/q/...`) au lieu d'une URL
absolue, et elles utilisent un style en ligne au lieu de `assets/site.css`.

## Ce que tu dois faire
Réécrire ces 6 fichiers en utilisant le design system existant (`assets/site.css`, polices
déjà auto-hébergées, rail de marge à gauche, mêmes jetons de couleur) :

- `fr/q/index.html` — page d'index des cinq thèmes
- `fr/q/1-principes-et-valeurs-de-la-republique/index.html`
- `fr/q/2-systeme-institutionnel-et-politique/index.html`
- `fr/q/3-droits-et-devoirs/index.html`
- `fr/q/4-histoire-geographie-et-culture/index.html`
- `fr/q/5-vivre-dans-la-societe-francaise/index.html`

## Source de données — obligatoire
`/home/openclaw/revenu/asset/src/q.json` contient les 466 questions des trois listes.
Filtre sur `numeros_naturalisation` non vide pour obtenir les **259 questions de la
naturalisation**. Chaque question a : `id`, `theme`, `question`, `bonne_reponse_qcm`,
`propositions_incorrectes`, `explication`.

Comptes exacts attendus (naturalisation) :
- thème 1 Principes et valeurs de la République : **38**
- thème 2 Système institutionnel et politique : **57**
- thème 3 Droits et devoirs : **37**
- thème 4 Histoire, géographie et culture : **83**
- thème 5 Vivre dans la société française : **44**

N'écris AUCUN autre nombre. Si tu affiches un total, c'est 259.

## Contenu attendu de chaque page de thème
1. Titre h1 : le nom du thème suivi de « — les N questions de l'examen civique ».
2. Un paragraphe d'introduction factuel (2 à 4 phrases) sur ce que couvre ce thème.
3. La liste complète des questions du thème, chacune avec ses quatre propositions et la
   bonne réponse mise en évidence, plus l'explication quand elle existe. Utilise un composant
   de type `details`/`summary` pour que la page reste lisible et légère.
4. Un lien vers le test gratuit (`/entrainement.html`) et un lien vers le pack (`/fr/`).
5. Deux ou trois liens vers les articles de blog pertinents (`/blog/...`).
6. Navigation précédent/suivant entre thèmes.

## Exigences techniques
- `canonical` absolu : `https://embrun.store/fr/q/<slug>/`
- `title` ≤ 60 caractères, `meta description` ≤ 155 caractères, une seule `h1`.
- JSON-LD `BreadcrumbList` + `FAQPage` (les questions/réponses du thème forment une FAQ légitime).
- Lien vers `/assets/site.css?v=9`.
- Aucune balise `<style>` en ligne, aucun style inline sauf largeur ponctuelle.
- Responsive à 390 px sans débordement horizontal.

## Interdits
- Ne touche à rien d'autre : ni `index.html`, ni `fr/index.html`, ni `prix/`, ni `blog/`,
  ni `entrainement.html`, ni `us/`, ni `sitemap.xml`, ni `robots.txt`.
- N'invente aucun chiffre, aucune date, aucune règle.
- N'ajoute pas de témoignages ni de notes clients.

## Vérification avant de rendre
Compte les questions réellement affichées sur chaque page et compare aux 38/57/37/83/44.
Signale l'écart s'il y en a un.

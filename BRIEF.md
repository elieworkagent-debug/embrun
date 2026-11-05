# BRIEF — Refonte complète de embrun.store

## Contexte produit
Embrun vend un pack de préparation à l'examen civique français 2026 : 19 € une fois
(audio des 259 questions, PDF 72 pages, 5 examens blancs, application hors ligne).
Le site est `embrun.store`. Vendeur : particulier, via Creem. Marché : France.

## Ce que tu dois livrer
Une refonte complète des pages FRANÇAISES + un blog. Fichiers statiques HTML/CSS, pas de framework.

### Pages à refaire entièrement
- `index.html` (hub bilingue FR/US)
- `fr/index.html` (page de vente principale)
- `prix/index.html` (comparatif de prix)
- `privacy.html`, `terms.html` : reprendre la nouvelle charte, NE PAS modifier le texte légal

### Pages à créer
- `blog/index.html` — liste des articles (4 au lancement)
- `blog/comment-se-passe-examen-civique/index.html`
- `blog/resultat-examen-civique-delai/index.html`
- `blog/echouer-examen-civique-que-faire/index.html`
- `blog/12-mises-en-situation/index.html`

### Interdits absolus
- NE TOUCHE PAS à `entrainement.html` (fichier généré par un script).
- NE TOUCHE PAS au dossier `us/` (cluster anglais existant).
- NE TOUCHE PAS à `CNAME`, `robots.txt`, au fichier `79e682011912692fcb5615e24daafef6.txt`.
- N'invente AUCUN chiffre, prix, date ou règle administrative. Utilise uniquement les faits ci-dessous.
- N'ajoute aucune fausse preuve sociale : pas d'avis clients, pas de « X candidats », pas de note sur 5.

## Faits vérifiés (source unique de vérité)
- Épreuve : 40 QCM, 45 minutes, une seule bonne réponse sur 4 propositions.
- Seuil de réussite : 32 bonnes réponses sur 40 (80 %). Une absence de réponse = 0 point.
- Composition : 28 questions de connaissance + 12 mises en situation.
- Les 12 mises en situation ne sont pas publiées par le ministère.
- Liste officielle : 259 questions publiées (258 énoncés distincts, un doublon), réparties :
  thème 1 Principes et valeurs de la République 38 ; thème 2 Système institutionnel et politique 57 ;
  thème 3 Droits et devoirs 37 ; thème 4 Histoire, géographie et culture 83 ;
  thème 5 Vivre dans la société française 44.
- Cadre : décret n° 2025-647 ; arrêté du 10 octobre 2025 (article 3 : publication des questions).
- Obligatoire depuis le 1er janvier 2026 pour : première carte de séjour pluriannuelle,
  première carte de résident, naturalisation.
- Organismes agréés : CCI Paris Île-de-France et France Éducation International.
- Coût : environ 70 à 90 € par présentation, fixé par chaque centre, dû à chaque passage.
- Résultat : généralement 24 à 48 heures ouvrées ; l'attestation de réussite n'a pas de durée de validité.
- Échec : nouvelle présentation possible, sans limite de nombre, chaque passage étant payant.
- Le pack Embrun : 19 € une fois, sans abonnement. Contient audio des 259 questions, PDF 72 pages,
  5 examens blancs de 40 questions, application d'entraînement hors ligne (un fichier HTML).
- Concurrence (prix publics relevés) : CiviqueQuiz 9,99 €/mois · 19,99 €/3 mois ;
  PrépaCivique 12 €/mois · 17 €/3 mois · 25 €/6 mois ; LeTestCivique 18 €/mois · 29 €/3 mois · 39 €/6 mois ;
  Civiquement 14,99 à 19,99 € pour 3 mois.
- Lien de paiement : https://www.creem.io/product/prod_56meS0QP6mZUhJTlR3icrG (19 €)
- Test gratuit : https://embrun.store/entrainement.html (40 questions chronométrées, sans compte)
- Volumes de recherche mensuels réels (Google Ads, France) : examen civique 40 500 ;
  test civique 12 100 ; examen civique naturalisation 9 900 ; examen civique 2026 8 100 ;
  examen civique test gratuit 5 400 ; examen civique titre de séjour 2 400 ;
  examen civique prix 1 600 ; qcm examen civique 1 600 ; examen civique 2026 pdf 1 600 ;
  test examen civique 1 300 ; examen civique 40 questions 880.

## Direction artistique — imposée, ne pas improviser
Registre : la salle d'examen. Froid, précis, administratif, mais éditorial et confiant.
Référence mentale : une convocation officielle bien composée, pas un site SaaS.

### Jetons
```
--paper:#ffffff      --slate:#f1f4f8      --ink:#0a1a2f
--ink-soft:#4a5a70   --rule:#d7dee7       --blue:#000091
--red:#c8102e        --pass:#0b6b45
```
Le bleu Marianne et le rouge servent de signal, jamais de décoration : filet tricolore de 3 px,
boutons primaires, un seul accent par écran. Pas de dégradé, pas d'ombre portée, rayon max 2 px.

### Typographie
- Interface et titres : **Instrument Sans** (Google Fonts), graisses 400/500/600/700.
- Texte long, questions, articles : **Newsreader** (Google Fonts), 400 et 500, italique pour les citations.
- Chiffres en `font-variant-numeric: tabular-nums` partout où il y a des scores, prix, durées.
- Échelle : h1 `clamp(2rem, 5vw, 3.4rem)` / h2 `clamp(1.4rem, 2.6vw, 2rem)` / corps 17 px / petites mentions 0,82 rem.
- Longueur de ligne : 68 caractères maximum pour le corps de texte.

### Structure
Grille 12 colonnes avec une **rail de marge à gauche de 132 px** qui porte les métadonnées
du document (référence de l'épreuve, thème, seuil) comme les marges d'un formulaire officiel.
Sur mobile (< 900 px), la rail disparaît et ses données passent en bandeau horizontal.

### Objet mémorable, un par page
- Accueil : la **feuille de réponses de 40 cases**, avec la ligne de seuil marquée à la 32e,
  la légende (juste / fausse / sans réponse) et un score réel.
- Prix : le **tableau comparatif** avec la ligne Embrun mise en évidence.
- Blog : la **carte de question** (énoncé en Newsreader, 4 propositions lettrées A-D, réponse révélée).

### Interdits de style (lisibles comme « généré par IA »)
- Fond crème + serif contrasté + accent terracotta.
- Fond quasi noir + accent acide.
- Cartes SaaS identiques avec la même ombre et le même rayon partout.
- Étiquettes en MAJUSCULES espacées au-dessus de chaque titre.
- Métadonnées jointes par des points médians « A · B · C ».
- Flèche « → » collée à chaque lien ou bouton.
- Numérotation décorative 01/02/03 : elle n'est admise que si le contenu est réellement séquentiel.
- Animations à l'apparition sur chaque section.

### Exigences techniques
- Une seule balise `h1` par page.
- `title` unique et descriptif (≤ 60 caractères), `meta description` (≤ 155 caractères), `canonical`.
- JSON-LD : `Product` + `Offer` sur la page de vente et sur /prix/ ; `FAQPage` là où il y a une FAQ ;
  `Article` + `BreadcrumbList` sur les articles de blog.
- Maillage interne : chaque article de blog renvoie vers la page de vente et vers le test gratuit ;
  la page de vente renvoie vers /prix/ et vers le blog.
- Accessibilité WCAG AA : contraste ≥ 4,5:1, focus visible, navigation au clavier, `prefers-reduced-motion` respecté.
- Responsive vérifié à 390 px et à 1440 px, aucun débordement horizontal.
- Poids : pas de framework, pas d'icônes en police, images et polices en `preload` si nécessaire.
- Toutes les pages portent la mention : « Embrun est un service privé et indépendant, sans lien avec
  le ministère de l'Intérieur, France Éducation international ou la CCI Paris Île-de-France. »

## Méthode
Charge les skills creation-site-web, seo-technique, seo-content, performance-web,
accessibilite-rgpd et conversion-landing. Travaille dans /home/openclaw/embrun-site.
Écris d'abord `assets/site.css` (le système complet), puis les pages, puis les articles.

# BRIEF 3 — SEO des articles de blog et de la page prix

## Constat mesuré
Les quatre articles font 737 à 979 mots. Les pages qui se classent sur ces requêtes en font
1 200 à 2 000. Aucun article ne couvre les questions réellement posées par les internautes
(données People Also Ask ci-dessous, relevées sur Google.fr).

## Règle absolue sur les faits
Tu peux reformuler, structurer et approfondir. Tu n'ajoutes **aucun chiffre et aucune règle
juridique qui ne figure pas déjà** dans l'article existant ou dans
`/home/openclaw/revenu/asset/src/q.json`. Si une question posée par les internautes n'est pas
couverte par ces faits, tu réponds avec ce qui est vérifiable et tu renvoies vers le site
officiel — tu n'inventes pas de délai, de tarif ni de procédure.

## Structure imposée à chaque article
1. `<h1>` contenant la requête cible.
2. Un paragraphe d'introduction de 35 à 50 mots qui **répond directement** à la requête.
3. Un sommaire cliquable (ancres) si l'article dépasse 1 200 mots.
4. Des `<h2>` qui reprennent les formulations des internautes, pas des titres abstraits.
5. Une section FAQ en fin d'article avec `FAQPage` en JSON-LD.
6. Un appel à l'action vers `/entrainement.html` (test gratuit) et un vers `/fr/` (le pack).
7. Liens internes vers au moins deux autres articles et vers `/prix/`.

Longueur cible : **1 300 à 1 700 mots** par article.

## Article 1 — `/blog/comment-se-passe-examen-civique/`
Requête cible : `comment se passe l'examen civique`.
Questions à couvrir en `<h2>` :
- Quelles sont les questions de l'examen civique ?
- Quel score faut-il pour réussir l'examen civique ?
- Qui ne passe pas l'examen civique ?
- Combien de temps dure l'épreuve ?
- Où se passe l'examen et comment s'inscrire ?

## Article 2 — `/blog/resultat-examen-civique-delai/`
Requête cible : `combien de jours pour avoir le résultat de l'examen civique`
(1 900 recherches/mois, difficulté 19 — la requête la plus facile du corpus).
Questions à couvrir :
- Combien de jours pour avoir le résultat ?
- Comment recevoir l'attestation de réussite ?
- Combien de temps l'attestation est-elle valable ?
- Que faire si le résultat n'arrive pas ?

## Article 3 — `/blog/echouer-examen-civique-que-faire/`
Requête cible : `que faire si on rate l'examen civique`.
Questions à couvrir :
- Peut-on repasser l'examen civique, et combien de fois ?
- Combien coûte chaque nouvelle tentative ?
- Que corriger avant de repasser ?
- Comment réviser l'examen civique efficacement ?

## Article 4 — `/blog/12-mises-en-situation/`
Requête cible : `mises en situation examen civique`.
À couvrir : ce qu'est une mise en situation, pourquoi les 12 questions ne sont pas publiées,
comment s'y préparer sans les connaître, exemples de raisonnement. Renvoie vers les
40 questions gratuites.

## Page `/prix/` — à restructurer
Le SERP de `examen civique prix` est dominé par l'inscription, les centres agréés et le coût
officiel — pas par les comparatifs de préparation. Nouvel ordre des sections :
1. Combien coûte l'examen civique (frais officiels, payés au centre agréé)
2. Qui fait passer l'examen et où le passer
3. Comment s'inscrire (rendez-vous en ligne)
4. Le timbre fiscal de la demande de naturalisation — question réelle des internautes
5. Combien coûte une préparation, avec le comparatif des services (contenu actuel conservé)
6. FAQ : Quel est le prix d'un examen ? Comment s'inscrire en ligne ? Qui fait passer ?
   Où et quand a lieu l'épreuve ?

Titre cible : `Prix de l'examen civique 2026 : combien ça coûte et où le passer`.
Conserve le tableau comparatif, le calcul du seuil de rentabilité et le JSON-LD existants.

## Interdits
- Ne touche pas à `entrainement.html`, `us/`, `fr/q/`, `sitemap.xml`, `robots.txt`, `CNAME`.
- Aucun témoignage, aucune note, aucun chiffre inventé.
- Ne supprime pas les mentions « Service privé indépendant ».

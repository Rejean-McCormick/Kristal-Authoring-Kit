# 10 — Alignement Kristal v6/v7/v8/v9/v10

Ce kit est une couche d'auteur. Les specs/TCK du Framework restent normatifs. En v3, le kit distingue explicitement le plan sémantique v9 du plan hosted-network v10.

## v6 — substrat portable

Le kit conserve référents, assertions atomiques quand elles sont utiles, valuations, applicabilité, provenance, conflits et projections portables.

## v7 — identité et orientations

```text
SEMANTIC IDENTITY != CONTENT IDENTITY
SUBJECT != AXIS
AXIS_TYPE != ORIENTATION_AXIS
PROJECTION != SOURCE
```

## v8 — langage, requête et contexte IA

```text
READ MODEL != CANONICAL STATE
QUERY INDEX != SOURCE OF TRUTH
AI CONTEXT != CANONICAL STATE
MODEL OUTPUT != AUTHORITY
```

## v9 — Semantic State Architecture

```text
LOGICAL STATE != PHYSICAL MATERIALIZATION
LOGICAL COMMITMENT != BLOB DIGEST
DOMAIN-NATIVE SHAPE != PORTABLE PROJECTION
REFERENCE != OWNERSHIP TRANSFER
```

`build-v9` construit toujours le State Snapshot et les Logical Commitments. Cette partie reste indépendante de GitHub.

## v10 — Hosted Kristal Network

```text
SEMANTIC STATE v9 != HOST BINDING v10
NODE ID != REPOSITORY NAME
DIRECTORY != AUTHORITY
QUALIFICATION != PUBLICATION != ACTIVATION
```

Le Local Kit ne bootstrappe pas les comptes/repos GitHub. Il suppose que le nœud v10 existe déjà et utilise `hosting/github.json` pour relier un workspace à ce nœud.

## Trois niveaux de preuve

1. `check` / `build-v9` : cohérence de l'enveloppe locale et engagements locaux.
2. `github-qualify` : preuve liée au commit exact du repo hôte.
3. `github-publish` + vérification bundle : preuve de publication réseau.

Ne jamais présenter un niveau comme preuve automatique du suivant.

# 07 — Validation v9

La validation couvre plusieurs couches qui ne doivent pas être confondues.

## A. Workspace

`tools/kristal.py check` vérifie :

- fichiers de contrôle ;
- JSON parseable ;
- lifecycle reconnu ;
- target v6/v7/v8/v9 attendu ;
- `state_ref` ;
- séparation canon/derived/runtime/build ;
- Logical Contracts déclarés ;
- modes de commitment cohérents ;
- références externes pinées ;
- unicité des sources ;
- recipes d'orientation.

C'est une validation locale, pas une preuve de vérité.

## B. Domaine et épistémologie

Chaque Kristal ajoute ses invariants propres : DAG sans cycles, ports valides, preuve cohérente, transitions légales, conservation, applicabilité, conflit, provenance, etc.

## C. Logical Commitments

Pour les artifacts `compute-json-jcs`, `build-v9` applique le profil baseline :

```text
kristal.logical/jcs-sha256-v1
```

Le commitment est indépendant de `artifact_id`, autorité et packing physique, mais inclut payload, scope, extensions logiques et dépendances pinées.

Pour les formes natives non supportées par ce baseline, utiliser `precomputed` avec un profil domain-native explicite. Le kit ne simule pas une équivalence qu'il ne sait pas démontrer.

## D. State Commitment

`build-v9` compose les member commitments et références externes pinées sous :

```text
kristal.state-commitment/jcs-sha256-v1
```

Compression, indexes, timestamps de publication et channels ne participent pas au State Logical Commitment.

## E. Materialization

Le kit crée toujours un Materialization Manifest `inline-json/1` pour les Logical Artifacts JSON qu'il génère effectivement, mais il sait aussi **préserver des Materialization Manifests v9 existants**.

Les manifests découverts sous `materializations/v9/manifests/` ou dans le layout legacy `.kristal/v9/materializations/` doivent :

- être `kristal_materialization_manifest` / v9.0 ;
- déclarer `reconstructability.lossless=true` ;
- viser exactement un Logical Artifact canonique courant (ID + contract + commitment) ;
- posséder des segments avec Blob Digest et taille valides.

Pour les locators locaux disponibles, `check` recalcule taille et SHA-256. Un blob distant ou absent n'est jamais téléchargé silencieusement : il produit un avertissement de disponibilité partielle, conformément au modèle v9.

`build-v9` conserve ces manifests dans le build et agrège les profils physiques réellement présents dans `v9-capabilities.json`. Le kit n'invente pas un profil générique à la place d'un profil de domaine. Voir `21_V9_MATERIALIZATION_AUTHORING.md`.

## F. Qualification indépendante

Si KristalDiag est disponible :

```bash
python tools/kristal.py qualify-v9 . --profile V9-State-Reader
```

Un projet plus avancé peut réclamer `V9-Builder`, `V9-Materializer`, `V9-Publisher` ou `V9-Full` seulement s'il fournit réellement les surfaces requises.

## G. Release

Avant `publish-v9` :

- scope clair ;
- Logical Contracts revus ;
- commitments vérifiés ;
- lacunes déclarées ;
- sources de vérité non ambiguës ;
- qualification requise réussie.

`released` ne veut pas dire « universellement vrai ».

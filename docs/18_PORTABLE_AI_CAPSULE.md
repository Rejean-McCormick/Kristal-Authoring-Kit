# 18 — Capsule IA portable (optionnelle)

Le profil `kristal.portable-ai/1.0` est un **read model dérivé**, utile lorsqu'un Kristal doit être remis directement à une IA ou consommé par un outil comme Kompiler.

Il n'est plus construit automatiquement par `build-v9`.

## Construction explicite

```bash
python tools/kristal.py build-v9 .
python tools/kristal.py build-ai .
python tools/kristal.py check-ai .
python tools/kristal.py pack-ai . --output Mon-Kristal-portable-ai.zip
```

Ou :

```bash
python tools/kristal.py build-v9 . --with-ai
```

`build-ai` crée au besoin `AI_START_HERE.md`, puis `AI_MANIFEST.json`, `ai/*` et `state/state-snapshot.json`. La copie du State Snapshot est liée au build v9 exact. Depuis 3.2.4, `ai/INDEX.json` inclut les Materialization Manifests v9 dans `files` et décrit séparément leurs blobs dans `materialization_blobs` avec disponibilité, taille, digest, locator et classe de transport. Les locators externes restent déclarés mais ne sont jamais téléchargés silencieusement.

## Autorité

```text
canon/                  source logique
build/v9/state-snapshot état construit
sources/                provenance
ai/                     lecture dérivée
```

Supprimer ou reconstruire `ai/` ne doit jamais changer le State Logical Commitment.

## Kompiler

Kompiler peut consommer les Local Kristals ou leurs publications et construire des Context Packs. Il reste optionnel et ne décide pas de la synchronisation GitHub, de la publication ou de l'activation.

## GitHub

Aucune donnée de hosting n'est requise pour lire la capsule. Le même read model sert maintenant de contrat de projection pour la synchronisation GitHub :

```bash
python tools/kristal.py read-surface . --require-ready
```

La sortie `kristal.github-read-surface/1.0` donne le `target_root`, l'entrypoint, le digest opérationnel de surface et la liste exacte `path + role + size + sha256` à projeter sous `kristals/<slug>/`. Ce digest n'est jamais un Logical/State Commitment.

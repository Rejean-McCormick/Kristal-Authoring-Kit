# 12 — Lifecycle local v9 et publication réseau v10

## Local / offline

```bash
python tools/kristal.py check .
python tools/kristal.py build-v9 .
python tools/kristal.py publish-v9 .
python tools/kristal.py activate-v9 . --channel current   # optionnel
```

`publish-v9` stocke un snapshot local sous `release/v9/states/...`. Ce mécanisme reste utile pour archives/tests hors réseau.

## Réseau v10

```bash
python tools/kristal.py configure-github . ...
python tools/kristal.py export-hosted . --repo-dir <checkout>
# review / git add / commit / push
python tools/kristal.py github-qualify .
python tools/kristal.py github-publish . --framework-path <framework> --yes
```

La publication réseau exige un état distant byte-identique au build local, un receipt de qualification du commit exact, puis une Release v10 avec `state-snapshot.json`, `bundle-manifest.json` et `publication.json`.

## Activation

L'activation réseau n'est pas déclenchée automatiquement par le kit v3. La séparation BUILD / QUALIFY / PUBLISH / ACTIVATE est conservée.

# Outils — Kristal Local Kit v3.2

Le CLI local utilise uniquement la bibliothèque standard Python. GitHub CLI n'est requis que pour les commandes de compatibilité `github-*`.

## Local Kristal

```bash
python tools/kristal.py init PATH --title "Titre" --slug slug --profile open
python tools/kristal.py migrate-v10 PATH
python tools/kristal.py check PATH
python tools/kristal.py status PATH
```

## Sources / modèle / state v9

```bash
python tools/kristal.py add-source PATH --id src:1 --title "Source" --locator external://source
python tools/kristal.py register-artifact PATH --file canon/domain/core.json --artifact-id urn:kristal:demo:core --contract-id demo.core
python tools/kristal.py register-materialization PATH --manifest path/to/materialization.json
python tools/kristal.py add-reference PATH --kind state --id urn:kristal:state:child --digest sha256:<64hex>
python tools/kristal.py build-v9 PATH
```

`build-v9` est **sémantique par défaut** : il ne reconstruit pas automatiquement `AI_MANIFEST.json` ni `ai/*`. Il préserve cependant les Materialization Manifests v9 validés et agrège leurs profils/capabilities physiques.


## Inspection / interop locale

```bash
python tools/kristal.py inspect <workspace>
python tools/kristal.py inspect <workspace> --compact
python tools/kristal.py read-surface <workspace> --require-ready
```

`inspect` est strictement en lecture seule. Il produit `kristal.local-inspection/1.0`. `read-surface` produit `kristal.github-read-surface/1.0`, la liste exacte et digérée des fichiers que Manager peut projeter sous `kristals/<slug>/` pour lecture GitHub/IA, sans miroir complet du workspace.

## IA / Kompiler — optionnel

```bash
python tools/kristal.py build-ai PATH
python tools/kristal.py check-ai PATH
python tools/kristal.py pack-ai PATH --output Mon-Kristal-portable-ai.zip
python tools/kristal.py build-v9 PATH --with-ai
```

## Lifecycle local v9

```bash
python tools/kristal.py qualify-v9 PATH --profile V9-State-Reader
python tools/kristal.py publish-v9 PATH
python tools/kristal.py activate-v9 PATH --channel current
```

## Réseau v10 — compatibilité avancée

Le workflow utilisateur recommandé est **Kristal GitHub Setup/Bootstrap**. Les commandes suivantes restent disponibles pour automatisation et compatibilité :

```bash
python tools/kristal.py configure-from-network PATH --network ../network.toml --repository kristal-public
python tools/kristal.py configure-github PATH --repository OWNER/REPO --framework-repository OWNER/KristalV10 --framework-sha <40sha>
python tools/kristal.py export-hosted PATH --repo-dir ../kristal-public
python tools/kristal.py github-status PATH
python tools/kristal.py github-qualify PATH
python tools/kristal.py github-publish PATH --framework-path ../KristalV10 --yes
```

## Synchronisation GitHub

La synchronisation public/privé de la **read surface** appartient à **Kristal Manager**. Le Local Kit définit seulement la projection exacte via `read-surface`. La publication/activation reste une opération distincte de GitHub Setup/Bootstrap.

## Archive locale

```bash
python tools/kristal.py hash-manifest PATH
python tools/kristal.py pack PATH --output Kristal-full-workspace.zip
```

`pack` n'active plus implicitement la couche IA. Utiliser `pack-ai` lorsqu'une capsule IA est voulue.

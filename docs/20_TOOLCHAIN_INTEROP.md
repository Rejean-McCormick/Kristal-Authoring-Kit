# 20 — Interop locale de la toolchain

## But

Un Local Kristal doit pouvoir être inspecté par plusieurs outils sans que chaque outil invente une autre convention de chemins ou une autre définition de la surface GitHub.

## Contrat d'inspection

Le Local Kit 3.2.4 expose :

```bash
python tools/kristal.py inspect <workspace>
python tools/kristal.py read-surface <workspace> --require-ready
```

`inspect` reste `kristal.local-inspection/1.0`, read-only et non sémantique. Il expose maintenant `github_read_surface` et `interop.suggested_collection_root`. `read-surface` émet directement `kristal.github-read-surface/1.0` pour éviter que Manager reconstruise lui-même la liste des fichiers.

## Ordre de découverte d'un State Snapshot v9

1. `state/state-snapshot.json` — export courant explicite ;
2. `build/v9/state-snapshot.json` — dernier build local ;
3. `.kristal/v9/...` et `state-snapshot.json` racine — compatibilité legacy ;
4. `release/v9/states/**/state-snapshot.json` — releases locales immuables.

La sélection d'un chemin ne change jamais `state_ref`, Logical Commitment ou State Commitment.

## Surface GitHub de lecture

La projection recommandée est :

```text
kristals/<slug>/
  AI_START_HERE.md
  AI_MANIFEST.json
  ai/*
  canon/*
  sources/*
  docs/*
  state/state-snapshot.json
  materializations/...   # descriptors/manifests; les blobs sont des candidats de transport séparés
```

Ce n'est ni un miroir complet du workspace, ni une publication immuable. Manager peut synchroniser exactement cette liste et son `surface_digest`, sans copier `tools/`, `build/`, `release/`, `hosting/`, `validation/` ou `runtime/`. Les bytes de matérialisation apparaissent séparément dans `materialization_objects` afin que la couche hosting choisisse Git, Release, GHCR, LFS ou un resolver adapté au lieu de pousser aveuglément de gros blobs dans l'arbre Git.

## Frontières

- **Kristal Manager** : inventaire, validation et synchronisation GitHub de la read surface ;
- **Kristal GitHub Setup / Bootstrap** : qualification, publication immuable et activation ;
- **Kompiler** : lecture/query/context optionnel ;
- **Local Kit** : structure, validation locale, build v9, read model IA et contrat de projection.

La visibilité `public/private` reste une décision opérationnelle et ne fait pas partie du canon sémantique.

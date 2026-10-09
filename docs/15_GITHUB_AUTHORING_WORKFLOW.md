# 15 — GitHub : synchronisation de lecture vs publication

## Deux opérations différentes

**Sync de lecture** : projection dérivée et vérifiable d'un Local Kristal sous `kristals/<slug>/`, optimisée pour une IA recevant une URL GitHub. Gérée par **Kristal Manager** à partir du contrat `read-surface` du Local Kit.

**Publication Kristal** : State Snapshot qualifié, bundle vérifié, Release immuable, activation éventuelle. Gérée par **Kristal GitHub Setup/Bootstrap**.

La visibilité du repo et le digest de la read surface n'entrent jamais dans le Logical Commitment.

## Chemin principal

```text
Local Kit: check → build-v9 → build-ai/read-surface
Manager: Validate → Sync to GitHub
GitHub Setup: qualify → publish → activate
```

Le sync recommandé n'est ni un `state-only export`, ni un miroir complet du workspace. Il embarque l'entrypoint IA, les index/digests, le contenu lisible utile, l'état exact et les matérialisations locales explicitement référencées.

Les commandes `export-hosted`, `github-status`, `github-qualify` et `github-publish` du CLI restent disponibles pour compatibilité/automatisation avancée.

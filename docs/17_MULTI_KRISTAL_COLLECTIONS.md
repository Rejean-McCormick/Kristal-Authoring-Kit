# 17 — Plusieurs Kristals par repo de collection

Créer un nouveau repo seulement lorsque changent les permissions, responsables, rétention, cycle de publication ou charge opérationnelle. Pour des milliers de Kristals partageant les mêmes contraintes, préférer une collection commune et des sous-arbres indépendants.

Chemin recommandé :

```text
kristals/<slug>/
  AI_START_HERE.md
  AI_MANIFEST.json
  ai/INDEX.json
  state/state-snapshot.json
  ...read surface...
```

Chaque workspace conserve son propre `state_ref` et son propre Logical Commitment. Le Node v10 héberge plusieurs états sans fusionner leurs identités sémantiques.

Le Local Kit ne définit pas le catalogue global de collection ; il fournit toutefois `read-surface` avec `target_root = kristals/<slug>` afin que Manager puisse maintenir efficacement un index dérivé de collection et batcher plusieurs mises à jour dans un seul commit/push.

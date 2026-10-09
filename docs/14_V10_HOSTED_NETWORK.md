# 14 — Hosted Network v10 pour auteurs

Kristal v10 ne remplace pas le State Snapshot v9. Il ajoute le plan opérationnel : Node Manifest, Host Binding, Publication et Directory.

```text
v9 = ce qui est l'état logique exact
v10 = où/comment cet état est qualifié, publié et découvert
```

Le fichier `hosting/github.json` du kit est une **liaison locale**, non un objet sémantique. Il indique dans quel nœud GitHub exporter le state et quel Framework SHA utiliser. Il n'entre jamais dans le Logical Commitment.

Un repo est une frontière de permissions/lifecycle, pas nécessairement un Kristal. Plusieurs workspaces peuvent publier dans le même repo via des `state_path` distincts.

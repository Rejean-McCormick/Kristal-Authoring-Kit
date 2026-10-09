# 13 — Migration des anciens workspaces vers v3

La commande actuelle est :

```bash
python tools/kristal.py migrate-v10 PATH
```

Elle accepte les workspaces Local Kristal v1 et v2.

## v1 → v2 sémantique

Pour un ancien v1, le migrateur ajoute `state_ref`, target v9 et convertit le State Index vers des entrées Logical Artifact structurées. Les anciens chemins sans contrat reçoivent un placeholder explicite `Local Kristal.legacy-json-artifact/1.0` avec `migration_note`.

## v2 → v3 hosted-network

Le passage v2 → v3 :

- change l'enveloppe en `kristal.local-workspace/3.2.0` ;
- ajoute `target.hosted_network_baseline = kristal.hosting/10.0` ;
- ajoute les politiques qualification-before-publication / exact-commit ;
- ajoute `hosting/` et `build/v10/` ;
- ne change pas `canon/state.index.json`, les payloads ni les commitments v9.

Aucune cible GitHub n'est inventée pendant migration. Exécuter `configure-github` seulement avec un repo et un Framework SHA réellement choisis.

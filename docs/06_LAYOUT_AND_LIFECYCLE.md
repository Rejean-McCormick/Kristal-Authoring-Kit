# 06 — Layout du workspace et lifecycle v9

## 1. Le layout standardise les responsabilités, pas le payload

Le workspace aide une IA à retrouver immédiatement frontière, sources, canon, épistémologie, opérations, build, release et runtime. Il ne dicte pas la structure du payload métier.

## 2. Layout v2

```text
<Kristal>/
├── README.md
├── kristal.workspace.json
├── AGENTS.md
├── docs/
├── sources/
│   └── source-catalog.json
├── schemas/
├── canon/
│   ├── state.index.json
│   ├── domain/          # forme métier libre
│   ├── epistemic/       # overlay/assertions si utilisés
│   └── operations/      # règles exécutables si utilisées
├── projections/
│   ├── recipes/
│   └── materialized/    # dérivé
├── derived/             # dérivé
├── runtime/             # read models, indexes, caches
├── build/
│   └── v9/              # candidat généré, dérivé
├── release/
│   └── v9/
│       ├── states/      # snapshots immuables publiés
│       └── channels/    # pointeurs d'activation mutables
├── validation/
├── tests/
└── tools/
```

## 3. Trois lifecycles distincts

Le statut local reste : `stub`, `design`, `building`, `validated`, `released`, `superseded`.

Il ne faut pas le confondre avec le lifecycle v9 :

```text
BUILD → PUBLISH → ACTIVATE
```

- BUILD crée un candidat reconstructible dans `build/v9/` ;
- PUBLISH crée un snapshot immuable sous `release/v9/states/<digest>/` ;
- ACTIVATE modifie un channel sous `release/v9/channels/`.

Une activation n'est pas obligatoire pour un Kristal distribué comme connaissance statique.

## 4. Ownership et fédération

`semantic_ownership` documente ce que le repo possède. `canon/state.index.json.external_references` contient les références externes pinées.

```text
PARENT REFERENCES CHILD
REFERENCE != OWNERSHIP TRANSFER
STATE COMPOSITION != AUTHORITY MERGE
```

## 5. Canon vs build/materialization/runtime

`canon/` contient les entrées logiques autoritatives du Local Kristal.

`build/`, `derived/`, `runtime/`, `materializations/` et `projections/materialized/` sont physiques/dérivés et ne sont pas canon par défaut.

Les Materialization Manifests v9 authorés vivent normalement sous `materializations/v9/manifests/`. Le layout legacy `.kristal/v9/materializations/` reste découvert pour migration. Une matérialisation peut être segmentée, factorisée, compressée ou domain-specific sans changer le Logical Commitment tant que sa reconstruction est lossless.

Les releases sous `release/v9/states/` sont des snapshots publiés immuables. Ils représentent le canon publié, mais ne doivent pas être édités manuellement pour modifier le canon local.

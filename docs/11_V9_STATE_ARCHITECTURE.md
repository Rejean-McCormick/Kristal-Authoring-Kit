# 11 — State Architecture v9 pour auteurs

## Logical Artifact

L'unité v9 polymorphe est le Logical Artifact : un ID stable, un Logical Contract et un Logical Commitment sur le contenu logique.

Le kit supporte deux modes :

- `compute-json-jcs` — payload JSON, commitment baseline calculé localement ;
- `precomputed` — profil domain-native externe, commitment fourni explicitement.

Ce second mode est essentiel au polymorphisme : v9 ne signifie pas « tout convertir en JSON ».

## State Snapshot

Le State Snapshot est une composition immuable de :

- members possédés ;
- références externes pinées.

Un selector mutable (`latest`, `HEAD`, `main`) n'est pas une référence de snapshot publiée.

## Materialization

La matérialisation décrit comment le Logical Artifact existe physiquement. Changer compression, segment ou emplacement ne doit pas changer le Logical Commitment.

Le Local Kit accepte plusieurs représentations simultanées du même artifact : `inline-json/1`, profils de référence v9 et profils custom de domaine. Depuis 3.2.3, les manifests existants sont découverts, liés au commitment canonique, vérifiés lorsqu'un blob local est disponible, puis préservés dans le build. Segmentation, dictionnaires et factorisation restent des propriétés physiques, jamais des identités sémantiques.

## Derivation

La Derivation décrit comment un artifact a été produit. Elle est distincte de la provenance épistémique.

Le kit n'en génère pas automatiquement : une Derivation fictive serait pire qu'une lacune explicite.

## Runtime

Indexes, caches, embeddings et read models vivent dans `runtime/` ou `derived/` et restent supprimables/reconstructibles.

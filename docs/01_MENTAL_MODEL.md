# 01 — Modèle mental

## 1. Kristal n'est pas un type unique de base de connaissances

Un Kristal est une **unité durable de mémoire sémantique** avec identité, frontière, provenance et règles de lecture. Sa forme interne dépend du domaine.

Il peut contenir ou organiser :

- des référents et assertions ;
- un payload métier structuré ;
- des transformations ou procédures ;
- des états et transitions ;
- des preuves et dépendances ;
- des observations et mesures ;
- des hypothèses et tentatives ;
- des décisions et actions ;
- des modèles exécutables ;
- des relations vers d'autres Kristals ;
- des projections et index reconstruisibles.

## 2. Quatre couches à ne pas confondre

### A. Identité du Kristal

L'unité existe comme nom, scope, ownership, parenté et lifecycle. Elle peut être un **stub** sans contenu sémantique cristallisé.

### B. État / payload sémantique

C'est ce que cette identité possède réellement à une version donnée. La forme peut être domain-native.

### C. State / Logical Artifact v9

Le Logical Artifact engage le contenu logique sous un contrat explicite. Le State Snapshot compose les members et références pinées sans imposer leur packing physique.

### D. Surface / projection / runtime

C'est une vue orientée ou optimisée. Une Surface est éphémère ; une Projection la matérialise ; un Runtime Pack optimise la lecture sans devenir canon.

## 3. Le core standardise des distinctions, pas une topologie

Invariants structurants :

```text
IDENTITY != LABEL
REFERENT != ASSERTION
COORDINATE != APPLICABILITY
PROJECTION != SOURCE
READ MODEL != CANONICAL STATE
SIMILARITY != EQUIVALENCE
AI PROPOSAL != ACCEPTED STRUCTURE
MODEL OUTPUT != AUTHORITY
LOGICAL STATE != PHYSICAL MATERIALIZATION
LOGICAL COMMITMENT != BLOB DIGEST
BUILD != PUBLISH != ACTIVATE
```

Le core existe pour que des formes radicalement différentes restent interopérables.

## 4. Le payload natif est ouvert

Ne limite jamais la découverte à cette liste, mais sache reconnaître :

- invariant polymorphe ;
- graphe / multi-graphe / hypergraphe ;
- DAG ;
- matrice ou tenseur sparse ;
- hiérarchie / polyhiérarchie ;
- réseau multiplexe ;
- automate / machine à états ;
- ledger événementiel ;
- modèle causal ;
- programme / procédure ;
- théorie formelle ;
- mémoire de recherche ;
- modèle pédagogique ;
- modèle exécutable/simulable ;
- assemblage hybride de plusieurs structures.

La liste est illustrative, jamais fermée.

## 5. Assertions et payload métier

Le framework Kristal fournit une couche d'assertions adressables et traçables. Cela ne signifie pas que tout domaine doit être aplati en triplets naïfs.

Un objet riche — recette, réaction n-aire, procédure, graphe de diagnostic, preuve structurée — peut rester une structure canonique métier, avec une enveloppe épistémique qui l'adresse, le source et le qualifie.

Règle :

```text
SEMANTIC ENVELOPE != FORCED DOMAIN SHAPE
```

## 6. Plusieurs dimensions internes ne signifient pas plusieurs axes v7

Un domaine peut avoir 3, 7 ou 50 dimensions internes.

Une **projection portable orientée** utilise :

```text
exactement 1 primary orientation axis
au plus 1 secondary orientation axis
```

La limite concerne la cohérence de la projection, pas la richesse du domaine.


## 7. Identité, revision et bytes

V9 sépare trois questions :

```text
Semantic ID       = de quel objet parle-t-on ?
Logical Commitment = quel contenu logique exact ?
Blob Digest        = quels bytes exacts ?
```

Une recompression ou resegmentation peut changer le Blob Digest sans changer le Logical Commitment.

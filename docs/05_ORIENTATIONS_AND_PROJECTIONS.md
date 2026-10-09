# 05 — Orientations, axes, Surfaces et projections

## 1. Ne pas commencer par les axes

L'axe est un mécanisme de lecture/organisation. Il ne doit pas déterminer prématurément la forme intrinsèque du domaine.

## 2. Distinctions

```text
CATEGORY != SUBJECT
SUBJECT != AXIS
AXIS != TAG
AXIS_TYPE != ORIENTATION_AXIS
DOMAIN DIMENSION != ORIENTATION AXIS
COORDINATE != APPLICABILITY
```

### Subject

Le territoire sémantique observé.

### Domain dimension

Dimension intrinsèque du modèle : espèce, système physiologique, couche réseau, régime d'interprétation, etc.

### Coordinate

Position d'un élément dans la géométrie du domaine.

### Facet/filter

Dimension de classification ou de sélection.

### Axis Type

Famille générique d'orientation. Les registres existants sont des seeds, pas un vocabulaire fermé.

### Orientation Axis

Angle concret qui change réellement la sélection ou l'organisation d'une vue.

## 3. Surface

Une Surface est une vue éphémère :

```text
Subject + Orientation + Context → Surface
```

Elle peut exister sans fichier Kristal distinct.

## 4. Projection portable

Lorsqu'une Surface est matérialisée en projection portable :

```text
primary_orientation_axis: exactement 1
secondary_orientation_axis: 0 ou 1
```

Cette règle ne limite pas la multidimensionnalité interne.

## 5. Plusieurs angles majeurs

Pour un même Subject :

```text
orientation A → Surface A → projection A éventuelle
orientation B → Surface B → projection B éventuelle
```

Ne fabrique pas un « super axe » artificiel pour éviter plusieurs projections.

## 6. v8/v9 : recomposition sans fusion du canon

Une requête peut mobiliser plusieurs Kristals ou shards :

```text
resolve identities
→ scope sources/kristals/shards
→ traverse/filter/evidence
→ semantic slice
→ AI context bundle
```

La vue combinée est dérivée.

```text
AI CONTEXT != CANONICAL STATE
QUERY INDEX != SOURCE OF TRUTH
```


## 7. Projection portable vs Logical Artifact v9

Une projection v6/v7 est un contrat d'interopérabilité ou de lecture. Elle ne devient pas automatiquement le Logical Artifact canonique v9.

```text
DOMAIN-NATIVE SHAPE != PORTABLE PROJECTION
```

Le `projection_contract.relationship_to_v9_canon` des recipes v2 est donc `derived_projection`.

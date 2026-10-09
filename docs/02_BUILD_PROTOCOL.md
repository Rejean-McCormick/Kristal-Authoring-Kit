# 02 — Protocole de construction

Ce protocole est destiné à un agent IA qui reçoit un corpus, des documents, une conversation ou un système à cristalliser.

## Phase 0 — Ne rien modéliser prématurément

Avant toute création de schéma :

- inventorier les fichiers et sources ;
- relever les artefacts déjà canoniques ;
- identifier les formats existants ;
- noter les contradictions, trous, versions et autorités ;
- détecter si un Kristal existe déjà sous forme de stub ou de version antérieure.

Livrable : `docs/00_INTENT_AND_SCOPE.md`.

## Phase 1 — Identité, frontière et ownership

Définir :

- `kristal_id` ou stratégie d'identité ;
- titre et slug ;
- Subject ou territoire sémantique ;
- ce que le Kristal **possède** ;
- ce qu'il **référence sans posséder** ;
- parents/enfants/peers éventuels ;
- état de lifecycle.

Question clé : **si deux équipes modifient deux Kristals différents, où doit vivre chaque vérité pour éviter les copies divergentes ?**

Livrable : `docs/01_SEMANTIC_BOUNDARY.md` + `kristal.workspace.json`.

## Phase 2 — Découvrir la forme native

Ne sélectionner aucune topologie par défaut.

Extraire d'abord les primitives réelles :

- identités ;
- objets ;
- états ;
- événements ;
- relations ;
- transformations ;
- dépendances ;
- invariants ;
- contraintes ;
- preuves ;
- mesures ;
- décisions ;
- actions ;
- tentatives / échecs ;
- temporalité ;
- échelles ;
- dimensions indépendantes.

Chercher ensuite la structure minimale qui préserve ces distinctions.

Livrable : `docs/02_NATIVE_MODEL.md` et, si nécessaire, schémas dans `schemas/`.

## Phase 3 — Définir les régimes épistémiques

Pour chaque classe d'information, déterminer son statut :

- observation ;
- source externe ;
- contrainte autoritative ;
- connaissance de référence ;
- interprétation ;
- hypothèse ;
- dérivation ;
- résultat de calcul ;
- preuve / certificat ;
- décision ;
- action ;
- note de recherche ;
- résonance/comparaison ;
- inconnu / non applicable.

Deux éléments qui se ressemblent mais n'ont pas le même régime ne doivent pas être fusionnés.

Livrable : `docs/03_EPISTEMIC_MODEL.md`.

## Phase 4 — Définir sources et autorité

Pour chaque source :

- identité ;
- type ;
- locator ;
- version/date si connue ;
- digest si possible ;
- portée d'autorité ;
- limitations ;
- relation avec le Kristal.

L'IA peut proposer une relation. Elle ne peut pas inventer l'autorité qui la rend vraie.

Livrable : `sources/source-catalog.json`.

## Phase 5 — Canonique vs dérivé

Déclarer explicitement la source de vérité de chaque artefact.

**Canonique possible :**

- payload métier natif ;
- référents ;
- assertions ;
- événements ou observations ;
- règles validées ;
- traces append-only qui doivent être conservées.

**Dérivé typique :**

- index ;
- vues ;
- résumés ;
- embeddings ;
- rankings ;
- fingerprints ;
- graphes de navigation ;
- caches ;
- semantic slices ;
- AI context bundles.

Règle : tout dérivé important doit avoir une recette de reconstruction ou un lineage.

Livrable : `docs/04_CANONICAL_DERIVED.md` + `canon/state.index.json`.

## Phase 6 — Sémantique opérationnelle optionnelle

Si le domaine est exécutable, définir :

- variables d'état ;
- préconditions ;
- transitions ;
- effets ;
- fonctions de calcul ;
- règles de propagation ;
- observables ;
- validateurs ;
- garanties et limites.

Exemples : procédure culinaire, simulation de panne, calcul mathématique, workflow, moteur de règles.

Ne réduis pas une sémantique exécutable à une description textuelle si l'exécution est un invariant important.

Livrable : `canon/operations/` + documentation.

## Phase 7 — Orientations et Surfaces

Seulement maintenant, demander :

- Quelle lecture principale est utile ?
- Qu'est-ce qui change réellement la sélection ou l'organisation ?
- Est-ce un Orientation Axis ou seulement une facette/coordonnée/filtre ?

Une Surface :

```text
Subject + orientation + contexte → vue éphémère
```

Une Projection matérialisée :

```text
1 primary axis + 0/1 secondary axis
```

Si deux orientations sont chacune dominantes, créer deux Surfaces/projections plutôt qu'un artefact ambigu.

Livrable : `docs/05_ORIENTATIONS.md` + `projections/recipes/*.projection.json`.

## Phase 8 — Population

Importer ou créer le contenu par lots petits et auditables.

À chaque lot :

- conserver provenance ;
- préserver IDs ;
- ne pas supprimer les conflits ;
- marquer les inconnues ;
- enregistrer les transformations ;
- tester les références.

Une sortie IA non sourcée entre comme proposition/hypothèse/dérivé, pas comme autorité.

## Phase 9 — Validation

Vérifier :

- cohérence structurelle ;
- références non pendantes ;
- invariants du domaine ;
- séparation canonique/dérivé ;
- provenance ;
- ownership ;
- applicabilité ;
- dimensions de valuation ;
- projections à 1+0/1 axes ;
- reproductibilité des dérivés ;
- état des lacunes.

Livrable : `validation/validation-report.json` et/ou rapports de domaine.

## Phase 10 — Cristallisation v9 et qualification

Après validation du domaine :

1. enregistrer chaque Logical Artifact canonique dans `canon/state.index.json` ;
2. pinner les références externes par Logical Commitment ;
3. enregistrer/préserver les Materialization Manifests v9 existants lorsqu'ils représentent physiquement ces artifacts ;
4. exécuter `check` afin de vérifier leur binding et les blobs locaux disponibles ;
5. exécuter `build-v9` pour construire un candidat déterministe ;
6. vérifier les Logical Commitments, le State Commitment et les capabilities de matérialisation annoncées ;
7. générer les projections v6/v7 et index v8 nécessaires comme dérivés ;
8. qualifier indépendamment avec KristalDiag lorsque disponible ;
9. exécuter `publish-v9` pour produire un snapshot immuable ;
10. n'utiliser `activate-v9` que si un channel opérationnel est réellement nécessaire.

```text
BUILD != PUBLISH != ACTIVATE
```

Ne pas créer automatiquement une Derivation fictive : si les entrées exactes et le transform ne sont pas connus, documenter la lacune au lieu d'inventer la provenance de build.

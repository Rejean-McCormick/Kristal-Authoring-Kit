# 09 — Bibliothèque de patterns ouverts

Ces patterns sont des **stress tests**, pas des catégories fermées.

## 1. Invariant polymorphe

Inspiré d'un Kristal de primalité.

```text
Invariant
├─ formulations équivalentes
├─ conséquences nécessaires/non suffisantes
├─ témoins/certificats
└─ algorithmes d'opérationnalisation
```

Le danger : confondre définition, théorème dérivé et test.

## 2. Plans interprétatifs superposés

Inspiré d'un Kristal où mécanique, structure, ontologie, épistémologie, résonance et histoire coexistent.

Le danger : transformer une transformation déterministe en preuve de l'interprétation suivante.

## 3. Mémoire de recherche

```text
KnowledgeGraph
ResearchGraph
StrategyGraph
append-only attempts
proof obligations
promotion workflow
```

Le danger : promouvoir automatiquement un résultat local ou faire d'une stratégie une vérité du domaine.

## 4. Hiérarchie de stubs

```text
University Kristal
  → Track Kristals
      → Course Kristals
```

Chaque parent possède la topologie, pas le contenu des enfants.

Le danger : duplication sémantique et divergence.

## 5. Modèle diagnostique exécutable

```text
identity/applicability
+ multiplex topology
+ operating state
+ failure perturbations
+ observability
+ diagnostic case
→ posterior / test plan
```

Le danger : laisser les fréquences statistiques réécrire la topologie structurale.

## 6. Procédure métier native

```text
RecipeVariant → ProcedureGraph(DAG)
```

Les assertions restent une enveloppe transversale, mais le DAG porte la vérité procédurale.

Le danger : aplatir le DAG en texte ou en triplets et perdre ordre partiel, parallélisme et états intermédiaires.

## 7. Nouveau pattern inconnu

Si aucun pattern ne convient : c'est acceptable.

Documente la nouvelle forme dans `docs/02_NATIVE_MODEL.md`, crée les schémas nécessaires et explique pourquoi les patterns existants auraient perdu de l'information.


## 8. Relation massive factorisée

Une famille de centaines de milliers de claims peut partager prédicat, envelope épistémique ou dictionnaires dans sa matérialisation. Les claims restent logiquement distinguables.

Le danger : prendre l'ordinal local ou le segment physique pour l'identité sémantique.

## 9. Artifact natif non JSON

Un AST, un format binaire formel ou un graphe natif peut utiliser un Logical Contract et un profil de commitment externe.

Le danger : convertir le format en JSON uniquement parce que l'outil baseline sait hasher du JSON. Utiliser `precomputed` plutôt que perdre la forme native.

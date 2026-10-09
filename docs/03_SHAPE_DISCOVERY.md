# 03 — Découverte de la forme native

Le risque principal d'un agent est le **premature schema lock-in** : choisir un graphe, une ontologie ou une taxonomie avant d'avoir compris le phénomène.

## Méthode : Shape Probes

Passe les données à travers ces sondes. Plusieurs peuvent être vraies simultanément.

### Probe A — Invariant

Question : plusieurs formulations expriment-elles exactement la même propriété ?

Forme possible :

```text
INVARIANT
├─ morphes équivalents
├─ conséquences non équivalentes
├─ contre-exemples
├─ certificats / témoins
└─ procédures d'opérationnalisation
```

Ne confonds pas caractérisation, conséquence et méthode de décision.

### Probe B — Transformation / procédure

Question : les objets deviennent-ils d'autres états par opérations ?

Forme possible : DAG, workflow, réseau de transformations, hyperarêtes n-aires.

Préserve ordre partiel, parallélisme, consommation/production et états intermédiaires.

### Probe C — État / transition

Question : la connaissance dépend-elle de conditions, phases ou transitions ?

Forme possible : automate, statechart, ledger d'événements.

### Probe D — Multiplexe / multi-réseau

Question : les mêmes entités sont-elles reliées par plusieurs couches indépendantes ?

Exemples : puissance + signal + réseau + mécanique ; social + financier + institutionnel.

Ne fusionne pas les couches sous une relation générique qui perd leur sémantique.

### Probe E — Matrice / espace sparse

Question : le domaine ressemble-t-il à un produit de dimensions dont seules certaines combinaisons existent ?

Évite de matérialiser le produit cartésien complet. Stocke les cellules réellement porteuses d'information.

### Probe F — Multi-échelle

Question : les mêmes phénomènes existent-ils à plusieurs échelles avec des relations entre niveaux ?

Préserve les relations inter-échelles au lieu de dupliquer l'objet dans chaque niveau.

### Probe G — Régimes d'interprétation

Question : une chaîne de traitement passe-t-elle de données mécaniques vers interprétation, hypothèse, comparaison ou résonance ?

Chaque passage doit être explicitement typé. Une transformation déterministe peut être certaine alors que son interprétation reste spéculative.

### Probe H — Mémoire de recherche

Question : faut-il conserver ce qui a été tenté, échoué, laissé ouvert ou promu ?

Forme possible :

```text
KnowledgeGraph  = ce qui est établi/importé
ResearchGraph   = obligations, hypothèses, essais, résultats
StrategyGraph   = mémoire procédurale, non vérité du domaine
```

Les échecs peuvent être des données importantes sans devenir des faits sur le monde.

### Probe I — Identity-first / stub

Question : la frontière, le parentage ou l'ownership doit-il être réservé avant que le contenu existe ?

Un Kristal peut commencer comme stub : identité stable + scope + children + statut `not_crystallized`.

### Probe J — Exécutable

Question : le modèle doit-il prédire, simuler, propager ou choisir une action ?

Si oui, conserver les règles opérationnelles séparément de leurs projections statistiques.

### Probe K — Polychronique / ledger

Question : l'ordre des événements et la succession des versions sont-ils eux-mêmes des données ?

Utiliser des événements append-only lorsque l'historique ne doit pas être écrasé.

## Test anti-réduction

Avant d'accepter un modèle, demande :

> Si je convertis tout en cette structure, quelles distinctions du domaine deviennent impossibles à reconstruire ?

Si la réponse contient quelque chose d'important, la structure est trop pauvre.

## Test anti-surmodélisation

À l'inverse :

> Est-ce que cette classe/relation/dimension existe parce que le domaine l'exige, ou parce que mon template la proposait ?

Supprimer ce qui n'est pas justifié.

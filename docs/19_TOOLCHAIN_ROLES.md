# 19 — Responsabilités de la toolchain

## Kristal Local Kit
Structure, sources, canon, validation locale et build v9.

## Kristal Manager
Inventaire des Local Kristals et synchronisation GitHub de chaque dossier complet vers un repo GitHub individuel, public ou privé.

## Kristal GitHub Bootstrap / Setup
Le **Bootstrap** est le produit/moteur d'infrastructure. **Setup** est son interface `.pyw`. Il gère les nœuds/collections, qualification, publication et activation.

## Kompiler
Outil optionnel de lecture/query/context pack. Il ne possède aucun lifecycle canonique.

## Médiathèque Kristal Sources
Réservoir de sources en amont. Une source n'est pas automatiquement un artefact canonique; son adoption dans un Local Kristal passe par le modèle/provenance du Kristal.

## Principe

```text
source → Local Kristal → synchronisation GitHub (Manager)
                       → build v9 (Local Kit)
                       → publish/activate (GitHub Setup)
                       → read/query (Kompiler)
```

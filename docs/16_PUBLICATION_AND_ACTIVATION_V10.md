# 16 — Publication et activation v10

La publication réseau de référence produit une Release contenant au minimum :

- `state-snapshot.json` ;
- `bundle-manifest.json` ;
- `publication.json`.

Le workflow lie la Release au commit Git exact qualifié. Le parcours principal appartient à **Kristal GitHub Setup/Bootstrap**, qui vérifie qualification, bundle et Release avec le Framework piné. Les commandes GitHub du Local Kit restent des compatibilités avancées.

Activation reste une transition mutable séparée. Le Local Kit 3.2 n'active pas automatiquement un channel après publication.

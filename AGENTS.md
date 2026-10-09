# AGENTS.md — Kristal Local Kit v3.2

Ce dépôt outille des **Local Kristals**.

Principes :

1. préserver la sémantique v9 et les Logical Commitments ;
2. ne jamais mélanger synchronisation GitHub, hosting, publication ou activation avec l'identité sémantique ;
3. traiter `ai/` et Kompiler comme une couche de lecture optionnelle et dérivée ;
4. utiliser Kristal Manager pour l'inventaire, la validation et la synchronisation GitHub public/privé de la read surface ;
5. utiliser Kristal GitHub Setup/Bootstrap comme parcours principal de qualification/publication/activation réseau ;
6. conserver les commandes `github-*` de ce kit uniquement comme compatibilité avancée ;
7. ne pas rendre une sortie IA canonique sans validation explicite.

Le build local normal est `check` → `build-v9`.

Interop locale : utiliser `python tools/kristal.py inspect <workspace>` et `python tools/kristal.py read-surface <workspace>` pour une vue machine read-only ; ne jamais traiter cette sortie comme du canon sémantique.

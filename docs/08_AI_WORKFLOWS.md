# 08 — Workflows IA (optionnels)

L'IA n'est pas une étape obligatoire du lifecycle d'un Local Kristal.

## Deux usages

1. **IA qui aide à modifier** : elle suit `AGENTS.md`; ses sorties restent des propositions jusqu'à validation.
2. **IA qui lit** : Kompiler ou une capsule `pack-ai` peut fournir un read model dérivé.

## Workflow local normal

```text
Local Kristal → check → build-v9
```

Aucun fichier `AI_MANIFEST.json` ou `ai/*` n'est requis.

## Quand une couche IA est utile

```bash
python tools/kristal.py build-ai .
python tools/kristal.py check-ai .
python tools/kristal.py pack-ai . --output Mon-Kristal-portable-ai.zip
```

Ou `build-v9 --with-ai`. Le read model reste dérivé, reconstruisible et n'entre jamais dans le Logical Commitment.

## Kompiler

Kompiler demeure un outil de lecture/contexte en aval. Il ne possède ni l'inventaire des Local Kristals, ni leur synchronisation GitHub, ni leur publication/activation.

## Publication v10

Une IA peut aider à préparer les changements, mais le chemin réseau recommandé reste Kristal GitHub Setup/Bootstrap.

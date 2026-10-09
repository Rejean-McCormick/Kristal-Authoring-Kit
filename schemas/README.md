# Local Kit schemas

- `workspace.schema.json` — enveloppe locale v3.2 : v9 semantic state + portable-AI read layer + optional v10 hosted network.
- `portable-ai-manifest.schema.json` — entrypoint machine-readable de la capsule offline `kristal.portable-ai/1.0`.
- `ai-index.schema.json` — index déterministe des fichiers utiles à la lecture IA, avec rôles et SHA-256.
- `ai-coverage.schema.json` — portée, ownership, références externes et limites explicites.
- `state-index.schema.json` — registre v2 inchangé des Logical Artifacts/références canoniques.
- `kristal-materialization-manifest.schema.json` — copie locale du contrat normatif v9 utilisé pour les matérialisations physiques.
- `kristal-v9-capabilities.schema.json` — copie locale du descriptor de capabilities v9.
- `source-catalog.schema.json` — sources du Local Kristal.
- `projection-recipe.schema.json` — projections portables.
- `github-hosting.schema.json` — liaison opérationnelle optionnelle d'un workspace vers un nœud GitHub v10.

Les schémas du Local Kit et de lecture IA ne remplacent pas les schémas normatifs du Kristal Framework. La couche `ai/` est dérivée et n'entre jamais dans le Logical Commitment v9.

- `github-read-surface.schema.json` — projection dérivée exacte à synchroniser sous `kristals/<slug>/` pour lecture GitHub/IA.

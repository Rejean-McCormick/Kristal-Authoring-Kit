<!-- kOA Doc Server · Docs IA · lot 02 · rédaction dérivée d’une capture, à valider par le propriétaire -->
# Navigation IA — Kristal-Authoring-Kit

**Rôle observé :** Atelier local de construction, validation et empaquetage des états Kristal, avec profils v9/v10 préservés et v11 en option.

**Autorité :** Le propriétaire du Kristal autorise son état; le Kit construit mais ne publie ni n'active sur l'hôte.

**Provenance :** `SmartDump_20261120_221507.zip` → `Kristal-Authoring-Kit_Code_snapshot.zip` (20 novembre 2026). Cette capture ne prouve ni la présence actuelle du dossier Windows, ni un déploiement, ni une qualification.

## Objet et état de cette fiche

La description ci-dessous est rattachée au `README.md` du snapshot; vérifier le code actif sur le poste. Cette fiche est un **guide de navigation**, non une spécification normative ni une validation de maturité.

## Processus conseillé

1. **Identifier la source et le profil.** Lire profil et contrats épinglés, examiner les sources, exécuter les vérifications natives dans un workspace d'essai et conserver les reçus.
2. **Contrôler l’autorité.** Le propriétaire du Kristal autorise son état; le Kit construit mais ne publie ni n'active sur l'hôte.
3. **Préparer un environnement de test.** Utiliser les fichiers réels de la révision étudiée et des données fictives ou autorisées.
4. **Vérifier sans promouvoir.** Documenter commandes, périmètre, résultat, chemins et empreintes; ne jamais transformer une observation locale en preuve historique validée.
5. **Revue propriétaire.** Une publication, activation, import ou effet externe nécessite l’accord du propriétaire et les gates correspondants.

## Garde-fous particuliers

- Ne pas convertir un ancien état en v11 par simple convention documentaire; pas de publication implicite.
- N’inclure aucun secret, donnée personnelle, sauvegarde privée ou sortie de diagnostic non autorisée dans les exports Doc Server.
- Préserver l’intégrité des sources et des états historiques; éviter toute réécriture automatique des références.

## Sources d’orientation vérifiables dans le snapshot

1. [`README.md`](../../README.md) — source propriétaire présente dans le snapshot.
2. [`docs/06_LAYOUT_AND_LIFECYCLE.md`](../../docs/06_LAYOUT_AND_LIFECYCLE.md) — source propriétaire présente dans le snapshot.
3. [`docs/07_VALIDATION.md`](../../docs/07_VALIDATION.md) — source propriétaire présente dans le snapshot.
4. [`docs/11_V9_STATE_ARCHITECTURE.md`](../../docs/11_V9_STATE_ARCHITECTURE.md) — source propriétaire présente dans le snapshot.
5. [`docs/24_CONSOLIDATION_CONSUMER_CONTRACTS.md`](../../docs/24_CONSOLIDATION_CONSUMER_CONTRACTS.md) — source propriétaire présente dans le snapshot.
6. [`docs/27_DIK_INTEGRATION.md`](../../docs/27_DIK_INTEGRATION.md) — source propriétaire présente dans le snapshot.
7. [`docs/28_V11_FRAMEWORK_QUALIFICATION.md`](../../docs/28_V11_FRAMEWORK_QUALIFICATION.md) — source propriétaire présente dans le snapshot.
8. [`docs/01_MENTAL_MODEL.md`](../../docs/01_MENTAL_MODEL.md) — source propriétaire présente dans le snapshot.

## Compatibilité Framework

S’il y a une dépendance Kristal, lire la révision du Framework et le profil **effectivement adoptés** par ce dépôt. Les nouvelles conventions v11 (identités sémantiques, dictionnaires séparés, provenance) servent de référence lorsque compatibles; **ne pas bloquer** la navigation IA ni imposer la migration de données historiques pour cette seule raison.

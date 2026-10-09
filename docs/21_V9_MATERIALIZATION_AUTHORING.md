# 21 — Authoring des matérialisations v9

## But

Le Logical Artifact et son Logical Commitment restent indépendants de leur représentation physique. Le Local Kit 3.2.4 sait désormais **préserver et vérifier des Materialization Manifests v9 existants** au lieu de retomber systématiquement sur `inline-json/1`.

Le kit ne choisit pas à la place du domaine un profil de factorisation. Les profils custom restent légitimes, par exemple :

```text
pokemon.materialization/factorized-zstd/1
```

## Emplacements découverts

Le kit découvre automatiquement les manifests v9 sous :

```text
materializations/v9/manifests/**/*.json
.kristal/v9/materializations/**/*.json   # layout legacy accepté
```

Seuls les documents ayant `artifact_type = kristal_materialization_manifest` sont traités comme manifests.

## Enregistrement explicite

Pour importer un manifest existant dans le layout d'authoring courant :

```bash
python tools/kristal.py register-materialization . \
  --manifest path/to/materialization.json
```

Le manifest est refusé si son `source.artifact_id`, son Logical Contract ou son Logical Commitment ne correspondent pas au Logical Artifact canonique courant.

## Validation

`check` vérifie :

- enveloppe v9 du manifest ;
- présence d'au moins un segment ;
- `reconstructability.lossless=true` ;
- binding exact au Logical Artifact canonique ;
- unicité des `materialization_id` et `segment_key` ;
- forme des Blob Digests et tailles ;
- pour un `locator` local présent : taille et SHA-256 réels du blob.

Un locator non local, ou un blob local actuellement absent, n'est pas téléchargé silencieusement. Le kit émet un avertissement : v9 autorise la disponibilité partielle et les resolvers externes.

## Build

`build-v9` :

1. calcule les Logical Artifacts et le State Snapshot comme avant ;
2. génère `inline-json/1` pour les artifacts JSON calculés localement ;
3. copie également les manifests v9 existants validés dans `build/v9/materializations/` ;
4. agrège les profils réellement présents dans `v9-capabilities.json` ;
5. dérive `segmentation` depuis les manifests multi-segments ;
6. dérive `factorization` depuis les dictionnaires, les extensions de capability explicites, ou un descriptor v9 existant qui couvre effectivement un profil découvert.

Les manifests importés ne participent ni au Logical Commitment d'un artifact, ni au State Commitment.

### Pas de duplication des gros blobs

Le build **ne recopie pas automatiquement les blobs référencés** par un manifest existant. Il copie/normalise le descriptor dans `build/v9/materializations/` et conserve les locators physiques déclarés.

Cette règle évite qu'un corpus de plusieurs centaines de Mo soit dupliqué à chaque `build-v9`. Une capsule d'échange autonome qui embarque les blobs est une opération de transport distincte et ne doit pas être confondue avec le build sémantique local.

```text
MANIFEST PRESERVATION != BLOB DUPLICATION
```

## Capabilities héritées

Pour les anciens Kristals, le kit peut lire comme **hint non sémantique** :

```text
.kristal/v9/capabilities.json
```

Les flags de matérialisation ne sont hérités que si ce descriptor mentionne au moins un profil réellement découvert dans les manifests courants. Cela permet de préserver proprement des profils custom existants sans les deviner à partir de leur nom.

Pour un nouveau profil custom qui factorise sans dictionnaire et sans descriptor legacy, l'auteur peut déclarer le hint physique non sémantique :

```json
{
  "extensions": {
    "capabilities": {
      "factorization": true,
      "segmentation": true
    }
  }
}
```

## Read model IA / GitHub

`build-ai` indexe les Materialization Manifests découverts avec le rôle `materialization_manifest`. Les blobs référencés ne sont pas injectés automatiquement dans la liste de fichiers Git/portable : ils sont décrits dans `ai/INDEX.json.materialization_blobs` avec leur locator, disponibilité, taille, digest et `transport_class=materialization`. Pour un blob workspace-local, taille et SHA-256 réels sont aussi exposés.

`ai/COVERAGE.json` expose séparément le nombre de manifests, de blobs locaux disponibles, de locators externes et de locators locaux actuellement absents. Une IA peut donc savoir si elle dispose des octets localement sans confondre disponibilité physique et identité logique.

`read-surface` réutilise exactement cet index pour la projection GitHub. Les manifests restent dans `files`; les bytes apparaissent séparément dans `materialization_objects` pour que le hosting choisisse une technologie GitHub adaptée (arbre Git, Release, GHCR, LFS, etc.). Aucun fetch distant n'est effectué par le Local Kit.

## Invariant

```text
REPACK / RESEGMENT / RECOMPRESS
        !=
LOGICAL CHANGE
```

Tant que la reconstruction définie par le profil reste lossless et que le Logical Commitment source est inchangé, la représentation physique peut évoluer indépendamment.

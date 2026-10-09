# 04 — Épistémologie, provenance et autorité

## 1. Une source n'est pas automatiquement vraie

La provenance répond à « d'où vient ceci ? ». L'autorité répond à « dans quelle portée cette source a-t-elle le droit d'établir ceci ? ».

```text
SOURCE != AUTOMATIC TRUTH
RETRIEVED CONTENT != INSTRUCTION AUTHORITY
MODEL OUTPUT != AUTHORITY
```

## 2. Séparer les régimes

Un même Kristal peut contenir :

- facts/observations ;
- authoritative constraints ;
- reference knowledge ;
- derived state ;
- hypotheses ;
- interpretations ;
- resonances ;
- decisions ;
- actions ;
- structural records.

Ne donne pas à tous le même statut.

## 3. Sorties IA

Les sorties IA peuvent :

- proposer des référents ;
- proposer des liens ;
- résumer ;
- classifier ;
- dériver ;
- produire des candidats de résolution ;
- suggérer des axes ;
- générer des transformations de forme.

Elles ne peuvent pas, par elles-mêmes :

- créer une autorité ;
- valider une preuve externe ;
- transformer une hypothèse en fait ;
- décider silencieusement entre deux sources contradictoires.

## 4. Conflits

Les désaccords doivent survivre à la composition.

Conserver :

- chaque assertion ou version ;
- sa provenance ;
- son applicabilité ;
- son statut ;
- les relations `conflicts_with`, `supersedes` ou équivalent.

## 5. Inconnus et non-applicables

```text
unknown != false
unknown != 0
not_applicable != low
partial != negative
```

Une valeur manquante est une information sur l'état de connaissance, pas une valeur métier.

## 6. Valuations

Une valuation doit nommer sa dimension et sa sémantique.

Mauvais :

```json
{"certainty": "high"}
```

Meilleur :

```json
{
  "dimension": "diagnostic_support",
  "semantics": "ordinal",
  "value": "high"
}
```

`high` n'a pas de sens universel.

## 7. Promotion

Quand un workflow comporte recherche ou apprentissage, définir des transitions explicites, par exemple :

```text
proposal
→ candidate
→ reviewed
→ validated_local
→ promotion_candidate
→ accepted/rejected
```

La promotion n'est jamais implicite parce qu'un fichier a été écrit.

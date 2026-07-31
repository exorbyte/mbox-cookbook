# M|BOX Python SDK

**Identity Resolution & Explainable Data Matching**

The **M|BOX** Python SDK brings our high-performance, fault-tolerant matching core directly into your Python and Pandas workflows. Built for enterprise data harmonization, it provides the deterministic, explainable data foundation required for robust agentic data retrieval systems. Search, match, and resolve identities in milliseconds without relying on rigid pre-filtering.

## Installation

Get started instantly by installing the SDK via pip:

```bash
pip install mbox
```

## Core Architecture: Two-Phase Matching
mbox operates on a strict two-phase architecture to deliver sub-50 ms search performance and fully explainable matching.

During the Indexing Phase, raw data is transformed into a highly optimized compiled index using configurable schema definitions. Once built, the index can be reused indefinitely or serialized for instant loading.

During the Recall Phase, queries are executed against the compiled index using configurable matching rules, producing transparent, scored results that are easy to inspect, validate, and integrate into downstream workflows.

## Quick Start: Match in 3 Lines

Transform any Pandas DataFrame into a fault-tolerant search index and start querying immediately.

```python
import pandas as pd
from mbox.indexing import TableIndexer

# Dummy data for demonstration
df = pd.DataFrame({
    "full_name": ["Robert Smith", "Katharina Müller", "Jochen Meyer"],
    "city": ["Konstanz", "Berlin", "Munich"]
})

# 1. Create an index from your existing DataFrame
index = TableIndexer.create_index(df, index_columns=["full_name", "city"])

# 2. Perform a fuzzy match with typos or variations
results = index.match(
    full_name="Bob Smit", 
    city="Konstanz", 
    include_field_scores=True
)

print(results)
```

**Example Output:**

The engine returns the best candidates along with explainable quality scores for every field.

| query_row | index_row | overall_score | full_name_candidate | full_name_score | city_candidate | city_score |
|-----------|-----------|---------------|---------------------|-----------------|----------------|------------|
| 0         | 142       | 88            | Robert Smith        | 85              | Konstanz       | 100        |
| 0         | 89        | 62            | Bodo Schmidt        | 65              | Konstanz       | 100        |

## Saving and Loading the Index

For production environments, you don't need to rebuild your index from the source DataFrame every time your application starts. You can compile your index into a highly optimized binary file, save it to disk, and load it instantly.

```python
from mbox.indexing import TableIndex

# Save the compiled index to a zip archive
index.to_binary("./customer_index.zip")

# Later, load the index back into memory
loaded_index = TableIndex.load_binary("./customer_index.zip")

# You are immediately ready to match again
results = loaded_index.match(full_name="Bob Smit", city="Konstanz")
```

## Data Harmonization: Mappings & Aliases

Real-world data is messy. Seamlessly inject domain knowledge into your index using `CharacterMapping` (to handle accents, casing, and special characters) and `AliasSet` (to handle synonyms and nicknames).

```python
from mbox.mapping import CharacterMapping
from mbox.aliases import AliasSet

# Standardize text (e.g., expand umlauts, deaccentuate, map casing)
german_mapping = CharacterMapping.create_german_standard()

# Define synonyms with custom penalties
name_aliases = AliasSet(name="first_names")
name_aliases.add(word="Robert", alias="Bob", penalty=0)
name_aliases.add(word="Katharina", alias="Kathi", penalty=5)

# Build the index with your rules applied
index = TableIndexer.create_index(
    df=df,
    index_columns=["full_name", "city"],
    character_mappings={"full_name": german_mapping},
    alias_sets={"full_name": name_aliases}
)
```

## Advanced Index Configuration

For production pipelines, you may need granular control over how data is tokenized and stored. While `TableIndexer` infers the best setup by default, you can explicitly define your architecture using `TableConfig`, `TableFieldConfig`, and `IndexType`.

```python
from mbox.config import TableConfig, TableFieldConfig, IndexType

# Explicitly define the behavior for each field
name_field = TableFieldConfig(
    column="full_name",
    index_type=IndexType.PHRASE,
    character_mapping=german_mapping,
    aliases=name_aliases
)

city_field = TableFieldConfig(
    column="city",
    index_type=IndexType.PHRASE
)

age_field = TableFieldConfig(
    column="age",
    index_type=IndexType.INTEGER
)

metadata_field = TableFieldConfig(
    column="source_system",
    index_type=IndexType.NON_SEARCHABLE # Available in results, but not searched
)

# Assemble the configuration and build
advanced_config = TableConfig(fields=[name_field,
                                      city_field,
                                      age_field,
                                      metadata_field
                                      ])

advanced_index = TableIndexer.create_index(df=df, config_overrides=advanced_config)

# Save your schema for reuse
advanced_config.to_json("./customer_index_schema.json")
```

## Advanced Recall Configuration

Control exactly how the engine evaluates a match at query time. Using `TableRecallConfig` and `TableRecallFieldConfig`, you can dictate field weights, minimum quality thresholds, and the algorithmic matching mode (`TableRecallMode`) on a per-field basis.

**Available String Modes:**

- `APPROX`: Levenshtein-based similarity (handles typos and phonetic variations).
- `EXACT`: Requires full strict equality.
- `COMPLETE`: Substring containment (input value exists within the indexed value).
- `DETECT`: Substring containment (indexed value exists within the input).

```python
from mbox.recall import TableRecallConfig, TableRecallFieldConfig, TableRecallMode

query_df = pd.DataFrame({
    "search_name": ["Bob Smit"],
    "search_city": ["Konstanz"]
})

# Define specific search behavior per field
name_recall = TableRecallFieldConfig(
    input_column="search_name",
    indexed_column="full_name",
    minimum_quality=60,       # Field must score at least 60
    weight=80,                # High impact on the overall_score
    mode=TableRecallMode.APPROX
)

city_recall = TableRecallFieldConfig(
    input_column="search_city",
    indexed_column="city",
    minimum_quality=100,
    weight=20,
    mode=TableRecallMode.EXACT # Must be a perfect match
)

# Assemble the recall settings
recall_settings = TableRecallConfig(
    fields=[name_recall, city_recall],
    max_results=5,
    min_total_match_value=75,
    max_quality_spread=20,     # Stop returning results if quality drops > 20 below the best match
    include_field_scores=True, # Explainability: show score per column
    include_queries=True, 
)

# Execute the finely-tuned search
results_advanced = advanced_index.match(
    queries=query_df,
    config=recall_settings
)

print(results_advanced)
```

*M|BOX is currently in `beta` status. We are iterating on adding more capabilities to the Python SDK.
Breaking changes may occur in minor releases until version `1.0.0`.*

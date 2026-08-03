# M|BOX Python SDK Cookbook
**Deterministic Data Resolution for Agentic AI**

Practical, runnable recipes for the [M|BOX Python SDK](https://exorbyte.ai/produkte/mbox-python/docs/getting-started/overview-quickstart): fuzzy matching and identity resolution for Python and Pandas, with field level explainability instead of black box embeddings.

```bash
pip install mbox
```

[Get started in under 5 minutes](01-getting-started/01_installation_and_quickstart.ipynb) &nbsp;·&nbsp; [Full documentation](https://exorbyte.ai/produkte/mbox-python/docs/getting-started/overview-quickstart)

## Where to start

New to M|BOX? Follow this order:

1. [`01-getting-started/`](01-getting-started/) : install, first index, first match
2. [`02-data-harmonization/`](02-data-harmonization/) : clean messy real world data before indexing
3. [`03-recall-tuning/`](03-recall-tuning/) : control precision, weights, and matching modes
4. [`04-explainability/`](04-explainability/) : understand why a match scored what it did
5. [`05-agentic-ai/`](05-agentic-ai/) : use M|BOX as a tool inside LLM and agent workflows
6. [`06-integrations/`](06-integrations/) : pandas pipelines, FastAPI services
7. [`07-production/`](07-production/) : schemas, validation, benchmarks for real deployments
8. [`08-use-cases/`](08-use-cases/) : complete end to end demo scenarios
9. [`09-community/`](09-community/) : recipes contributed by the community

Each notebook is self contained. You do not need to work through the repo in order, jump to whatever solves your problem.


### Try it without installing anything

| Notebook | Launch |
|---|---|
| [Installation & Quickstart](01-getting-started/01_installation_and_quickstart.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/exorbyte/mbox-cookbook/blob/main/01-getting-started/01_installation_and_quickstart.ipynb)  |
| [Loading Your Own CSV](01-getting-started/02_loading_your_own_csv.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/exorbyte/mbox-cookbook/blob/main/01-getting-started/02_loading_your_own_csv.ipynb) |
| [Saving & Loading Indexes](01-getting-started/03_saving_and_loading_indexes.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/exorbyte/mbox-cookbook/blob/main/01-getting-started/03_saving_and_loading_indexes.ipynb) |


## Why deterministic matters

Most fuzzy matching today relies on embeddings and similarity scores you can't fully explain. M|BOX takes a different approach: matches are computed deterministically, and every result can be broken down field by field so you can see exactly why a candidate scored the way it did. That's what makes it a safe building block for agentic systems, where an agent needs to ground its output in data it can trust and explain, not just data that looks close.

## Requirements

* Python 3.9+
* `pip install mbox`
* Some recipes use `pandas`; a few in `05-agentic-ai/` also require an API key for the relevant LLM provider (noted at the top of each notebook)

## Contributing

We welcome recipes from the community. See [CONTRIBUTING.md](CONTRIBUTING.md) for the format and submission process. Good candidates: novel use cases, integrations with other tools, and domain specific examples (finance, healthcare, logistics, and similar) that are broadly useful to others.

## License

See [LICENSE](LICENSE).
# Libdots

Library to build [DOTS](https://github.com/dots-energy/) calculation services.

# Documentation
* https://libdots.readthedocs.io/en/latest/

# Installation
* `pip install libdots`
or with extras
* `pip install libdots[google-cloud]`

# Development
* `poetry self add poethepoet poetry-plugin-export`
* `poetry install --all-extras --with=docs`
* `poetry run pre-commit install`
* `poetry run pytest`

# Generate docs
* `poetry install --with=docs`
* `poetry build-docs`

Generate requirements.txt in docs:
* `poetry export --only=docs > docs/requirements.txt`

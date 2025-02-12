# Libdots

Library to build [DOTS](https://github.com/dots-energy/) calculation services.

# Installation
* `pip install libdots`
or with extras
* `pip install libdots[google-cloud]`

# Development
* `poetry install --all-extras`
* `poetry run pre-commit install`
* `poetry run pytest`

# Generate docs
* `poetry install --with=docs`
* `poetry run sphinx-build -M html docs/ docs/_build/`

Generate requirements.txt in docs:
* `poetry export --only=docs > docs/requirements.txt`

# zuos-python-package-template
Template repository to be used to base other python packages off.

In order to create a new pacakge:
* Base a new repository off this one.
* Clone the repository
* Replace `zuos_python_package_template` and `zuos-python-package-template` in the following files (making sure to keep _ vs - unchanged).
  * pyproject.toml
  * .github/workflows/ci.yml
* Run `poetry lock`
* Update the README.md

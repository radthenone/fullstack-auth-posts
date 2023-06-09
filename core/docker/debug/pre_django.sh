#!/bin/bash
echo "Start tests and linter configuration"

if [ $PWD == "/src" ]; then
    echo "Run pytest"
    pytest -s -v --no-migrations
    echo "End pytest"

    echo "Run coverage"
    pytest --cov-config=.coveragerc && coverage html
    echo "End coverage"

    echo "Run mypy"
    mypy . --config-file mypy.ini --explicit-package-bases
    echo "End mypy"

    echo "Run flake8"
    flake8 . --config=setup.cfg
    echo "End flake8"

    echo "Run isort"
    isort . --settings-path=isort.cfg
    echo "End isort"
else
    echo "Wrong run"
fi

echo "End of tests and linter configuration"

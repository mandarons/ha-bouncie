#!/bin/bash
deleteDir() {
    if [ -d $1 ]; then rm -rf $1; fi
}
deleteFile() {
    if [ -f $1 ]; then rm -f $1; fi
}
echo "Cleaning ..."
deleteDir .pytest_cache
deleteDir .mypy_cache
deleteDir allure-results
deleteDir allure-report
deleteDir htmlcov
deleteFile .coverage
deleteFile coverage.xml

echo "Linting ..." &&
    pylint custom_components/ tests/ &&
    # echo "Type checking ..." &&
    # mypy custom_components/ &&
    echo "Testing ..." &&
    pytest --cov --cov-report html --cov-report xml --alluredir=./allure-results --cov-config=Coveragerc --cov-fail-under=100
    echo "Reporting ..." &&
    allure generate --clean
echo "Done."
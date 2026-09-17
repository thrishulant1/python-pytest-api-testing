# API Automation with python, pytest for reqres.in

This project is a Python-based API automation framework for testing the `reqres.in` RESTful web service. It uses the pytest testing framework and GitHub Actions for continuous integration.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Test execution](#runtests)
- [GitHub Workflow](#workflow)

## Features

- Automated testing of various API endpoints on `reqres.in`.
- Positive, negative, and edge test cases.
- Continuous integration with GitHub Actions.
- Dynamic working directory setup in the GitHub Actions workflow.
- Test report generation and saving as an artifact.

## Prerequisites

Before you get started, ensure you have the following prerequisites:

- Python 3.x
- `pip` for package management

## Installation

git clone https://github.com/thrishulant1/python-pytest-api-testing.git

cd python-pytest-api-testing

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt


## Test execution

pytest tests/test_users.py


## Test Reports
The tests generate an HTML test report, which can be found in the project directory as report.html.

## GitHub Workflow
This project includes a GitHub Actions workflow that automates the testing process on each push, pull request, and a daily schedule. The workflow is configured in the .github/workflows directory.

Push: The workflow is triggered automatically when changes are pushed to the main branch.

Pull Request: It's also triggered when pull requests are created or updated.

Scheduled Run: The workflow runs daily at midnight UTC to ensure regular testing.

Manual Run: You can manually trigger the workflow using the "Run workflow" button in the GitHub Actions tab.

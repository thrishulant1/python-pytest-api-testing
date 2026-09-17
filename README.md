# API Automation with Python & Pytest for reqres.in

![CI](https://github.com/thrishulant1/python-pytest-api-testing/actions/workflows/main.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.x-blue)
![Pytest](https://img.shields.io/badge/tested%20with-pytest-0A9EDC)

A Python API test automation framework built around **pytest**, targeting the public
[`reqres.in`](https://reqres.in) REST API. It demonstrates a small, readable structure for
API testing: a reusable HTTP client, shared fixtures, custom assertions, HTML/Allure reporting,
and a GitHub Actions CI pipeline.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Test Coverage](#test-coverage)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Tests](#running-the-tests)
- [Test Reports](#test-reports)
- [CI/CD with GitHub Actions](#cicd-with-github-actions)

## Features

- Thin, dependency-light HTTP client wrapper around `requests`.
- Positive, negative, and edge-case test scenarios for the `/api/users` endpoints.
- Reusable pytest fixtures (`conftest.py`) and custom assertion helpers.
- HTML test reports via `pytest-html`, with optional Allure reporting support.
- GitHub Actions workflow to run the suite and publish the report as a build artifact.

## Project Structure

```
python-pytest-api-testing/
├── .github/workflows/main.yml   # CI pipeline definition
├── config.py                    # Base URL for the API under test
├── conftest.py                  # Shared pytest fixtures (api client, auth token)
├── pytest.ini                   # Pytest configuration (report output, etc.)
├── requirements.txt             # Python dependencies
├── env_setup.txt                # Quick reference for local venv commands
├── src/
│   ├── api_client.py             # APIClient: GET/POST/PUT/DELETE wrapper
│   ├── assertions.py              # Reusable custom assertions
│   └── helpers.py                 # Place for additional shared test utilities
└── tests/
    ├── test_data.json              # Sample request payloads used by the tests
    └── test_users.py                # Test cases for the /api/users endpoints
```

## How It Works

1. **`config.py`** holds the single source of truth for the API's base URL
   (`https://reqres.in`).
2. **`src/api_client.py`** defines `APIClient`, a small wrapper around `requests` with
   `get`, `post`, `put`, and `delete` methods that prefix every request with the base URL.
3. **`conftest.py`** exposes an `api` fixture that hands each test a ready-to-use
   `APIClient` instance, plus an `auth_token` fixture as a placeholder for tests that
   need authentication.
4. **`tests/test_users.py`** uses the `api` fixture to call the endpoints under test, then
   asserts on status codes and response bodies — either directly or via the helpers in
   `src/assertions.py`.
5. **`tests/test_data.json`** centralizes sample payloads (e.g. user create/update data)
   so test data isn't duplicated across test functions.

This keeps each test focused on *behavior* (what the API should do) rather than on
HTTP or request plumbing.

## Test Coverage

`tests/test_users.py` covers the `/api/users` resource:

| Test | Type | What it checks |
|---|---|---|
| `test_list_users` | Positive | Listing users returns `200` with a non-empty list, each with `id` and `email` |
| `test_get_single_user` | Positive | Fetching one user by ID returns the expected `id`/`email` |
| `test_create_user` | Positive | Creating a user returns `201` with the submitted data echoed back |
| `test_update_user` | Positive | Updating a user returns `200` with the updated fields |
| `test_delete_user` | Positive | Deleting a user returns `204` |
| `test_user_not_found` | Negative | Requesting a non-existent user returns `404` |
| `test_user_pagination` | Edge | Paginated listing returns the requested page size |
| `test_concurrent_requests` | Edge | Ten concurrent `GET` requests all succeed |
| `test_create_user_invalid_data` | Negative | *Skipped* |
| `test_unauthorized_access` | Negative | *Skipped* |
| `test_create_user_max_data_size` | Edge | *Skipped* |

The three skipped tests are marked `@pytest.mark.skip` because `reqres.in` is a public
mock API that doesn't actually enforce input validation, authentication, or payload-size
limits — it returns success for arbitrary input. They're kept in the suite as examples of
how such cases *would* be tested against a real backend that enforces these rules.

## Prerequisites

- Python 3.x
- `pip` for package management

## Installation

```bash
git clone https://github.com/thrishulant1/python-pytest-api-testing.git
cd python-pytest-api-testing

python -m venv venv
venv\Scripts\activate      # on Windows
# source venv/bin/activate # on macOS/Linux

pip install -r requirements.txt
```

## Running the Tests

Run the full suite:

```bash
pytest tests/test_users.py
```

Run with verbose output:

```bash
pytest -v tests/test_users.py
```

Run a single test:

```bash
pytest tests/test_users.py::test_list_users
```

## Test Reports

**HTML report (default):** `pytest.ini` is configured with `pytest-html`, so every run
writes a self-contained HTML report to `reports/report.html`. Open it in a browser after
running the tests to see a pass/fail breakdown per test.

**Allure report (optional):** `allure-pytest` is included in `requirements.txt` for a
richer, interactive report:

```bash
pytest --alluredir=./allure-results
allure generate ./allure-results -o ./allure-report --clean
allure open ./allure-report
```

(Requires the [Allure commandline](https://docs.qameta.io/allure/#_installing_a_commandline)
to be installed separately.)

Generated reports (`reports/`, `allure-results/`, `allure-report/`) are intentionally not
committed to the repository — they're build output, regenerated on every run. When the
suite runs in CI, the HTML report is uploaded as a downloadable workflow artifact (see
below) instead of being checked into source control.

## CI/CD with GitHub Actions

The workflow in `.github/workflows/main.yml` runs automatically:

- **On every push to `main`**
- **On every pull request**
- **On a daily schedule** (midnight UTC), so regressions in the external API are caught
  even without any code changes
- **On demand**, via the **Run workflow** button on the *Actions* tab (or `gh workflow run main.yml`)

On each run it:

1. Checks out the repository.
2. Sets up Python.
3. Installs dependencies from `requirements.txt`.
4. Runs `pytest -v tests/test_users.py --html=report.html`.
5. Uploads `report.html` as a workflow artifact you can download from the run's summary
   page.

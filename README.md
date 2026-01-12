[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=softwareone-platform_swo-extension-playground&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=softwareone-platform_swo-extension-playground)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=softwareone-platform_swo-extension-playground&metric=coverage)](https://sonarcloud.io/summary/new_code?id=softwareone-platform_swo-extension-playground)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

# SoftwareONE Extension playground

Playground Extension with the SoftwareONE Marketplace


## Getting started

### Prerequisites

- Docker and Docker Compose plugin (`docker compose` CLI)
- `make`
- Valid `.env` file
- Adobe credentials and authorizations JSON files in the project root
- [CodeRabbit CLI](https://www.coderabbit.ai/cli) (optional. Used for running review check locally)


### Make targets overview

Common development workflows are wrapped in the `makefile`:

- `make help` – list available commands
- `make bash` – start the app container and open a bash shell
- `make build` – build the application image for development
- `make check` – run code quality checks (ruff, flake8, lockfile check)
- `make check-all` – run checks and tests
- `make format` – apply formatting and import fixes
- `make down` – stop and remove containers
- `make review` –  check the code in the cli by running CodeRabbit
- `make run` – run the service
- `make shell` – open a Django shell inside the running app container
- `make test` – run the test suite with pytest

## Running tests

Tests run inside Docker using the dev configuration.

Run the full test suite:

```bash
make test
```

Pass additional arguments to pytest using the `args` variable:

```bash
make test args="-k test_playground -vv"
make test args="tests/test_steps.py"
```

## Running the service

### 1. Configuration files

In the project root, create and configure the following files.

#### Environment files

Start from the sample file:

```bash
cp .env.sample .env
```

Update `.env` with your values. This file is used by all Docker Compose configurations and the `make run` target.

### 2. Running

Run the service against real SoftwareONE Marketplace APIs. It uses `compose.yaml` and reads environment from `.env`.

Ensure:
- `.env` is populated with real endpoints and tokens.

Start the app:

```bash
make run
```

The service will be available at `http://localhost:8080`.

Example `.env` snippet for real services:

```env
MPT_PRODUCT_ID=PRD-1111-1111,PRD-2222-2222
MPT_PORTAL_BASE_URL=https://portal.s1.show
MPT_API_BASE_URL=Lhttps://api.s1.show/public
MPT_API_TOKEN=<c0fdafd7-xxxx-xxxx-xxxx-xxxxxxxxxxxx
MPT_ORDERS_API_POLLING_INTERVAL_SECS=120
EXT_WEBHOOKS_SECRETS={"PRD-1111-1111": "<webhook-secret-for-product>", "PRD-2222-2222": "<webhook-secret-for-product>"}
MPT_INITIALIZER="swo_playground.initializer.initialize"
MPT_KEY_VAULT_NAME=""
MPT_NOTIFY_CATEGORIES={"ORDERS": "NTC-0000-0006"}
```

`MPT_PRODUCTS_IDS` is a comma-separated list of SWO Marketplace Product identifiers.
For each product ID in the `MPT_PRODUCTS_IDS` list, define the corresponding entry in the `WEBHOOKS_SECRETS` JSON using the product ID as the key.


## Developer utilities

Useful helper targets during development:

```bash
make bash      # open a bash shell in the app container
make check     # run ruff, flake8, and lockfile checks
make check-all # run checks and tests
make format    # auto-format code and imports
make review    # check the code in the cli by running CodeRabbit
make shell     # open a Django shell in the app container
```


# Configuration

The following environment variables are typically set in `.env`. Docker Compose reads them when using the Make targets described above.

## Application

| Environment Variable            | Default                 | Example                               | Description                                                                                |
|---------------------------------|-------------------------|---------------------------------------|--------------------------------------------------------------------------------------------|
| `EXT_WEBHOOKS_SECRETS`          | -                       | {"PRD-1111-1111": "123qweasd3432234"} | Webhook secret of the Draft validation Webhook in SoftwareONE Marketplace for the product  |
| `MPT_PRODUCTS_IDS`              | PRD-1111-1111           | PRD-1234-1234,PRD-4321-4321           | Comma-separated list of SoftwareONE Marketplace Product ID                                 |
| `MPT_API_BASE_URL`              | `http://localhost:8000` | `https://portal.softwareone.com`      | SoftwareONE Marketplace API URL                                                            |
| `MPT_API_TOKEN`                 | -                       | eyJhbGciOiJSUzI1N...                  | SoftwareONE Marketplace API Token                                                          |
| `MPT_INITIALIZER`               | -                       | swo_playground.initializer.initialize | Initializer function                                                                       |
| `MPT_NOTIFY_CATEGORIES`         | -                       | {"ORDERS": "NTC-0000-0006"}           | Notify categories for the orders                                                           |
| `MPT_KEY_VAULT_NAME`            | -                       | swo-playground-kv                     | Key Vault name                                                                             |
| `MPT_PORTAL_BASE_URL`           | `http://localhost:8000` | `https://portal.softwareone.com`      | SoftwareONE Marketplace Portal URL                                                         |


## Other

| Environment Variable                   | Default | Example | Description                                                          |
|----------------------------------------|---------|---------|----------------------------------------------------------------------|
| `MPT_ORDERS_API_POLLING_INTERVAL_SECS` | 120     | 60      | Orders polling interval from the Software Marketplace API in seconds |

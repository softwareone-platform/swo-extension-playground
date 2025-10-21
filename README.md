[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=softwareone-platform_swo-extension-playground&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=softwareone-platform_swo-extension-playground)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=softwareone-platform_swo-extension-playground&metric=coverage)](https://sonarcloud.io/summary/new_code?id=softwareone-platform_swo-extension-playground)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

# SoftwareONE Extension playground

Playground Extension with the SoftwareONE Marketplace

# Run tests

```
$ docker-compose build app_test
$ docker-compose run --service-ports app_test
```

# Local run using SoftwareONE Marketplace API

## Create configuration files

1. Create environment file

```
$ cp .env.sample .env
```

1. Setup parameters for `.env` file

```
MPT_PRODUCTS_IDS=PRD-1111-1111
MPT_PORTAL_BASE_URL=http://devmock:8000
MPT_API_BASE_URL=http://devmock:8000
MPT_API_TOKEN=<vendor-api-token>
MPT_ORDERS_API_POLLING_INTERVAL_SECS=120
EXT_WEBHOOKS_SECRETS={"PRD-1111-1111": "<super-jwt-secret>"}
MPT_INITIALIZER="swo_playground.initializer.initialize"
MPT_KEY_VAULT_NAME=""
MPT_NOTIFY_CATEGORIES={"ORDERS": "NTC-0000-0006"}
```

`MPT_PRODUCTS_IDS` should be a comma-separated list of the SWO Marketplace Product identifiers
For each of the defined product id in the `MPT_PRODUCTS_IDS` list define `WEBHOOKS_SECRETS` json variables using product
ID as key.

```
EXT_WEBHOOKS_SECRETS={"PRD-1111-1111": "<webhook-secret-for-product>"}
```

Example of `.env` file

```
MPT_PRODUCTS_IDS=PRD-1111-1111
MPT_PORTAL_BASE_URL=http://devmock:8000
MPT_API_BASE_URL=http://devmock:8000
MPT_API_TOKEN=<vendor-api-token>
MPT_ORDERS_API_POLLING_INTERVAL_SECS=120
EXT_WEBHOOKS_SECRETS={"PRD-1111-1111": "<super-jwt-secret>"}
MPT_INITIALIZER="swo_playground.initializer.initialize"
MPT_KEY_VAULT_NAME=""
MPT_NOTIFY_CATEGORIES={"ORDERS": "NTC-0000-0006"}
```

```


## Build and run extension

1. Build and run the extension
```

$ docker-compose build app
$ docker-compose run --service-ports app

```

# Configuration

## Application
| Environment Variable            | Default               | Example                                | Description                                                                               |
|---------------------------------|-----------------------|----------------------------------------|-------------------------------------------------------------------------------------------|
| `EXT_WEBHOOKS_SECRETS`          | -                     | {"PRD-1111-1111": "123qweasd3432234"}  | Webhook secret of the Draft validation Webhook in SoftwareONE Marketplace for the product |
| `MPT_PRODUCTS_IDS`              | PRD-1111-1111         | PRD-1234-1234,PRD-4321-4321            | Comma-separated list of SoftwareONE Marketplace Product ID                                |
| `MPT_API_BASE_URL`              | http://localhost:8000 | https://portal.softwareone.com         | SoftwareONE Marketplace API URL                                                           |
| `MPT_API_TOKEN`                 | -                     | eyJhbGciOiJSUzI1N...                   | SoftwareONE Marketplace API Token                                                         |
| `MPT_INITIALIZER`               | -                     | swo_playground.initializer.initialize  | Initializer function                                                                     |
| `MPT_NOTIFY_CATEGORIES`         | -                     | {"ORDERS": "NTC-0000-0006"}            | Notify categories for the orders                                                          |
| `MPT_KEY_VAULT_NAME`            | -                     | swo-playground-kv                      | Key Vault name                                                                           |
| `MPT_PORTAL_BASE_URL`           | http://localhost:8000 | https://portal.softwareone.com         | SoftwareONE Marketplace Portal URL                                                        |


## Other
| Environment Variable                   | Default | Example | Description                                                          |
|----------------------------------------|---------|---------|----------------------------------------------------------------------|
| `MPT_ORDERS_API_POLLING_INTERVAL_SECS` | 120     | 60      | Orders polling interval from the Software Marketplace API in seconds |

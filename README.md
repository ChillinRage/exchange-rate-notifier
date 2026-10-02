# Exchange Rate Notifier

Simple script that uses an FX API to periodically check the current exchange rate between 2 currencies, then sends a broadcast via Telegram Channel (that multiple users can subscribe to).

### Architecture

Currently deployed as an AWS Lambda and configured to execute once every few hours (limit executions to remain under the free tier as well as reducing channel spam).

### For other's use.

Note that you'll need to setup and create your own AWS Lambda and the necessary roles and permissions (for the GitHub workflow to work), as well as your own Telegram Bot and Channel. This repository is mainly for my own use and I do not plan to code this into an easily shareable state (not for now at least).

1. Fork this repository.
2. (MUST) Change the following values in the repository:
    - AWS role to assume in `./github/workflows/deploy.yml`
3. Ensure the following values match your setup (change if need to):
    - AWS Region in `./github/workflows/deploy.yml`
    - Lambda function name in `./github/workflows/deploy.yml`
4. You can change the following values if you want a different currency comparison:
    - `BASE_CURRENCY` in `main.py`
    - `TO_CURRENCY` in `main.py`
    - `EXCEED_RATE_THRESHOLD` in `main.py`
  
The current code uses _ExchangeRate.fun_ public API and has rate limits for its free tier (refer to usage documentation [here](https://exchangerate.fun/docs)), but it works well enough for my use case.

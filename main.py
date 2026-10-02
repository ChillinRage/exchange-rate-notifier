import logging
import json
import urllib.request
import os

from datetime import datetime
from zoneinfo import ZoneInfo


EXCHANGE_RATE_THRESHOLD = 125.00
BASE_CURRENCY = "SGD"
TO_CURRENCY = "JPY"
EXCHANGE_API_URL = f"https://api.exchangerate.fun/latest?base={BASE_CURRENCY}"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{os.environ['TELEGRAM_TOKEN']}/sendMessage"

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    rate_req = urllib.request.Request(
        EXCHANGE_API_URL,
        headers = {
            "User-Agent": "exchange-rate-lambda/1.0",
            "Accept": "application/json"
        },
        method = "GET"
    )

    with urllib.request.urlopen(rate_req) as response:
        data = json.loads(response.read().decode('utf-8'))
        rate = float(data['rates'][TO_CURRENCY])
        timestamp = datetime.fromtimestamp(
            int(data['timestamp']),
            tz=ZoneInfo("Asia/Singapore")
        ).strftime("%d %b, %I %p")

    logger.info("Current rate (per %s): %f %s", BASE_CURRENCY, rate, TO_CURRENCY)

    # send message only if exceed threshold
    if rate >= EXCHANGE_RATE_THRESHOLD:
        payload = {
            "chat_id": os.environ['TELEGRAM_CHAT_ID'],
            "text": f"[{timestamp}] 1 {BASE_CURRENCY} is <b>{rate:.2f}</b> {TO_CURRENCY}!",
            "parse_mode": "HTML"
        }

        req = urllib.request.Request(
            TELEGRAM_API_URL,
            data = json.dumps(payload).encode(),
            headers = {"content-type": "application/json"},
            method = "POST"
        )

        logger.info("Telegram POST request sent.")

        with urllib.request.urlopen(req) as response:
            output = response.read().decode('utf-8')
    else:
        output = f"[{timestamp}] Rate ({rate:.2f}) is below threshold ({EXCHANGE_RATE_THRESHOLD})"

    return {
        'statusCode': 200,
        'body': json.dumps(output)
    }

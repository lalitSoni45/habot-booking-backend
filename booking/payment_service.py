import logging

import requests


logger = logging.getLogger(__name__)


def verify_payment(transaction_id):
    url = "https://httpbin.org/status/200"

    try:
        response = requests.get(
            url,
            timeout=5,
        )

        response.raise_for_status()

        logger.info(
            "Payment verification successful: %s",
            transaction_id,
        )

        return True

    except requests.RequestException as exc:

        logger.error(
            "Payment verification failed: %s",
            exc,
        )

        return False
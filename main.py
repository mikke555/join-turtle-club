import random

import inquirer

from modules.client import Client
from modules.config import actions, logger
from modules.utils import sleep

USE_PROXY = False
SHUFFLE_WALLETS = False
SLEEP_BETWEEN_WALLETS = [20, 60]

REF_POOL = ["YOUR_REF1", "YOUR_REF2"]  # Add your own referrals here


def main():
    with open("keys.txt") as file:
        keys = [row.strip() for row in file]

        if SHUFFLE_WALLETS:
            random.shuffle(keys)

    with open("proxies.txt") as file:
        proxies = [f"http://{row.strip()}" for row in file]

    if USE_PROXY == False:
        logger.warning("Not using proxy \n")

    answer = inquirer.prompt(actions)

    for index, private_key in enumerate(keys, start=1):
        client = Client(
            private_key=private_key,
            wallet_label=f"[{index}/{len(keys)}]",
            proxy=random.choice(proxies) if USE_PROXY else None,
        )

        try:
            if answer["user_action"] == "Parse accounts":
                client.check_ref()
                continue

            client.login()
            used_ref = client.check_ref()

            if used_ref:
                print()
                continue  # Skip if referral is already used

            status = client.use_ref(REF_POOL)

            if status and index < len(keys):
                sleep(*SLEEP_BETWEEN_WALLETS)

        except Exception as error:
            print(f"An error occurred for {client.address}: {error}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("Cancelled by user")

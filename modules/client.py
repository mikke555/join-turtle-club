import random
import string
from datetime import datetime, timezone

import requests
from eth_account import Account
from eth_account.messages import encode_defunct
from fake_useragent import UserAgent

from modules.config import logger
from modules.utils import random_sleep

base_url = "https://points.turtle.club"


class Client:
    def __init__(self, private_key, wallet_label, proxy=None):
        self.private_key = private_key
        self.account = Account.from_key(private_key)
        self.address = self.account.address
        self.label = f"{wallet_label} {self.address} |"
        self.ua = UserAgent()
        self.session = self.create_session(proxy)

    def create_session(self, proxy):
        session = requests.Session()

        if proxy:
            session.proxies.update({"http": proxy, "https": proxy})

        session.headers.update(
            {
                "Accept": "*/*",
                "Content-Type": "application/json",
                "Origin": "https://app.turtle.club",
                "Referer": "https://app.turtle.club/",
                "User-Agent": self.ua.random,
            }
        )

        return session

    def check_ip(self):
        proxy = self.session.proxies

        try:
            resp = self.session.get("https://httpbin.org/ip", proxies=proxy, timeout=10)
            ip = resp.json()["origin"]
            logger.info(f"{self.label} Current IP: {ip}")

        except Exception as error:
            logger.error(f"{self.label} Failed to get IP: {error}")

    def check_ref(self):
        url = f"{base_url}/referral/{self.address}"

        resp = self.session.get(url)

        if resp.status_code != 200:
            logger.warning(f"{self.label} {resp.text}")
            return False

        data = resp.json()

        used_ref, own_ref = data["used_referral"], data["referral"]
        logger.info(f"{self.label} used {used_ref}, own {own_ref}")

        return used_ref

    def get_random_nonce(self, length=17):
        characters = string.ascii_letters + string.digits
        nonce = "".join(random.choice(characters) for _ in range(length))
        return nonce

    def get_timestamp(self):
        # Get the current UTC time with timezone-aware datetime object
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        return timestamp

    def get_message(self, nonce, timestamp):
        message = (
            "app.turtle.club wants you to sign in with your Ethereum account:\n"
            f"{self.address}\n\n"
            "Turtle Membership Agreement, by signing this agreement, you acknowledge and agree to the following terms and conditions governing your membership in Turtle found at: https://turtle.club/terms\n\n"
            "URI: https://app.turtle.club\n"
            "Version: 1\n"
            "Chain ID: 137\n"
            f"Nonce: {nonce}\n"
            f"Issued At: {timestamp}"
        )

        return message

    def sign_message(self, message):
        message_encoded = encode_defunct(text=message)
        signed_message = Account.sign_message(
            message_encoded, private_key=self.private_key
        )
        return "0x" + signed_message.signature.hex()

    def login(self):
        self.check_ip()

        url = f"{base_url}/user/verify_siwe"
        nonce = self.get_random_nonce()
        timestamp = self.get_timestamp()

        message = self.get_message(nonce, timestamp)
        signature = self.sign_message(message)

        payload = {"message": message, "signature": signature}

        resp = self.session.post(url, json=payload)

        if resp.status_code != 200:
            logger.error(f"{self.label} Authorization failed")
            return False

        self.session.headers.update({"Authorization": f"Bearer {resp.text}"})
        logger.debug(f"{self.label} Authorization successfull")

        random_sleep(5, 10)

    def use_ref(self, ref_pool):
        ref = random.choice(ref_pool)
        url = f"{base_url}/referral/{ref}/use"

        resp = self.session.post(url)

        if resp.status_code != 200:
            logger.error(f"{self.label} {resp.text} \n")
            return False

        logger.success(f"{self.label} {resp.text} {ref}")

        return True

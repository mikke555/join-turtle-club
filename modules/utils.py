import random
import time
from datetime import datetime

from tqdm import tqdm


def random_sleep(from_sleep, to_sleep):
    time.sleep(random.randint(from_sleep, to_sleep))


def sleep(from_sleep, to_sleep):
    x = random.randint(from_sleep, to_sleep)
    desc = datetime.now().strftime("%H:%M:%S")

    for _ in tqdm(
        range(x), desc=desc, bar_format="{desc} | Sleeping {n_fmt}/{total_fmt}"
    ):
        time.sleep(1)
    print()

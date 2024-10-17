## Getting started
1. Register at least 1 referral code via https://app.turtle.club/
2. Create venv and install packages
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
3. Specify settings in _main.py_
4. Populate _keys.txt_ with private keys, one key on each line
5. OPTIONAL: Populate _proxies.txt_ with at least 1 proxy server or set `USE_PROXY` to `False`. Format LOGIN:PASS@IP:PORT
4. Run _main.py_
```
py main.py
```
## ⚙️Settings

* `USE_PROXY` - True | False
* `SHUFFLE_WALLETS` - True | False
* `SLEEP_BETWEEN_WALLETS` - 2 values in seconds
* `REF_POOL` - ["YOUR_REF1", "YOUR_REF2"] etc. 

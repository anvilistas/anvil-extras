#
# This repository is an Anvil app. Learn more at https://anvil.works/
# To run the server-side code on your own machine, run:
# pip install anvil-uplink
# python -m anvil.run_app_via_uplink YourAppPackageName

import os

__path__ = [
    os.path.join(os.path.dirname(__file__), "server_code"),
    os.path.join(os.path.dirname(__file__), "client_code"),
]

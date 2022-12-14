from pycardano import *
import os

def build_context(network: Network) -> OgmiosChainContext:
    ws_url = f"ws://{os.environ['OGMIOS_HOST']}:{os.environ['OGMIOS_PORT']}"
    return OgmiosChainContext(ws_url, network)
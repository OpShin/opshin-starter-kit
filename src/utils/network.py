import os

from pycardano import Network

ogmios_host = os.getenv("OGMIOS_API_HOST", "localhost")
ogmios_port = os.getenv("OGMIOS_API_PORT", "1337")
ogmios_protocol = os.getenv("OGMIOS_API_PROTOCOL", "ws")
ogmios_url = f"{ogmios_protocol}://{ogmios_host}:{ogmios_port}"

kupo_host = os.getenv("KUPO_HOST", None)
kupo_port = os.getenv("KUPO_PORT", "80")
kupo_protocol = os.getenv("KUPO_PROTOCOL", "http")
kupo_url = f"{kupo_protocol}://{kupo_host}:{kupo_port}" if kupo_host is not None else None

network = Network.TESTNET

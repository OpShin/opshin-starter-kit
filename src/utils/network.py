import os

from pycardano import Network

ogmios_host = os.getenv("OGMIOS_API_HOST", "localhost")
ogmios_port = os.getenv("OGMIOS_API_PORT", "1337")
ogmios_protocol = os.getenv("OGMIOS_API_PROTOCOL", "ws")
ogmios_url = f"{ogmios_protocol}://{ogmios_host}:{ogmios_port}"

kupo_host = os.getenv("KUPO_API_HOST", None)
kupo_port = os.getenv("KUPO_API_PORT", "80")
kupo_protocol = os.getenv("KUPO_API_PROTOCOL", "http")
kupo_url = f"{kupo_protocol}://{kupo_host}:{kupo_port}" if kupo_host is not None else None

blockfrost_key = os.getenv("BLOCKFROST_API_KEY", None)

network = Network.MAINNET

def get_chain_context():
    from pycardano import (
        BlockFrostChainContext,
        KupoOgmiosV6ChainContext,
        OgmiosV6ChainContext,
    )

    if blockfrost_key:
        return BlockFrostChainContext(
            project_id=blockfrost_key,
            network=network,
        )
    elif kupo_host:
        return KupoOgmiosV6ChainContext(
            host=ogmios_host,
            port=int(ogmios_port),
            path="",
            secure=False,
            network=network,
            kupo_url=kupo_url,
        )
    else:
        return OgmiosV6ChainContext(
            host=ogmios_host,
            port=int(ogmios_port),
            path="",
            network=network,
        )


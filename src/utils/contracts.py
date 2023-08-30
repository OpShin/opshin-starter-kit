from pathlib import Path

from pycardano import PlutusV2Script, plutus_script_hash, Address, Network


def get_contract(name: str, network=Network.TESTNET):
    # Load script info about a contract built with opshin
    script_path = Path(f"./build/{name}/script.cbor")
    with open(script_path) as f:
        cbor_hex = f.read()

    cbor = bytes.fromhex(cbor_hex)

    plutus_script = PlutusV2Script(cbor)
    script_hash = plutus_script_hash(plutus_script)
    script_address = Address(script_hash, network=network)
    return plutus_script, script_hash, script_address

import time

import click
from pycardano import (
    OgmiosChainContext,
    TransactionBuilder,
    UTxO,
    Redeemer,
    VerificationKeyHash,
    DeserializeException, Network,
)

from src.on_chain import vesting
from src.utils import get_signing_info, get_address, ogmios_url, network, kupo_url
from src.utils.contracts import get_contract
from src.utils.network import get_chain_context


@click.command()
@click.argument("name")
def main(name: str):
    # Load chain context
    context = get_chain_context()

    script_cbor, script_hash, script_address = get_contract("vesting")

    # Get payment address
    payment_address = get_address(name)

    # Find a script UTxO
    utxo_to_spend = None
    for utxo in context.utxos(str(script_address)):
        if utxo.output.datum:
            try:
                params = vesting.VestingParams.from_cbor(utxo.output.datum.cbor)
            except DeserializeException:
                continue
            if (
                params.beneficiary == bytes(payment_address.payment_part)
                and params.deadline < time.time() * 1000  # POSIXTime is in ms!
            ):
                utxo_to_spend = utxo
                break
    assert isinstance(utxo_to_spend, UTxO), "No script UTxOs found!"

    # Find a collateral UTxO
    non_nft_utxo = None
    for utxo in context.utxos(str(payment_address)):
        # multi_asset should be empty for collateral utxo
        if not utxo.output.amount.multi_asset and utxo.output.amount.coin > 5000000:
            non_nft_utxo = utxo
            break
    assert isinstance(non_nft_utxo, UTxO), "No collateral UTxOs found!"

    # Make redeemer
    redeemer = Redeemer(0)

    # Build the transaction
    builder = TransactionBuilder(context)
    builder.add_script_input(utxo_to_spend, script=script_cbor, redeemer=redeemer)
    builder.collaterals.append(non_nft_utxo)
    # This tells pycardano to add vkey_hash to the witness set when calculating the transaction cost
    vkey_hash: VerificationKeyHash = payment_address.payment_part
    builder.required_signers = [vkey_hash]
    # we must specify at least the start of the tx valid range in slots
    builder.validity_start = context.last_block_slot
    # This specifies the end of tx valid range in slots
    builder.ttl = builder.validity_start + 1000

    # Sign the transaction
    payment_vkey, payment_skey, payment_address = get_signing_info(name)
    signed_tx = builder.build_and_sign(
        signing_keys=[payment_skey],
        change_address=payment_address,
    )

    # Submit the transaction
    context.submit_tx(signed_tx.to_cbor())

    # context.submit_tx(signed_tx.to_cbor())
    print(f"transaction id: {signed_tx.id}")
    if network == Network.TESTNET:
        print(f"Cexplorer: https://preview.cexplorer.io/tx/{signed_tx.id}")
    else:
        print(f"Cexplorer: https://cexplorer.io/tx/{signed_tx.id}")


if __name__ == "__main__":
    main()

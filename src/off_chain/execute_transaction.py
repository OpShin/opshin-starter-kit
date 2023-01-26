from pycardano import *
from ogmios import build_context

address_from = input('Enter source address: ')
sk_path = input('Enter the name of the file with the signing key: ')
address_to = input('Enter destination address: ')

context = build_context(Network.TESTNET)
tx_builder = TransactionBuilder(context)

tx_builder.add_input_address(address_from)
tx_builder.add_output(TransactionOutput.from_primitive([address_to, 10000000]))

payment_signing_key = PaymentSigningKey.load(sk_path)

signed_tx = tx_builder.build_and_sign([payment_signing_key], change_address=Address.from_primitive(address_from))

context.submit_tx(signed_tx.to_cbor())

print('transaction submitted')
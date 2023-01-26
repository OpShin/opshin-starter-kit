from pycardano import *
from ogmios import build_context

address = input('Enter the address: ')

context = build_context(Network.TESTNET)
utxos = context.utxos(address)

print(utxos)
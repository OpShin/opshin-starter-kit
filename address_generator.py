from pycardano import *

# Specifies the output files for saving the generated keys information
PAYMENT_SIGNING_KEY_PATH = 'payment.skey'
PAYMENT_VERIFICATION_KEY_PATH = 'payment.vkey'

NETWORK = Network.TESTNET

# Generates Keys
payment_signing_key = PaymentSigningKey.generate()
payment_signing_key.save(PAYMENT_SIGNING_KEY_PATH)

payment_verification_key = PaymentVerificationKey.from_signing_key(payment_signing_key)
payment_verification_key.save(PAYMENT_VERIFICATION_KEY_PATH)

# Generates Address
address = Address(payment_part=payment_verification_key.hash(), network=NETWORK)

print(address)

import rgb_lib
import os
import json
import logging

SUPPORTED_NETWORKS = [
    rgb_lib.BitcoinNetwork.REGTEST,
    rgb_lib.BitcoinNetwork.TESTNET
]

def generate_or_load_keys(wallet_path: str, network: rgb_lib.BitcoinNetwork) -> rgb_lib.Keys:
    if network not in SUPPORTED_NETWORKS:
        raise Exception(f'Network {network} not supported.')

    if not os.path.exists(wallet_path):
        return generate_new_keys(wallet_path, network)

    try:
        # Load keys from json file
        with open(wallet_path, 'r') as file:
            data = json.load(file)
            mnemonic = data.get('mnemonic', None)
            if not mnemonic:
                raise Exception('No mnemonic found in file.')
    except Exception as e:
        raise Exception(f'Error loading keys from file: {e}')
    
    return rgb_lib.restore_keys(network, mnemonic)

def generate_new_keys(wallet_path: str, network: rgb_lib.BitcoinNetwork) -> rgb_lib.Keys:
    keys = rgb_lib.generate_keys(network)
    log_keys(keys)
    export_keys(wallet_path, keys)
    return keys

def log_keys(keys: rgb_lib.Keys):
    logging.info(f'===Wallet keys===')
    logging.info(' - mnemonic:', keys.mnemonic)
    logging.info(' - xpub:', keys.xpub)
    logging.info(f'- xpub fingerprint: {keys.xpub_fingerprint}')

def export_keys(wallet_path: str, keys: rgb_lib.Keys):
    if not os.path.exists(os.path.dirname(wallet_path)):
        os.makedirs(os.path.dirname(wallet_path))

    with open(wallet_path, 'w') as file:
        json.dump({
            'mnemonic': keys.mnemonic,
            'xpub': keys.xpub,
            'xpub_fingerprint': keys.xpub_fingerprint
        }, file, indent=4)


if __name__ == "__main__":
    wallet_path = 'wallet.json'
    network = rgb_lib.BitcoinNetwork.REGTEST
    keys = generate_or_load_keys(wallet_path, network)
    log_keys(keys)
    print(keys.xpub_fingerprint)

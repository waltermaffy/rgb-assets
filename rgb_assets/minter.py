import rgb_lib
from rgb_assets.config import WalletConfig    
import argparse
import os
from rgb_assets.wallet_helper import generate_or_load_keys
import logging 
import json 
from rgb_assets.config import get_config

class NftMintingService:
    def __init__(self, cfg: WalletConfig):
        self.cfg = cfg
        self.network = self._set_network(cfg.net)
        self.wallet = self.initialize_wallet()

    def initialize_wallet(self):
        # Load keys or generate new ones
        wallet_path = os.path.join(self.cfg.data_dir, f"{self.cfg.wallet_name}.json")
        keys = generate_or_load_keys(wallet_path, self.network)
        wallet_data = rgb_lib.WalletData(
            self.cfg.data_dir,
            self.network,
            rgb_lib.DatabaseType.SQLITE,
            1,
            keys.xpub,
            keys.mnemonic,
            self.cfg.vanilla_keychain
        )        
        self.wallet = rgb_lib.Wallet(wallet_data)
        self.online = self.wallet.go_online(False, self.cfg.electrum_url)
        logging.info(f'Wallet initialized!')

    def _set_network(self, network: str) -> rgb_lib.BitcoinNetwork:
        supported_networks = {
            'regtest': rgb_lib.BitcoinNetwork.REGTEST,
            'testnet': rgb_lib.BitcoinNetwork.TESTNET
        }
        if network not in supported_networks:
            raise Exception(f'Network {network} not supported.')
        return supported_networks[network]

    def create_new_utxos(self, amount: int):
        self.wallet.create_utxos(self.online, True, amount, None, self.cfg.fee_rate)

    def get_receiving_address(self):
        return self.wallet.get_address()

    def mint_nft(self, definition_file: str) -> str:
    
        if not os.path.exists(definition_file):
            raise FileNotFoundError(f"NFT definition file '{definition_file}' not found.")
        
        # Loading the NFT definition
        nft_definition = json.load(open(definition_file, 'r'))
        logging.info(f'NFT definition loaded: {nft_definition}')
        
        # Create a new UTXO to hold the NFT
        self.create_new_utxos(1)

        # issue the asset
        cfa_asset = self.wallet.issue_asset_cfa(
            self.online, 
            nft_definition.get("name", ""),
            nft_definition.get("description", ""),
            nft_definition.get("precision", 0),
            nft_definition.get("amounts", [1]),
            nft_definition.get("file_path", "")
        )
        logging.info(f'issued asset with ID: {cfa_asset.asset_id}')
        return cfa_asset.asset_id
    
    def send_nft(self, blinded_utxo: str, asset_id: str, amount_sat: int = 1000, amount_cfa: int = 1):
        # Sending the newly minted NFT to the blinded UTXO
        script_data = rgb_lib.ScriptData(blinded_utxo, amount_sat, None)
        recipient_map_cfa = {
            asset_id: [
                rgb_lib.Recipient(None, script_data, amount_cfa, self.cfg.transport_endpoints),
            ]
        }
        txid = self.wallet.send(self.online, recipient_map_cfa, False, self.cfg.fee_rate, 1)
        logging.info(f'Sent a CFA token with txid: {txid} to blinded UTXO: {blinded_utxo}')
        return txid

def main():
    parser = argparse.ArgumentParser(description='NFT Minting Service')
    parser.add_argument('--definition', '-d', type=str, help='Path to the NFT definition file')
    parser.add_argument('--blinded_utxo', '-b', type=str, help='Blinded UTXO where the NFT will be sent')
    parser.add_argument('--data-dir', '-dir', type=str, default='./wallet_data', help='Directory to store wallet data')
    parser.add_argument('--network', '-n', type=str, choices=['regtest', 'testnet'], default='regtest', help='Bitcoin network type')
    args = parser.parse_args()

    cfg = get_config()
    mint_service = NftMintingService(cfg)

    try:
        # mint nft form definition file 
        asset_id = mint_service.mint_nft(args.definition)
        print(f'NFT minted with asset ID: {asset_id}')
        # send nft to blinded utxo
        tx_id = mint_service.send_nft(args.blinded_utxo, asset_id)
        print(f'NFT sent with txid: {tx_id}')

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()

import os
import shutil
import magic
import matplotlib.pyplot as plot
import qrcode
from IPython.display import Image, display
import rgb_lib
import logging
from typing import List
logging.basicConfig(level=logging.DEBUG)
from schemas import RGB20Asset, RGB21Asset

@dataclass
class Network:
    electrum_url: str = 'tcp://electrs:50001'
    proxy_url: str = 'https://proxy.rgbtools.org'
    bitcoin_network: str = rgb_lib.BitcoinNetwork.REGTEST
    

class RGBWallet:
    
    def __init__(self, name: str, data_dir: str = '/data/recv_wallet'):
        
        self.name = name 
        self.network = Network()
        self.data_dir = data_dir
        
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        # Load keys or generate new ones        
        if os.path.exists(os.path.join(self.data_dir, 'keys')):
            self.load_keys()
        else:
            self.generate_keys()

        self.init_wallet()

    def generate_keys(self):
        self.keys = rgb_lib.generate_keys(self.network.bitcoin_network)
        self.mnemonic = self.keys.mnemonic
        self.xpub = self.keys.xpub
        print(f'{self.name} wallet keys:')
        print(' - mnemonic:', self.mnemonic)
        print(' - xpub:', self.xpub)
        print(f'- xpub fingerprint: {self.keys.xpub_fingerprint}')
        self.export_keys()

    def export_keys(self):
        key_dir = os.path.join(self.data_dir, 'keys')
        if not os.path.exists(key_dir):
            os.makedirs(key_dir)

        if self.mnemonic:
            #TODO: encrypt mnemonic
            with open(os.path.join(key_dir, 'keys.txt'), 'w') as f:
                # add mnemonic and xpub to file
                f.write(self.mnemonic)
                f.write('\n')
                f.write(self.xpub)
        else:
            raise Exception('No mnemonic found.')

    def load_keys(self):
        # Load keys from file
        key_dir = os.path.join(self.data_dir, 'keys')
        if not os.path.exists(key_dir):
            raise Exception('No keys found.')
        with open(os.path.join(key_dir, 'keys.txt'), 'r') as f:
            self.mnemonic = f.readline().strip()
            self.xpub = f.readline().strip()
            print(f'{self.name} wallet keys:')
            print(' - mnemonic:', self.mnemonic)
            print(' - xpub:', self.xpub)
        
    def init_wallet(self):
        
        if not self.mnemonic or not self.xpub:
            raise Exception('You need to generate keys first.') 

        wallet_data = rgb_lib.WalletData(
                self.data_dir,
                self.network.bitcoin_network,
                rgb_lib.DatabaseType.SQLITE,
                self.xpub,
                self.mnemonic
        )
        self.wallet = rgb_lib.Wallet(wallet_data)
        self.online_wallet = self.wallet.go_online(False, self.network.electrum_url, self.network.proxy_url)
        print(f'wallet initialized!')

    def get_address(self):
        return self.wallet.get_address()

    def get_address_qr(self):
        return qrcode.make(self.get_address())

    def get_blinded_utxo(self):
        # create UTXOs to hold RGB allocations
        self.wallet.create_utxos(self.online_wallet, True, 5)
        # check wallet unspents
        self.wallet.refresh(self.online_wallet, None)
        recv_unspents = self.wallet.list_unspents(settled_only=False)
        for unspent in recv_unspents:
            print(unspent.utxo)
            for allocation in unspent.rgb_allocations:
                print(f'\t- {allocation}')
                
        blind_data = self.wallet.blind(None, None)
        blinded_utxo = blind_data.blinded_utxo
        return blinded_utxo

    def issue_rgb21(self, name: str, description: str, precision: int, amounts: int, file_path: str = ""):
        issued_asset = self.wallet.issue_asset_rgb21(
            self.online_wallet,
            name,
            description,
            precision,
            amounts,
            None,
            file_path
        )
        print(f'issued asset with ID: {issued_asset.asset_id}')
        return issued_asset

    def issue_rgb20(self, name: str, ticker: str, precision: int, amounts: int):
        # issue RGB20 asset
        rgb20_asset = self.wallet.issue_asset_rgb20(
            self.online_wallet,
            ticker,
            name,
            precision,
            [amounts]
        )
        print(f'issued asset with ID: {rgb20_asset.asset_id}')
        return rgb20_asset

    def get_asset(self, asset_id: str):
        asset = self.wallet.list_assets(filter_asset_types=[])
        
        if asset_id not in asset:
            print(f'Asset {asset_id} not found.')
            return None

        return asset[asset_id]

    def send_rgb21(self, blinded_utxo, asset_token, amount: int):

        recipient_map_rgb21 = {
            asset_token.asset_id: [
                rgb_lib.Recipient(blinded_utxo, amount),
            ]
        }
        txid = self.wallet.send(self.online_wallet, recipient_map_rgb21, False)
        print(f'RGB21 txid: {txid}')
        return txid

    def send_rgb20(self, blinded_utxo, asset_token, amount: int):
        recipient_map_rgb20 = {
            asset_token.asset_id: [
                rgb_lib.Recipient(blinded_utxo, amount),
            ]
        }
        txid = self.wallet.send(self.online_wallet, recipient_map_rgb20, False)
        print(f'RGB20 txid: {txid}')
        return txid        

    def get_asset_transfers(self, asset_token):
        transfers = self.wallet.list_transfers(asset_token.asset_id)
        for transfer in transfers:
            print(f'- {transfer}')

    def refresh(self):
        self.wallet.refresh(self.online_wallet, None)

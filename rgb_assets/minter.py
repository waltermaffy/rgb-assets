import argparse
import json
import os
import rgb_lib
from typing import Union
from rgb_assets.models import NftDefinition, NftMint
from rgb_assets.config import WalletConfig, get_config, SUPPORTED_NETWORKS
from rgb_assets.wallet_helper import generate_or_load_wallet, setup_logger

logger = setup_logger("./data/minter.log")


class NftMintingService:
    def __init__(self, cfg: WalletConfig):
        self.cfg = cfg
        self.wallet, self.online = generate_or_load_wallet(cfg)

    def create_new_utxos(self, amount: int):
        self.wallet.create_utxos(self.online, True, amount, None, self.cfg.fee_rate)
        logger.info(f"Create {amount} new utxos")

    def get_new_blinded_utxo(self):
        try:
            self.create_new_utxos(1)
            data = self.wallet.blind_receive(None, None, None, self.cfg.transport_endpoints, 1)        
            logger.info(f"New blinded utxo: {data}")
            return data.recipient_id
        except Exception as e:
            logger.error(e)
            raise Exception(e)

    def get_receiving_address(self):
        return self.wallet.get_address()

    def get_assets(self):
        assets = self.wallet.list_assets(filter_asset_schemas=[])
        return assets.cfa

    def mint_nft_from_file(self, file_path: str) -> str:
        nft_definition = self.load_nft_definition_from_file(file_path)
        return self.mint_nft(nft_definition)

    def list_unspent(self):
        return self.wallet.list_unspents(self.online, settled_only=False)

    def load_nft_definition_from_file(file_path: str) -> Union[NftDefinition, None]:
        try:
            with open(file_path, 'r') as file:
                json_data = json.load(file)
                return NftDefinition.parse_obj(json_data)
        except FileNotFoundError:
            logger.error(f"File '{file_path}' not found.")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            return None
            
    def mint_nft(self, nft_definition: NftDefinition) -> str:
        try:
            logger.info(f"Got NFT definition: {nft_definition}")
            # Create a new UTXO to hold the NFT
            self.create_new_utxos(1)
            logger.info("New utxo created")
            # issue the asset
            cfa_asset = self.wallet.issue_asset_cfa(
                self.online,
                nft_definition.name,
                nft_definition.description,
                nft_definition.precision,
                nft_definition.amounts,
                nft_definition.file_path,
            )
            logger.info(f"issued asset with ID: {cfa_asset.asset_id}")
            return cfa_asset.asset_id
        except Exception as e:
                logger.error(e)
                raise Exception(e)
    
    def refresh(self):
        self.wallet.refresh(self.online, None, [])

    def send_nft(
        self,
        blinded_utxo: str,
        asset_id: str,
        amount_sat: int = 1000,
        amount_cfa: int = 1,
    ):

        # Sending the newly minted NFT to the blinded UTXO
        script_data = rgb_lib.ScriptData(blinded_utxo, amount_sat, None)
        logger.debug(f"ScriptData: {script_data}")
        recipient_map_cfa = {
            asset_id: [
                rgb_lib.Recipient(
                    blinded_utxo, None, amount_cfa, self.cfg.transport_endpoints
                ),
            ]
        }
        logger.debug(f"{recipient_map_cfa}")
        txid = self.wallet.send(
            self.online, recipient_map_cfa, False, self.cfg.fee_rate, 1
        )
        logger.info(
            f"Sent a CFA token with txid: {txid} to blinded UTXO: {blinded_utxo}"
        )
        return txid

def main():
    parser = argparse.ArgumentParser(description="NFT Minting Service")
    parser.add_argument(
        "--definition", "-d", type=str, help="Path to the NFT definition file"
    )
    parser.add_argument(
        "--blinded_utxo", "-b", type=str, help="Blinded UTXO where the NFT will be sent"
    )
    parser.add_argument(
        "--data-dir",
        "-dir",
        type=str,
        default="./data",
        help="Directory to store wallet data",
    )
    parser.add_argument(
        "--network",
        "-n",
        type=str,
        choices=["regtest", "testnet"],
        default="regtest",
        help="Bitcoin network type",
    )
    args = parser.parse_args()
    print(args)
    cfg = get_config()
    
    cfg.data_dir = args.data_dir
    cfg.definition = args.definition
    print(cfg)

    mint_service = NftMintingService(cfg)

    try:
        # mint nft form definition file
        asset_id = mint_service.mint_nft(args.definition)
        print(f"NFT minted with asset ID: {asset_id}")
        # send nft to blinded utxo
        tx_id = mint_service.send_nft(args.blinded_utxo, asset_id)
        print(f"NFT sent with txid: {tx_id}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

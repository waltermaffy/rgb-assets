# import argparse
import json
import os
from typing import Union

import rgb_lib

from rgb_assets.config import SUPPORTED_NETWORKS, WalletConfig, get_config
from rgb_assets.models import DataConverter, NftDefinition, NftMint
from rgb_assets.wallet_helper import generate_or_load_wallet, logger
from rgb_assets.wallet_service import WalletService


class NftMintingService(WalletService):
    def __init__(self, cfg: WalletConfig):
        #logger.info("Running minter with cfg: ", cfg)
        super().__init__(cfg)

    def mint_nft_from_file(self, file_path: str) -> str:
        nft_definition = self.load_nft_definition_from_file(file_path)
        return self.mint_nft(nft_definition)

    def load_nft_definition_from_file(file_path: str) -> Union[NftDefinition, None]:
        try:
            with open(file_path, "r") as file:
                json_data = json.load(file)
                return NftDefinition.parse_obj(json_data)
        except FileNotFoundError:
            logger.error(f"File '{file_path}' not found.")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            return None


    def issue_asset_cfa(self, nft_definition: NftDefinition) -> str:
        try:
            logger.info(f"Got NFT definition")
            encoded_data = nft_definition.encoded_data
            if encoded_data:
                file_path = DataConverter.decode_data(
                    encoded_data, nft_definition.file_type, self.cfg.data_dir
                )
                if file_path:
                    nft_definition.file_path = file_path

            # Create a new UTXO to hold the NFT
            self.create_new_utxos(1)
            logger.info("Created a new utxo for the NFT created")
            # issue the asset
            cfa_asset = self.wallet.issue_asset_cfa(
                self.online,
                nft_definition.name,
                nft_definition.description,
                nft_definition.precision,
                nft_definition.amounts,
                nft_definition.file_path,
            )
            logger.info(f"Issued asset with ID: {cfa_asset.asset_id}")
            return cfa_asset.asset_id
        except Exception as e:
            logger.error(e)
            raise Exception(e)

    def mint_nft(
        self, 
        blinded_utxo: str,
        nft_definition: NftDefinition, 
    ) -> str:
        # Issue an RGB asset and send it to the blinded UTXO provided
        asset_id = self.issue_asset_cfa(nft_definition)
        tx_id = self.send_nft(blinded_utxo, asset_id)
        return tx_id


    def send_nft(
        self,
        blinded_utxo: str,
        asset_id: str,
        amount_sat: int = 1000,
        amount_cfa: int = 1,
    ):
        # Sending the newly minted NFT to the blinded UTXO
        recipient_map_cfa = {
            asset_id: [
                rgb_lib.Recipient(
                    blinded_utxo, None, amount_cfa, self.cfg.transport_endpoints
                ),
            ]
        }
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

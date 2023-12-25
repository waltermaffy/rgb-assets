# import argparse
import json
import os
from typing import Union

import rgb_lib
import argparse
from rgb_assets.config import SUPPORTED_NETWORKS, WalletConfig, get_config
from rgb_assets.models import DataConverter, NftDefinition, NftMint
from rgb_assets.wallet_helper import generate_or_load_wallet, logger
from rgb_assets.wallet_service import WalletService


class NftMintingService(WalletService):
    def __init__(self, cfg: WalletConfig):
        #logger.info("Running minter with cfg: ", cfg)
        super().__init__(cfg)
        self.mints = {}

    def issue_nft_from_file(self, file_path: str) -> str:
        nft_definition = NftDefinition.from_file(file_path)
        if not nft_definition:
            raise Exception(f"Error loading NFT definition from file: {file_path}")
        return self.issue_asset_cfa(nft_definition)

    def issue_nft_from_folder(self, folder_path: str) -> str:
        nft_definitions = NftDefinition.from_folder(folder_path)
        if not nft_definitions:
            raise Exception(f"Error loading NFT definitions from folder: {folder_path}")
        asset_ids = []
        logger.info(f"Issuing #{len(nft_definitions)} NFTs from folder: {folder_path}")
        for nft_definition in nft_definitions:
            asset_id = self.issue_asset_cfa(nft_definition)
            asset_ids.append(asset_id)
        return asset_ids
        
    def issue_asset_cfa(self, nft_definition: NftDefinition) -> str:
        try:
            logger.info(f"Issuing NFT definition: {nft_definition}")
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

    def mint_nft_from_file(
        self, blinded_utxo: str, file_path: str
    ) -> str:
        nft_definition = NftDefinition.from_file(file_path)
        if not nft_definition:
            raise Exception(f"Error loading NFT definition from file: {file_path}")
        return self.mint_nft(blinded_utxo, nft_definition)


    def mint_nft(
        self, 
        blinded_utxo: str,
        nft_definition: NftDefinition, 
    ) -> str:
        # Issue an RGB asset and send it to the blinded UTXO provided, return txid
        if not (rgb_lib.BlindedUtxo(blinded_utxo)):
            return {
                "message": f"Invalid blinded UTXO: {blinded_utxo}", 
                "error": "InvalidBlindedUtxo"  
            }

        asset_id = self.issue_asset_cfa(nft_definition)
        if not asset_id:
            raise Exception(f"Error issuing asset CFA: {nft_definition.name}")
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
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Sub-parser for minting an NFT from a file
    parser_mint = subparsers.add_parser('mint', help='Mint an NFT from a definition file or a folder')
    parser_mint.add_argument('-d', '--definition', type=str, help='Path to the NFT definition file or folder')
    parser_mint.add_argument('-b', '--blinded_utxo', type=str, help='Blinded UTXO where the NFT will be sent')

    # Sub-parser for sending an NFT to a blinded UTXO
    parser_send = subparsers.add_parser('send', help='Send an NFT to a blinded UTXO')
    parser_send.add_argument('-a', '--asset_id', type=str, help='Asset id to send to the blinded UTXO')
    parser_send.add_argument('-b', '--blinded_utxo', type=str, help='Blinded UTXO where the NFT will be sent')

    parser.add_argument('--data-dir', '-dir', type=str, default='./data', help='Directory of the wallet data')
    parser.add_argument('--network', '-n', type=str, choices=['regtest', 'testnet'], default='regtest',
                        help='Bitcoin network type')
    parser.add_argument(
        "--init",
        action="store_true",
        default=False,
        help="Initialize a new wallet",
    )

    args = parser.parse_args()

    cfg = get_config()
    cfg.data_dir = args.data_dir
    cfg.network = args.network
    cfg.init = args.init
    cfg.electrum_url="tcp://localhost:50001"
    cfg.transport_endpoints=["rpc://localhost:3000/json-rpc"] 
    cfg.data_dir = args.data_dir
    print(cfg)

    mint_service = NftMintingService(cfg)

    try:
        if args.command == 'mint':
            # check if definition is a folder
            if os.path.isdir(args.definition):
                asset_ids = mint_service.issue_nft_from_folder(args.definition)
                print(f"NFTs minted from folder: {args.definition}")
                print(f"New asset IDs: {asset_ids}")

            else:
                if args.blinded_utxo:
                    print(f"Minting NFT from file: {args.definition} to blinded UTXO: {args.blinded_utxo}")
                    txid = mint_service.mint_nft_from_file(args.blinded_utxo, args.definition)
                    print(f"NFT minted with txid: {txid}")
                else:
                    asset_id = mint_service.issue_nft_from_file(args.definition)
                    print(f"NFT minted with asset ID: {asset_id}")
                

        elif args.command == 'send':
            tx_id = mint_service.send_nft(args.blinded_utxo, args.asset_id)
            print(f"NFT sent with txid: {tx_id}")
        else:
            parser.print_help()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

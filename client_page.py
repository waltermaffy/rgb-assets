import streamlit as st
import base64
from rgb_assets.client import NftClient
from rgb_assets.config import WalletConfig
from rgb_assets.models import MintRequest
from PIL import Image
from io import BytesIO

MINTER_URL = "http://localhost:8000"


def get_asset_dict(assets):
    """Return a dict of the available assets."""
    asset_dict = {}
    for asset in assets:
        asset_dict[asset.asset_id] = {
            'balance': {
                'settled': asset.balance.settled,
                'future': asset.balance.future,
                'spendable': asset.balance.spendable,
            },
            'name': asset.name,
            'precision': asset.precision,
        }
        if hasattr(asset, 'ticker'):
            asset_dict[asset.asset_id]['ticker'] = asset.ticker
        if hasattr(asset, 'description'):
            asset_dict[asset.asset_id]['description'] = asset.description
        if hasattr(asset, 'data_paths'):
            for data_path in asset.data_paths:
                path_list = asset_dict[asset.asset_id].setdefault(
                    'data_paths', [])
                attachment_id = data_path.file_path.split('/')[-2]
                path_list.append({
                    'mime-type': data_path.mime,
                    'attachment_id': attachment_id,
                })
    return asset_dict

def main():
    st.title("NFT Client")

    if "nft_client" not in st.session_state:
        cfg = WalletConfig()
        cfg.wallet_name = "nft_client"
        with st.spinner(text='Loading RGB wallet...'):
            st.session_state.nft_client = NftClient(cfg, MINTER_URL)

    st.header("Receiving Address")
    if st.button("Get Receiving Address"):
        receiving_address = st.session_state.nft_client.get_address()
        st.text(f"Receiving Address: {receiving_address}")

    st.header("New Blinded UTXO")
    if st.button("Generate New Blinded UTXO"):
        new_blinded_utxo = st.session_state.nft_client.get_new_blinded_utxo()
        st.text(f"New Blinded UTXO: {new_blinded_utxo}")

    st.header("Wallet Assets")
    if st.button("List Wallet Assets"):
        assets = st.session_state.nft_client.get_cfa_assets()
        st.write(f"Wallet Assets:")
        st.write(get_asset_dict(assets))


    st.header("Create NFT")
    uploaded_file = st.file_uploader("Upload JPEG Image", type="jpg")
    nft_name = st.text_input("NFT Name")
    blinded_utxo = st.text_input("Blinded UTXO")
    amount = st.number_input("Select how many NFT to mint", 1, 100000)
    nft_description = st.text_area("NFT Description")
    encoded_img = None 
    if uploaded_file is not None and nft_name != "":
        image = Image.open(uploaded_file)
        img_buffer = BytesIO()
        image.save(img_buffer, format="JPEG")
        encoded_img = base64.b64encode(img_buffer.getvalue()).decode("utf-8")

    nft_definition = {
        "name": nft_name,
        "precision": 0,
        "amounts": [amount],
        "description": nft_description,
        "encoded_data": encoded_img,
        "file_type": "JPEG"
    }
    st.write(nft_definition)
    if not blinded_utxo:
        st.warning("Please create a blinded UTXO first")

    if st.button("Mint NFT"):
        with st.spinner(text='Asking for NFT minting..'):
            mint_request = MintRequest(
                nft_definition=nft_definition,
                blinded_utxo=blinded_utxo
            )
            txid = st.session_state.nft_client.ask_mint(mint_request)
            st.success(f"NFT minted and sent. TxId: {txid}")

if __name__ == "__main__":
    main()

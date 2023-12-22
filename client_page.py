import streamlit as st

from rgb_assets.client import NftClient
from rgb_assets.config import WalletConfig
from rgb_assets.wallet_helper import generate_or_load_wallet, setup_logger


def main():
    st.title("NFT Client")

    if "nft_client" not in st.session_state:
        cfg = (
            WalletConfig()
        )  # Initialize the WalletConfig with default values or set through environment variables
        cfg.wallet_name = "nft_client"
        st.session_state.nft_client = NftClient(cfg)

    st.header("Receiving Address")
    if st.button("Get Receiving Address"):
        receiving_address = st.session_state.nft_client.get_address()
        st.write(f"Receiving Address: {receiving_address}")

    st.header("New Blinded UTXO")
    if st.button("Generate New Blinded UTXO"):
        new_blinded_utxo = st.session_state.nft_client.get_new_blinded_utxo()
        st.write(f"New Blinded UTXO: {new_blinded_utxo}")

    st.header("Wallet Assets")
    if st.button("List Wallet Assets"):
        assets = st.session_state.nft_client.get_assets()
        st.write(f"Wallet Assets: {assets}")


if __name__ == "__main__":
    main()

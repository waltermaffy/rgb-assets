import streamlit as st 
from rgbassets.wallet import RGBWallet 


def main():
    st.title("RGB Assets")
    st.subheader("RGB Assets is a framework to issue RGB-21 assets to blinded-testnet utxos.")
    
    st.subheader("Wallet")
    st.write("The wallet is a simple interface to interact with the RGB assets.")

    wallet_name = st.text_input("Wallet Name")
    generate_button = st.button("Generate Wallet")
    if generate_button:
        wallet = RGBWallet(name=wallet_name, data_dir="data")
        st.success("Wallet loaded!")

    st.subheader("Issue Asset")
    st.write("Issue an asset to a blinded-testnet utxo.")
    utxo_select = st.selectbox("Select UTXO", ["Input", "Generate"])
    if utxo_select == "Generate":
        st.write("Generating a blinded-testnet utxo.")
        blinded_utxo = wallet.get_blinded_utxo()
    elif utxo_select == "Input":
        st.write("Input a blinded-testnet utxo.")
        blinded_utxo = st.text_input("Blinded UTXO")
    
    asset_select = st.selectbox("Select Asset", ["RGB20", "RGB21"])
    if asset_select == "RGB20":
        asset_name = st.text_input("Asset Name", max_chars=32, value="BelToken")
        asset_ticker = st.text_input("Asset Ticker", max_chars=5, value="WLF")
        max_supply = st.number_input("Max Supply", min_value=1, value=1000000)
        precision = st.number_input("Precision", min_value=0, value=0)
        token = wallet.issue_rgb20(asset_name, asset_ticker, int(precision), int(max_supply))

        st.write("Issued asset: ", token)

    
    elif asset_select == "RGB21":
        # TODO: Add image from file or generate with diffusion model
        asset_name = st.text_input("Asset Name", max_chars=32, value="BelToken")
        description = st.text_input("Description", max_chars=128, value="BelToken is a token bello.")
        precision = st.number_input("Precision", min_value=0, value=0)
        max_supply = st.number_input("Max Supply", min_value=1, value=1000000)
        token = wallet.issue_rgb21(asset_name, description, int(precision), int(max_supply))
    
        st.write("Issued asset: ", token)

        
if __name__ == "__main__":
    main()
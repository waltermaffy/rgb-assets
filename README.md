# RGB Assets

RGB Assets is a framework designed for testing the minting and transfers of [RGB](rgb.info) assets over the Bitcoin network. Leveraging [rgb-lib-python](https://github.com/RGB-Tools/rgb-lib-python/tree/master), this library offers the following functionalities:

- A FastAPI application with an API for minting and sending CFA assets (NFTs).
- A Streamlit web interface serving as a client RGB wallet.
- Command-line interface (CLI) for minting NFTs from files.

⚠️ **WARNING: This code is not intended for use in the mainnet and should not be considered secure. Exercise caution while using it.**

## Requirements

Running this demo requires Poetry, Docker, and docker-compose.

## Testing Setup

Initiate the regtest blockchain services along with the FastAPI app using the provided script:
```shell
./services.sh start
```

The app should be accessible on port 8000. Explore and test the endpoints here: [http://localhost:8000/docs](http://localhost:8000/docs)

Execute tests using pytest:
```shell
poetry run pytest
```

Launch the Streamlit page for the client:
```shell
./services.sh streamlit
```

The Streamlit frontend should be available on port 8501. Open your browser at [http://localhost:8501](http://localhost:8501). Users can load an image, triggering a mint request sent to the minter API.

The MintRequest comprises a NFT Definition and a blinded UTXO. To obtain a blinded UTXO from the wallet, ensure sufficient funds are available.

To fund a Bitcoin address and mine some Bitcoin in the regtest environment, use these scripts:
```shell
./services.sh fund <bitcoin_address>
```
```shell
./services.sh mine <number_of_blocks>
```

For loading a new wallet, allocate funds to the minter using this command:
```shell
./services.sh fund_minter
```

Upon completion of testing, stop all services (this will delete all produced data) using:
```shell
./services.sh stop
```

## CLI

Once the containers are running in the background, you can issue new RGB CFA assets and send them to a blinded UTXO. If a blinded UTXO is not provided, assets are issued to the minter wallet.

Additionally, you can send assets from the minter wallet to a new blinded UTXO using "send".

- **MINT** a new RGB asset based on a JSON file:
```shell
poetry run python -m rgb_assets.minter mint -d rgb_assets/tests/data/nft_definition.json 
```

- **MINT** new RGB assets from a folder:
```shell
poetry run python -m rgb_assets.minter mint -d rgb_assets/tests/data/
```

- **MINT** RGB assets from a file and send them to a blinded UTXO:
```shell
poetry run python -m rgb_assets.minter mint -d rgb_assets/tests/data/nft_definition.json -b utxob:MGhM2x9-AccWrjNjm-XVCpaGhF7-gdk51ZpmY-ANtqMLBKJ-hKaiKU
```

- **SEND** RGB assets to a blinded UTXO:
```shell
poetry run python -m rgb_assets.minter send -a rgb:21e9Mer-tBuZY42LF-Z6RtgW7aJ-JnTPuJTt4-csvejq4a3-LUoJsYj -b utxob:DASV5L2-vV8j6EGSn-B7WutZ86W-LBm5PcDWo-wov61mJcs-ewon83
```

### API Endpoints

- **GET /cfa_assets:** Retrieve minted assets of the minter wallet.
- **GET /new_address:** Obtain a new address to fund the minter wallet.
- **GET /new_blinded_utxo:** Get a new blinded UTXO (wallet must be funded).
- **GET /list_unspent:** Fetch a list of UTXOs.
- **POST /issue_cfa:** Issue a new NFT based on a NftDefinition.
- **POST /mint_nft:** Issue a new NFT based on a NftDefinition and send it to a blinded UTXO.
- **POST /send_nft:** Send an already minted NFT to a blinded UTXO.

## NFT Definition

When creating a new mint, provide a NFT Definition in a JSON file with the following format:
```json
{
    "name": "RGB-01",
    "precision": 0,
    "amounts": [1],
    "description": "A new incredible collectible",
    "parent_id": null,
    "file_path": null
}
```

## Configuration

To provide your configuration to the minter, create a default `.env` file:
```shell
mv .env.example .env
```

Modify it as per your requirements.

### Wallet Settings

If not provided, a new wallet will be created. To load an existing wallet, provide in `.env`:

- **WALLET_NAME.backup** file inside DATA_DIR.
- **WALLET_NAME_keys.json** file inside DATA_DIR, structured as:
```json
{
    "mnemonic": "keys.mnemonic",
    "xpub": "keys.xpub",
    "xpub_fingerprint": "keys.xpub_fingerprint"
}
```
- Password of the wallet backup in BACKUP_PASS.


## TODO List

- [ ] Add a database (SQLite/Mongo).
- [ ] L402 for paid mint requests.
- [ ] Refined error handling.
- [ ] Request validation.
- [ ] Add a response model for consistent output.
- [ ] Improved testing.

---

This revised README aims to provide clearer instructions and improve readability for users or developers accessing and using the RGB Assets framework. Adjustments were made for better organization and clarity in each section.

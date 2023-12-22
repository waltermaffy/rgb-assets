# RGB Assets 

A framework for testing issues and transfers of [RGB](rgb.info) assets over Bitcoin.

Using [rgb-lib-python](https://github.com/RGB-Tools/rgb-lib-python/tree/master) this library provides a FastAPI app for a NFT Minter and a streamlit web interface for a client.
Both minter and client use a WalletService for RGB wallet functionalities. 


WARNING: This code is to be considered as NOT secure. It is NOT recommended to use it in mainnet 

## Requirements
Poetry, Docker and docker-compose are required to run this demo.


## Configuration
In order to provide your conf you can create a default .env file

mv .env.example .env

Modify it with your needs.


## Testing setup
Build the app docker image with:
```shell
./services.sh build
```

Start regtest blockchain services along with app with:
```shell
./services.sh start
```

The app should listen on port 8000 for requests. You can see and test enpoints here [http://localhost:8000/docs](http://localhost:8000/docs) 

Run tests for wallet and minter
```shell
poetry run pytest
```

Start streamlit page for client
```shell
./services.sh streamlit
```

The streamlit frontend should listen on port 8501 . Open your browser at [http://localhost:8501](http://localhost:8501)


### ENPOINTS
- GET /cfa_assets --> get minted assets of minter wallet
- GET /new_address --> get a new address to fund minter wallet 
- GET /new_blinded_utxo --> get a new blinded UTXO (wallet must be funded)
- GET /list_unspent --> get a list of UTXOs
- POST  /mint_nft --> Mint a new NFT based on a NftDefinition
- POST  /send_nft --> Send an alredy minted NFT to a blinded UTXO

### Wallet Settings
If the following are not provided, a new wallet will be created. 

If you want to load an existing wallet provide in .env :
- WALLET_NAME.backup file inside DATA_DIR
- WALLET_NAME_keys.json file inside DATA_DIR, with this structure:
{
    "mnemonic": keys.mnemonic,
    "xpub": keys.xpub,
    "xpub_fingerprint": keys.xpub_fingerprint,
}
- password of the wallet backup in BACKUP_PASS

In the future the keys file may be encryped with BACKUP_PASS

# HOW TO USE IT

mint: 

rgbassets mint -u <blinded_utxo> -token tokens/nft.yml

0. Create a wallet giving a name. A file will be created in the folder wallets with the name of the wallet.

1. Configure the nft data in the token configuration file. 


# Mint a new token

rgbassets mint -u blinded_utxo 


## Testing setup
Build the jupyter docker image with:
```shell
./services.sh build
```

Start regtest blockchain services along with jupyter with:
```shell
./services.sh start
```

Get the link from the console output (`http://localhost:8888/...`) and open it
in a web browser.

Once services are running, a regtest bitcoin address can be funded from the
console with:
```shell
./services.sh fund <bitcoin_address>
```
and a regtest block can be mined with:
```shell
./services.sh mine <number_of_blocks>
```

Executing each code cell in the notebook from top to bottom reproduces an
example of wallet creation, asset issuance and asset transfer, with alternating
sender and receiver roles.

Once done with the example, close the jupyter browser page and stop all
services (this will also delete all data produced by services and the demo)
with:
```shell
./services.sh stop
```

The jupyter docker image that has been built will not be removed automatically,
it can be deleted with:
```shell
docker image rm rgb-lib-python-demo
```

## Possible future improvements
- [ ] Add a database (SQLite/Mongo)
- [ ] Refined error hanlding
- [ ] Request Validation
- [ ] Add response model for consistent output


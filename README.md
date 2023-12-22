# RGB Assets 

A framework for issuing and transferring [RGB](rgb.info) assets.

Use rgb-lib-python to create and manage RGB assets.

The library provide a NFT Minter that by creating or loading a RGB wallet can allow mint of new NFT/RGB121/CFA rgb assets 


Features:
- FastAPI app
- CLI interface for minter, client 

## Requirements
Docker and docker compose are required to run this demo.


## Configuration
In order to provide your conf you can create a default .env file

mv .env.example .env

Modify it with your needs.

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
- password of the wallet backup in PASSWORD_BACKUP

In the future the keys file may be encryped with PASSWORD_BACKUP

# HOW TO USE IT

mint: 

rgbassets mint -u <blinded_utxo> -token tokens/nft.yml

0. Create a wallet giving a name. A file will be created in the folder wallets with the name of the wallet.

1. Configure the nft data in the token configuration file. 


# Mint a new token

rgbassets mint -u blinded_utxo 



## Jupyter demo
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

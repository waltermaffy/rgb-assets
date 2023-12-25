# RGB Assets 

A framework for testing issues and transfers of [RGB](rgb.info) assets over Bitcoin.

Using [rgb-lib-python](https://github.com/RGB-Tools/rgb-lib-python/tree/master) this library provides a FastAPI app for a NFT Minter and a streamlit web interface for a client.
Both minter and client use a WalletService for RGB wallet functionalities. 


WARNING: This code is to be considered as NOT secure. It is NOT recommended to use it in mainnet 

## Requirements
Poetry, Docker and docker-compose are required to run this demo.

## Testing setup

Start regtest blockchain services along with FastAPI app with:
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


Once services are running, a regtest bitcoin address can be funded from the
console with:
```shell
./services.sh fund <bitcoin_address>
```
and a regtest block can be mined with:
```shell
./services.sh mine <number_of_blocks>
```

Once done with testing, stop all services (this will also delete all data produced by services)
with:
```shell
./services.sh stop
```


## CLI 
After the containers rum in the background you can start issuing new RGB CFA assets and send them to a blinded_utxo. If a blinded_uxto is not provided their are issued to the minter wallet. 
It is also possible to sends assets from the minter wallet to a new blinded_utxo

- MINT a new RGB asset based on a json file
```shell
poetry run python -m rgb_assets.minter mint -d rgb_assets/tests/data/nft_definition.json 
```

- MINT new RGB assets from a folder
```shell
poetry run python -m rgb_assets.minter mint -d rgb_assets/tests/data/ 
```

- MINT RGB assets from a folder and send it to a blinded utxo
```shell
poetry run python -m rgb_assets.minter mint -d rgb_assets/tests/data/ -b utxob:MGhM2x9-AccWrjNjm-XVCpaGhF7-gdk51ZpmY-ANtqMLBKJ-hKaiKU
```

### API ENPOINTS
- GET /cfa_assets --> get minted assets of minter wallet
- GET /new_address --> get a new address to fund minter wallet 
- GET /new_blinded_utxo --> get a new blinded UTXO (wallet must be funded)
- GET /list_unspent --> get a list of UTXOs
- POST  /issue_nft --> Issue a new NFT based on a NftDefinition
- POST  /mint_nft --> Issue a new NFT based on a NftDefinition and send it to a blinded UTXO
- POST  /send_nft --> Send an alredy minted NFT to a blinded UTXO


## NFT Definition 
<!--  -->
When you want to create a new mint, you should provide a NFT Definition. It should have the following format.

```
class NftDefinition(BaseModel):
    name: str
    precision: int = 0
    amounts: List[int] = [1]
    description: str = ""
    parent_id: Optional[str] = None
    file_path: Optional[str] = None
    encoded_data: Optional[str] = None
    file_type: Optional[str] = "JPEG"


```
## Configuration
In order to provide your conf to the minter you can create a default .env file

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
- password of the wallet backup in BACKUP_PASS

In the future the keys file may be encryped with BACKUP_PASS


## TODO List:
- [ ] Add a database (SQLite/Mongo)
- [ ] L402 for paid mint requests
- [ ] Refined error hanlding
- [ ] Request Validation
- [ ] Add response model for consistent output
- [ ] Improved testing

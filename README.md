# RGB Assets 

A framework for issuing and transferring assets on top of the Bitcoin using client-side validation.

Use rgb-lib-python to create and manage RGB assets.

Simple webapp using streamlit to create and manage RGB assets.

## TODO
- [ ] Create a RGB21 token in streamlit
- [ ] Create a RGB20 token in streamlit
- [ ] Generate multiple wallets 


## Requirements
Docker and docker compose are required to run this demo.


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

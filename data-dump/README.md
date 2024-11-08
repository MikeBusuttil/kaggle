# Cross Validation Data Dump

## Server Installation

- clone to ubuntu machine with [docker engine](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository) installed
```bash
git clone https://github.com/MikeBusuttil/kaggle.git
cd kaggle/data-dump
```
- create DNS A-record for dump.techiteasy.ca to point to the public IP of the server
- define environment secrets
```bash
python generate_env.py
source .env
```
- fire up the environment
```bash
sudo docker compose -f nginx.yml up -d
sudo docker compose -f db-portal.yml up -d
```

## Client/Worker Installation

- clone to ubuntu machine with [poetry](https://python-poetry.org/docs/#installation) installed
```bash
git clone https://github.com/MikeBusuttil/kaggle.git
pipx install poetry
poetry completions bash >> ~/.bash_completion
cd kaggle
```
- copy `CLIENT_KEY` from server to root `.env`
- fire up environment
```bash
poetry install
source .env
```
- run a worker
```bash
poetry run python 1-home-data/optimize-gbr-custom.py
```

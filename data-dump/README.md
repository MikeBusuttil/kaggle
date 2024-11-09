# Cross Validation Data Dump

## Server Installation

- clone to ubuntu machine with [docker engine](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository) installed
```bash
git clone https://github.com/MikeBusuttil/kaggle.git
cd kaggle/data-dump
```
- create DNS A-record for dump.techiteasy.ca and dump-admin.techiteasy.ca to point to the public IP of the server
- define environment secrets
```bash
python3 generate_env.py
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
apt install pipx
pipx install poetry
cd kaggle
```
- copy `AGENT_KEY` from server to repo root `.env`
- re-login & fire up environment
```bash
poetry self add poetry-plugin-dotenv
poetry install
```
- run a worker
```bash
nohup poetry run python -u 1-home-data/optimize-gbr-custom.py &
tail -f kaggle/nohup.out
```

## Browse Results

To browse results visit https://dump-admin.techiteasy.ca with username `admin` and password from `ADMIN_KEY` in the server's `.env` file

## Analysis TBD

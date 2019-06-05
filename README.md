## API MOCKs

## Requirements

+ python3.6 >
+ pip
+ virtualenv
+ docker
+ docker-compose

## Run project

```bash
git clone $(link_repository)
cd repository
python3.6 -m venv .env
source .env/bin/activate
pip install -r requirements.txt

# run mongo db
docker-compose up -d

# Run tests
pytest src/test

# Run project
python src/main.py

```
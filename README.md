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

# Export environment variables
export PORT=5000
export DB_NAME_MONGO=API_MOCK
export MONGO_CONNECTION=mongodb://localhost:27017/

# run mongo db
docker-compose up -d

# Run project
python src/main.py

# Run tests
pytest src/test

```
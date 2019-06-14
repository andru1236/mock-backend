## API MOCKs

## Requirements

+ python3.6 >
+ pip
+ virtualenv
+ docker
+ docker-compose

## Run project
### without docker
```bash
git clone $(link_repository)
cd repository
python3.6 -m venv .env
source .env/bin/activate
pip install -r requirements.txt

## Required mongo run on port 27017

# Export environment variables
export PORT=5000
export DB_NAME_MONGO=API_MOCK
export MONGO_CONNECTION=mongodb://localhost:27017/


# Run project
python src/main.py

# Run tests
pytest src/test
```

### With docker
```bash
git clone $(link_repository)
cd repository

# view with all logs
docker-compose up
 
# or like daemoon
docker-compose up -d

# stop project
docker-compose down
```

## Author

_Andres Gutierrez P._

**andres.gutierrez@jalasoft.com**

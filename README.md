## Mock backend

## Requirements
+ python3.6 >
+ pip
+ virtualenv (python-venv)
+ docker
+ docker-compose

### Aditional requirements(On linux)
#### On debian / ubuntu
```bash
sudo apt-get install gcc python3-dev
```
## Run project
### Automatic (Make file, or dot files)
```bash
make install # you should have installed python3-venv
make start
make test # To run the test
```
### Without docker
```bash
git clone $(link_repository)

cd repository
python3.9 -m venv .env

source .env/bin/activate

pip install --upgrade pip
python -m pip install --upgrade setuptools
pip install -r requirements-dev.txt
pip install -r requirements-docker.txt

## Required mongo run on port 27017

# Export environment variables
export API_REST_PORT=5000
export GRPC_PORT=5001
export MONGO_CONNECTION=mongodb://localhost:27017/
export MONGO_DB=MOCK
export COLLECTION_API=apis
export COLLECTION_RESPONSE=responses
export COLLECTION_DEVICE=devices

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
docker-compose docker/docker-compose.yml up
 
# or like daemoon
docker-compose docker/docker-compose.yml up -d

# stop project
docker-compose docker/docker-compose.yml down
```

## Author

_Andres Gutierrez P_

**andru1236@gmail.com**

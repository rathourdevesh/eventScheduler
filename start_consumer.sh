export BOOTSTRAP_SERVER="localhost:9092"
export COMSUMER_TOPIC="mytopic1"
export CONSUMER_GROUP_ID="temp-test-group-1"
export MONGO_HOST="localhost:27017"
export DB_NAME="mytasks"
export COLLECTION_NAME="tasks"
export MODE="consumer"

python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m run

# start.sh
export FLASK_APP=app.py
export FLASK_DEBUG=1
export APP_CONFIG_FILE=config.py
python3 -m flask run

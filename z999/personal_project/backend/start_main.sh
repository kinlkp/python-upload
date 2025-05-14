#!/bin/bash


if [ -z $FLASK_RUNTIME_ENV ]; then
    echo "Usage: docker run -d -e FLASK_RUNTIME_ENV='DEV' -p 5000:5000 docker-name"
    exit 1
fi

export PYTHONPATH=$PWD
export FLASK_APP=web_ui/main.py
export FLASK_DEBUG=0
export FLASK_RUNTIME_ENV

flask run --host 0.0.0.0

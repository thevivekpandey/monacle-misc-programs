#!/bin/bash

NAME="email_sender"
PROCESSDIR=/home/ubuntu/misc-programs/email-sender/
USER=ubuntu
GROUP=ubuntu

echo "Starting $NAME"

# Activate the virtual environment
cd $PROCESSDIR
source /home/ubuntu/venv/bin/activate
export PYTHONPATH=$PROCESSDIR:$PYTHONPATH

exec python3 email_sender.py

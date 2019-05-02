
# Host computer configuration

This directory contains:

**model.py** - Helper class for making predictions

**ipc.py** - Helper class for handling messages between the Pi and the host computer

**server.py** - Script for recieving predictions from the robot (running run_model.py), and returning prediction


### To run a model:

1. On the host computer, run `python3 server.py`
2. On the pi, run `python run_model true true` 

# Raspberry Pi configuration

This directory contains:

**/src** - includes classes that interface with Pixy and game the controller

**collect.py** - Script for collecting data

**run_model.py** - Script for running a model 

### Dependancies:

1. Follow steps <a href="https://docs.pixycam.com/wiki/doku.php?id=wiki:v1:hooking_up_pixy_to_a_raspberry_pi">here</a> to install the Pixy Python API
2. Install explorer_hat <a href="https://github.com/pimoroni/explorer-hat#full-install-recommended"> here 

### To collect data:

1. Connect a game controller to the Raspberry Pi
2. Ensure Pixy is connected 
3. Run `./load` 
4. Run `sudo ./run`

### To run a model

1. On the host computer, run `python3 server.py`
2. On the pi, run `python run_model true true` 

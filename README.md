# Networked Calculator

A simple calculator that sends an expression to a server and returns the result to the client.


## Install Instructions

**Required installs**
- Python 3.7+ (This was developed with Python 3.9)
- Docker (Optional)

### From Source
***NOTE: virtual environment setup is assumed***

Once the source is downloaded and unzipped `cd` into
networked-calculator directory and `pip install -r requirements.txt`
to install the base requirements. Now you're ready to go.

### From pip

Optionally you can use pip in your environement and `cd` into
networked-calculator directory and run `pip setup.py`


## How to Run

**Run the server**
From the `src` directory run `python -m calculator.server`

**Run the client**
From the `src` directory run `python -m calculator.client`
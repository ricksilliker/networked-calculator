# Networked Calculator

A simple calculator that sends an expression to a server and returns the result to the client.
TODO: why choose http server

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

**Run the client with PySide UI**
From the `src` directory run `python -m calculator.view`


## Limitations/Caveats

These are just things I probably could implement, but seemed outside the scope of this test.

- (UI) - The minus/subtract button is also used for changing the sign of a number, dunno why Android does this, probably easier to just make a dedicated button for changing signs.
- (Server) - Really really big numbers are tough on Python in general (try 9**9**9), so right now it just times out versus waiting for the solve after 60s.
- (Client) - Double operators are useful to use for things like exponents, changing signs, etc, but there are instances where they can be problematic, and the UI doesn't support them.
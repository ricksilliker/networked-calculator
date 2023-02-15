# Networked Calculator

A simple calculator that sends an expression to a server and returns the result to the client.
I chose to use an HTTP protocol because of how familiar/comfortable I am using with it, and how easy they
are to setup. I also tried to keep the dependencies to a minimum. I knew I didn't want to make my own
request objects because of the scope of that task, so the only dependency other than PySide2 for the UI is requests.
If I want to scale this out I would probably go with a WSGI config and nginx to setup some sort of basic load balancing,
but for this simple use case the ThreadingHTTPServer is good enough at managing multiple client requests.

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
networked-calculator directory and run `python setup.py install`


## How to Run

**Run the server**
From the `src` directory run `python -m calculator.server` or `calculator-server` if installed with `setup.py`

**Run the client**
From the `src` directory run `python -m calculator.client` or `calculator-client` if installed with `setup.py`

**Run the client with PySide UI**
From the `src` directory run `python -m calculator.view`

**Run the Dockerfile server**
Run `docker build -t networked-calculator .` to build
Then `docker run -dp 5454:5454 networked-calculator` to run

## Limitations/Caveats

These are just things I probably could implement, but seemed outside the scope of this test.

- (UI) - The minus/subtract button is also used for changing the sign of a number, dunno why Android does this, probably easier to just make a dedicated button for changing signs.
- (Server) - Really really big numbers are tough on Python in general (try 9**9**9), so right now it just times out versus waiting for the solve after 60s.
- (Server) - Because of the multiprocessing I introduced to enable killing requests, I'm pretty sure I introduced some slowness which I believe is just related to the timeout length.
- (Client) - Double operators are useful to use for things like exponents, changing signs, etc, but there are instances where they can be problematic, and the UI doesn't support them.
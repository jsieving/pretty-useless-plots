## Pretty useless plots: a pretty useless plotting program.

You might as well move along.

## If you decided not to move along

This is a fun little program I'm working on to plot different math-related things...not for data visualization or anything useful, just for fun. You can make some pretty cool art, and maybe even learn something about math. Who knows?

## Installation

You'll need Python 3 installed to run this program.

To get the program, clone this repository:

`git clone https://github.com/jsieving/pretty-useless-plots.git`

This will download all of the code into a folder called `pretty-useless-plots`, within the folder where you ran the clone command.

Next, you'll need to make sure you have the required Python modules to run the program. As of this writing, the following are required:

* numpy - handy mathematical functions
* matplotlib - plotting library, mainly using its color maps
* PySide2 - graphical user interface (GUI) library

Change directory into the repository folder:
`cd pretty-useless-plots`

***Optional***: if you want to keep these requirements specific to this project, rather than installing them globally, you should create a virtual environment. Here's one way to do that, using `venv`:

`python3 -m venv env`

This tells Python 3 to run the `venv` module as a script (`-m`), which will create a virtual environment named `env`.

To activate the environment (i.e., to install modules or run code using that environment), you can run

`source env/bin/activate`

Where `env` is the path to the environment, whatever you named it and wherever you created it. You can tell whether you are in a venv by typing `which python`. The output should have the path to the virtual environment if it's active.

To deactivate the environment, just run `deactivate`.

So, create and activate an environment if you'd like, then run `pip install -r requirements.txt` to install these requirements.

After that, run `python3 app.py` to run the program.

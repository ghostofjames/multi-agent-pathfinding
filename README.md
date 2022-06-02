# Running the Application

The application was written using Python 3.10 utilising built in
libraries only, therefore no additional libraries or software needs to
be installed. The application can be started but running the
`application.py` file, such as with the terminal command
`python application.py`, which will start the application and load the
graphical interface.

Once open, the visualisation of the simulation can be seen on the left.
The controls on the right hand side can be used to control the
simulation, as well as change the path finding algorithm used. Note that
in order to change the algorithm the simulation must be reset using the
`reset` button at the top. Below these controls various details about
the simulation can be seen.

The configuration to load can be changed within the `simulation.py` file
by editing the `DEFAULT_CONFIG` parameter at the top of the file.
Multiple example configurations are included within the `configs` folder
and can be used as a template to create new configurations. Within the
`simulation.py` there are also parameters for adjusting the maximum
number of agents and tasks that the simulation should load from the
configuration file.
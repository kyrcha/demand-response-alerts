# dr-ieee-trans-smart-grid

Demand response research, code for the submission in the IEEE Transactions on Smart Grid

## Pre-processing and lib

- A library file of common methods: [lib.py](./lib.py)
- [The pre-processing notebook for REFIT (TO ADD)](), transforming raw data into pandas dataframes for each appliance
- [The pre-processing notebook for HES (TO ADD)](), transforming raw data into pandas dataframes for each appliance

## Experiment 1

In experiment 1, we send targetted messages to a pre-specified number of households for a pre-specified device using our modelling methodology and randomly

- [REFIT washing machines](./REFIT%20Experiment%201%20-%20Washing%20Machines.ipynb)
- [REFIT dish washers](./REFIT%20Experiment%201%20-%20Dish%20Washers.ipynb)
- [REFIT tumble dryers](./REFIT%20Experiment%201%20-%20Tumble%20Dryers.ipynb)
- [HES washing machines](./HES%20Experiment%201%20-%20Washing%20Machines.ipynb)
- [HES dish washers](./HES%20Experiment%201%20-%20Dish%20Washers.ipynb)
- [HES tumble dryers](./HES%20Experiment%201%20-%20Tumble%20Dryers.ipynb)

### Working vs. non working days

Where instead of modelling per day of week, we model per working vs. non-working day

- [Notebook](./REFIT%20Experiment%201%20-%20Washing%20Machines%20-%20Workdays%20vs.%20Weekends.ipynb)

### Yesterday

Where instead of modelling per day of week, we whether the appliance was on or off the previous day

- [Notebook](./REFIT%20Experiment%201%20-%20Washing%20Machines%20-%20Yesterday.ipynb)

## Experiment 2

In experiment 2, we sent targetted messages based on a pre-specifid threshold to all households that their probability of opening a wet or heating device is above that threshold.

- For [REFIT](./REFIT%20Experiment%202%20-%20MultiDevice.ipynb)
- For [HES](./HES%20Experiment%202%20-%20MultiDevice.ipynb)

## Experiment 3

In experiment 3, we sent targetted messages based on a pre-specifid threshold to all households that their probability of opening a specific device out of their wet and heating devices is above that threshold.

- For [REFIT](./REFIT%20Experiment%203%20-%20Personalized.ipynb)
- For [HES](./HES%20Experiment%203%20-%20Personalized.ipynb)

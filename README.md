# dr-ieee-trans-smart-grid

Demand response research, code for the submission in the IEEE Transactions on Smart Grid

## Pre-processing and lib

- A library file of common methods: [lib.py](./lib.py)
- [The pre-processing notebook for REFIT](), transforming raw data into pandas dataframes for each appliance
- [The pre-processing notebook for HES](), transforming raw data into pandas dataframes for each appliance

## Experiment 1

In experiment 1, we send targetted messages to a pre-specified number of households for a pre-specified device using our modelling methodology and randomly

- [REFIT washing machines]()
- [REFIT dish washers]()
- [REFIT tumble dryers]()
- [HES washing machines]()
- [HES dish washers]()
- [HES tumble dryers]()

### Working vs. non working days

Where instead of modelling per day of week, we model per working vs. non-working day

### Yesterday

Where instead of modelling per day of week, we whether the appliance was on or off the previous day

## Experiment 2

In experiment 2, we sent targetted messages based on a pre-specifid threshold to all households that their probability of opening a wet or heating device is above that threshold.

- For [REFIT]()
- For [HES]()

## Experiment 3

In experiment 3, we sent targetted messages based on a pre-specifid threshold to all households that their probability of opening a specific device out of their wet and heating devices is above that threshold.

- For [REFIT]()
- For [HES]()

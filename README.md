# Simple Queueing System Simulator (SQSS)

## Overview

The queueing system in question consists of the following parts:
* a single source of requests, which generates requests according to Poisson process or ON/OFF modulated Poisson process,
* a queue of requests awaiting acceptance (its maximum size can be equal to 0, finite or infinite),
* a token bucket, characterised by maximum token capacity and token arrival speed (constant),
* an entry point, where requests are accepted or rejected based on the state of the token bucket and the queue.

The main purpose of the simulator is to measure the following quality indicators:
* D - average waiting time of requests before being accepted,
* P<sub>B</sub> - blockage probability, i.e. probability that a request will be rejected.


## Instructions

The simulator is a console application written in Python. It takes the following command line arguments:

| Parameter | Values | Description                                                                                         |
|-----------|--------|-----------------------------------------------------------------------------------------------------|
| --debug   | 0 or 1           | Turn debug mode on/off. While in debug mode, additional info will be displayed and the execution will be stopped after each simulation step. Press **ENTER** to proceed. By default, debug is set to 0. |
| --samples | int              | Number of samples, i.e. times the simulation is run for the same set of parameters. The resulting D and P<sub>B</sub> are averages of D and P<sub>B</sub> acquired in each simulation run. The default is 1. |
| --accqty  | int              | The stop condition. The simulation will end if the specified number of accepted requests is reached. Large accqty values are needed to achieve stability of the queueing system. The default value is 1000. |
| --lq      | int or INF       | The maximum size of the queue of requests awaiting acceptance. Can be either 0 (no queue at all), a finite natural number or INF (infinite size). The default is 100. |
| --lz      | int              | The capacity of the token bucket. The default is 40. |
| --vz      | int              | The speed of new tokens' arrival. The default is 5. |
| --gentype | poisson or onoff | The type of request generator. The default is poisson. |
| --lamb    | int              | The intensity of requests' arrivals, i.e. the average number of requests' arrivals per time unit. In other words, it's the &lambda; parameter of the Poisson distribution describing requests' arrivals. |
| --ton     | int              | The average length of ON state intervals. In the ON state, the generator produces requests according to Poisson process. Taken into account only if *--gentype onoff* is used. The default is 10. |
| --toff    | int              | The average length of OFF state intervals. In the OFF state, the generator produces no requests. Taken into account only if *--gentype onoff* is used. The default is 20. |


### Running the simulator for a single data instance

For a single data instance, the **simulation.py** can be run in a terminal like this:

`python simulation.py --accqty 1000 --samples 20 --lq INF --lz 30 --vz 5 --lamb 10`

or, for ON/OFF:

`python simulation.py --accqty 4000 --samples 20 --lq 40 --lz 30 --vz 5 --lamb 10 --gentype onoff --ton 5 --toff 25`


### Running the simulator for a scenario (multiple data instances)

To run the simulator using data from the specified scenario, use:

`python run_scenario.py SCENARIO_NAME`

where *SCENARIO_NAME* is the name of a txt file placed in the scenarios subdirectory.

E.g.:

`python run_scenario.py test_scenario_poisson`

or

`python run_scenario.py test_scenario_onoff`

The scenario format is the following (*?* denotes a parameter value):

```
--gentype ? --samples ? --accqty ?
--lq ? --lz ? --vz ? --lamb ? --ton ? --toff ?
--lq ? --lz ? --vz ? --lamb ? --ton ? --toff ?
--lq ? --lz ? --vz ? --lamb ? --ton ? --toff ?
...
```

The first line (containing --gentype, --samples, --accqty) is used in all tests. The following lines describe single tests. Please refer to *scenarios/test_scenario_onoff.txt* and *scenarios/test_scenario_onoff.txt* for an example.

After run_scenario.py finishes, files containing results can be found in the scenarios subdirectory.


### Running tests

To run simple simulator tests, use:

`python mini_tester.py`


## Further development

No exhaustive analysis was done to ensure the extensibility of the simulator. A quick look at the code suggests that:
* adding different Generator **types** should pose no problems,
* adding a variable priority and a variable token cost to requests should be easy,
* adding multiple generators would require implementing some sort of scheduling procedure to the Simulation class,
* changing the token bucket algorithm to a different algorithm would require modifications in the Simulation class,
* more unit testing should be done. Changing the MiniTester to unittest framework would be welcome.


## Acknowledgements

Thanks go to Franz Schubert for composing his fourth symphony in C minor, Nikolaus Harnoncourt and Wiener Philharmoniker for performing it in a satisfactory manner, YouTube user [Eliahavani](https://www.youtube.com/user/Eliahavani/) for [uploading a good quality version](https://www.youtube.com/watch?v=CnoI-sYtCOU). It provided an excellent environment for quick coding.

## License

Copyright (C) 2016 Wojciech Kuprianowicz. Licensed under the GNU GPLv3 license (see LICENSE.txt for details).

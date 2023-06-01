# Robotics: Markov Localization and Monte Carlo Localization

Implementation of **Markov Localization** where the goal is for a robot to determine its pose in a known environment. An example of the use is when a robot that is fully aware of its envoronment gets picked up ("kidnapped") and re-positioned somewhere.

The robot updates its pose belief in the known environment by iterating two steps:

- ```See```: For each possible pose $l$, update the current belief by getting a sensor measurement $i$.

$$
p(l|i) = \frac{p(i|l)p(l)}{p(i)} \propto p(i|l)p(l)
$$

where $p(i|l)$ is the probability of getting a measurement $i$ given that the robot's pose is $l$, to take measurement uncertainty into account.

- ```Act```: For each possible pose $l$, update the current belief by issuing a command $o$ to the robot.

$$
p(l_t|o_t) = \int p(l_t|l_{t-1}^{'}, o_t)p(l_{t-1}^{'})dl_{t-1}^{'}
$$

where $p(l_t|l_{t-1}^{'}, o_t)$ is the motion model of the robot that for a given command $o$ represents the probabilities for new poses $l_t$.


## How to run:
First of all, install the required libraries:
```shell
$ pip install -r requirements.txt
```
#### Run with default settings:
Simply execute the main file with python and control the robot with the allow keys.
```shell
$ python main.py
```

#### Controls:
Go forwards and backwards with the ARROW_UP and ARROW_DOWN keys. Rotate left and right with the ARROW_LEFT and ARROW_RIGHT keys. 
The robot can be "kidnapped" (picked up) and relocated in any area of the environment by a left-click on the desired location. 

#### Run with custom settings:
The file `./definitions.py` defines global variables and objects that will be used in the simulation. You can control the following variables:

`COMMAND_TYPE = {'KEYBOARD'|'RANDOM'}` defines whether the robot is controlled by the keyboard or is moving randomly.

`FPS = [0,..,60]` defines the target FPS of the simulation. Under heavy computations, they will drop.

`SPEED = [0,...]`  defines the speed in tiles per second

`SIM_TYPE = {'DISCRETE'|'CONTINUOUS'}` defines whether the simulation will be discrete (grid world) or it allows continuous movements. In the first case a Markov Localization  approach will be used and in the latter case a Monte Carlo approach will be used.

`PARTICLE_SIZE = [0,...]` defines the size of the particle in case of a Monte Carlo approach. Suggested size: 10.

`NUM_PARTICLES = [0,...]` defines the number of particles used in the Monte Carlo approach (particle filter). Suggested: 100 or 200 for a relatively small environment.

`PARTICLE_NOISE = [0,...]` Defines the particle noise which is the $\sigma$ for displacement of resampled particles. Suggested: 1.0

`JITTER_RATE = [0,...]` Defines the jitter rate which is the percentage of randomly sampled particles without following the current distribution. It helps to recover from situations where the robot is lost. Suggested: 0.1

`SCALE = [1, ...]` Scaling of the environment. Must be an integer value.

`ENVIRONMENT = {"custom", ...}` Defines the envorinment to use. Must be one of the strings defined in the dictionary `defs` (definitions), which containes pre-defined environments. 

Each definition is an instance of the class:
```python
class Definition(
    width: int,
    height: int,
    robot_start: Tuple[int, int],
    sensor_sig: float,
    objects: list = (),
    sensor_len: float = 900,
    generate_plots: bool = False,
    tile_size: int = 20
)
```
where `width` and `height` define the world size in tiles. `robot_start` defines the initial position of the robot in tile coordinates. `sensor_sigma` defines the standard deviation of the sensor's uncertainty, which is modelled as a normal distribution. `objects` is a list of objects/obstacles placed on the environment. `sensor_len` is the length/range of the laser sensor in tiles. A long-ranged sensor usually helps the convergence. `generate_plots` generates at each iteration 8 plots displaying the probabilities of poses associated with the 8 possible orientations. It is highly suggested not to use this functionality. `tile_size` defines the size of the (square) tiles in pixels. 

The list of objects passed to a `Definition` are defined in `./environments.py`. Each list is a list of tuples of the form `(DisplayableObstacle, {"points": [5, 5, 2, 10], "color": color})` representing the data type of the object and a dictionary of arguments that define the object properties. 

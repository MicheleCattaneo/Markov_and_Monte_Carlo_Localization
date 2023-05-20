# Robotics: Markov Localization

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

import numpy as np

from base.localization import LocalizationBase
from base.robot import RobotBase
from base.sensor import SensorBase
from definitions import ROBOT_SIZE, TILE_SIZE
from model.movement_model import MovementModel


class DiscreteRobot(RobotBase):

    def __init__(self, world, x, y, sensor: SensorBase, localization: LocalizationBase) -> None:
        """Initializes a robot at the given coordinates with a specific sensor type and markov localization method.

        Args:
            world (model.grid_world.GridWorld): The world where the robot resides.
            x (float): the x coordinate
            y (float): the y coordinate
            sensor (SensorBase): the sensor type
            localization (LocalizationBase): the localization type
        """
        self.sensor = sensor
        self.set_position(x, y)

        self.world = world
        self.localization = localization
        self.movement_model = self.localization.movement_model

        # reset sensor to fit the robots position
        self.sensor.sense(self.position + ROBOT_SIZE, self.orientation)

    def move(self, action: RobotBase.Action, dt: float):
        self.current_action = action
        if action == action.TURN_LEFT:
            self.orientation = self.Direction((self.orientation.value - 1) % len(self.Direction))
        elif action == action.TURN_RIGHT:
            self.orientation = self.Direction((self.orientation.value + 1) % len(self.Direction))
        else:

            uncertainty_multiplier = 1.
            # unless the robot uses a deterministic movement model, change the multiplier
            if not isinstance(self.movement_model, MovementModel):
                # a multiplier of 1 keeps the same direction, 0 annihilates the action
                # and -1 reverses the action.
                uncertainty_multiplier = np.random.choice([1., 0., -1.], p=self.movement_model.probs)

            move_dir = self.orientation.value \
                if action == action.FORWARD \
                else (self.orientation.value + 4) % len(self.Direction)

            new_pos_deterministic = self.position + DiscreteRobot.directions[move_dir]
            new_pos = self.position + uncertainty_multiplier * DiscreteRobot.directions[move_dir]

            # get i,j coordinates and check whether that tile is occupied by an object (obstacle)
            if not self.world.walkable[tuple(new_pos.astype(int))]:
                return
            # bumper sensor; even the uncertainty tells you not to move,
            # if you are in front of an obstacle, don't execute any action.
            if not self.world.walkable[tuple(new_pos_deterministic.astype(int))]:
                return
            self.set_position(new_pos)

        reading = self.sensor.sense(self.position + ROBOT_SIZE, self.orientation)

        self.localization.act(action)
        self.localization.see(reading)

        self.on_move.notify()

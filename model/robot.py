import numpy as np

from base.localization import LocalizationBase
from model.movement_model import DiscreteMovementModel
from base.sensor import SensorBase
from definitions import *
from base.robot import RobotBase


class DiscreetRobot(RobotBase):
    directions = [
        np.array([0, 1]),
        np.array([1, 1]),
        np.array([1, 0]),
        np.array([1, -1]),
        np.array([0, -1]),
        np.array([-1, -1]),
        np.array([-1, 0]),
        np.array([-1, 1])
    ]

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

    def move(self, action: RobotBase.Action):
        self.current_action = action
        if action == action.TURN_LEFT:
            self.orientation = self.Direction((self.orientation.value - 1) % len(self.Direction))
        elif action == action.TURN_RIGHT:
            self.orientation = self.Direction((self.orientation.value + 1) % len(self.Direction))
        else:
            
            uncertainty_multiplier = 1.
            # unless the robot uses a deterministic movement model, change the multiplier
            if not isinstance(self.movement_model, DiscreteMovementModel):
                # a multiplier of 1 keeps the same direction, 0 annihilates the action 
                # and -1 reverses the action.
                uncertainty_multiplier = np.random.choice([1.,0.,-1.], p=self.movement_model.probs)

            move_dir = self.orientation.value \
                if action == action.FORWARD \
                else (self.orientation.value + 4) % len(self.Direction)


            new_pos_deterministic = self.position + DiscreetRobot.directions[move_dir]
            new_pos = self.position + uncertainty_multiplier * DiscreetRobot.directions[move_dir]

            # get i,j coordinates and check whether that tile is occupied by an object (obstacle)
            if not self.world.walkable[tuple(new_pos.astype(int))]:
                return
            # bumper sensor; even the uncertainty tells you not to move,
            # if you are in front of an obstacle, dont execute any action.
            if not self.world.walkable[tuple(new_pos_deterministic.astype(int))]:
                return
            self.set_position(new_pos)

        reading = self.sensor.sense(self.position + ROBOT_SIZE, self.orientation)

        
        self.localization.act(action)
        self.localization.see(reading)

        self.on_move.notify()

    def teleport(self, x: float, y: float) -> None:
        """Teleports the robot to a new position.
        Calls robot.set_position()

        Args:
            x (float): x pixel coordinates
            y (float): y pixel coordinates
        """
        self.set_position(x // TILE_SIZE, y // TILE_SIZE)


class ContinuousRobot(RobotBase):
    directions = [
        np.array([0, 1]),
        np.array([1, 1]),
        np.array([1, 0]),
        np.array([1, -1]),
        np.array([0, -1]),
        np.array([-1, -1]),
        np.array([-1, 0]),
        np.array([-1, 1])
    ]

    def __init__(self, world, x, y, sensor: SensorBase, localization: LocalizationBase) -> None:
        self.sensor = sensor
        self.set_position(x, y)

        self.world = world
        self.localization = localization

        # reset sensor to fit the robots position
        self.sensor.sense(self.position + ROBOT_SIZE, self.orientation)

    def move(self, action: RobotBase.Action):
        self.current_action = action

        if action == action.TURN_LEFT:
            self.orientation = self.Direction((self.orientation.value - 1) % len(self.Direction))
        elif action == action.TURN_RIGHT:
            self.orientation = self.Direction((self.orientation.value + 1) % len(self.Direction))
        else:
            
            uncertainty_multiplier = 1.

            move_dir = self.orientation.value \
                if action == action.FORWARD \
                else (self.orientation.value + 4) % len(self.Direction)

            speed_mult = SPEED / FPS
            new_pos = self.position + uncertainty_multiplier * speed_mult * ContinuousRobot.directions[move_dir] * TILE_SIZE / np.linalg.norm(ContinuousRobot.directions[move_dir] * TILE_SIZE)

            new_center = (new_pos + ROBOT_SIZE) * TILE_SIZE
            if not self.world.check_within_boundaries(new_center[0], new_center[1]) or self.world.is_occupied(new_center[0], new_center[1]):
                return
            self.set_position(new_pos)

        reading = self.sensor.sense(self.position + ROBOT_SIZE, self.orientation)[0]

        self.localization.act(action)
        self.localization.see(reading)

        self.sensor.sense(self.position + ROBOT_SIZE, self.orientation)[0]

        self.on_move.notify()

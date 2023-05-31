from model.definition import Definition
from environments import custom, base_with_obstacle, symmetric_rooms

COMMAND_TYPE = 'KEYBOARD'  # KEYBOARD, RANDOM
FPS = 15
SPEED = 100  # tiles per second

# Environment
SCALE = 1  # must be int
ENVIRONMENT = "symmetric_rooms"
defs = {
    "custom": Definition(
        width=30,
        height=40,
        robot_start=(20, 30),
        sensor_len=30*1.5,
        sensor_sig=5,
        objects=custom
    ),
    "base": Definition(
        width=20,
        height=20,
        robot_start=(10, 10),
        sensor_sig=.7,
        generate_plots=False
    ),
    "base_with_obstacle": Definition(
        width=20,
        height=20,
        robot_start=(4, 4),
        sensor_sig=.7,
        objects=base_with_obstacle,
        generate_plots=False
    ),
    "symmetric_rooms": Definition(
        width=51,
        height=31,
        generate_plots=False,
        objects=symmetric_rooms,
        robot_start=(9,9),
        sensor_sig=2.5
    )
}[ENVIRONMENT]


RES_WIDTH = SCALE * defs.width * defs.tile_size
RES_HEIGHT = SCALE * defs.height * defs.tile_size
TILE_SIZE = SCALE * defs.tile_size

# Robot
ROBOT_SIZE = 0.5
ROBOT_START_X, ROBOT_START_Y = defs.robot_start

# Sensor
SENSOR_LENGTH = SCALE * TILE_SIZE * defs.sensor_len
MEASUREMENT_SIGMA = SCALE * TILE_SIZE * defs.sensor_sig

# Visualization
GENERATE_PLOTS = defs.generate_plots

assert RES_HEIGHT % TILE_SIZE == 0 and RES_WIDTH % TILE_SIZE == 0, "Width and height should be a multiple of TILE_SIZE"

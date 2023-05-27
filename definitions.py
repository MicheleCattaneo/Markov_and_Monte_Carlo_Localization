from model.definition import Definition
from environments import custom, base_with_obstacle

COMMAND_TYPE = 'KEYBOARD'  # KEYBOARD, RANDOM
FPS = 15
SPEED = 10 # tiles per second

# Environment
SCALE = 1  # must be int
ENVIRONMENT = "base_with_obstacle"
defs = {
    "custom": Definition(
        width=30,
        height=40,
        robot_start=(20, 30),
        sensor_len=30*1.5,
        sensor_sig=5,
        generate_plots=True,
        objects=custom
    ),
    "base": Definition(
        width=20,
        height=20,
        robot_start=(10, 10),
        sensor_sig=.7,
    ),
    "base_with_obstacle": Definition(
        width=20,
        height=20,
        robot_start=(4, 4),
        sensor_sig=.7,
        objects=base_with_obstacle
    )
}[ENVIRONMENT]


RES_WIDTH = SCALE * defs.width * defs.tile_size
RES_HEIGHT = SCALE * defs.height * defs.tile_size
TILE_SIZE = SCALE * defs.tile_size

# Robot
ROBOT_SIZE = 0.5
ROBOT_START_X, ROBOT_START_Y = defs.robot_start

# Sensor
SENSOR_LENGTH = TILE_SIZE * defs.sensor_len
MEASUREMENT_SIGMA = TILE_SIZE * defs.sensor_sig

# Visualization
GENERATE_PLOTS = False

assert RES_HEIGHT % TILE_SIZE == 0 and RES_WIDTH % TILE_SIZE == 0, "Width and height should be a multiple of TILE_SIZE"

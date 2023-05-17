COMMAND_TYPE = "KEYBOARD"  # 'RANDOM'

# Environment
RES_WIDTH = 100
RES_HEIGHT = 200
TILE_SIZE = 10

# Robot
ROBOT_SIZE = 0.5
SENSOR_LENGTH = 30


assert RES_HEIGHT % TILE_SIZE == 0 and RES_WIDTH % TILE_SIZE == 0, "Width and height should be a multiple of TILE_SIZE"

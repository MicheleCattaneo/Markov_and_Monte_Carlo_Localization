COMMAND_TYPE = "KEYBOARD"  # 'RANDOM'

# Environment
RES_WIDTH = 800
RES_HEIGHT = 720
TILE_SIZE = 10

# Robot
ROBOT_SIZE = 0.5
SENSOR_LENGTH = 200


assert RES_HEIGHT % TILE_SIZE == 0 and RES_WIDTH % TILE_SIZE == 0, "Width and height should be a multiple of TILE_SIZE"

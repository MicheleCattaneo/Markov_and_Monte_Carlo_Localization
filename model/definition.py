from dataclasses import dataclass
from typing import Tuple


@dataclass
class Definition(dict):
    width: int
    height: int
    robot_start: Tuple[int, int]
    sensor_sig: float
    objects: list = ()
    sensor_len: float = 900
    generate_plots: bool = False
    tile_size: int = 20

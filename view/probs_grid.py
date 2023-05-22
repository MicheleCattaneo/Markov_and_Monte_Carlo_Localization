from base.observer_pattern import Observer
from base.robot import RobotBase
from base.shapes import DisplayableRectangle
import numpy as np
import pyglet.graphics



class ProbabilitiesView(Observer):
    '''
    View of probabilities (pose belief) on the grid of possible poses.
    '''
    def __init__(self, robot: RobotBase, batch: pyglet.graphics.Batch, 
                 res_width: int, 
                 res_height: int, 
                 tile_size,
                 walkable) -> None:
        
        super().__init__()
        self.robot = robot
        self.batch = batch
        self.res_width = res_width
        self.res_height = res_height
        self.tile_size = tile_size

        self.tiles = np.empty(walkable.shape, dtype=object)

        # print(walkable.shape)
        color = (0, 0, 255)
        for i in range(0, res_width, tile_size):
            for j in range(0, res_height, tile_size):
                # print(i,j)
                if walkable[i // tile_size, j // tile_size]:
                    self.tiles[i // tile_size, j // tile_size] = DisplayableRectangle(
                        i+1, j+1, tile_size-2, tile_size-2,
                        color = color, batch=self.batch)
                
        self.robot.on_move.subscribe(self)


    def update(self) -> None:
        # sum probabilities over the rotation dimension
        robot_probs_sum = self.robot.belief.sum(axis=2)
        min_prob = robot_probs_sum.min()
        max_prob = robot_probs_sum.max()

        def rescale(x, old_min, old_max, new_min, new_max):
            return  ( (x - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min
        
        # for each walkable tile, change the opacity by rescaling it 
        # from (min_prob, max_prob) to (0,255)
        for x in range(0, self.res_width, self.tile_size):
            for y in range(0, self.res_height, self.tile_size):
                i = x // self.tile_size
                j = y // self.tile_size
                if self.tiles[i, j]:
                    if robot_probs_sum[i, j] == 0:
                        self.tiles[i, j].opacity = 255
                        self.tiles[i, j].color = (0, 0, 0)
                    else:
                        new_opacity = rescale(robot_probs_sum[i, j], min_prob, max_prob, 128, 255)
                        self.tiles[i, j].opacity = int(new_opacity)
                        self.tiles[i, j].color = (0, 0, 255)



    
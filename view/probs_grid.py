from PIL import Image
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
import pyglet.graphics
from scipy.ndimage import rotate

from base.observer_pattern import Observer
from base.robot import RobotBase
from base.shapes import DisplayableRectangle
from definitions import GENERATE_PLOTS
from model.environment import GridWorld


class LocalizationBeliefView(Observer):
    '''
    View of probabilities (pose belief) on the grid of possible poses.
    '''

    def __init__(self, robot: RobotBase, world: GridWorld, batch: pyglet.graphics.Batch) -> None:
        self.robot = robot
        self.world = world

        self.tiles = np.empty_like(world.walkable, dtype=object)

        # print(walkable.shape)
        color = (0, 0, 255)
        tile_size = world.tile_size
        for i in range(world.width):
            for j in range(world.height):
                if world.walkable[i, j]:
                    self.tiles[i, j] = DisplayableRectangle(
                        i * tile_size + 1, j * tile_size + 1, tile_size - 2, tile_size - 2,
                        color=color, batch=batch)

        self.robot.on_move.subscribe(self)

    def update(self) -> None:
        self.color_tiles_according_to_localization_beliefs()
        if GENERATE_PLOTS:
            self.plot_8_orientations()

    def color_tiles_according_to_localization_beliefs(self):
        # sum probabilities over the rotation dimension
        robot_probs_sum = self.robot.localization.belief.sum(axis=2)

        # for each walkable tile, change the opacity by rescaling it
        # from (min_prob, max_prob) to (0,255)
        for i in range(self.world.width):
            for j in range(self.world.height):
                if self.tiles[i, j]:
                    new_opacity = robot_probs_sum[i, j]**0.1
                    self.tiles[i, j].opacity = int(new_opacity*255)

    def plot_8_orientations(self):
        plt.close()
        colormap = sns.color_palette("PuBuGn", as_cmap=True)
        fig, ax = plt.subplots(3, 3, figsize=(12, 12))

        indices = [
            [7, 0, 1],
            [6, None, 2],
            [5, 4, 3]
        ]
        for i in range(3):
            for j in range(3):
                if i == 1 and j == 1:
                    img = np.asarray(Image.open("rob.png"))
                    img = rotate(img, 90 - 45*self.robot.orientation.value, reshape=False)
                    ax[i, j].imshow(img)
                    ax[i, j].axis("off")
                    continue
                idx = indices[i][j]
                sns.heatmap(self.robot.localization.belief[:, :, idx].T, ax=ax[i, j], linewidths=0.1, cmap=colormap)
                ax[i, j].title.set_text(self.robot.Direction(idx).name.replace("_", " "))

                ax[i, j].invert_yaxis()
        fig.savefig("plots/probs.png")
        # fig.show()

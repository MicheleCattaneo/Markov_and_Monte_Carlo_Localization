class GridWorld:

    def __init__(self, grid_size, tile_size) -> None:
        self.grid_size = grid_size
        self.tile_size = tile_size
        self.objects = []

    def add(self, object):
        self.objects.append(object)

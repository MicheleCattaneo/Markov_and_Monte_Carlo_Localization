from base.movement_models import MovementModelBase
import numpy as np

class DiscreteMovementModel(MovementModelBase):


    def _get_convolution_forward(self):
        filter = np.zeros((3,3,8))
        filter[0,1,0] = 1
        filter[0,2,1] = 1
        filter[1,2,2] = 1
        filter[2,2,3] = 1
        filter[2,1,4] = 1
        filter[2,0,5] = 1
        filter[1,0,6] = 1
        filter[0,0,7] = 1

        return filter

    def _get_convolution_backward(self):
        filter = np.zeros((3,3,8))
        filter[2,1,0] = 1
        filter[2,0,1] = 1
        filter[1,0,2] = 1
        filter[0,0,3] = 1
        filter[0,1,4] = 1
        filter[0,2,5] = 1
        filter[1,2,6] = 1
        filter[2,2,7] = 1

        return filter
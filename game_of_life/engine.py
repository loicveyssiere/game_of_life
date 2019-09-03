import numpy as np

# ==============================================================================
# INTERFACE
# ==============================================================================
class Engine():
    def __init__(self):
        pass

# ==============================================================================
# PYTHON IMPLEMENTATION
# ==============================================================================
class EnginePythonV1(Engine):
    def __init__(self):
        super().__init__()
        self.matrix = None

    def get(self, coord):
        return self.matrix[self.map_board_engine(coord)]

    def set(self, coord, value):
        #print(self.map_board_engine(coord))
        self.matrix[self.map_board_engine(coord)] = value
        #print(self.matrix)

    def one_step_simulation(self):
        tmp = np.zeros((self.engine_nx, self.engine_ny))

        for i in range(1, self.engine_nx - 1):
            for j in range(1, self.engine_ny - 1):
                counter = 0
                counter += self.matrix[i-1, j-1]
                counter += self.matrix[i-1, j]
                counter += self.matrix[i-1, j+1]
                counter += self.matrix[i, j+1]
                counter += self.matrix[i+1, j+1]
                counter += self.matrix[i+1, j]
                counter += self.matrix[i+1, j-1]
                counter += self.matrix[i, j-1]

                if counter == 3:
                    tmp[i, j] = 1
                elif counter == 2 and self.matrix[i, j] == 1:
                    tmp[i, j] = 1

        self.matrix[:,:] = tmp[:,:]

    def fit(self, nx, ny):

        #if self.matrix = None:
        #self.matrix = np.zeros((self.engine_nx, self.engine_ny), dtype=int)
        #else:
        #    pass
            #tmp = 
            #self.matrix[0:nx, 0:ny] = 

        #self.clear() # free object and memory

        self.board_nx = nx
        self.board_ny = ny
        self.engine_nx = self.board_nx + (2 * 10)
        self.engine_ny = self.board_ny + (2 * 10)
        self.zero_x = 10
        self.zero_y = 10

        self.matrix = np.zeros((self.engine_nx, self.engine_ny), dtype=int)

    def map_board_engine(self, coord):
        return (coord[0] + self.zero_x, coord[1] + self.zero_y)

    def map_engine_board(self, coord):
        # TODO check if is inside
        return (coord[0] - self.zero_x, coord[1] - self.zero_y)

    def clear(self):
        pass

class EnginePythonV2(EnginePythonV1):
    def __init__(self):
        super().__init__()

    def one_step_simulation(self):
        
        tmp = np.zeros((self.engine_nx, self.engine_ny))
        inner = self.matrix[1:self.engine_nx-1, 1:self.engine_ny-1]
        
        tmp[0:self.engine_nx-2, 0:self.engine_ny-2] += inner
        tmp[0:self.engine_nx-2, 1:self.engine_ny-1] += inner
        tmp[0:self.engine_nx-2, 2:self.engine_ny] += inner
        tmp[1:self.engine_nx-1, 2:self.engine_ny] += inner
        tmp[2:self.engine_nx, 2:self.engine_ny] += inner
        tmp[2:self.engine_nx, 1:self.engine_ny-1] += inner
        tmp[2:self.engine_nx, 0:self.engine_ny-2] += inner
        tmp[1:self.engine_nx-1, 0:self.engine_ny-2] += inner
        
        self.matrix = 1 * np.logical_or(tmp == 3, np.logical_and(tmp == 2, self.matrix == 1))


class EngineC(Engine):
    pass
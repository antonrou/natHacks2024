import numpy as np

def random_matrix():
    rows = 8
    columns = 256
    matrix = np.random.uniform(50, 100, size = (rows, columns))
    return matrix
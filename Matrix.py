import numpy as np
from numpy.lib import utils
import Algo
import Util
import sys


def sidewise_weights(col_number, overlap, otherOverlap, weights, node_matrix, adj_matrix):
    dim = overlap.shape[0]
    for i in range(0, dim):
        # value = np.linalg.norm(matrix1[i, col] - matrix2[i, col]) + np.linalg.norm(matrix1[i, col + 1] - matrix2[i, col + 1])
        value = weights[i] = np.sum(np.square(overlap[i, col_number] - otherOverlap[i, col_number], dtype=np.float) + np.square(
            overlap[i, col_number + 1] - otherOverlap[i, col_number + 1]), dtype=np.float) + pow(.01, 3)
        weights[i] = value

    col1 = node_matrix[:, col_number]
    col2 = node_matrix[:, col_number + 1]

    for i in range(0, len(col1)):
        leftPos = col1[i]
        rightPos = col2[i]

        adj_matrix[leftPos][rightPos] = weights[i]

    return adj_matrix


def downwise_weights(rownumber, overlap, otherOverlap, weights, node_matrix, adj_matrix):
    dim = overlap.shape[1]
    for i in range(0, dim):
        # edge_weights[i] = np.linalg.norm(matrix1[row, i] - matrix2[row, i]) + np.linalg.norm(matrix1[row + 1, i] - matrix2[row + 1, i])
        weights[i] = np.sum(np.square(overlap[rownumber, i] - otherOverlap[rownumber, i], dtype=np.float) + np.square(
            overlap[rownumber + 1, i] - otherOverlap[rownumber + 1, i]), dtype=np.float) + pow(.01, 3)
    # adjacency_matrix[currentPos][rightPos] = edge_weight

    row1 = node_matrix[rownumber, :]
    row2 = node_matrix[rownumber + 1, :]

    for i in range(0, len(row1)):
        adj_matrix[row1[i], row2[i]] = weights[i]

    return adj_matrix


def adding_edgeCapacity(node_matrix, adj_matrix, cut):
    w_adj = adj_matrix.shape[1]
    alignment = None
    otheralignment = None

    if cut == "leftright_merge":
        alignment = node_matrix[:, 0]
        otheralignment = node_matrix[:,  node_matrix.shape[1] - 1]
    else:
        alignment = node_matrix[0, :]
        otheralignment = node_matrix[node_matrix.shape[0]-1, :]

    for i, j in enumerate(alignment):
        adj_matrix[0, j] = sys.maxsize

    for i, j in enumerate(otheralignment):
        adj_matrix[j, w_adj - 1] = sys.maxsize

    return adj_matrix


def calGraph(node_matrix, nodecount, overlap, otherOverlap, cut):
    adj_matrix = np.zeros([nodecount+2, nodecount+2], dtype=float)

    weights1 = np.zeros([overlap.shape[0], 1])
    weights2 = np.zeros([overlap.shape[1], 1])

    adj_matrix = adding_edgeCapacity(node_matrix, adj_matrix, cut)

    for col in range(overlap.shape[1] - 1):
        adj_matrix = sidewise_weights(
            col, overlap, otherOverlap, weights1, node_matrix, adj_matrix)

    for row in range(overlap.shape[0] - 1):
        adj_matrix = downwise_weights(row, overlap, otherOverlap,
                                      weights2, node_matrix, adj_matrix)

    Util.writefile(adj_matrix.tolist())

    return Algo.algo(adj_matrix.tolist(), 0, adj_matrix.shape[1] - 1)

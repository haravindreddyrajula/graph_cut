
from image import image
import Matrix
import Util
import numpy as np


class main:

    def __init__(self, row, col, patchdim):
        self.m = row
        self.n = col
        self.patch = patchdim
        self.myOverlap = self.patch // 6
        self.res = None
        self.node_matrix = None
        self.counter = 0
        # Util().createdirs()

    def start(self, s):
        print(s)

    # reading image and passing to quilt func
    def run(self, path):
        self.quilting(image().readimage(path))

    def check_position(self, pos_one, pos_two, cut):

        x1, y1 = pos_one
        x2, y2 = pos_two

        if cut == "leftright_merge":
            return False if x1 != x2 else True
        else:
            return False if y1 != y2 else True

    def final_overlap(self, algo_output, cut, overlap, other_overlap, node_matrix_map):

        top_overlap = overlap
        bottom_overlap = other_overlap
        for cut in enumerate(algo_output):
            pos = cut[1].split("-")
            pos_map = node_matrix_map[int(pos[0])]
            if self.check_position(pos_map, node_matrix_map[int(pos[1])], cut):

                x1, y1 = pos_map
                if cut == "leftright_merge":
                    other_overlap[x1, :y1+1] = overlap[x1, :y1 + 1]
                else:
                    bottom_overlap[:x1+1, y1] = top_overlap[:x1+1, y1]

        if cut == "leftright_merge":
            return other_overlap
        else:
            return bottom_overlap

    # computes the overlap regions for the resultant and sample patch and performs the graph cut
    # using the graph cut output, final pixels are decided in overlap
    def minCutPatch(self, bestpatch, y, x):
        bestpatch = bestpatch.copy()
        dy, dx, _ = bestpatch.shape

        # filling the tiles of first row
        if y == 0:
            left = self.res[:self.patch, x:x+self.patch]
            right = bestpatch

            self.res[:self.patch, x+self.myOverlap:x+self.patch] = bestpatch[:,
                                                                             self.myOverlap:]  # 0-17 20:37 Plotted Correctly

            overlap = left[:, self.patch - self.myOverlap:self.patch]
            other_overlap = right[:, :self.myOverlap]

            self.node_matrix = np.zeros(
                [overlap.shape[0], overlap.shape[1]], dtype=int)
            count = 1
            for i in range(overlap.shape[1]):
                for j in range(overlap.shape[0]):
                    self.node_matrix[j][i] = count
                    count = count + 1

            node_matrix_map = {}

            for i in range(self.node_matrix.shape[0]):
                for j in range(self.node_matrix.shape[1]):
                    pos = (i, j)
                    val = self.node_matrix[i][j]
                    node_matrix_map[val] = pos

            algo_output = Matrix.calGraph(self.node_matrix,
                                          overlap.shape[0]*overlap.shape[1], overlap, other_overlap, "leftright_merge")

            Util.writealgooutputfile(algo_output)
            last_overlap = self.final_overlap(
                algo_output, "leftright_merge", overlap, other_overlap, node_matrix_map)

            self.seam_find(
                algo_output, "leftright_merge", overlap, other_overlap, node_matrix_map)
            # saving final patch
            self.res[:self.patch, x:x +
                     self.myOverlap] = last_overlap[:, :]

            image().plotting(self.res)

        # filling the first column tiles
        elif x == 0:
            top_overlap = self.res[self.patch -
                                   self.myOverlap:self.patch, :self.patch]
            bottom_overlap = bestpatch[:self.myOverlap, :]

            self.res[y+self.myOverlap:y+self.patch,
                     :self.patch] = bestpatch[self.myOverlap:, :]

            self.node_matrix = np.zeros(
                [top_overlap.shape[0], top_overlap.shape[1]], dtype=int)
            count = 1
            for i in range(top_overlap.shape[1]):
                for j in range(top_overlap.shape[0]):
                    self.node_matrix[j][i] = count
                    count = count + 1

            node_matrix_map = {}

            for i in range(self.node_matrix.shape[0]):
                for j in range(self.node_matrix.shape[1]):
                    pos = (i, j)
                    val = self.node_matrix[i][j]
                    node_matrix_map[val] = pos

            algo_output = Matrix.calGraph(self.node_matrix,
                                          top_overlap.shape[0] * top_overlap.shape[1], top_overlap, bottom_overlap, "topdown_merge")
            Util.writealgooutputfile(algo_output)
            last_overlap = self.final_overlap(
                algo_output, "topdown_merge", top_overlap, bottom_overlap, node_matrix_map)

            self.seam_find(
                algo_output, "topdown_merge", top_overlap, bottom_overlap, node_matrix_map)

            # self.res[:patchLength, x:x + overlap:] = final_overlap_patch[:, :]
            # merging final overlap with result
            self.res[y:y + self.myOverlap:,
                     :self.patch] = last_overlap[:, :]

            image().plotting(self.res)

        else:
            # filling the middle tiles
            left = self.res[y:y+self.patch, x:x + self.patch]
            right = bestpatch

            overlap = left[:, self.patch - self.myOverlap:self.patch]
            other_overlap = right[:, :self.myOverlap]

            self.node_matrix = np.zeros(
                [overlap.shape[0], overlap.shape[1]], dtype=int)
            count = 1
            for i in range(overlap.shape[1]):
                for j in range(overlap.shape[0]):
                    self.node_matrix[j][i] = count
                    count = count + 1

            node_matrix_map = {}

            for i in range(self.node_matrix.shape[0]):
                for j in range(self.node_matrix.shape[1]):
                    pos = (i, j)
                    val = self.node_matrix[i][j]
                    node_matrix_map[val] = pos

            algo_output = Matrix.calGraph(self.node_matrix,
                                          overlap.shape[0] * overlap.shape[1], overlap, other_overlap, "leftright_merge")

            Util.writealgooutputfile(algo_output)
            last_overlap = self.final_overlap(
                algo_output, "leftright_merge", overlap, other_overlap, node_matrix_map)

            self.seam_find(
                algo_output, "leftright_merge", overlap, other_overlap, node_matrix_map)

           # merging final overlap with result
            self.res[y:y+self.patch, x:x +
                     self.myOverlap] = last_overlap[:, :]

            # # Do horizontal for reduced length
            # top_overlap = self.res[y+self.patch -
            #                        self.myOverlap:y+self.patch, x:x+self.patch]
            # bottom_overlap = bestpatch[:self.myOverlap, :]

            # # First Fill The Non Overlapping part
            # self.res[y + self.myOverlap:y + self.patch,
            #          x:x+self.patch] = bestpatch[self.myOverlap:, :]

            self.res[y + self.myOverlap:y+self.patch, x+self.myOverlap:x +
                     self.patch] = bestpatch[self.myOverlap:, self.myOverlap:]

            image().plotting(self.res)

        # np.copyto(patch, self.res[y:y + dy, x:x + dx])

        return bestpatch

    def selectBestPatch(self, image, y, x):

        errors = np.zeros(
            (image.shape[0] - self.patch, image.shape[1] - self.patch))

        for i in range(image.shape[0] - self.patch):
            for j in range(image.shape[1] - self.patch):
                portion = image[i:i + self.patch, j:j + self.patch]

                error = 0
                if x > 0:
                    leftPortion = portion[:, :self.myOverlap] - \
                        self.res[y:y + self.patch, x:x + self.myOverlap]
                    error += np.sum(leftPortion ** 2)

                if y > 0:
                    abovePortion = portion[:self.myOverlap, :] - \
                        self.res[y:y + self.myOverlap, x:x + self.patch]
                    error += np.sum(abovePortion ** 2)

                if x > 0 and y > 0:
                    cornerPortion = portion[:self.myOverlap, :self.myOverlap] - \
                        self.res[y:y + self.myOverlap, x:x + self.myOverlap]
                    error -= np.sum(cornerPortion ** 2)

                errors[i, j] = error

        i, j = np.unravel_index(np.argmin(errors), errors.shape)
        return image[i:i + self.patch, j:j + self.patch]

    def seam_find(self, algo_output, cut, overlap, other_overlap, node_matrix_map):
        temp1 = overlap.copy()
        temp2 = other_overlap.copy()
        temp1[:, :] = [1, 1, 0]
        temp2[:, :] = [0, 1, 1]

        top_overlap = temp1
        bottom_overlap = temp2

        for cut in enumerate(algo_output):
            pos = cut[1].split("-")
            pos_map = node_matrix_map[int(pos[0])]
            if self.check_position(pos_map, node_matrix_map[int(pos[1])], cut):

                x1, y1 = pos_map
                if cut == "leftright_merge":
                    temp2[x1, :y1+1] = temp1[x1, :y1 + 1]
                else:
                    bottom_overlap[:x1+1, y1] = top_overlap[:x1+1, y1]

        if cut == "leftright_merge":
            image().savingimg(temp2, self.counter)
            self.counter += 1

        else:
            image().savingimg(bottom_overlap, self.counter)
            self.counter += 1

    def selectPatch(self, image):
        l, b, _ = image.shape
        i = np.random.randint(l - self.patch)
        j = np.random.randint(b - self.patch)

        return image[i:i + self.patch, j:j + self.patch]

    # main block to process image and computing indexes for sample patches in outputs
    # using the index it gets random best patches and performs the grpah cut
    def quilting(self, image):

        self.res = np.zeros(
            ((self.m * self.patch) - (self.m - 1) * self.myOverlap,
             (self.n * self.patch) - (self.n - 1) * self.myOverlap,
             image.shape[2]))

        for i in range(self.m):
            for j in range(self.n):
                # Row index in final tile
                y = i * (self.patch - self.myOverlap)
                # Column index in final tile
                x = j * (self.patch - self.myOverlap)

                if i == 0 and j == 0:
                    self.res[y:y + self.patch,
                             x:x + self.patch] = self.selectPatch(image)
                else:
                    self.minCutPatch(
                        self.selectBestPatch(image, y, x), y, x)

        return self.res


if __name__ == "__main__":
    # arguments are no.of tiles (rows*column) and sample patch dimension
    main = main(3, 3, 20)
    # main.start('hello')

    main.run("test.png")

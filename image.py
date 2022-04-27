import cv2 as cv2
import matplotlib.pyplot as plt
import os


class image:
    def __init__(self):
        self.img = None

    # plot func
    def plotting(self, data):
        plt.imshow(data)
        plt.show()

    # save func
    def savingimg(self, data, counter):
        # cv2.imwrite(str(counter)+"_seam.png", data)
        plt.imshow(data)
        # plt.show()
        # os.mkdir()
        plt.savefig(str(counter)+"_seam.png")

    # redaing image and making it to float values of RBG
    def readimage(self, path):
        # Read RGB image
        #self.img = cv2.imread(path, cv2.IMREAD_COLOR)
        self.img = cv2.imread(path)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB) / 255.0

        # Output img with window name as 'image'
        # cv2.imshow("test", self.img)
        # cv2.waitKey(0)

        # Printing the RGB Values
        # print(img)

        # finding the dimensions
        self.plotting(self.img)

        # (height, width) = self.img.shape[:2]
        # print(height)
        # print(width)

        return self.img

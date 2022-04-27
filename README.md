# Graph-cut

`Graph-cut` has the implementation of quilting of a image. the approach followed is taking an random patch of a given image and overlapping the pixels partially with the new or already existing pixels. usually the overlapping region is determined initially by the block size. For example, the implementation is on 3x3 and taken a 20 patch dimension for the test image i have taken. But to determine which pixels to be considered for overlap is possible by the graph which created and generated the weights using algorithm. Based on this grpah cut output we get the idea of which pixels should be considered for final patch.

## Installing

The depedencies you require are :

1. Python environment
2. packages/libraries such as numpy, os, cv2, matplotlib
3. One can use `pip install` to have those libraries in your env.

## Usage

`Graph-cut` can be run by running the `main.py` file. You can run either by double clicking or running through CLI.

Once you run the main.py file it will take the default entries and default image. you should always close the pop up images to get to next step. the pop up images are nothing but step by step image quilting.

You can see the patch allignment step by step on the screen. As given in the project requirement seam cut images stored as well as adjacency matrix in the file format.

## References:

```
https://github.com/axu2/image-quilting
https://people.eecs.berkeley.edu/~efros/research/quilting/quilting.pdf
https://www.geeksforgeeks.org/minimum-cut-in-a-directed-graph/?ref=lbp
```

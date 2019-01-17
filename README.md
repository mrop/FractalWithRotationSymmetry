# Fractal With Rotation Symmetry

The fractal is build using the following formula's. Each imaginary number corresponts to a point in a two dimensional plane. 
The color is determined using a histogram of the distribution.




![img](http://latex.codecogs.com/svg.latex?f%28x%29%20%3D%20%28%5Calpha%5Ccdot%20x%20%5Ccdot%20%5Coverline%20x%20%2B%20%5Cbeta%20%5Ccdot%20%5Coperatorname%7BRe%7D%28x%5Em%29%20%2B%20%5Clambda%20%29%20%5Ccdot%20x%20%2B%20%5Cgamma%20%5Ccdot%20%5Coverline%20x%5E%7Bm-1%7D)

![img](http://latex.codecogs.com/svg.latex?f%28x_i%29%3Df%28x_%7Bi-1%7D%29)

# Usage

Usage: python Icon --config==[FILENAME]
Construct an icon 2D mapping based on the parameters in [FILENAME]
Example: python Icon -c exampleA.cfg -v

  -v, --verbose             		display progress
  -h, --help                		display this message
  -c [FILENAME], --config=[FILENAME]	read configuration parameters from [FILENAME]

  [FILENAME] is the absolute path of the config file

Report bugs to <mrop@xs4all.nl>

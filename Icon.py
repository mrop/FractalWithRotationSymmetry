import numpy
from numpy import zeros
from numpy import add
from numpy import array
from PIL import Image
import ConfigParser
import getopt
import sys
import os
import math

class Icon():
	"""The parameters and function to produce a icon"""
	def __init__(self, alpha, beta, gamma, lmbd, m):
		self.alpha = alpha
		self.beta = beta
		self.gamma = gamma
		self.lmbd = lmbd
		self.m = m


	def p(self,x):
        	return self.alpha * x * x.conjugate() + self.beta*((x**self.m).real) + self.lmbd
        
        def f(self,x):
        	return self.p(x)*x+self.gamma*(x.conjugate()**(self.m-1))

class IconMapping():
	def __init__(self, spaceStep, start, min, max, numberOfIterations, startIteration, verbose):
		self.spaceStep = spaceStep
		self.start = start
		self.min = min
		self.max = max
		self.numberOfIterations = numberOfIterations
		self.startIteration = startIteration
		self.verbose = verbose
        	self.size = (max - min)/spaceStep
        	self.matrix= zeros((self.size.real,self.size.imag),dtype=int)
        
        def construct(self,icon):
        	z = self.start
                i=0
		matrix = self.matrix
                while i<self.numberOfIterations:
			z_old = z
                	try:
                		z = icon.f(z)
                	except (ValueError, OverflowError):
                		print "ERROR: Divergent solution - exiting"
				return False
			if z.real!=z.real or z.imag!=z.imag:
				print "ERROR: Divergent solution - exiting"
				return False
			
                	zrel = z - self.min
			zrel_old = z_old - self.min
                	if i%10000==0 and self.verbose:
                		print str(i)+","+str(z)
			if i>self.startIteration:
        			c = zrel/self.spaceStep
				c_old = zrel_old/self.spaceStep
				diff = c - c_old
				if  round(diff.real,8)==0 and round(diff.imag,8)==0:
					print "WARNING: changing in attracter not mappable in current scale"
					return False
				if c.real < 0 or c.real > self.size.real or c.imag<0 or c.imag > self.size.imag:
					if self.verbose:
                				print "WARNING: attractor lies outside extends ("+str(z)+")"
					return False
                		else:
                			self.matrix[c.real,c.imag]=self.matrix[c.real,c.imag] + 1
                	i = i + 1
		return True	

class ColorMapping():
	def __init__(self, from_color, to_color, fileName):
		self.from_color = numpy.array(HTMLColorToRGB(from_color),dtype=int)
		self.to_color = numpy.array(HTMLColorToRGB(to_color),dtype=int)
		self.fileName = fileName
		self.color_range = numpy.array(self.to_color)-numpy.array(self.from_color) 


	def color(self,x):
		ratio = self.totalNumberOfCellsHit[x]/float(self.maxTotalNumberOfCellsHit)
		rgb = array(ratio *  self.color_range + self.from_color,dtype=int)
		return (rgb[0],rgb[1],rgb[2])
		
		
	def construct(self, iconMapping):
		matrix = iconMapping.matrix
		max_n = matrix.max()
		numberOfCellsHit = zeros(max_n+1)
		for a in matrix:
			numberOfCellsHit[a] = numberOfCellsHit[a]+1
		self.totalNumberOfCellsHit = add.accumulate(numberOfCellsHit)
		self.maxTotalNumberOfCellsHit = self.totalNumberOfCellsHit.max()
		image = Image.new("RGB",(matrix.shape[0],matrix.shape[1]))
		for ny in range(matrix.shape[0]):
			for nx in range(matrix.shape[1]):
				image.putpixel((nx,ny),self.color(matrix[nx,ny]))
		image.save(self.fileName)
		


def main():
	"""read command line options and construct icon 2D mapping bases on the parameters"""
	try: 
		opts, args = getopt.getopt(sys.argv[1:],"hc:v",["help","config="])
	except getopt.GetoptError, err:
		print str(err)
		usage()
		sys.exit(2)
	output = None
	verbose = False
	fileName = None
	for o, a in opts:
		if o == "-v":
			verbose = True
		elif o in ("-h","--help"):
			usage()
			sys.exit()
		elif o in ("-c","--config"):
			fileName = a
	if fileName == None:
		usage()
		sys.exit(2)
	config = ConfigParser.ConfigParser()
	if verbose:
		print "using " + fileName + " as config file"

	filepath = os.path.abspath(fileName)
	file = config.read(filepath)
	if len(file)==0:
		usage()
		sys.exit(2)
	icon, iconMapping, colorMapping = processConfig(config,verbose)
	if iconMapping.construct(icon):
		colorMapping.construct(iconMapping)

def HTMLColorToRGB(colorstring):
	""" convert #RRGGBB to an (R, G, B) tuple """
	colorstring = colorstring.strip()
	if colorstring[0] == '#': colorstring = colorstring[1:]
	if len(colorstring) != 6:
		raise ValueError, "input #%s is not in #RRGGBB format" % colorstring
	r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
	r, g, b = [int(n, 16) for n in (r, g, b)]
	return (r,g,b)

def processConfig(config,verbose):
	""" read config file and construct icon, iconMapping and colorMapping instances"""
	""" return icon, iconMapping and colorMapping"""
	alpha = float(config.get('Parameters','alpha'))
        beta = float(config.get('Parameters','beta'))
	alpha = float(config.get('Parameters','alpha'))
        beta = float(config.get('Parameters','beta'))
        gamma =  float(config.get('Parameters','gamma'))
        lmbd = float(config.get('Parameters','lambda'))
        m = float(config.get('Parameters','m'))
        spaceStep = float(config.get('Dimensions','scale'))
	real = float(config.get('Construction','start.real'))
	imag = float(config.get('Construction','start.imag'))
	start= complex(real,imag)
	real = float(config.get('Dimensions','min.real'))
	imag = float(config.get('Dimensions','min.real'))
	min = complex(real,imag)
	real = float(config.get('Dimensions','max.real'))
	imag = float(config.get('Dimensions','max.imag'))
	max = complex(real,imag)
	numberOfIterations = float(config.get('Construction','numberOfIterations'))
	startIteration = float(config.get('Construction','startIteration'))
	fileName = config.get('Files','picture.filename')
	from_color = config.get('Colors','from')
	to_color = config.get('Colors','to')
	icon = Icon(alpha,beta,gamma,lmbd,m)
	iconMapping = IconMapping(spaceStep, start, min, max, numberOfIterations, startIteration,verbose)
	colorMapping = ColorMapping(from_color,to_color,fileName)
	return icon, iconMapping, colorMapping


	
def usage():
	"""print help"""
	print """Usage: python Icon --config==[FILENAME]
Construct an icon 2D mapping based on the parameters in [FILENAME]
Example: python Icon -c exampleA.cfg -v

  -v, --verbose             		display progress
  -h, --help                		display this message
  -c [FILENAME], --config=[FILENAME]	read configuration parameters from [FILENAME]

  [FILENAME] is the absolute path of the config file

Report bugs to <mrop@xs4all.nl>
"""

if __name__ == "__main__":
	main()

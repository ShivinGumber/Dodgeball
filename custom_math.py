"""
Equation: a1*x1+a2*x2+......an*xn=b
Given n equations,
they are solved by the following recursive method
the following set of equations
a1*X11+a2*X12+......an*X1n=b1
a1*X21+a2*X22+......an*X2n=b2
.
.
.
an*Xn1+a2*Xn2+......an*Xnn=bn

becomes,

a2(X22-X12*X21/X11)+a3(X23-X13*X21/X11)+......an(X2n-X1n*X21/X11)=b2-b1*X21/X11
a2(X32-X12*X31/X11)+a3(X33-X13*X31/X11)+......an(X3n-X1n*X31/X11)=b3-b1*X31/X11
.
.
.
a2(Xn2-X12*Xn1/X11)+a3(Xn3-X13*Xn1/X11)+......an(Xnn-X1n*Xn1/X11)=b2-b1*Xn1/X11
"""
import math


class equation:
	def __init__(self, coefficients, value):
		self.coefficients = coefficients
		self.value = value


def solve_equations(equations):#Recursively solve points to get an equation for the surface created
	if equations[0].coefficients[0] == 0:
		if len(equations) == 1:
			return [equations[0].value]
		else:
			coefficients = [[equations[i].coefficients[j]-equations[0].coefficients[j]*equations[i].coefficients[0] for j in range(1, len(equations[0].coefficients))] for i in range(1, len(equations))]
			value = [equations[i].value-equations[0].value*equations[i].coefficients[0] for i in range(1, len(equations))]
			variables = solve_equations([equation(coefficients[i], value[i]) for i in range(len(equations)-1)])
			a0 = equations[0].value
			for i in range(1, len(equations[0].coefficients)):
				a0 -= variables[i-1]*equations[0].coefficients[i]
			return [a0]+variables
	else:
		if len(equations) == 1:
			return [equations[0].value/equations[0].coefficients[0]]
		else:
			coefficients = [[equations[i].coefficients[j]-equations[0].coefficients[j]*equations[i].coefficients[0]/equations[0].coefficients[0] for j in range(1, len(equations[0].coefficients))] for i in range(1, len(equations))]
			value = [equations[i].value-equations[0].value*equations[i].coefficients[0]/equations[0].coefficients[0] for i in range(1, len(equations))]
			variables = solve_equations([equation(coefficients[i], value[i]) for i in range(len(equations)-1)])
			a0 = equations[0].value
			for i in range(1, len(equations[0].coefficients)):
				a0 -= variables[i-1]*equations[0].coefficients[i]
			a0 /= equations[0].coefficients[0]
			return [a0]+variables


def normal_from_surface(point, surface):#Get equation of the normal of a surface
	den = 0
	for i in range(len(point)):
		den += surface.coefficients[i]*surface.coefficients[i]
	den = math.sqrt(den)
	num = -surface.value
	for i in range(len(point)):
		num += surface.coefficients[i]*point[i]
	return abs(num/den)


def Cos(A, B):#Cosine of angle between two vectors
	num = 0
	for i in range(len(A)):
		num += A[i]*B[i]
	den1 = 0
	for i in A:
		den1 += i*i
	den1 = math.sqrt(den1)
	den2 = 0
	for i in B:
		den2 += i*i
	den2 = math.sqrt(den2)
	return (num/den1)/den2


def Magnitude(A):#Magnitude of a vector
	mag = 0
	for i in A:
		mag += i*i
	mag = math.sqrt(mag)
	return mag

def dist(PointA,PointB):#Calculate distance between points
	dist=0
	for i in range(len(PointA)):
		dist+=(PointA[i]-PointB[i])*(PointA[i]-PointB[i])
	return math.sqrt(dist)

def value_at(point,obj):#Calculate values of a point with respect to an equation
	ans=-obj.value
	for i in range(len(obj.coefficients)):
		ans+=obj.coefficients[i]*point[i]
	return ans;

def In_Surface(point,surface):#Checks if a point is on the same side of all boundries as the centre of the surface
	cross_section_point=[]
	if(surface.use_perspective2):
		cross_section_point=point[1:]
		for i in range(len(surface.boundry_list_perspective2)):
			Point_Parity=value_at(cross_section_point,surface.boundry_list_perspective2[i])
			if(Point_Parity<0 and surface.Centre_Parity[i]>0):
				return False
			if(Point_Parity>0 and surface.Centre_Parity[i]<0):
				return False
	else:
		cross_section_point=point[:-1]
		for i in range(len(surface.boundry_list_perspective1)):
			Point_Parity=value_at(cross_section_point,surface.boundry_list_perspective1[i])
			if(Point_Parity<0 and surface.Centre_Parity[i]>0):
				return False
			if(Point_Parity>0 and surface.Centre_Parity[i]<0):
				return False
	return True

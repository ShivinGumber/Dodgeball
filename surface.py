"""
Each surface is a1*x1+a2*x2+.......=b
The way this is achieved is n n-dimensional points are given and checked which surface which surface passes through it.
Let the points be P1,P2,......Pn
Pm=(Xm1,Xm2,......,Xmn)
a1*X11+a2*X12+......an*X1n=30
a1*X21+a2*X22+......an*X2n=30
.
.
.
an*Xn1+a2*Xn2+......an*Xnn=30
Here, 30 is chosen as am will scale according to it and 30=2*3*5
The above mentioned equations are solved to get a1,a2,......an
"""
import custom_math as m2

class Boundry:
	def __init__(self, points, dimension):
		coefficients = []
		values = []
		self.points = points
		for i in range(dimension):
			coefficients.append([points[i][j] for j in range(dimension)])
			values.append(30)
		self.coefficients = m2.solve_equations([m2.equation(coefficients[i], values[i]) for i in range(dimension)])
		self.value = 30

class Surface:
	def __init__(self, points, dimension, material=0):
		coefficients = []
		values = []
		self.points = points
		for i in range(dimension):
			coefficients.append([points[i][j] for j in range(dimension)])
			values.append(30)
		self.coefficients = m2.solve_equations([m2.equation(coefficients[i], values[i]) for i in range(dimension)])
		self.value = 30
		
		boundry_points=[i[:-1] for i in points]
		boundry_list_perspective1=[]
		for i in range(len(boundry_points)):
			boundry_list_perspective1.append(Boundry(boundry_points[:i]+boundry_points[i+1:],dimension-1))
		
		boundry_points=[i[1:] for i in points]
		boundry_list_perspective2=[]
		for i in range(len(boundry_points)):
			boundry_list_perspective2.append(Boundry(boundry_points[:i]+boundry_points[i+1:],dimension-1))
		
		centre=[0 for i in points[0]]
		for i in points:
			for j in range(len(i)):
				centre[j]+=i[j]
		for i in range(len(points[0])):
			centre[i]/=len(points)
		self.centre=centre
		self.boundry_list_perspective1=boundry_list_perspective1
		self.boundry_list_perspective2=boundry_list_perspective2
		
		self.Centre_Parity=[];
		self.use_perspective2=True
		for i in boundry_list_perspective1:
			self.Centre_Parity.append(m2.value_at(centre[:-1],i));
			if(not self.Centre_Parity[-1]<=10**(-6)):
				self.use_perspective2=False
		if(self.use_perspective2):
			self.Centre_Parity=[]
			for i in boundry_list_perspective2:
				self.Centre_Parity.append(m2.value_at(centre[1:],i))
		
		self.material=material

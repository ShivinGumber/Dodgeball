"""
0.0:	target_mass
0.1:	target_charge
0.2.x:	target_coordinate
0.3.x:	target_axial_velocity
1.0:	source_mass
1.1:	source_charge
1.2.x:	source_coordinate
1.3.x:	source_axial_velocity
"""
import math
import custom_math as m2


class newtonian_physics_model:

	def __init__(self, dimensions=2, point_ground_gravity=9.81, Gravitational_Constant=6.6743e-11,
				 Vacuum_Electric_Permittivity=8.85412878128e-12, Vacuum_Magnetic_Permeability=1.25663706212e-6):

		self.dimensions = dimensions
		self.point_ground_gravity = point_ground_gravity
		self.Gravitational_Constant = Gravitational_Constant
		self.Electrostatic_Constant = 1 / (4 * math.pi * Vacuum_Electric_Permittivity)
		self.Vacuum_Electric_Permittivity = Vacuum_Electric_Permittivity
		self.Vacuum_Magnetic_Permeability = Vacuum_Magnetic_Permeability
		self.Elasticity=[
		[1,	0.5],
		[0.5,	0]]

	def Update_Kinematics(self, Radial_Object, force=[0, 0], time_step=1 / 60, values={}):#Moves the system one time_step amount of time ahead

		acceleration = []
		for i in force:
			acceleration.append(i / Radial_Object.mass)
		for i in range(len(acceleration)):
			Radial_Object.velocity[i] += acceleration[i] * time_step
			Radial_Object.position[i] += Radial_Object.velocity[i] * time_step

	def Get_Gravity(self):#Gives equation of gravity for the desried dimensions using the hypothetical systemm of gravitons
		def den(values):
			target_coordinate = [values["0.2." + str(i)] for i in range(self.dimensions)]
			source_coordinate = [values["1.2." + str(i)] for i in range(self.dimensions)]
			sum = 0
			for i in range(self.dimensions):
				sum += (target_coordinate[i] - source_coordinate[i]) ** 2;
			return sum;

		return [(lambda values: self.Gravitational_Constant * values["0.0"] * values["1.0"] * (
					values["1.2." + str(i)] - values["0.2." + str(i)]) / (den(values) ** (self.dimensions / 2))) for i
				in range(self.dimensions)]

	def Get_Electrostatic_Force(self):#Gives equation of gravity for the desired dimensions
		def den(values):
			target_coordinate = [vaules["0.2." + str(i)] for i in range(self.dimensions)]
			source_coordinate = [vaules["1.2." + str(i)] for i in range(self.dimensions)]
			sum = 0
			for i in range(self.dimensions):
				sum += (target_coordinate[i] - source_coordinate[i]) ** 2;
			return sum;

		return [(lambda values: self.Electrostatic_Constant * values["0.1"] * values["1.1"] * (
					values["0.2." + str(i)] - values["1.2." + str(i)]) / (den(values) ** (self.dimensions / 2))) for i
				in range(self.dimensions)]

	def Equate_Electrostatic_Potential(self, obj1, obj2):#Used to transfer charge between conductive bodies
		if (obj1.conductivity and obj2.conductivity):
			Charge_Transferred = 0
			if (self.dimensions == 2):
				log1 = math.log(obj1.radius)
				log2 = math.log(obj2.radius)
				Charge_Transferred = (obj1.charge * log1 - obj2.charge * log2) / (log1 + log2)
			else:
				Charge_Transferred = (obj1.charge * (obj2.radius ** (1 - self.dimensions)) - obj2.charge * (
							obj1.radius ** (1 - self.dimensions))) / (
												 obj1.radius ** (1 - self.dimensions) + obj2.radius ** (
													 1 - self.dimensions))
			obj1.charge -= Charge_Transferred
			obj2.charge += Charge + Transferred

	def Surface_Collision(self, Radial_Object_List, Surface_List, time_step=1 / 60):#Account for radial object  collision with surfaces
		for i in Surface_List:
			Magnitude_of_Coeff = m2.Magnitude(i.coefficients)
			Unit_Vector_Along_Normal = [j / Magnitude_of_Coeff for j in i.coefficients]
			for j in Radial_Object_List:
				Magnitude_of_Normal=m2.normal_from_surface(j.position, i)
				if (j.radius >= Magnitude_of_Normal):
					Base_of_Normal=[]
					if(m2.value_at(j.position,i)>0):
						Base_of_Normal=[j.position[i]-Magnitude_of_Normal*Unit_Vector_Along_Normal[i] for i in range(len(Unit_Vector_Along_Normal))]
					else:
						Base_of_Normal=[j.position[i]+Magnitude_of_Normal*Unit_Vector_Along_Normal[i] for i in range(len(Unit_Vector_Along_Normal))]
					if(m2.In_Surface(Base_of_Normal,i)):
						Cos = m2.Cos(j.velocity, i.coefficients)
						Speed_Along_Normal = m2.Magnitude(j.velocity) * Cos
						Velocity_Along_Normal = [Speed_Along_Normal * k for k in Unit_Vector_Along_Normal]
						Velocity_Along_Surface = [j.velocity[k] - Velocity_Along_Normal[k] for k in range(len(j.velocity))]
						j.position = [j.position[k] - Velocity_Along_Normal[k] * time_step for k in range(len(j.velocity))]
						j.velocity = [Velocity_Along_Surface[k] - self.Elasticity[i.material][j.material]*Velocity_Along_Normal[k] for k in range(len(j.velocity))]
					else:
						collide=False
						for k in range(len(i.boundry_list_perspective1)):
							dist = math.sqrt( m2.normal_from_surface(j.position[:-1],i.boundry_list_perspective1[k])**2 + m2.normal_from_surface(j.position[1:],i.boundry_list_perspective2[k])**2 )
							if(dist<=j.radius):
								collide=True
								break
						if(collide):
							Normal_Along_Boundry=[j.position[k]-i.centre[k] for k in range(len(i.centre))]
							Cos=m2.Cos(j.velocity,Normal_Along_Boundry)
							Speed_Along_Normal = m2.Magnitude(j.velocity) * Cos
							Magnitude_of_Normal = m2.Magnitude(Normal_Along_Boundry)
							Unit_Vector_Along_Boundry_Normal = [k/Magnitude_of_Normal for k in Normal_Along_Boundry]
							Velocity_Along_Normal = [Speed_Along_Normal * k for k in Unit_Vector_Along_Boundry_Normal]
							Velocity_Along_Surface = [j.velocity[k] - Velocity_Along_Normal[k] for k in range(len(j.velocity))]
							j.position = [j.position[k] - Velocity_Along_Normal[k] * time_step for k in range(len(j.velocity))]
							j.velocity = [Velocity_Along_Surface[k] - self.Elasticity[i.material][j.material]*Velocity_Along_Normal[k] for k in range(len(j.velocity))]
	
	def Radial_Object_Collision(self, Radial_Object_List,time_step=1/60):#Account for collision between radial objects
		player_hit=False
		object_collision=False
		for i in range(len(Radial_Object_List)):
			for j in range(i+1,len(Radial_Object_List)):
				if(m2.dist(Radial_Object_List[i].position,Radial_Object_List[j].position)<Radial_Object_List[i].radius+Radial_Object_List[j].radius):
					if(i==0):
						player_hit=True
					object_collision=True
					
					Normal=[Radial_Object_List[j].position[k]-Radial_Object_List[i].position[k] for k in range(len(Radial_Object_List[0].position))]
					Magnitude_of_Coeff=m2.Magnitude(Normal)
					Unit_Vector_Along_Normal=[k/Magnitude_of_Coeff for k in Normal]
					
					Cosi=m2.Cos(Radial_Object_List[i].velocity,Normal)
					Mag_Vin1=m2.Magnitude(Radial_Object_List[i].velocity)*Cosi
					Vin1=[k*Mag_Vin1 for k in Unit_Vector_Along_Normal]
					Vip=[Radial_Object_List[i].velocity[k]-Vin1[k] for k in range(len(Vin1))]
					
					Cosj=m2.Cos(Radial_Object_List[j].velocity,Normal)
					Mag_Vjn1=m2.Magnitude(Radial_Object_List[j].velocity)*Cosj
					Vjn1=[k*Mag_Vjn1 for k in Unit_Vector_Along_Normal]
					Vjp=[Radial_Object_List[j].velocity[k]-Vjn1[k] for k in range(len(Vin1))]
					
					e=self.Elasticity[Radial_Object_List[i].material][Radial_Object_List[j].material]
					Vi0r=[Vin1[k]-Vjn1[k] for k in range(len(Vin1))]
					mult_fact=(Radial_Object_List[i].mass-e*Radial_Object_List[j].mass)/(Radial_Object_List[i].mass+Radial_Object_List[j].mass)
					Vi1r=[mult_fact*k for k in Vi0r]
					mult_fact=(Radial_Object_List[i].mass)*(1+e)/(Radial_Object_List[i].mass+Radial_Object_List[j].mass)
					Vj1r=[mult_fact*k for k in Vi0r]
					
					Radial_Object_List[i].velocity=[Vip[k]+Vjn1[k]+Vi1r[k] for k in range(len(Vi1r))]
					Radial_Object_List[j].velocity=[Vjp[k]+Vjn1[k]+Vj1r[k] for k in range(len(Vj1r))]
					Radial_Object_List[i].position = [Radial_Object_List[i].position[k] + Radial_Object_List[i].velocity[k] * time_step for k in range(len(Radial_Object_List[i].velocity))]
					Radial_Object_List[j].position = [Radial_Object_List[j].position[k] + Radial_Object_List[j].velocity[k] * time_step for k in range(len(Radial_Object_List[j].velocity))]
		return (player_hit,object_collision)

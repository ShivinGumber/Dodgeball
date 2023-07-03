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
import pygame
import Radial_Object as RO
import surface as SU
import physics as phy
import custom_math as m2
import math
import random

pygame.init()
pygame.mixer.music.load("Collide.wav")
infoObject = pygame.display.Info()
pygame.display.set_caption("Dodgeball by Phang")
screen = pygame.display.set_mode((infoObject.current_w, int(infoObject.current_w/2)))
clock = pygame.time.Clock()
width = infoObject.current_w
height = infoObject.current_w/2
font = pygame.font.Font('freesansbold.ttf', (32*width)//1920)
highscore_file = open("Data.txt","r")
highscore=int(highscore_file.readline())
render_time_step=float(highscore_file.readline())

def make_triangle(centre):#places a randomly oriented traingle at the given point
	Thita=random.random()*2*math.pi
	point1=[centre[0]+40*(width/1920)*math.sin(Thita), centre[1]+40*(width/1920)*math.cos(Thita)]
	point2=[centre[0]+40*(width/1920)*math.sin(2*math.pi/3+Thita), centre[1]+40*(width/1920)*math.cos(2*math.pi/3+Thita)]
	point3=[centre[0]+40*(width/1920)*math.sin(4*math.pi/3+Thita), centre[1]+40*(width/1920)*math.cos(4*math.pi/3+Thita)]
	next_surface_list=[]
	next_surface_list.append(SU.Surface([point1, point2], 2))
	next_surface_list.append(SU.Surface([point2, point3], 2))
	next_surface_list.append(SU.Surface([point3, point1], 2))
	return next_surface_list

Physics_Model_List = [phy.newtonian_physics_model()]
Gravity_List = [Physics_Model_List[i].Get_Gravity() for i in range(len(Physics_Model_List))]
	
def main_menu(highscore,render_time_step):
	running=True
	user_text=""
	entering=False
	while(running):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running=False
			if event.type == pygame.KEYDOWN and entering:#Keyboard input system
				if event.key == pygame.K_BACKSPACE and len(user_text)>0:
					user_text = user_text[:-1]
				elif(event.key==pygame.K_RETURN):
					render_time_step=1/int(user_text)
					highscore_file = open("Data.txt","w")
					highscore_file.write(str(highscore)+" \n")
					highscore_file.write(str(render_time_step)+" \n")
					entering=False
				elif(event.unicode<='9' and event.unicode>='0'):
					user_text += event.unicode
		screen.fill((0, 0, 0))
		text = font.render("Main Menu", True, (255,0,255))
		screen.blit(text, (width/2-text.get_width()/2, 40))
		mouse_posx,mouse_posy=pygame.mouse.get_pos()
		LMB=pygame.mouse.get_pressed(num_buttons=3)[0]
		
		if(mouse_posx < width/2-20 and mouse_posx > 20 and mouse_posy < (height+text.get_height())/2 and mouse_posy > 60+text.get_height()):#Play button
			text = font.render("Play", True, (0,0,0))
			pygame.draw.rect(screen, (255,0,0), pygame.Rect(20, 60+text.get_height(), width/2-40, (height-40-text.get_height())/2 -40 ))
			if(LMB):
				return True,render_time_step
		else:
			text = font.render("Play", True, (255,255,255))
			pygame.draw.rect(screen, (255,0,0), pygame.Rect(20, 60+text.get_height(), width/2-40, (height-40-text.get_height())/2 -40 ),5)
		screen.blit(text, (width/4-text.get_width()/2, (40+text.get_height()+(height+40+text.get_height())/2)/2))
		
		if(mouse_posx < width/2-20 and mouse_posx > 20 and mouse_posy < height-20 and mouse_posy > (height+40+text.get_height())/2 +20):#Frame Rate adjustment button
			if(entering):
				text = font.render("Enter Frame Rate: "+user_text, True, (0,0,0))
			else:
				text = font.render("Set Frame Rate", True, (0,0,0))
			pygame.draw.rect(screen, (0,0,255), pygame.Rect(20, (height+40+text.get_height())/2 +20, width/2-40, (height-40-text.get_height())/2 -40))
			if(LMB):
				entering=True
				user_text=""
		else:
			if(entering):
				text = font.render("Enter Frame Rate: "+user_text, True, (255,255,255))
			else:
				text = font.render("Set Frame Rate", True, (255,255,255))
			pygame.draw.rect(screen, (0,0,255), pygame.Rect(20, (height+40+text.get_height())/2 +20, width/2-40, (height-40-text.get_height())/2 -40),5)
		screen.blit(text, (width/4-text.get_width()/2, (height+(height+40+text.get_height())/2)/2))
		
		if(mouse_posx > width/2+20 and mouse_posx < width-20 and mouse_posy < (height+text.get_height())/2 and mouse_posy > 60+text.get_height()):#Highscore Display
			text = font.render("Highscore: "+str(highscore), True, (0,0,0))
			pygame.draw.rect(screen, (0,255,0), pygame.Rect(width/2+20, 60+text.get_height(), width/2-40, (height-40-text.get_height())/2 -40))
		else:
			text = font.render("Highscore: "+str(highscore), True, (255,255,255))
			pygame.draw.rect(screen, (0,255,0), pygame.Rect(width/2+20, 60+text.get_height(), width/2-40, (height-40-text.get_height())/2 -40),5)
		screen.blit(text, (3*width/4-text.get_width()/2, (40+text.get_height()+(height+40+text.get_height())/2)/2))
		
		if(mouse_posx > width/2+20 and mouse_posx < width-20 and mouse_posy < height-20 and mouse_posy > (height+40+text.get_height())/2 +20):#Quit Button
			text = font.render("Quit", True, (0,0,0))
			pygame.draw.rect(screen, (255,255,255), pygame.Rect(width/2+20, (height+40+text.get_height())/2 +20, width/2-40, (height-40-text.get_height())/2 -40))
			if(LMB):
				return False,render_time_step
		else:
			text = font.render("Quit", True, (255,255,255))
			pygame.draw.rect(screen, (255,255,255), pygame.Rect(width/2+20, (height+40+text.get_height())/2 +20, width/2-40, (height-40-text.get_height())/2 -40),5)
		screen.blit(text, (3*width/4-text.get_width()/2, (height+(height+40+text.get_height())/2)/2))
		pygame.display.update()
	return False,render_time_step

play,render_time_step=main_menu(highscore,render_time_step)
while play:
	Radial_Object_List = [RO.Radial_Object([width/2, 50*(width/1920)], [0, 0], 50*22474266964325.848, 0, 10*(width/1920), False, [0,255,0])]#PLayr Creation
	Surface_List = []
	Surface_List.append(SU.Surface([[0, 0], [width-1, 0]], 2))#Map initialisation
	Surface_List.append(SU.Surface([[width/2-400*(width/1920), height/2], [width/2+400*(width/1920), height/2]], 2))
	Surface_List.append(SU.Surface([[width/2-400*(width/1920), height/2-20*(width/1920)], [width/2-400*(width/1920), height/2+20*(width/1920)]], 2))
	Surface_List.append(SU.Surface([[width/2+400*(width/1920), height/2-20*(width/1920)], [width/2+400*(width/1920), height/2+20*(width/1920)]], 2))
	Surface_List.append(SU.Surface([[width/2, height/2-200*(width/1920)], [width/2, height/2+200*(width/1920)]], 2))
	Surface_List.append(SU.Surface([[width/2-20*(width/1920), height/2-200*(width/1920)], [width/2+20*(width/1920), height/2-200*(width/1920)]], 2))
	Surface_List.append(SU.Surface([[width/2-20*(width/1920), height/2+200*(width/1920)], [width/2+20*(width/1920), height/2+200*(width/1920)]], 2))
	Surface_List.append(SU.Surface([[width-1, 0], [width-1, height-1]], 2))
	Surface_List.append(SU.Surface([[width-1, height-1], [0, height-1]], 2))
	Surface_List.append(SU.Surface([[0, 0], [0, height-1]], 2))
	running = True
	player_hit = False
	physics_prev_time=pygame.time.get_ticks()/1000
	render_prev_time=pygame.time.get_ticks()/1000
	starting_time=pygame.time.get_ticks()/1000
	while running:
		physics_time_step=pygame.time.get_ticks()/1000-physics_prev_time
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
	
		while(len(Radial_Object_List)<5+((render_prev_time-starting_time)//15) and (not player_hit)):#Spawning System
			rand=random.random()
			if(rand<0.25):
				Radial_Object_List.append(RO.Radial_Object([width/4-(200-400*random.random())*(width/1920), height/4-(100-200*random.random())*(width/1920)], [100*random.random(), 100*random.random()], 15*22474266964325.848, 0, 15*(width/1920), False, [40+215*random.random(),40+215*random.random(),40+215*random.random()]))
				Surface_List.extend(make_triangle([3*width/4-(200-400*random.random())*(width/1920), 3*height/4-(100-200*random.random())*(width/1920)]))
			elif(rand<0.5):
				Radial_Object_List.append(RO.Radial_Object([width/4-(200-400*random.random())*(width/1920), 3*height/4-(100-200*random.random())*(width/1920)], [100*random.random(), 100*random.random()], 15*22474266964325.848, 0, 15*(width/1920), False, [40+215*random.random(),40+215*random.random(),40+215*random.random()]))
				Surface_List.extend(make_triangle([3*width/4-(200-400*random.random())*(width/1920), height/4-(100-200*random.random())*(width/1920)]))
			elif(rand<0.75):
				Radial_Object_List.append(RO.Radial_Object([3*width/4-(200-400*random.random())*(width/1920), 3*height/4-(100-200*random.random())*(width/1920)], [100*random.random(), 100*random.random()], 15*22474266964325.848, 0, 15*(width/1920), False, [40+215*random.random(),40+215*random.random(),40+215*random.random()]))
				Surface_List.extend(make_triangle([width/4-(200-400*random.random())*(width/1920), height/4-(100-200*random.random())*(width/1920)]))
			else:
				Radial_Object_List.append(RO.Radial_Object([3*width/4-(200-400*random.random())*(width/1920), height/4-(100-200*random.random())*(width/1920)], [100*random.random(), 100*random.random()], 15*22474266964325.848, 0, 15*(width/1920), False, [40+215*random.random(),40+215*random.random(),40+215*random.random()]))
				Surface_List.extend(make_triangle([width/4-(200-400*random.random())*(width/1920), 3*height/4-(100-200*random.random())*(width/1920)]))
	
		if(not (physics_time_step==0 or player_hit)):#Physics System
			physics_prev_time=pygame.time.get_ticks()/1000
			radial_object_counter=0
			for i in Radial_Object_List:
				force = [0, 0]
				values = {
				"0.0": i.mass,
				"0.1": i.charge 
				}
				for j in range(Physics_Model_List[0].dimensions):
					values["0.2."+str(j)] = i.position[j]
				for j in range(Physics_Model_List[0].dimensions):
					values["0.3."+str(j)] = i.velocity[j]
				if(not radial_object_counter==0):
					for j in Radial_Object_List:
						if not j == i:
							values["1.0"] = j.mass
							values["1.1"] = j.charge
							for k in range(Physics_Model_List[0].dimensions):
								values["1.2."+str(k)] = j.position[k]
							for k in range(Physics_Model_List[0].dimensions):
								values["1.3."+str(k)] = j.velocity[k]
							temp = [Gravity_List[0][i](values) for i in range(len(Gravity_List[0]))]#Gravitation System
							force = [force[i]+temp[i] for i in range(len(temp))]
				else:
					dist=m2.dist(pygame.mouse.get_pos(),i.position)#Player Control System
					i.velocity[0]=1500*(width/1920)*(pygame.mouse.get_pos()[0]-i.position[0])/dist
					i.velocity[1]=1500*(width/1920)*(pygame.mouse.get_pos()[1]-i.position[1])/dist
					
				radial_object_counter+=1
				
				Physics_Model_List[0].Update_Kinematics(i, force=force, time_step=physics_time_step)
			
			Physics_Model_List[0].Surface_Collision(Radial_Object_List, Surface_List, time_step=physics_time_step)#Collision System with surface
			player_hit,object_collision=Physics_Model_List[0].Radial_Object_Collision(Radial_Object_List, time_step=physics_time_step)#Collision system with other circles
			if(object_collision):
				pygame.mixer.music.play()
		
		render_time_delay=pygame.time.get_ticks()/1000-render_prev_time
		if(render_time_delay>=render_time_step):#Render system
			render_prev_time+=render_time_delay
			text = font.render("Score: "+str(math.floor(physics_prev_time-starting_time)), True, (0,255,0))#Score Display
			screen.fill((0, 0, 0))
			screen.blit(text, (20*(width/1920), 20*(width/1920)))
			
			if(player_hit):#Back to Main Menu button
				mouse_posx,mouse_posy=pygame.mouse.get_pos()
				LMB=pygame.mouse.get_pressed(num_buttons=3)[0]
				text = font.render("Main Menu", True, (0,0,0))
				if(mouse_posx>width/2-text.get_width()/2-20 and mouse_posx<width/2+text.get_width()/2+20 and mouse_posy>20 and mouse_posy<60+text.get_height()):
					pygame.draw.rect(screen, (255,0,255), pygame.Rect(width/2-text.get_width()/2-20, 20, text.get_width()+40, text.get_height()+40))
					if(LMB):
						running=False
				else:
					text = font.render("Main Menu", True, (255,255,255))
					pygame.draw.rect(screen, (255,0,255), pygame.Rect(width/2-text.get_width()/2-20, 20, text.get_width()+40, text.get_height()+40),5)
				screen.blit(text,(width/2-text.get_width()/2,40))
			
			pygame.draw.circle(screen, Radial_Object_List[0].color, Radial_Object_List[0].position, Radial_Object_List[0].radius, width=5*(width//1920))
			for i in Radial_Object_List[1:]:#Object Rendering
				pygame.draw.circle(screen, i.color, i.position, i.radius)
			for i in Surface_List:#Surface Rendering
				pygame.draw.line(screen,(255,255,255),i.points[0],i.points[1],1)
			pygame.display.update()
	if(highscore<math.floor(physics_prev_time-starting_time)):#Save Data writing
		highscore=math.floor(physics_prev_time-starting_time)
		highscore_file = open("Data.txt","w")
		highscore_file.write(str(highscore)+" \n")
		highscore_file.write(str(render_time_step)+" \n")
	play,render_time_step=main_menu(highscore,render_time_step)
highscore_file.close()

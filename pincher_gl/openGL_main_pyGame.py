'''
@see: http://www.pygame.org/wiki/OBJFileLoader
@description: This program attempts to implement a sequence
@date:
@info:
'''
# wild imports
import sys, pygame #@UnusedImport
from pygame.locals import * #@UnusedWildImport
from pygame.constants import * #@UnusedWildImport
from OpenGL.GL import * #@UnusedWildImport
from OpenGL.GLU import *#@UnusedWildImport
import random

# Local class imports
from mat_obj_loader import * #@UnusedWildImport
from camera import * #@UnusedWildImport
from skybox import * #@UnusedWildImport
from rayTrace import * #@UnusedWildImport
from robot_coord import * #@UnusedWildImport

pygame.init()
'''-----------------------------Variables----------------------------------------------------'''
#global object
game = game_screen(800,600) #window size
arm_coord = Robot_Cord([258.762, 141, 51.43, 0, 512])#INITIAL COORDINATES)
tool = tool_cord() #tool point object (robot_coord)
new_angles = plot_angles(np.array([0.0]*5,dtype=float), 
                         np.array([0.0]*5,dtype=float))#used to get angles from tool point
caught_bal_coord = coordinate(68, -25, 181)#y = up/-down Z=front/-back

#global variables
angle = np.array([0.0]*5)#s_a,b_a,b001_a,w_a,g_a
gripper_angles = np.sort(np.arange(-90, 90, 5, dtype=int)) # a list of gripper angles
space_bar = 0 #space bar is pressed
list_count = 0 #a counter for the gripper angle

#the location of the ball
circ2 = coordinate(x=100.0, y=50.0, z=131.75)#red #blue positive z is forward
r2 = 10 #radius of the ball

#globals used for collision detection of drop box
box_coord = coordinate(-2.0, -250.0, 30 )
box_radius = 25 #radius of the box for collision capture

'''------------------------------ functions -----------------------------------------------------------'''
#initializes screen and loads obj files
def init():
    global ball, cube, clock, room_T_B, room_F_B_B, room_L_R_B, room_FB_T, room_LR_T,room_sill, base, shoulder, bicep, bicep001, wrist, gRail, gripper, gripper001
    glClearColor(0.5, 0.5, 0.5, 1.0) #Gray Background
    
    #light 0
    glLightfv(GL_LIGHT0, GL_POSITION,  (-100, 500,  0, 1.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (.1, .1, .1, .1))
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glEnable(GL_LIGHT0)
   
    #Light 1
    glLightfv(GL_LIGHT1, GL_AMBIENT,  [0.0, 0.0, 0.0, 1.0]) # R G B A
    glLightfv(GL_LIGHT1, GL_DIFFUSE,  [.85, .85, .85, 1]) # R G B A
    glLightfv(GL_LIGHT1, GL_POSITION, [300, 550, 300, 0.0]) # x y z w y = height, z = distance
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glEnable(GL_LIGHT1)
    
    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
         
    # LOAD OBJECT AFTER PYGAME INIT
    room_T_B = OBJ(PATH+'room_T_B.obj', swapyz=False, my_texture = True, use_mat = False)
    room_F_B_B = OBJ(PATH+'room_F_B_B.obj', swapyz=False, my_texture = True, use_mat = False)
    room_L_R_B = OBJ(PATH+'room_LR_B.obj', swapyz=False, my_texture = True, use_mat = False)
    room_FB_T = OBJ(PATH+'room_FB_T.obj', swapyz=False, my_texture = True, use_mat = False)
    room_LR_T = OBJ(PATH+'room_LR_T.obj', swapyz=False, my_texture = True, use_mat = False)
    room_sill = OBJ(PATH+'room_sill.obj', swapyz=False, my_texture = True, use_mat = False)
    base = OBJ(PATH+'base_bm.obj', swapyz=False, my_texture=False, use_mat = False)
    shoulder = OBJ(PATH+'shoulder_b.obj', swapyz=False, my_texture=False, use_mat = False)
    bicep = OBJ(PATH+'bicep_b.obj', swapyz=False, my_texture=False, use_mat = False)
    bicep001 = OBJ(PATH+'bicep001_b.obj', swapyz=False, my_texture=False, use_mat = False)
    wrist = OBJ(PATH+'wrist_b.obj', swapyz=False, my_texture=False, use_mat = False)
    gRail = OBJ(PATH+'grail_b.obj', swapyz=False, my_texture=False, use_mat = False)
    gripper = OBJ(PATH+'gripper_b.obj', swapyz=False, my_texture=False, use_mat = False)
    gripper001 = OBJ(PATH+'gripper001_b.obj', swapyz=False, my_texture=False, use_mat = False)
    cube = OBJ(PATH+'sphere.obj', swapyz=False, my_texture=False, use_mat = True)
    ball = OBJ(PATH+'cube_m.obj', swapyz=False, my_texture=False, use_mat = False)
    
    clock = pygame.time.Clock()
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, game.width/float(game.height), 1, 2000.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW) 
    initskybox()
    glEnable(GL_COLOR_MATERIAL)
    
    #initial robot sequence
    init_sequence()
 
#load the robot movement sequence drop box location is constant  
def init_sequence():
    tool.sequence[0]= coordinate(circ2.x, circ2.y, circ2.z - tool.offset.z, 
                        gripper_angles[list_count], tool.pounce_distance) 
    #ball pick pos
    tool.sequence[1] = coordinate(circ2.x, circ2.y, circ2.z - tool.offset.z, 
                        gripper_angles[list_count], 0) 
    #ball close gripper
    tool.sequence[2] = tool.sequence[1]
    #ball release position 
    tool.sequence[3] = coordinate(tool.point.x, tool.point.y, tool.point.z- 
                        tool.offset.z+10, gripper_angles[list_count], 0)
    #drop pounce pos
    tool.sequence[4] = coordinate(init_sequence.drop_loc.x, init_sequence.drop_loc.y, 
                        init_sequence.drop_loc.z, init_sequence.drop_loc.angle, tool.pounce_distance)
    #drop pos
    tool.sequence[5] = coordinate(init_sequence.drop_loc.x, init_sequence.drop_loc.y, 
                        init_sequence.drop_loc.z, init_sequence.drop_loc.angle,0)
    #drop release
    tool.sequence[6] = tool.sequence[5]
    #drop release pos
    tool.sequence[7] = tool.sequence[4]
init_sequence.drop_loc = coordinate(.0001,-250.0, -70, -45) 

#sets lighting for focul objects
def set_specular():
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT)
    glColor(.2, .2, .2)
    glColorMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE)
    glColor(.3,1,.1) 
    glColorMaterial(GL_FRONT_AND_BACK, GL_SPECULAR)
    glColor(.75,.75,.75)
    glColorMaterial(GL_FRONT_AND_BACK, GL_EMISSION)
    glColor(.1,.1,.1)
    glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, 128 )

#clear lighting to initial values   
def clear_specular():
    glColorMaterial(GL_FRONT, GL_SPECULAR)
    glColor(.0,.0,.0)
    glColorMaterial(GL_FRONT, GL_EMISSION)
    glColor(.0,.0,.0)
    glMaterial(GL_FRONT, GL_SHININESS, 128 )

#draw the robot and update the angles    
def render_robot():    
    #begin render robot
    glPushMatrix()
    set_specular()
    glRotate(-90, 1, 0, 0)
    glTranslate(-99.5, -131, 0)  
    glCallList(base.gl_list)  
    glPushMatrix()
    shoulder_rot(angle[0])#this rotates backwards
    bicep_rot(angle[1])
    bicep001_rot(angle[2])
    wrist_rot(angle[3])
    #check to see if captured if it is draw the captured ball
    if tool.caught == True:
        glPushMatrix()
        glPushAttrib(GL_CURRENT_BIT)
        glPushAttrib(GL_LIGHTING_BIT)
        
        glTranslate(circ2.x,circ2.y,circ2.z)   #dont swap here 
        glRotate(-tool.angle, 0,0,1) 
        glColorMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE)
        glColor(0,.3,.0) #set the captured color remove this later
        clear_specular()
        glCallList(cube.gl_list)
        
        glPopAttrib()
        glPopAttrib()
        glPopMatrix()
    
    gripper_mov(angle[4])
    
    glPopMatrix()
    glPopMatrix()

#draw a tool point
#@todo make this a cross hair
def render_tool_point():
    glPushMatrix()
    glTranslate(tool.point.x, tool.point.z, tool.point.y) #swap yz add offset 
    glRotate(-tool.angle, 0,1,0) 
    glColor(0,.0,.8)
    glCallList(ball.gl_list)  
    glPopMatrix()
 
#If the ball is not caught draw it    
def render_free_ball():
    if tool.caught == False:
        if tool.collision == False:
            glColorMaterial(GL_FRONT, GL_DIFFUSE)
            glColor(.8,.0,.0) 
        else:
            glColorMaterial(GL_FRONT, GL_DIFFUSE)
            glColor(.0,.0,.5) 
        clear_specular()
        glPushMatrix()
        glTranslate(circ2.x,circ2.z,circ2.y)   #swap y and z 
        glCallList(cube.gl_list)
        glPopMatrix()
        
#check if the object is grabable
def grab_object():
    global tool
    #check to see if object is grabable
    tool.collision = simp_sphere(tool.point , tool.radius, circ2, r2)      
    #update robot coordinates, do after collision check
    tool.point.x, tool.point.y, tool.point.z, tool.angle= arm_coord.change_in_joints(angle)
    tool.point.z += tool.offset.z
    
#doPlot = False 
def set_angles():
    global angle
    #plot the angle path
    if new_angles.done == False:
        angle = new_angles.get_next() 

#add the new coordinates to the next sequence
#@todo fix the gripper open close
def update_sequence():
    global next_sequence, angle   
    
    #@todo:change this to give a angle position or make a function that closes grippers
    if tool.next_seq == 0 or tool.next_seq == 6:
        angle[4] = 0 
    elif tool.next_seq == 2:
        angle[4] = 5 
            
    #ball pounce sequence
    tool.sequence[0].set_cord(circ2.x, circ2.y, circ2.z - tool.offset.z, gripper_angles[list_count], tool.pounce_distance) 
    #ball pick pos
    tool.sequence[1].set_cord(circ2.x, circ2.y, circ2.z - tool.offset.z, gripper_angles[list_count], 0) 
    #ball close gripper
    tool.sequence[2] = tool.sequence[1]
    #ball release position 
    tool.sequence[3].set_cord(tool.point.x, tool.point.y, tool.point.z- tool.offset.z+10, gripper_angles[list_count], 0)

    next_sequence = tool.sequence[tool.next_seq]

#if the ball is dropped off set new random coordinates
#@todo could do something more interesting like make it animated
def calc_new_ball_cord():
    global tool, circ2
    #check if ball is dropped off
    if tool.caught == False:
        #test to see if ball is collided with drop box
        tool.drop_box = simp_sphere(box_coord , box_radius, circ2, r2)
        if tool.drop_box: #sphere goes away and pops up at random
            print "dropped the ball off at the box"
            circ2.set_cord(random.randrange(-210,210,1.0), random.randrange(20,210,1.0),123.5)  
 
#gets the next sequence angles and moves the gripper angle                       
def move_sequence():
    global tool, list_count, new_angles
    print "next sequence angle = ", next_sequence.angle
    error, myA = arm_coord.calc_positions(next_sequence.x,next_sequence.y, next_sequence.z, next_sequence.angle, next_sequence.pounce)#x, y, z, gripper angle200, 131.75
    #check for pounce
    if error != True:
        new_angles.set_angles(angle, myA)
        tool.next_seq = (tool.next_seq+1)%len(tool.sequence)
        
    else:#do something here like try and get a new gripper angle
        #@todo: change so gripper angle resets after every pick
        list_count +=1
        if list_count >= gripper_angles.size:
            list_count = 0  
        print "return angles error: trying to get new gripper angle new angle = ", gripper_angles[list_count]

'''start of basic movement function'''
#getts the new motor angle
#@todo set limits of actual servo motors              
def calc_angle(a, speed=1):
    a=a*speed
    if a>360:
        a-=360
    return a  

'''
#getts the new motor angle
#dynamixels have 300degree range             
def calc_angle(a, speed=1):
    a=a*speed
    if a>330:
        a=330
    elif a<30:
        a=30
    return a  
'''

'''functions to rotate robot joints'''
def shoulder_rot(a=0):
    glTranslate(99, 131.75, 87.4)
    glRotatef(a, 0.0, 0, 1)
    glTranslate(-99, -131.75, -87.4)   
    glCallList(shoulder.gl_list)
    
def bicep_rot(a=0):
    glTranslate(99, 131.75, 128.9)
    glRotatef(a, .98052, -0.1964, 0)
    glTranslate(-99, -131.75, -128.9) 
    glCallList(bicep.gl_list)
    
def bicep001_rot(a=0):
    glTranslate(105.11, 162.26, 230.96)
    glRotatef(a, .98052,-0.1964, 0)
    glTranslate(-105.11, -162.26, -230.96) 
    glCallList(bicep001.gl_list)
    
def wrist_rot(a=0):#86.6, 180.29, 70.3
    glTranslate(86.6, 70.3, 180.29)
    glRotatef(a, .98052,  -0.1964, 0)
    glTranslate(-86.6, -70.3, -180.29) 
    
    glCallList(wrist.gl_list)
    glCallList(gRail.gl_list)
    
def gripper_mov(a=0):
    global tool, circ2
    glTranslate(a*.9805, a*-0.1964, 0)
    glCallList(gripper.gl_list)
    glTranslate(-a*1.961,  a*0.3928, 0)
    glCallList(gripper001.gl_list)
    if a < 4 and tool.caught == True:
        circ2.set_cord(tool.point.x, tool.point.y, tool.point.z)
        tool.caught = False
        print "caught object False"
        print "setting new circ2 coord = ", circ2.get_cord()
        #print "box coord is", box_coord.get_cord() 
    if a > 4.0 and tool.collision == True: #open
        print "caught object TRUE"
        print "circ 2 loc = ", circ2.get_cord()
        tool.caught = True  
        #update position
        circ2.set_cord(caught_bal_coord.x, caught_bal_coord.y, caught_bal_coord.z) #translation of centerpoint of grippers
        #print "box coord is", box_coord.get_cord()

#rotates the skybox to make room feel like its floating in space
def rotate_angle():
    rotate_angle.screen_angle -=.1
    if rotate_angle.screen_angle >360:
        rotate_angle.screen_angle-=360
    glRotate(rotate_angle.screen_angle,1,1,1)     
rotate_angle.screen_angle = 0 

#the main display function calls methods to move robot
#@todo: put this in a class and get rid of globals
def display():
    global  space_bar
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    #set the camera position
    control(0.1,0.1, mouse_down)
    
    #update tool point
    grab_object()
                 
    #render skybox
    glPushMatrix()
    rotate_angle() 
    drawskybox(500) #50
    glPopMatrix()
    
    #render new camera position
    update_camera()

    #render room
    #@todo:fix the room walls need own material
    glCallList(room_T_B.gl_list) 
    glCallList(room_F_B_B.gl_list)
    glCallList(room_L_R_B.gl_list)
    glCallList(room_FB_T.gl_list)
    glCallList(room_LR_T.gl_list)
    glCallList(room_sill.gl_list)
    # save start up atributes
    glPushAttrib(GL_CURRENT_BIT)
    glPushAttrib(GL_LIGHTING_BIT)
     
    #draw robot and ball if ball is grabbed 
    render_robot()
    
    '''
    #render cube to show tool point position
    #@todo:change this to cross hairs
    draw_tool = False
    if draw_tool == True:
        render_tool_point()
    '''  
      
    #render the static ball if it is not grabbed
    render_free_ball()
    
    #pop start up atributes       
    glPopAttrib() 
    glPopAttrib()
    
    #render a box to put object in
    render_drop_box()
    
    #set this up to do the whole sequence
    if space_bar == 1:
        update_sequence()
        #move to the next sequence
        move_sequence()
        space_bar = 0
        
    #check if ball is dropped off   
    calc_new_ball_cord()
    set_angles()

#main function to handle loop and keyboard the camera also uses keyboard
class main():
    def __init__(self):
        self.run_game()
    
    def run_game(self):
        global mouse_down, space_bar
        init()
        while 1:
            clock.tick(30) 
            for e in pygame.event.get():
                if e.type == QUIT:
                    sys.exit()
        
                elif e.type == KEYDOWN:
                    #keypress = True # this may be used for camera collision detection
                    if e.key == K_ESCAPE:
                        sys.exit() 
                    elif e.key == K_q:
                        button[0] = 1
                    elif e.key == K_w:
                        button[1] = 1
                    elif e.key == K_e:
                        button[2] = 1
                    elif e.key == K_s:
                        button[3] = 1
                    elif e.key == K_SPACE:
                            space_bar = 1                     
                
                elif e.type == KEYUP:
                    #keypress = False #this will be used for camera collision detection
                    if e.key == K_ESCAPE:
                        sys.exit() 
                    elif e.key == K_q:
                        button[0] = 0
                    elif e.key == K_w:
                        button[1] = 0
                    elif e.key == K_e:
                        button[2] = 0
                    elif e.key == K_s:
                        button[3] = 0
                    elif e.key == K_SPACE:
                        space_bar = 0
                            
                elif e.type == MOUSEBUTTONUP:
                    pygame.mouse.set_visible(True)
                    mouse_down = False
                elif e.type == MOUSEBUTTONDOWN:
                    mouse_down = True
            #get keypress
            a_s = a_b = a_b001= a_w = a_g = 0
            kp = pygame.key.get_pressed()
            if kp[pygame.K_F1]:
                a_s = 1
            if kp[pygame.K_1]:
                a_s = -1
            if kp[pygame.K_F2]:
                a_b = 1
            if kp[pygame.K_2]:
                a_b = -1
            if kp[pygame.K_F3]:
                a_b001 = 1
            if kp[pygame.K_3]:
                a_b001 = -1
            if kp[pygame.K_F4]:
                a_w = 1
            if kp[pygame.K_4]:
                a_w = -1
            if kp[pygame.K_a]:
                a_g = 1
            if kp[pygame.K_d]:
                a_g = -1 
    
            #get angle rotation
            angle[0] += calc_angle(a_s)
            angle[1] += calc_angle(a_b)
            angle[2] += calc_angle(a_b001)
            angle[3] += calc_angle(a_w)
            angle[4] += calc_angle(a_g) 
            if angle[4] > 17:
                angle[4]=17
            elif angle[4] < 1:
                angle[4] = 1  
            
            display()                            
            pygame.display.flip()
    
        killskybox()    

if __name__ == "__main__":
    mane = main()
  
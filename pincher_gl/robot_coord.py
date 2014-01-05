'''
Created on Dec 22, 2013

@author: Phil Williammee
'''
import numpy as np
import math

class coordinate():  
    def __init__(self, x, y, z, angle=0.0, pounce = 0.0): 
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.angle = angle
        self.pounce = pounce
    def set_cord(self, x, y, z, angle=0, pounce =0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.angle = angle
        self.pounce = pounce
    def get_cord(self):
        return self.x, self.y, self.z
    
class tool_cord():
    def __init__(self):
        self.point = coordinate(200, 131.75, 0)#starting position of the tool
        self.offset = coordinate(0,0,127.5) #distance between base and zero of shoulder, or absolute and incremental
        self.radius = 4
        self.angle = 283
        self.caught = False
        self.collision = False
        self.drop_box = False
        self.pounce_position = False
        self.pounce_distance = 40
        self.drop_release = False
        self.sequence = list([coordinate(0.0,0.0,0.0)]*8)
        self.next_seq = 0
          
class plot_angles():
    def __init__(self, start, finish):
        self.speed = 1
        self.counter = 0
        self.iter = 0
        self.start = start#five starting angles
        self.finish = finish
        self.delta_a = np.array([0.0]*5,dtype=float)
        self.distance = np.array([0.0]*5,dtype=float) 
        self.done = False
        self.close_gripper = False
        for i in range(5):
            if start[i]==0:
                start[i]=.0001
            if finish[i]==0:
                start[i]=.0001
        self.calc_pos()
        
    def set_angles(self, start, finish):
        self.start = start
        self.finish = finish
        self.done = False
        for i in range(5):
            if start[i]==0:
                start[i]=.0001
            if finish[i]==0:
                start[i]=.0001
        self.calc_pos()
           
    def calc_pos(self):
        self.distances = np.add(self.finish, -self.start)
        self.distances[0] = self.distances[0]%360
        if self.distances[0] > 180:
            self.distances[0] = self.distances[0] - 360
        if self.distances[0] < -180:
            self.distances[0] = self.distances[0] + 360 
        
        if self.close_gripper == False:    
            self.distances[4] = 0.0000001
        else:
            self.distances[4] = 5
        
        self.test_limits()
        self.iter = np.max(abs(self.distances))
        
        if self.iter != 0:
            for i, angle in enumerate(self.distances):
                self.delta_a[i] = angle / self.iter
                        
    def get_next(self):
        if self.counter < self.iter:
            self.counter += 1
            self.new_angle = np.add(self.start, np.multiply(self.delta_a, self.counter))
            #print self.counter
            return self.new_angle
        else:
            self.counter = 0
            self.done = True
            return self.new_angle  
              
    def test_limits(self):
        #print "start angles =", self.start
        #print "finish angles = ", self.finish
        start_angle = (np.array([11.5, 108, 45, 28, 0]))
        for i in range(5):
            if (start_angle[i] + self.distances[i]) > 180:
                print "max limit error a",i, " = ", start_angle[i] + self.distances[i]
            if (start_angle[i] + self.distances[i]) < -180:
                print "min limit error a", i, " = ", start_angle[i] + self.distances[i]


class Robot_Cord(object):
    def __init__(self, init_slider=list([0]*5)):
        SEGMENTS = int(5) #number of phantomX segments
        SLIDER_HOME = init_slider
        SLIDER_HOME[0] = 281.5 #starting angle
        
        #initial settings of sliders, could pass these?
        self.tw = SLIDER_HOME[1] # w axis position depth
        self.tz = SLIDER_HOME[2]# z axis starting position height
        self.gripper_angle = SLIDER_HOME[3] #preselected gripper angles
        self.gripper = SLIDER_HOME[4]
  
        #variables used to calculate data
        self.l12 = 0.0 # hypotenuse belween a1 & a3
        self.a12 = 0.0 #inscribed angle between hypotenuse, w 
        self.w = np.array([0]*SEGMENTS,dtype=float) #horizontal coordinate
        self.z = np.array([0]*SEGMENTS,dtype=float) #vertical coordinate
        self.x = np.array([0]*SEGMENTS,dtype=float) #x axis components 
        self.y = np.array([0]*SEGMENTS,dtype=float) #y axis components
        self.sliders_val = np.array([0]*SEGMENTS,dtype=float)
        
        self.l = np.array([0, 105, 105, 98])# actual measurements of segment length in mm        
        self.a = np.array([SLIDER_HOME[0]]*SEGMENTS,dtype=float) #angle for the link, reference is previous link
        
        #temp
        self.Joints_tw = 0
        self.joints_l12 = 0
        self.joints_tool_angle  = 0
        
    def angles_to_toolPoint(self, angles): 
        tool_angle = angles[1]+angles[2]+angles[3]
        self.joints_tool_angle = tool_angle 
        l12 = math.sqrt((self.l[1]*self.l[1])+(self.l[2]*self.l[2])
                      -(2*self.l[1]*self.l[2]*math.cos(angles[2])))
        
        if angles[2]%(6.2831853) > math.pi: #the other side of the triangle
            l12 = -l12

        if l12 > 210:#this should not be possible
            print "error can not reach position"   
        
        if self.l[1]*l12 != 0:#don't divide by 0
            sigma = math.acos(((self.l[1]*self.l[1])+(l12*l12)
                        -(self.l[2]*self.l[2])) / (2*self.l[1]*l12))
        else:
            sigma = 0
            
        a12 = angles[1]-sigma
        self.joints_l12 = l12
        w2 = l12*math.cos(a12)
        z2 = l12*math.sin(a12)
        wt = (self.l[3]*math.cos(tool_angle))+w2
        zt = (self.l[3]*math.sin(tool_angle))+z2
        
        return wt, zt #tool point
          
    def change_in_joints(self, an):#281.5, 108, 45, 208, 0
        start_angle = (np.array([281.5, 108, 45, 208, 0]))
        an = np.deg2rad(np.add(-an, start_angle))
        
        t_w, t_z = self.angles_to_toolPoint(an)
        self.Joints_tw = t_w

        #calc (x,y) coordinates of the plane
        t_x = t_w*math.cos(an[0])
        t_y = t_w*math.sin(an[0])
        return -t_x, -t_y, t_z, math.degrees(an[0])
                
    def calc_p2(self):#calculates position 2
        self.w[3] = self.tw
        self.z[3] = self.tz
        self.w[2] = self.tw-np.cos(np.radians(self.gripper_angle))*self.l[3]
        self.z[2] = self.tz-np.sin(np.radians(self.gripper_angle))*self.l[3]
        #print "w2 = ", self.w[2], "z2 = ", self.z[2]
        self.l12 = np.sqrt(np.square(self.w[2])+np.square(self.z[2])) 
        if self.l12 > (self.l[1]+self.l)[2]:
            print "target position can not be reached"
        #print self.l12, " l12 should equal ", self.joints_l12
           
    def calc_p1(self):#calculate position 1
        self.a12 = np.arctan2(self.z[2],self.w[2])#return the appropriate quadrant  
        self.a[1] = np.arccos((np.square(self.l[1])+np.square(self.l12)-np.square(self.l[2])) 
                              /(2*self.l[1]*self.l12))+self.a12
        self.w[1] = np.cos(self.a[1])*self.l[1]
        self.z[1] = np.sin(self.a[1])*self.l[1]
    
    def calc_angles(self): #calculate all of the motor angles see diagram
        self.a[2] = np.arctan((self.z[2]-self.z[1])/(self.w[2]-self.w[1]))-self.a[1]
        self.a[3] = np.deg2rad(self.gripper_angle)-self.a[1]-self.a[2]  

    def calc_x_y(self):#calc x_y of servoscoordinates 
        for i in range(4):#fixed number of segments
            self.x[i] = self.w[i]*np.cos(self.a[0])
            self.y[i] = self.w[i]*np.sin(self.a[0])
    
    #recieves final position and calculates all join angles         
    def calc_positions(self, t_x, t_y, t_z, g_a, pounce=0):#no swap because robot is rotated
        error = False
        #self.a[0] = math.atan2(t_y,t_x )
        #print "tx =", t_x
        #print "tx =", t_y
        if t_x ==0:
            print "x =0"
            a0=.00001
        else:
            a0 = math.atan(t_y / t_x )
        if t_x >= 0 and t_y >= 0:#first quadrant starting angle i 
            print "first quadrant"
        elif t_x <= 0 and t_y >= 0:#second quadrant tan is negative + 90
            print "second quadrant"
            a0 = a0 + 3.14159
        elif t_x <= 0 and t_y <= 0:#third quadrant tan is positive     
            print "third qudrant"
            a0 = a0 + 3.14159 #78.5
        elif t_x >= 0 and t_y <= 0:#fourth quadrant it should be negative 
            print "fourth qudrant"
        else :
            print "ERROR no quadrant"
        self.a[0] = a0
        print "a0 = ", math.degrees(a0)
        
        
        self.tw = math.sqrt((t_x*t_x) + (t_y*t_y)) - pounce
        self.tz = t_z + pounce
        self.gripper_angle  = g_a #recieved in degrees
        self.a[4] = self.gripper_angle 
        #print "gripper angle = ", self.gripper_angle, "should equal", math.degrees(self.joints_tool_angle)
        
        #self.sliders_to_var()
        self.calc_p2() 
        self.calc_p1() 
        self.calc_x_y()
        self.calc_angles() 
        
        start_angle = (np.array([101.5, 108, -135, 28, 0]))#coord -360 + 180
        angle = np.add(-np.rad2deg(self.a), start_angle)
        #print "gripper = ", angle[3]
        
        if self.l12 > (self.l[1]+self.l)[2]:
            print "target position can not be reached"
            error = True
        return  error, angle
    

    
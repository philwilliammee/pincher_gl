'''
Created on Dec 15, 2013
@author: Phil Williammee
this should be a class
'''
import sys, pygame
from pygame.locals import *
from pygame.constants import *
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

 #camera 
camX=0
camY=150
camZ=500
camYaw = 0.0
camPitch = 0.0
mouse_down=False
button = np.zeros(4)

def lockCamera():
    global camPitch, camYaw
    if camPitch > 180:
        camPitch = 180
    if camPitch < -180:
        camPitch = -180
    if camYaw<0.0:
        camYaw+=360
    if camYaw>360:
        camYaw-=360

def moveCamera(dist, direction):
    global camX, camZ
    rad = np.radians(camYaw+direction)
    camX -= np.sin(rad)*dist
    camZ -= np.cos(rad)*dist
    

def moveCameraUp(dist , direction):
    global camY
    rad = np.radians(camPitch+direction)
    camY += np.sin(rad)*dist

def control(move_vel, mouse_vel, mi):
    global camYaw, camPitch
    mov_speed = 1
    if mi:
        midx = 400
        midy = 300
        #disable cursor to hide it?
        pygame.mouse.set_visible(False)
        tmpx, tmpy = pygame.mouse.get_pos() 
        camYaw += mouse_vel*(midx-tmpx)
        camPitch += mouse_vel * (midy -tmpy)
        lockCamera()
        pygame.mouse.set_pos(midx, midy)#pan mouse in center of screen
        
        mov_speed = 50
        
        if button[1]:
            #if camPitch != 90 and camPitch != -90:
            moveCamera(move_vel*mov_speed,0.0)
            moveCameraUp(move_vel*mov_speed,0.0)
        elif button[3]:
            #if camPitch!=90 and camPitch != -90:
            moveCamera(move_vel*mov_speed,180.0)
            moveCameraUp(move_vel*mov_speed,180.0)
                    
        elif button[0]:
            moveCamera(move_vel*mov_speed, 90.0)
                    
        elif button[2]:
            moveCamera(move_vel*mov_speed, 270.0)
            
        elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
            print " kp exit" 
            sys.exit()
                    
    glRotatef(-camPitch, 1.0, 0.0, 0.0)  
    glRotatef(-camYaw, 0.0, 1.0, 0.0)
    
    
def update_camera():
    glTranslatef(-camX, -camY,-camZ)
    
def moveTo(c):
    global camX, camY, camZ
    camX=c.x;
    camY=c.y;
    camZ=c.z;

def camPos():
    return camX,camY,camZ
       

'''
@descriptio: functions to calculate collision detection
@reference: http://www.youtube.com/watch?v=TJs0l0lj7dk&list=PL0AB023E769342AFE&index=34
'''
import sys, pygame #@UnusedImport
from pygame.locals import * #@UnusedWildImport
from pygame.constants import * #@UnusedWildImport
from robot_coord import coordinate 

class game_screen():
    def __init__(self, width=800, height=600):
        self.viewport = (width,height)
        self.width = width
        self.height = height
        self.srf = pygame.display.set_mode(self.viewport, OPENGL | DOUBLEBUF )#FULLSCREEN | HWSURFACE )


def pointdistance(c1,c2):
    pointdistance.Pvec .x = c2.x-c1.x
    pointdistance.Pvec .y= c2.y-c1.y
    pointdistance.Pvec .z = c2.z-c1.z
    return (pointdistance.Pvec.x*pointdistance.Pvec.x + pointdistance.Pvec.y *
            pointdistance.Pvec.y +pointdistance.Pvec.z*pointdistance.Pvec.z)
pointdistance.Pvec = coordinate(0,0,0)

def simp_sphere(c1,r1,c2,r2,):
    dist=pointdistance(c1,c2)
    if(dist<=(r1+r2)*(r1+r2)):  
        return True
    else:
        return False

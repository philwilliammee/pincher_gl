from mat_obj_loader import *
import numpy as np

SKY_LEFT = 0
SKY_BACK = 1
SKY_RIGHT = 2 
SKY_FRONT = 3
SKY_TOP = 4
SKY_BOTTOM = 5
skybox = np.arange(6)

def initskybox(picture="space"):
    global skybox
    if (picture == "space"):
        skybox[SKY_LEFT]=loadTexture('sky_neg_z.jpg')
        skybox[SKY_BACK]=loadTexture('sky_neg_x.jpg')
        skybox[SKY_RIGHT]=loadTexture('sky_pos_z.jpg')
        skybox[SKY_FRONT]=loadTexture('sky_pos_x.jpg')
        skybox[SKY_TOP ]=loadTexture('sky_pos_y.jpg')
        skybox[SKY_BOTTOM]=loadTexture('sky_neg_y.jpg')
        
    if (picture == "storm"):
        skybox[SKY_LEFT]=loadTexture('images\\left.bmp')
        skybox[SKY_FRONT]=loadTexture('images\\front.bmp')
        skybox[SKY_RIGHT]=loadTexture('images\\right.bmp')
        skybox[SKY_BACK]=loadTexture('images\\back.bmp')
        skybox[SKY_TOP ]=loadTexture('images\\top.bmp')
        skybox[SKY_BOTTOM]=loadTexture('images\\bottom.bmp')
        
def killskybox():
    for i in range(len(skybox)):
        glDeleteTextures(skybox[i]) 

def drawskybox(size):
    b1 = glIsEnabled(GL_TEXTURE_2D);    #new, we left the textures turned on, if it was turned on
    
    glDisable(GL_LIGHTING);    #turn off lighting, when making the skybox
    glDisable(GL_DEPTH_TEST);    #turn off depth texting
    glEnable(GL_TEXTURE_2D);    #and turn on texturing
    
    glBindTexture(GL_TEXTURE_2D,skybox[SKY_BACK]);    #use the texture we want
    
    glBegin(GL_QUADS);    #and draw a face
    #back face
    glTexCoord2f(0,0);    #use the correct texture coordinate
    glVertex3f(size/2,size/2,size/2);    #and a vertex
    glTexCoord2f(1,0);    #and repeat it...
    glVertex3f(-size/2,size/2,size/2);
    glTexCoord2f(1,1);
    glVertex3f(-size/2,-size/2,size/2);
    glTexCoord2f(0,1);
    glVertex3f(size/2,-size/2,size/2);
    glEnd();
    
    glBindTexture(GL_TEXTURE_2D,skybox[SKY_LEFT]);
    
    glBegin(GL_QUADS);    
    #left face
    glTexCoord2f(0,0);
    glVertex3f(-size/2,size/2,size/2);
    glTexCoord2f(1,0);
    glVertex3f(-size/2,size/2,-size/2);
    glTexCoord2f(1,1);
    glVertex3f(-size/2,-size/2,-size/2);
    glTexCoord2f(0,1);
    glVertex3f(-size/2,-size/2,size/2);
    glEnd();
    
    glBindTexture(GL_TEXTURE_2D,skybox[SKY_FRONT]);
    
    glBegin(GL_QUADS);    
    #front face
    glTexCoord2f(1,0);
    glVertex3f(size/2,size/2,-size/2);
    glTexCoord2f(0,0);
    glVertex3f(-size/2,size/2,-size/2);
    glTexCoord2f(0,1);
    glVertex3f(-size/2,-size/2,-size/2);
    glTexCoord2f(1,1);
    glVertex3f(size/2,-size/2,-size/2);
    glEnd();
    
    glBindTexture(GL_TEXTURE_2D,skybox[SKY_RIGHT]);  
      
    glBegin(GL_QUADS);    
    #right face
    glTexCoord2f(0,0);
    glVertex3f(size/2,size/2,-size/2);
    glTexCoord2f(1,0);
    glVertex3f(size/2,size/2,size/2);
    glTexCoord2f(1,1);
    glVertex3f(size/2,-size/2,size/2);
    glTexCoord2f(0,1);
    glVertex3f(size/2,-size/2,-size/2);
    glEnd();
    
    glBindTexture(GL_TEXTURE_2D,skybox[SKY_TOP]); 
           
    glBegin(GL_QUADS);            #top face
    glTexCoord2f(1,0);
    glVertex3f(size/2,size/2,size/2);
    glTexCoord2f(0,0);
    glVertex3f(-size/2,size/2,size/2);
    glTexCoord2f(0,1);
    glVertex3f(-size/2,size/2,-size/2);
    glTexCoord2f(1,1);
    glVertex3f(size/2,size/2,-size/2);
    glEnd();
    
    glBindTexture(GL_TEXTURE_2D,skybox[SKY_BOTTOM]);  
          
    glBegin(GL_QUADS);    
    #bottom face
    glTexCoord2f(1,1);
    glVertex3f(size/2,-size/2,size/2);
    glTexCoord2f(0,1);
    glVertex3f(-size/2,-size/2,size/2);
    glTexCoord2f(0,0);
    glVertex3f(-size/2,-size/2,-size/2);
    glTexCoord2f(1,0);
    glVertex3f(size/2,-size/2,-size/2);
    glEnd();
    
    glEnable(GL_LIGHTING);    #turn everything back, which we turned on, and turn everything off, which we have turned on.
    glEnable(GL_DEPTH_TEST);
    if not b1:
        glDisable(GL_TEXTURE_2D);
        
#drop box for ball drop off
def render_drop_box():
    glPushMatrix()
    glTranslate(0,-50,-250)
    glEnable(GL_BLEND); #Enable blending.
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA); #Set blending function.
    glColor4f(1, .2, .2, .5)
    glBegin(GL_QUADS);    #and draw a face
    glVertex3f(-50.0,125.0,-50.0);
    glVertex3f(50.0,125.0,-50.0);
    glVertex3f(50.0,50.0,-50.0);
    glVertex3f(-50.0,50.0,-50.0);

    glEnd()

    glBegin(GL_POLYGON)    
    #left face
    glVertex3f(-50.0,125.0,50.0);
    glVertex3f(50.0,125.0,50.0);
    glVertex3f(50.0,50.0,50.0);
    glVertex3f(-50.0,50.0,50.0);
    glEnd();
    
    
    glBegin(GL_POLYGON) 
    #front face
    glVertex3f(50.0,125.0,-50.0);
    glVertex3f(50.0,125.0,50.0);
    glVertex3f(50.0,50.0,50.0);
    glVertex3f(50.0,50.0,-50.0);
    glEnd();
    
    glBegin(GL_POLYGON) 
    #right face
    glVertex3f(-50.0,125.0,50.0);
    glVertex3f(-50.0,125.0,-50.0);
    glVertex3f(-50.0,50.0,-50.0);
    glVertex3f(-50.0,50.0,50.0);
    glEnd();
    glPopMatrix()
    glDisable(GL_BLEND); #Enable blending.
    glColor4f(.8, .8, .8, 1)

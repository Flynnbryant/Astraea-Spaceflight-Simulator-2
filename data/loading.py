'''
loading.py - 3 functions

Reading all textures from storage (data/textures/) and processing them to be mapped
onto spheroids or other uses. This is where the majority of start up time is taken
(approximately 2 seconds, down from 40+ without multithreading.)
'''

import concurrent.futures
import multiprocessing
import pyglet
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np
import time
import os

def loading_screen(universe, camera):
    camera.window.clear()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-camera.halfwidth, camera.halfwidth, -camera.halfheight, camera.halfheight)
    camera.loadingscreen.draw()
    if camera.screenstate == 1:
        universe.populate()
        camera.populate(universe)
        load_textures(universe, camera)
    camera.screenstate += 1
    glFlush()

def load_textures(universe, camera):
    ''' Manager to load textures using multithreading to reduce startup time.

    Inputs: universe and camera overarching objects.

    Outputs:
    * body.texture: Imported, processed, and assigned textures for every simulated body.
    * camera.background.star_texture: The imported and processed star background.
    '''

    Image.MAX_IMAGE_PIXELS = None #Required to allow very large image files.
    with concurrent.futures.ThreadPoolExecutor() as executor:
        required_textures = ['GalaxyLR','Default']

        ''' Return all filenames in the folder of object textures without an extension '''
        available_textures = [i[:-4] for i in os.listdir('data/textures/highres/')]

        ''' Match up which objects have textures present (if not they will be given the default texture)'''
        for body in universe.bodies:
            if body.name in available_textures:
                required_textures.append(body.name)
                body.texture = body.name #overrites the default texture assignment.

        ''' Distribute textures for multithreading (I/O operation)'''
        results = [executor.submit(import_texture, objectname) for objectname in required_textures]

        ''' Move each texture through for processing as soon as it has been imported.
        Multithreading is not useful here so the smallest texture files are processed
        while others are still being imported. Unlike importing, processing a texture
        can be completed in near constant time and is not dependent on texture size.'''
        for finished in concurrent.futures.as_completed(results):
            imported_tex = finished.result()
            mapped_texture = process_texture(*imported_tex)

            ''' Assign the textures to their respective objects '''
            if imported_tex[2] == 'GalaxyLR':
                camera.background.star_texture = mapped_texture
            for body in universe.bodies:
                if body.texture == imported_tex[2]:
                    body.texture = mapped_texture



def import_texture(objectname):
    ''' Load an RGB image file (without transparency) into an image file in bytes.

    Inputs:
    * objectname: name of the image file (typically the planet or moon name.)

    Outputs:
    * Image format object
    '''

    filename = 'data/textures/highres/'+objectname+'.jpg'
    img = Image.open(filename)
    return img.tobytes('raw', 'RGB', 0, -1), img.size, objectname



def process_texture(img_data, size, name):
    ''' Convert the image into a texture format that openGL can then map onto spheroids.

    Inputs:
    * img_data: Image file (converted to bytes in the inport step.)
    * size: Size of the image

    Outputs:
    * texture: format to be mapped onto speroids.
    '''

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size[0], size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    return texture

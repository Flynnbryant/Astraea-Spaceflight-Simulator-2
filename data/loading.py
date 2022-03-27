import concurrent.futures
import multiprocessing
from OpenGL.GL import *
from OpenGL.GLU import gluNewQuadric, gluQuadricTexture
from PIL import Image
import numpy as np
import time
import os

def load_textures(universe, camera):
    Image.MAX_IMAGE_PIXELS = None
    with concurrent.futures.ThreadPoolExecutor() as executor:
        required_textures = ['GalaxyLR','Default']
        camera.highres = True
        available_textures = [i[:-4] for i in os.listdir('data/textures/highres/')]
        for body in universe.bodies:
            if body.name in available_textures:
                required_textures.append(body.name)
                body.texture = body.name

        results = [executor.submit(import_texture, objectname) for objectname in required_textures]
        for finished in concurrent.futures.as_completed(results):
            imported_tex = finished.result()
            mapped_texture = process_texture(imported_tex[0], imported_tex[1])
            if imported_tex[2] == 'GalaxyLR':
                camera.background.star_texture = mapped_texture
            else:
                for body in universe.bodies:
                    if body.texture == imported_tex[2]:
                        body.texture = mapped_texture

def import_texture(objectname):
    filename = 'data/textures/highres/'+objectname+'.jpg'
    img = Image.open(filename)
    return img.tobytes('raw', 'RGB', 0, -1), img.size, objectname
    # Compare tobytes with tostring and check performance. If so, change on ring loading too

def process_texture(img_data, size):
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

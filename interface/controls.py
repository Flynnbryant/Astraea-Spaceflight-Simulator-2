import numpy as np
import time
import pyglet
from interface.prioritiser import *
from spacecraft.node import *
from interface.mouse import *

def key_controls(universe, camera, dt):
    camera.window.push_handlers(camera.keys)
    if any(camera.keys):
        simulation_keys(universe, camera, dt)
        vessel_keys(universe, camera, dt)
        if camera.keys[pyglet.window.key.LSHIFT]:
            precise_keys(universe, camera, dt)
        else:
            camera_keys(universe, camera, dt)
    universe.profile.add('con')

def simulation_keys(universe, camera, dt):
    if camera.keys[pyglet.window.key.P]:
        universe.usertime = min(universe.usertime*(1+10*dt), 31500000)
    elif camera.keys[pyglet.window.key.O]:
        universe.usertime *= (1-10*dt)
    if camera.keys[pyglet.window.key.F] or camera.keys[pyglet.window.key.BRACKETLEFT]:
        update_focus(universe, camera, -1)
    elif camera.keys[pyglet.window.key.G] or camera.keys[pyglet.window.key.BRACKETRIGHT]:
        update_focus(universe, camera, 1)
    elif camera.keys[pyglet.window.key.C]:
        if not camera.switch:
            camera.cinematic_view = not camera.cinematic_view
            camera.switch = True
            update_zoom(universe, camera, 1)
    else:
        camera.switch = False

def vessel_keys(universe, camera, dt):
    if camera.keys[pyglet.window.key.H]:
        prograde(universe, universe.vessels[0], min(universe.timestep,np.linalg.norm(universe.vessels[0].bodycentre.rvel*0.01)))
    elif camera.keys[pyglet.window.key.N]:
        prograde(universe, universe.vessels[0], max(-universe.timestep,-np.linalg.norm(universe.vessels[0].bodycentre.rvel*0.01)))
    if camera.keys[pyglet.window.key.I]:
        normal(universe, universe.vessels[0], min(universe.timestep,np.linalg.norm(universe.vessels[0].bodycentre.rvel*0.01)))
    elif camera.keys[pyglet.window.key.K]:
        normal(universe, universe.vessels[0], max(-universe.timestep,-np.linalg.norm(universe.vessels[0].bodycentre.rvel*0.01)))
    if camera.keys[pyglet.window.key.L]:
        radial(universe, universe.vessels[0], min(universe.timestep,np.linalg.norm(universe.vessels[0].bodycentre.rvel*0.01)))
    elif camera.keys[pyglet.window.key.J]:
        radial(universe, universe.vessels[0], max(-universe.timestep,-np.linalg.norm(universe.vessels[0].bodycentre.rvel*0.01)))

def camera_keys(universe, camera, dt):
    if  camera.keys[pyglet.window.key.EQUAL]:
        update_zoom(universe, camera, (1-10*dt))
    elif camera.keys[pyglet.window.key.MINUS]:
        update_zoom(universe, camera, (1+10*dt))
    if camera.keys[pyglet.window.key.UP] or camera.keys[pyglet.window.key.W]:
        camera.vertical_rot = np.clip(camera.vertical_rot +100*dt, -180, 0)
    elif camera.keys[pyglet.window.key.DOWN] or camera.keys[pyglet.window.key.S]:
        camera.vertical_rot = np.clip(camera.vertical_rot -100*dt, -180, 0)
    if camera.keys[pyglet.window.key.LEFT] or camera.keys[pyglet.window.key.A]:
        camera.horizontal_rot += 200*dt
    elif camera.keys[pyglet.window.key.RIGHT] or camera.keys[pyglet.window.key.D]:
        camera.horizontal_rot -= 200*dt

def precise_keys(universe, camera, dt):
    if  camera.keys[pyglet.window.key.EQUAL]:
        update_zoom(universe, camera, (1-dt))
    elif camera.keys[pyglet.window.key.MINUS]:
        update_zoom(universe, camera, (1+dt))
    if camera.keys[pyglet.window.key.UP]:
        camera.vertical_rot += 10*dt
    elif camera.keys[pyglet.window.key.DOWN]:
        camera.vertical_rot -= 10*dt
    if camera.keys[pyglet.window.key.LEFT]:
        camera.horizontal_rot += 10*dt
    elif camera.keys[pyglet.window.key.RIGHT]:
        camera.horizontal_rot -= 10*dt
    if camera.keys[pyglet.window.key.W]:
        camera.pos[1] += 0.05*dt*camera.pos[2]
    elif camera.keys[pyglet.window.key.S]:
        camera.pos[1] -= 0.05*dt*camera.pos[2]
    if camera.keys[pyglet.window.key.A]:
        camera.pos[0] -= 0.05*dt*camera.pos[2]
    elif camera.keys[pyglet.window.key.D]:
        camera.pos[0] += 0.05*dt*camera.pos[2]
    if camera.keys[pyglet.window.key.Q]:
        camera.tilt -= 20*dt
    elif camera.keys[pyglet.window.key.E]:
        camera.tilt += 20*dt
    if camera.keys[pyglet.window.key.R]:
        camera.vertical_rot = -75
        camera.tilt = 0
        camera.pos[0] = 0
        camera.pos[1] = 0

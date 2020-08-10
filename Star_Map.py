import OpenGL.GL as gl
import numpy as np

import GraphicModules.Renderer as rnd
import GraphicModules.GL_MatrixModule as mm
import GraphicModules.Objects as obj

import pygame
from pygame.locals import *



def main():
    pygame.init()
    display = (800, 600)

    pygame.display.gl_set_attribute(GL_MULTISAMPLEBUFFERS, 1)
    pygame.display.gl_set_attribute(GL_MULTISAMPLESAMPLES, 4)

    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    clock = pygame.time.Clock()

    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    gl.glEnable(gl.GL_POINT_SPRITE)
    gl.glEnable(gl.GL_PROGRAM_POINT_SIZE)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glEnable(gl.GL_MULTISAMPLE)

    av_pos = 60.0
    bv_pos = 0.0
    cv_pos = -90.0

    proj = mm.perspective(60., display[0] / display[1], 10., 20000.)
    viewt = mm.viewtranslation(0, 0, 25)

    renderer = rnd.Renderer()

    grid = obj.Grid()
    stars = obj.nearstars()

    x_pos = 0.0
    y_pos = 0.0
    z_pos = 0.0
    t_speed = 0.1

    rv_speed = 1

    center = np.array([0., 0., 0.], dtype = 'single')

    while True:

        dt = clock.tick_busy_loop(60) / (1000. / 60.)

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if keys[K_s]:
            x_pos += -t_speed * dt
            center[0] = x_pos
            stars.UpdateBuffer(center)
        if keys[K_w]:
            x_pos += t_speed * dt
            center[0] = x_pos
            stars.UpdateBuffer(center)
        if keys[K_a]:
            y_pos += t_speed * dt
            center[1] = y_pos
            stars.UpdateBuffer(center)
        if keys[K_d]:
            y_pos += -t_speed * dt
            center[1] = y_pos
            stars.UpdateBuffer(center)
        if keys[K_r]:
            z_pos += t_speed * dt
            center[2] = z_pos
            stars.UpdateBuffer(center)
        if keys[K_f]:
            z_pos += -t_speed * dt
            center[2] = z_pos
            stars.UpdateBuffer(center)

        if keys[K_LEFT]:
            cv_pos += -rv_speed * dt
        if keys[K_RIGHT]:
            cv_pos += rv_speed * dt
        if keys[K_DOWN]:
            av_pos += rv_speed * dt
        if keys[K_UP]:
            av_pos += -rv_speed * dt

        renderer.Clear()

        modelt = mm.modeltranslation(-x_pos, -y_pos, -z_pos)
        viewr = mm.viewrotation(av_pos, bv_pos, cv_pos)

        mvp = mm.matrixmultiplication(viewr, viewt, proj)
        mvpstar = mm.matrixmultiplication(modelt, viewr, viewt, proj)

        grid.Draw(mvp, renderer)
        stars.Draw(mvpstar, renderer)

        pygame.display.flip()



main()

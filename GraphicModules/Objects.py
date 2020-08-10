# If you need some insight about how OpenGL works, I recommed watching the
# amazing series made by The Cherno:
# https://www.youtube.com/watch?v=W3gAzLwfIP0&list=PLlrATfBNZ98foTJPJ_Ev03o2oq3-GGOS2
# About 90% of the things i know about OpenGL comes from there and it would be
# truly hypocritical not to recognize the fantastic teaching work that the
# Cherno has done

import OpenGL.GL as gl
import numpy as np
import pandas as pd

import GraphicModules.VertexArray as va
import GraphicModules.VertexBuffer as vb
import GraphicModules.VertexBufferLayout as vbl
import GraphicModules.IndexBuffer as ib
import GraphicModules.Shader as shd
import GraphicModules.Texture as txtr

import CelestiaModules.ParseCelestiaFiles as pcf

# Global paths
res_path = 'res/'
shaders_path = res_path + 'shaders/'
textures_path = res_path + 'textures/'



class Grid:

    def __init__(self):

        grid_vertices = []

        for i in range(0, 121):
            if i % 10:
                grid_vertices.extend([60. - i, 60., 0.,
                                      60. - i, -60., 0.])
        for i in range(0, 121):
            if i % 10:
                grid_vertices.extend([60., 60. - i, 0.,
                                      -60., 60. - i, 0.])

        grid_vertices = np.array(grid_vertices, dtype = 'single')
        grid_indices = np.array(list(range(0, 432)), dtype = 'uintc')


        # Initialize Vertex Array and Buffer
        self._va = va.VertexArray()
        self._vb = vb.VertexBuffer(grid_vertices)

        # Create Layout with the first attribute composed by 3 float and add it
        # to the vertex array
        self._layout = vbl.VertexBufferLayout()
        self._layout.PushFloat(3)
        self._va.AddBuffer(self._layout)

        # Index Buffer
        self._ib = ib.IndexBuffer(grid_indices)

        # Shader
        self._shader = shd.Shader(shaders_path + 'TransparentBlue.glsl')

    # Drawing function
    def Draw(self, mvp, renderer):
        self._shader.Bind()
        self._shader.SetUniformMat4f('u_MVP', mvp)

        renderer.DrawL(self._va, self._ib, self._shader)



class nearstars:

    def __init__(self):
        self._df = pcf.stcparser('nearstars.stc')

        # Initialize Vertex Array and dynamic Buffer
        self._va = va.VertexArray()
        self._vb = vb.DynamicVertexBuffer()

        # Create Layout with
        # attribute #1 composed by 3 float (position)
        # attribute #2 composed by 3 float (RGB)
        # and add it to the vertex array
        self._layout = vbl.VertexBufferLayout()
        self._layout.PushFloat(3)
        self._layout.PushFloat(4)
        self._va.AddBuffer(self._layout)

        # Update buffer for the first time
        center = np.array([0., 0., 0.], dtype = 'single')
        self._vb.Bind()

        # Get all stars within grid range:
        # center.x - 30 <= x < center.x + 30
        # center.y - 30 <= y < center.y + 30
        # center.z - 10 <= z < center.z + 10
        visiblestars = self._df[(center[0]-30 <= self._df.x) &
                                (self._df.x < center[0]+30)]

        visiblestars = visiblestars[(center[1]-30 <= visiblestars.y) &
                                    (visiblestars.y < center[1]+30)]

        visiblestars = visiblestars[(center[2]-10 <= visiblestars.z) &
                                    (visiblestars.z < center[2]+10)]

        self._count = len(visiblestars.index)

        # Generate array
        vsa = visiblestars.to_numpy(dtype = 'single').flatten()

        # Update Vertex Buffer
        self._vb.Fill(vsa)

        # Shader
        self._shader = shd.Shader(shaders_path + 'Star.glsl')


    # Function which updates the vertex buffer depending on the the center
    # coordinates.
    def UpdateBuffer(self, center):

        # Get all stars within grid range:
        # center.x - 30 <= x < center.x + 30
        # center.y - 30 <= y < center.y + 30
        # center.z - 10 <= z < center.z + 10
        visiblestars = self._df[(center[0]-30 <= self._df.x) &
                                (self._df.x < center[0]+30)]

        visiblestars = visiblestars[(center[1]-30 <= visiblestars.y) &
                                    (visiblestars.y < center[1]+30)]

        visiblestars = visiblestars[(center[2]-10 <= visiblestars.z) &
                                    (visiblestars.z < center[2]+10)]

        self._count = len(visiblestars.index)

        # Generate array
        vsa = visiblestars.to_numpy(dtype = 'single').flatten()

        # Update Vertex Buffer
        self._vb.Fill(vsa)

    # Drawing funtion
    def Draw(self, mvp, renderer):
        self._shader.Bind()
        self._shader.SetUniformMat4f('u_MVP', mvp)

        renderer.DrawP(self._va, self._shader, 0, self._count)



#  ______________________________________________
# |                                              |
# | Old code used during some of the first tests |
# |______________________________________________|
#



quads_vertices = np.array([-2.5, -2.5, 0.,      1.0, 1.0, 0.0,
                            2.5, -2.5, 0.,      1.0, 1.0, 0.0,
                            2.5,  2.5, 0.,      1.0, 1.0, 0.0,
                           -2.5,  2.5, 0.,      1.0, 1.0, 0.0,

                           -2.5, -2.5, 5.,      0.0, 0.0, 1.0,
                            2.5, -2.5, 5.,      0.0, 0.0, 1.0,
                            2.5,  2.5, 5.,      0.0, 0.0, 1.0,
                           -2.5,  2.5, 5.,      0.0, 0.0, 1.0],
                           dtype = 'single')

quads_indices = np.array([0, 1, 2,
                          2, 3, 0,

                          4, 5, 6,
                          6, 7, 4],
                          dtype = 'uintc')

class TestQuads:

    def __init__(self):
        self._va = va.VertexArray()
        self._vb = vb.VertexBuffer(quads_vertices)

        self._layout = vbl.VertexBufferLayout()
        self._layout.PushFloat(3)
        self._layout.PushFloat(3)
        self._va.AddBuffer(self._layout)

        self._ib = ib.IndexBuffer(quads_indices)

        self._shader = shd.Shader(shaders_path + 'TestQuads.glsl')

    def Draw(self, mvp, renderer):
        self._shader.Bind()
        self._shader.SetUniformMat4f('u_MVP', mvp)

        renderer.DrawT(self._va, self._ib, self._shader)

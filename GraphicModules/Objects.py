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



# Cartesian grid vertices
grid_vertices = np. array(
                        [ -5., -10., 0.,        #0
                         -2.5, -10., 0.,        #1
                           0., -10., 0.,        #2
                          2.5, -10., 0.,        #3
                           5., -10., 0.,        #4

                           5., -7.5, 0.,        #5
                           5.,  -5., 0.,        #6
                           5., -2.5, 0.,        #7
                           5.,   0., 0.,        #8
                           5.,  2.5, 0.,        #9
                           5.,   5., 0.,        #10
                           5.,  7.5, 0.,        #11
                           5.,  10., 0.,        #12

                          2.5,  10., 0.,        #13
                           0.,  10., 0.,        #14
                         -2.5,  10., 0.,        #15
                          -5.,  10., 0.,        #16

                          -5.,  7.5, 0.,        #17
                          -5.,   5., 0.,        #18
                          -5.,  2.5, 0.,        #19
                          -5.,   0., 0.,        #20
                          -5., -2.5, 0.,        #21
                          -5.,  -5., 0.,        #22
                          -5., -7.5, 0.],       #23
                         dtype = 'single'
                        )

# Vertices drawing order
grid_indices = np.array(
                        [0,  4,
                         4, 12,
                        12, 16,
                        16,  0,

                         1, 15,
                         2, 14,
                         3, 13,

                         5, 23,
                         6, 22,
                         7, 21,
                         8, 20,
                         9, 19,
                        10, 18,
                        11, 17],
                        dtype = 'uintc')



class Grid:

    def __init__(self):

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
        self._shader = shd.Shader(shaders_path + 'Grid.glsl')

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
        self._layout.PushFloat(3)
        self._va.AddBuffer(self._layout)

        # Update buffer for the first time
        self.UpdateBuffer(np.array([0., 0., 0.], dtype = 'single'), init = True)

        # Shader
        self._shader = shd.Shader(shaders_path + 'Star.glsl')

    # Function which updates the vertex buffer depending on the the center
    # coordinates. The init status must be set True only for the first update
    def UpdateBuffer(self, center, init = False):

        if not init:
            self._vb.Bind()

        # Get all stars within grid range:
        # center.x - 5 <= x < center.x + 5
        # center.y - 10 <= y < center.y + 10
        # center.z - 5 <= z < center.z +5
        visiblestars = self._df[(center[0]-5 <= self._df.x) & (self._df.x < center[0]+5)]
        visiblestars = visiblestars[(center[1]-10 <= visiblestars.y) & (visiblestars.y < center[1]+10)]
        visiblestars = visiblestars[(center[2]-5 <= visiblestars.z) & (visiblestars.z < center[2]+5)]

        self._count = len(visiblestars.index)

        # Translate stars
        visiblestars.x -= center[0]
        visiblestars.y -= center[1]
        visiblestars.z -= center[2]

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

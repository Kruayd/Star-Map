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

    def __init__(self, color = (0., 0.42, 1., 0.5)):

        grid_vertices = []

        for i in range(0, 121):
            if i % 10:
                grid_vertices.extend([60. - i, 60., 0.,     *color,
                                      60. - i, -60., 0.,    *color])
        for i in range(0, 121):
            if i % 10:
                grid_vertices.extend([60., 60. - i, 0.,     *color,
                                      -60., 60. - i, 0.,    *color])

        grid_vertices = np.array(grid_vertices, dtype = 'single')
        grid_indices = np.array(list(range(0, 432)), dtype = 'uintc')


        # Initialize Vertex Array and Buffer
        self._va = va.VertexArray()
        self._vb = vb.VertexBuffer(grid_vertices)

        # Create Layout with the first attribute composed by 3 float and add it
        # to the vertex array
        self._layout = vbl.VertexBufferLayout()
        self._layout.PushFloat(3)
        self._layout.PushFloat(4)
        self._va.AddBuffer(self._layout)

        # Index Buffer
        self._ib = ib.IndexBuffer(grid_indices)

        # Shaders:
        # - InitShader
        # - PeelShader
        self._InitShader = shd.Shader(shaders_path + 'ColoredMeshInit.glsl')
        self._PeelShader = shd.Shader(shaders_path + 'ColoredMeshPeel.glsl')

        # Uniforms
        # - MVP
        self._mvp = np.array([[1., 0., 0., 0.],
                              [0., 1., 0., 0.],
                              [0., 0., 1., 0.],
                              [0., 0., 0., 1.]], dtype = 'single')

    # Update model view projection matrix
    def UpdateMVP(self, mvp):
        self._mvp = mvp

    # Bind self._InitShader
    def BindInitShader(self):
        self._InitShader.Bind()
        self._InitShader.SetUniformMat4f('u_MVP', self._mvp)

    # Bind self._PeelShader
    def BindPeelShader(self, screensize = np.array([100, 100], dtype =
                                                   'single')):
        self._PeelShader.Bind()
        self._PeelShader.SetUniformMat4f('u_MVP', self._mvp)
        self._PeelShader.SetUniform2fv('u_Res', screensize)
        # The Depth Texture and the Front Blending Texture are bindend
        # respectively to the zeroth and the first slot
        self._PeelShader.SetUniform1i('u_DepthTex', 0)
        self._PeelShader.SetUniform1i('u_FrontBlender', 1)

    # Drawing function
    def Draw(self):
        self._va.Bind()
        self._ib.Bind()
        gl.glDrawElements(gl.GL_LINES, self._ib.GetCount(), gl.GL_UNSIGNED_INT,
                          None)



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

        # Shaders:
        # - InitShader
        # - PeelShader
        self._InitShader = shd.Shader(shaders_path + 'StarInit.glsl')
        self._PeelShader = shd.Shader(shaders_path + 'StarPeel.glsl')

        # Uniforms
        # - MVP
        self._mvp = np.array([[1., 0., 0., 0.],
                              [0., 1., 0., 0.],
                              [0., 0., 1., 0.],
                              [0., 0., 0., 1.]], dtype = 'single')


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

    # Update Model View Projection Matrix
    def UpdateMVP(self, mvp):
        self._mvp = mvp

    # Bind self._InitShader
    def BindInitShader(self):
        self._InitShader.Bind()
        self._InitShader.SetUniformMat4f('u_MVP', self._mvp)

    # Bind self._PeelShader
    def BindPeelShader(self, screensize = np.array([100, 100], dtype =
                                                   'single')):
        self._PeelShader.Bind()
        self._PeelShader.SetUniformMat4f('u_MVP', self._mvp)
        self._PeelShader.SetUniform2fv('u_Res', screensize)
        # The Depth Texture and the Front Blending Texture are bindend
        # respectively to the zeroth and the first slot
        self._PeelShader.SetUniform1i('u_DepthTex', 0)
        self._PeelShader.SetUniform1i('u_FrontBlender', 1)

    # Drawing funtion
    def Draw(self):
        self._va.Bind()
        gl.glDrawArrays(gl.GL_POINTS, 0, self._count)



class Canvas:

    def __init__(self):

        CanvasVertices = np.array([-1.0, -1.0,      0.0, 0.0,
                                    1.0, -1.0,      1.0, 0.0,
                                    1.0,  1.0,      1.0, 1.0,
                                   -1.0,  1.0,      0.0, 1.0],
                                  dtype = 'single')

        CanvasIndices = np.array([0, 1, 2,
                                  2, 3, 0],
                                 dtype = 'uintc')

        self._va = va.VertexArray()
        self._vb = vb.VertexBuffer(CanvasVertices)

        self._layout = vbl.VertexBufferLayout()
        self._layout.PushFloat(2)
        self._layout.PushFloat(2)
        self._va.AddBuffer(self._layout)

        self._ib = ib.IndexBuffer(CanvasIndices)

        self._BlendShader = shd.Shader(shaders_path + 'CanvasBlend.glsl')
        self._FinalShader = shd.Shader(shaders_path + 'CanvasFinal.glsl')

    def BindBlendShader(self):
        self._BlendShader.Bind()
        # The Back Temporary Texture is bindend to the zeroth slot
        self._BlendShader.SetUniform1i('u_BackTemp', 0)

    def BindFinalShader(self):
        self._FinalShader.Bind()
        # The Front Blending Texture and the Back Blending Texture are binded
        # respectively  to the zeroth and the first slot
        self._FinalShader.SetUniform1i('u_FrontBlender', 0)
        self._FinalShader.SetUniform1i('u_BackBlender', 1)

    def Draw(self):
        self._va.Bind()
        self._ib.Bind()
        gl.glDrawElements(gl.GL_TRIANGLES, self._ib.GetCount(),
                          gl.GL_UNSIGNED_INT, None)

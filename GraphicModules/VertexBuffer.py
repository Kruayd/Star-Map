# If you need some insight about how OpenGL works, I recommed watching the
# amazing series made by The Cherno:
# https://www.youtube.com/watch?v=W3gAzLwfIP0&list=PLlrATfBNZ98foTJPJ_Ev03o2oq3-GGOS2
# About 90% of the things i know about OpenGL comes from there and it would be
# truly hypocritical not to recognize the fantastic teaching work that the
# Cherno has done

import OpenGL.GL as gl
import numpy as np



# Abstracting the vertex buffer type into a class
class VertexBuffer:

    def __init__(self, data):
        self._RendererID = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._RendererID)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data, gl.GL_STATIC_DRAW)

    def __del__(self):
        gl.glDeleteBuffers(1, np.array([self._RendererID], dtype = 'uintc'))

    def Bind(self):
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._RendererID)

    def Unbind(self):
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

# This is a class for dynamic vertex buffer
class DynamicVertexBuffer:

    # The buffer length in bytes is now fixed at 4 * 10 * 100 000, thus it can
    # load a maximum of 100 000 vertices with 10 attributes, each represented
    # by a single precision float (4 bytes). It takes up 4M of memory
    def __init__(self):
        self._RendererID = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._RendererID)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, np.dtype('single').itemsize * 10 * 100000, None, gl.GL_DYNAMIC_DRAW)

    def __del__(self):
        gl.glDeleteBuffers(1, np.array([self._RendererID], dtype = 'uintc'))

    def Bind(self):
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._RendererID)

    def Unbind(self):
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

    def Fill(self, data):
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0, data.nbytes, data)

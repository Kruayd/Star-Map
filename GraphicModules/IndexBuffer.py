# If you need some insight about how OpenGL works, I recommed watching the
# amazing series made by The Cherno:
# https://www.youtube.com/watch?v=W3gAzLwfIP0&list=PLlrATfBNZ98foTJPJ_Ev03o2oq3-GGOS2
# About 90% of the things i know about OpenGL comes from there and it would be
# truly hypocritical not to recognize the fantastic teaching work that the
# Cherno has done

import OpenGL.GL as gl
import numpy as np



# Abstracting the index buffer type into a class
class IndexBuffer:

    def __init__(self, data):
        self._RendererID = gl.glGenBuffers(1)
        self._Count = data.size
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self._RendererID)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, data.nbytes, data, gl.GL_STATIC_DRAW)

    def __del__(self):
        gl.glDeleteBuffers(1, np.array([self._RendererID], dtype = 'uintc'))

    def Bind(self):
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self._RendererID)

    def Unbind(self):
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)

    def GetCount(self):
        return self._Count

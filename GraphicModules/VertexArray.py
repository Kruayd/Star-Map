# If you need some insight about how OpenGL works, I recommed watching the
# amazing series made by The Cherno:
# https://www.youtube.com/watch?v=W3gAzLwfIP0&list=PLlrATfBNZ98foTJPJ_Ev03o2oq3-GGOS2
# About 90% of the things i know about OpenGL comes from there and it would be
# truly hypocritical not to recognize the fantastic teaching work that the
# Cherno has done

import OpenGL.GL as gl
import numpy as np
from ctypes import c_void_p



# Abstracting the vertex array type into a class
class VertexArray:

    def __init__(self):
        self._RendererID = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self._RendererID)
        self._Elements = []

    def __del__(self):
        gl.glDeleteVertexArrays(1, np.array([self._RendererID], dtype = 'uintc'))

    def Bind(self):
        gl.glBindVertexArray(self._RendererID)

    def Unbind(self):
        gl.glBindVertexArray(0)

    def AddBuffer(self, layout):
        self._Elements = layout.GetElements()
        offset = 0

        for i in range(0, len(self._Elements)):
            element = self._Elements[i]
            gl.glEnableVertexAttribArray(i)
            gl.glVertexAttribPointer(i, element.Count, element.Gltype, element.Normalized, layout.GetStride(), c_void_p(offset))

            offset += element.Count * element.GetSizeOfType()

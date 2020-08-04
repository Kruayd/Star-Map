# If you need some insight about how OpenGL works, I recommed watching the
# amazing series made by The Cherno:
# https://www.youtube.com/watch?v=W3gAzLwfIP0&list=PLlrATfBNZ98foTJPJ_Ev03o2oq3-GGOS2
# About 90% of the things i know about OpenGL comes from there and it would be
# truly hypocritical not to recognize the fantastic teaching work that the
# Cherno has done

import OpenGL.GL as gl
import numpy as np



# Class aimed to represent a Vertex attribute by its fundamental properties
# (such as type, size and normalization)
class VertexBufferElement:

    def __init__(self, gltype, count, normalized):
        self.Gltype = gltype
        self.Count = count
        self.Normalized = normalized

    def GetSizeOfType(self):
        if self.Gltype == gl.GL_FLOAT:
            return np.dtype('single').itemsize
        elif self.Gltype == gl.GL_UNSIGNED_INT:
            return np.dtype('uintc').itemsize
        elif self.Gltype == gl.GL_UNSIGNED_BYTE:
            return np.dtype('ubyte').itemsize



# Class representing the vertex buffer layout with all the fundamental
# properties of its elements
class VertexBufferLayout:

    def __init__(self):
        self._Elements = list()
        self._Stride = 0

    def PushFloat(self, count):
        vbe = VertexBufferElement(gl.GL_FLOAT, count, gl.GL_FALSE)
        self._Elements.append(vbe)
        self._Stride += count * vbe.GetSizeOfType()

    def PushUInt(self, count):
        vbe = VertexBufferElement(gl.GL_UNSIGNED_INT, count, gl.GL_FALSE)
        self._Elements.append(vbe)
        self._Stride += count * vbe.GetSizeOfType()

    def PushUChar(self, count):
        vbe = VertexBufferElement(gl.GL_UNSIGNED_BYTE, count, gl.GL_TRUE)
        self._Elements.append(vbe)
        self._Stride += count * vbe.GetSizeOfType()

    def GetStride(self):
        return self._Stride

    def GetElements(self):
        return self._Elements

# If you need some insight about how OpenGL works, I recommed watching the
# amazing series made by The Cherno:
# https://www.youtube.com/watch?v=W3gAzLwfIP0&list=PLlrATfBNZ98foTJPJ_Ev03o2oq3-GGOS2
# About 90% of the things i know about OpenGL comes from there and it would be
# truly hypocritical not to recognize the fantastic teaching work that the
# Cherno has done

import OpenGL.GL as gl
import numpy as np
from PIL import Image



# Dictionary useful for converting from color model to various info, such as
# gl.colormode, gl.colordepth and byte per pixel
mode_to_info = {
        'RGBA' : {'mode' : gl.GL_RGBA, 'depth' : gl.GL_RGBA8, 'bpp' : 4 * 8}
        }



class Texture:

    def __init__(self, path):
        self._LocalBuffer = None

        self._FilePath = path

        im = Image.open(self._FilePath, 'r')
        im = im.transpose(Image.FLIP_TOP_BOTTOM)
        # OpenGL loads texture upside-down (from the left-bottom corner to the
        # right-upper corner)

        self._Width = im.width
        self._Height = im.height
        self._BPP = mode_to_info[im.mode]['bpp']

        # Get picture bytes array
        self._LocalBuffer = im.tobytes()

        self._RendererID = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._RendererID)

        # Fundamental TexParameters

        # Minification filter, sample down (target, parameter, method)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER,
                           gl.GL_LINEAR)
        # Magnification filter, sample up
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER,
                           gl.GL_LINEAR)
        # Horizontal wrap, GL_CLAMP_TO_EDGE: texture is shrinked to fit
        # surface
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S,
                           gl.GL_CLAMP_TO_EDGE)
        # Vertical wrap
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T,
                           gl.GL_CLAMP_TO_EDGE)

        # TexImage2D( target, level/multilevel, internal format (how OpenGL
        # should handle data), width, height, border (in pixels), format
        # (format of read data), type, data array)

        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, mode_to_info[im.mode]['depth'],
                        self._Width, self._Height, 0,
                        mode_to_info[im.mode]['mode'],
                        gl.GL_UNSIGNED_BYTE, self._LocalBuffer)

        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

        # If array is not empty
        if self._LocalBuffer:
            del im

    def __del__(self):
        gl.glDeleteTextures(1, np.array([self._RendererID], dtype = 'uintc'))

    def Clear(self):
        gl.glDeleteTextures(1, np.array([self._RendererID], dtype = 'uintc'))

    # OpenGL provides 32 slot but availability also depends on device
    # capabilities
    def Bind(self, slot = 0):
        gl.glActiveTexture(gl.GL_TEXTURE0 + slot)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._RendererID)

    def Unbind(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

    def GetWidth(self):
        return self._Width

    def GetHeight(self):
        return self._Height



class SingleEmptyColorTexture:

    def __init__(self, width, height):
        self._RendererID = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._RendererID)

        # Fundamental TexParameters

        # Minification filter, sample down (target, parameter, method)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER,
                           gl.GL_LINEAR)
        # Magnification filter, sample up
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER,
                           gl.GL_LINEAR)
        # Horizontal wrap, GL_CLAMP_TO_EDGE: texture is shrinked to fit
        # surface
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S,
                           gl.GL_CLAMP_TO_EDGE)
        # Vertical wrap
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T,
                           gl.GL_CLAMP_TO_EDGE)

        # TexImage2D( target, level/multilevel, internal format (how OpenGL
        # should handle data), width, height, border (in pixels), format
        # (format of read data), type, data array)

        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA8,
                        width, height, 0,
                        gl.GL_RGBA,
                        gl.GL_UNSIGNED_BYTE, None)

        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

    def __del__(self):
        gl.glDeleteTextures(1, np.array([self._RendererID], dtype = 'uintc'))

    def Clear(self):
        gl.glDeleteTextures(1, np.array([self._RendererID], dtype = 'uintc'))

    # OpenGL provides 32 slot but availability also depends on device
    # capabilities
    def Bind(self, slot = 0):
        gl.glActiveTexture(gl.GL_TEXTURE0 + slot)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._RendererID)

    def Unbind(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

    def TextureID(self):
        return self._RendererID



class MultipleEmptyColorTexture:

    def __init__(self, width, height, quantity):
        self._IDsBuffer = gl.glGenTextures(quantity)

        for ID in self._IDsBuffer:
            gl.glBindTexture(gl.GL_TEXTURE_2D, ID)

            # Fundamental TexParameters

            # Minification filter, sample down (target, parameter, method)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER,
                               gl.GL_LINEAR)
            # Magnification filter, sample up
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER,
                               gl.GL_LINEAR)
            # Horizontal wrap, GL_CLAMP_TO_EDGE: texture is shrinked to fit
            # surface
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S,
                               gl.GL_CLAMP_TO_EDGE)
            # Vertical wrap
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T,
                               gl.GL_CLAMP_TO_EDGE)

            # TexImage2D( target, level/multilevel, internal format (how
            # OpenGL should handle data), width, height, border (in
            # pixels), format (format of read data), type, data array)

            gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA8,
                            width, height, 0,
                            gl.GL_RGBA,
                            gl.GL_UNSIGNED_BYTE, None)

        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

    def __del__(self):
        gl.glDeleteTextures(len(self._IDsBuffer), self._IDsBuffer)

    def Clear(self):
        gl.glDeleteTextures(len(self._IDsBuffer), self._IDsBuffer)


    # OpenGL provides 32 slot but availability also depends on device
    # capabilities
    def Bind(self, index, slot = 0):
        gl.glActiveTexture(gl.GL_TEXTURE0 + slot)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._IDsBuffer[index])

    def Unbind(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

    def TextureID(self, index):
        return self._IDsBuffer[index]



# Depth texture with double channel (R and G), useful for dual depth peeling
class SingleEmptyDualDepthTexture:

    def __init__(self, width, height):
        self._RendererID = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._RendererID)

        # Fundamental TexParameters

        # Minification filter, sample down (target, parameter, method)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER,
                           gl.GL_LINEAR)
        # Magnification filter, sample up
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER,
                           gl.GL_LINEAR)
        # Horizontal wrap, GL_CLAMP_TO_EDGE: texture is shrinked to fit
        # surface
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S,
                           gl.GL_CLAMP_TO_EDGE)
        # Vertical wrap
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T,
                           gl.GL_CLAMP_TO_EDGE)

        # TexImage2D( target, level/multilevel, internal format (how OpenGL
        # should handle data), width, height, border (in pixels), format
        # (format of read data), type, data array)

        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RG32F,
                        width, height, 0,
                        gl.GL_RG,
                        gl.GL_FLOAT, None)

        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

    def __del__(self):
        gl.glDeleteTextures(1, np.array([self._RendererID], dtype = 'uintc'))

    def Clear(self):
        gl.glDeleteTextures(1, np.array([self._RendererID], dtype = 'uintc'))

    # OpenGL provides 32 slot but availability also depends on device
    # capabilities
    def Bind(self, slot = 0):
        gl.glActiveTexture(gl.GL_TEXTURE0 + slot)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._RendererID)

    def Unbind(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

    def TextureID(self):
        return self._RendererID



# Depth texture array with double channel (R and G), useful for dual depth peeling
class MultipleEmptyDualDepthTexture:

    def __init__(self, width, height, quantity):
        self._IDsBuffer = gl.glGenTextures(quantity)

        for ID in self._IDsBuffer:
            gl.glBindTexture(gl.GL_TEXTURE_2D, ID)

            # Fundamental TexParameters

            # Minification filter, sample down (target, parameter, method)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER,
                               gl.GL_LINEAR)
            # Magnification filter, sample up
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER,
                               gl.GL_LINEAR)
            # Horizontal wrap, GL_CLAMP_TO_EDGE: texture is shrinked to fit
            # surface
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S,
                               gl.GL_CLAMP_TO_EDGE)
            # Vertical wrap
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T,
                               gl.GL_CLAMP_TO_EDGE)

            # TexImage2D( target, level/multilevel, internal format (how
            # OpenGL should handle data), width, height, border (in
            # pixels), format (format of read data), type, data array)

            gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RG32F,
                            width, height, 0,
                            gl.GL_RG,
                            gl.GL_FLOAT, None)

        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

    def __del__(self):
        gl.glDeleteTextures(len(self._IDsBuffer), self._IDsBuffer)

    def Clear(self):
        gl.glDeleteTextures(len(self._IDsBuffer), self._IDsBuffer)


    # OpenGL provides 32 slot but availability also depends on device
    # capabilities
    def Bind(self, index, slot = 0):
        gl.glActiveTexture(gl.GL_TEXTURE0 + slot)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._IDsBuffer[index])

    def Unbind(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

    def TextureID(self, index):
        return self._IDsBuffer[index]

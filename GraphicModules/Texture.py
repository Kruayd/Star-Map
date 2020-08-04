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

# Dictionary useful for converting from index to corresponding GL_SLOT
gl_slot = {
        0 : gl.GL_TEXTURE0,
        1 : gl.GL_TEXTURE1,
        2 : gl.GL_TEXTURE2,
        3 : gl.GL_TEXTURE3,
        4 : gl.GL_TEXTURE4,
        5 : gl.GL_TEXTURE5,
        6 : gl.GL_TEXTURE6,
        7 : gl.GL_TEXTURE7,
        8 : gl.GL_TEXTURE8,
        9 : gl.GL_TEXTURE9,
        10 : gl.GL_TEXTURE10,
        11 : gl.GL_TEXTURE11,
        12 : gl.GL_TEXTURE12,
        13 : gl.GL_TEXTURE13,
        14 : gl.GL_TEXTURE14,
        15 : gl.GL_TEXTURE15,
        16 : gl.GL_TEXTURE16,
        17 : gl.GL_TEXTURE17,
        18 : gl.GL_TEXTURE18,
        19 : gl.GL_TEXTURE19,
        20 : gl.GL_TEXTURE20,
        21 : gl.GL_TEXTURE21,
        22 : gl.GL_TEXTURE22,
        23 : gl.GL_TEXTURE23,
        24 : gl.GL_TEXTURE24,
        25 : gl.GL_TEXTURE25,
        26 : gl.GL_TEXTURE26,
        27 : gl.GL_TEXTURE27,
        28 : gl.GL_TEXTURE28,
        29 : gl.GL_TEXTURE29,
        30 : gl.GL_TEXTURE30,
        31 : gl.GL_TEXTURE31
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

        # Fundamental TexParameter

        # Minification filter, sample down (target, parameter, method)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        # Magnification filter, sample up
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        # Horizontal wrap, GL_CLAMP_TO_EDGE: texture is shrinked to fit surface
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
        # Vertical wrap
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)

        # TexImage2D( target, level/multilevel, internal format (how OpenGL
        # should handle data), width, height, border (in pixels), format
        # (format of read data), type, data array)

        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, mode_to_info[im.mode]['depth'],
                        self._Width, self._Height, 0, mode_to_info[im.mode]['mode'],
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
        gl.glActiveTexture(gl_slot[slot])
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._RendererID)

    def Unbind(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

    def GetWidth(self):
        return self._Width

    def GetHeight(self):
        return self._Height

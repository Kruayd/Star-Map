# If you need some insight about how OpenGL works, I recommed watching the
# amazing series made by The Cherno:
# https://www.youtube.com/watch?v=W3gAzLwfIP0&list=PLlrATfBNZ98foTJPJ_Ev03o2oq3-GGOS2
# About 90% of the things i know about OpenGL comes from there and it would be
# truly hypocritical not to recognize the fantastic teaching work that the
# Cherno has done

import OpenGL.GL as gl



# Abstracting Rendering operations into a class
class Renderer:

    def __init__(self):
        pass

    # Draw Triangles
    def DrawT(self, va, ib, shader):
        va.Bind()
        ib.Bind()
        gl.glDrawElements(gl.GL_TRIANGLES, ib.GetCount(), gl.GL_UNSIGNED_INT, None)
        va.Unbind()
        ib.Unbind()
        shader.Unbind()

    # Draw Lines
    def DrawL(self, va, ib, shader):
        va.Bind()
        ib.Bind()
        gl.glDrawElements(gl.GL_LINES, ib.GetCount(), gl.GL_UNSIGNED_INT, None)
        va.Unbind()
        ib.Unbind()
        shader.Unbind()

    # Draw Points
    def DrawP(self, va, shader, start, quantity):
        va.Bind()
        gl.glDrawArrays(gl.GL_POINTS, start, quantity)
        va.Unbind()
        shader.Unbind()

    def Clear(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    def SetClearColor(self, r, g, b, a):
        gl.glClearColor(r, g, b, a)

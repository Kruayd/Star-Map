# If you need some insight about how OpenGL works, I recommed watching the
# amazing series made by The Cherno:
# https://www.youtube.com/watch?v=W3gAzLwfIP0&list=PLlrATfBNZ98foTJPJ_Ev03o2oq3-GGOS2
# About 90% of the things i know about OpenGL comes from there and it would be
# truly hypocritical not to recognize the fantastic teaching work that the
# Cherno has done
# I also recommend watching these videos to understand better what frame buffer
# objects and query objects do
# Frame buffers: https://youtu.be/atp3bzebWJE
# Query objects: https://www.youtube.com/watch?v=LMpw7foANNA
#
# Finally, if you wish to learn more about dual depth peeling, you can look at
# the famous paper written by Nvidia and the relative code
# paper only: http://developer.download.nvidia.com/SDK/10/opengl/src/dual_depth_peeling/doc/DualDepthPeeling.pdf
# paper + code: http://developer.download.nvidia.com/SDK/10/opengl/screenshots/samples/dual_depth_peeling.html

import numpy as np
import OpenGL.GL as gl
import GraphicModules.Objects as obj
import GraphicModules.Texture as txtr


Attachments = np.array([gl.GL_COLOR_ATTACHMENT0,
                        gl.GL_COLOR_ATTACHMENT1,
                        gl.GL_COLOR_ATTACHMENT2,
                        gl.GL_COLOR_ATTACHMENT3,
                        gl.GL_COLOR_ATTACHMENT4,
                        gl.GL_COLOR_ATTACHMENT5,
                        gl.GL_COLOR_ATTACHMENT6],
                       dtype = 'uintc')



# Abstracting the dual depth peeling rendering process into a class
class DualDepthPeelingRenderer:

    def __init__(self, screen_width, screen_height):

        self._ScreenSize = np.array([screen_width, screen_height], dtype =
                                  'single')

        # Generate 2 Depth Textures, 2 Front Blending Textures, 2 Back
        # Temporary Textures and 1 Back Blending Texture
        self._DepthTex = txtr.MultipleEmptyDualDepthTexture(screen_width,
                                                            screen_height, 2)
        self._FrontBlender = txtr.MultipleEmptyColorTexture(screen_width,
                                                            screen_height, 2)
        self._BackTemp = txtr.MultipleEmptyColorTexture(screen_width,
                                                        screen_height, 2)
        self._BackBlender = txtr.SingleEmptyColorTexture(screen_width,
                                                         screen_height)

        self._RendererID = gl.glGenFramebuffers(1)
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self._RendererID)

        # Attach all the generated texture to the newly created frame buffer
        # object
        #
        # Since only 1 GL_DEPTH_ATTACHMENT is available per frame buffer
        # object, an effective workaround is to use GL_COLOR_ATTACHMENT instead
        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, Attachments[0],
                                  gl.GL_TEXTURE_2D,
                                  self._DepthTex.TextureID(0), 0)
        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, Attachments[1],
                                  gl.GL_TEXTURE_2D,
                                  self._FrontBlender.TextureID(0), 0)
        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, Attachments[2],
                                  gl.GL_TEXTURE_2D,
                                  self._BackTemp.TextureID(0), 0)
        # Since only 1 GL_DEPTH_ATTACHMENT is available per frame buffer
        # object, an effective workaround is to use GL_COLOR_ATTACHMENT instead
        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, Attachments[3],
                                  gl.GL_TEXTURE_2D,
                                  self._DepthTex.TextureID(1), 0)
        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, Attachments[4],
                                  gl.GL_TEXTURE_2D,
                                  self._FrontBlender.TextureID(1), 0)
        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, Attachments[5],
                                  gl.GL_TEXTURE_2D,
                                  self._BackTemp.TextureID(1), 0)
        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, Attachments[6],
                                  gl.GL_TEXTURE_2D,
                                  self._BackBlender.TextureID(), 0)

        self._OcclusionQueryID = gl.glGenQueries(1)

        self._Canvas = obj.Canvas()



    # Drawing Function
    def Render(self, *args):
        gl.glEnable(gl.GL_BLEND)
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self._RendererID)

        # The background is cleaned before textures 0, 1 and 2 so that after
        # _TextureClear(0) the DrawBuffer is set on the first depth texture
        # (Attachments[0]) and there is no need to bind it again before drawing
        self._BackgroundClear()
        self._TextureClear(0)

        # The InitShader stores, in the texture pixels, the max and min depth
        # of the fragment. The result is similar to what could happen by
        # watching the scene from front and back at the same time
        gl.glBlendEquation(gl.GL_MAX)
        for element in args:
            element.BindInitShader()
            element.Draw()

        # Dual depth peeling algorithm pass counter
        peelingPass = 0
        anySamplePassed = 1
        currId = 0

        while(anySamplePassed):

            # This part of code makes the prevId and currId variables
            # oscillate between 0 and 1. At the first while iteration prevId
            # should be set to 0 and currId to 1
            prevId = peelingPass % 2
            currId = 1 - prevId
            peelingPass += 1

            # Clear the textures referring to the current Id
            self._TextureClear(currId)

            # Draw on Attachments 0-1-2 or 3-4-5, starting from 3-4-5 at
            # the first while iteration, and set the blend equation to GL_MAX
            # (at the end of this while cycle the equation is seto to
            # GL_FUNC_ADD so it is mandatory to this operation in the first
            # while iteration too even though we have already done it about 30
            # lines above
            gl.glDrawBuffers(3, Attachments[3*currId:3 + currId*3])
            gl.glBlendEquation(gl.GL_MAX)

            # The previous Depth Texture is binded to the zeroth slot, whilst
            # the previous Front Blending Texture is binded to the first slot
            self._DepthTex.Bind(prevId, 0)
            self._FrontBlender.Bind(prevId, 1)
            for element in args:
                element.BindPeelShader(self._ScreenSize)
                element.Draw()

            # Passage to alpha blend the Back Temporary Texture on the Back
            # Blending Texture
            # The Blend Equation and the Blending Function are the classic ones
            gl.glDrawBuffer(Attachments[6])
            gl.glBlendEquation(gl.GL_FUNC_ADD)
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

            # Begin Occlusion Culling
            gl.glBeginQuery(gl.GL_ANY_SAMPLES_PASSED, self._OcclusionQueryID[0])

            # The current Back Temporary Texture is binded and is blended on
            # the Back Blending Texture through a normalized quad
            self._BackTemp.Bind(currId, 0)
            self._Canvas.BindBlendShader()
            self._Canvas.Draw()

            # End Occlusion Culling and get results
            gl.glEndQuery(gl.GL_ANY_SAMPLES_PASSED)
            anySamplePassed = gl.glGetQueryObjectuiv(self._OcclusionQueryID[0],
                                                     gl.GL_QUERY_RESULT)

        # Bind the standard frame buffer and select the back color attachments
        # for drawing
        gl.glDisable(gl.GL_BLEND)
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
        gl.glDrawBuffer(gl.GL_BACK_LEFT)

        # Bind the current Front Blending Texture and the Back Blending
        # Texture, blend them together and draw a normalized quad
        self._FrontBlender.Bind(currId, 0)
        self._BackBlender.Bind(1)
        self._Canvas.BindFinalShader()
        self._Canvas.Draw()


    def _TextureClear(self, index):
        # Clear color textures 1 and 2 or 4 and 5
        gl.glDrawBuffers(2, Attachments[3*index + 1:3 + index*3])
        gl.glClearColor(0, 0, 0, 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        # Clear depth texture 0 or 3
        gl.glDrawBuffer(Attachments[3*index + 0])
        gl.glClearColor(-1, -1, 0, 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    def _BackgroundClear(self, color = (0, 0, 0, 0)):
        # Clear color texture 6
        gl.glDrawBuffer(Attachments[6])
        gl.glClearColor(*color)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    def Clear(self):
        gl.glClearColor(0, 0, 0, 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

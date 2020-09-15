# If you need some insight about how OpenGL works, I recommed watching the
# amazing series made by The Cherno:
# https://www.youtube.com/watch?v=W3gAzLwfIP0&list=PLlrATfBNZ98foTJPJ_Ev03o2oq3-GGOS2
# About 90% of the things i know about OpenGL comes from there and it would be
# truly hypocritical not to recognize the fantastic teaching work that the
# Cherno has done

import OpenGL.GL as gl



# Class incorporating Vertex source string and Fragment source string
class ShaderProgramSource:

    def __init__(self):
        self.VertexSource = ''
        self.FragmentSource = ''

# Abstracting shader operations into a class
class Shader:

    def __init__(self, filepath):
        self._Filepath = filepath
        self._Source = self._ParseShader()
        self._RendererID = self._CreateShader()
        self._UniformLocationCache = {}

    def __del__(self):
        gl.glDeleteProgram(self._RendererID)

    def Bind(self):
        gl.glUseProgram(self._RendererID)

    def Unbind(self):
        gl.glUseProgram(0)


    # Second operation of Shader.__init__(filepath): read line by line the file
    # at 'filepath' and parse it into Vertex shader and Fragment shader
    def _ParseShader(self):
        sps = ShaderProgramSource()
        shadertype = ''

        with open(self._Filepath, 'r') as stream:

            for line in stream:
                if line == '#shader vertex\n':
                    shadertype = 'VERTEX'

                elif line == '#shader fragment\n':
                    shadertype = 'FRAGMENT'

                elif shadertype == 'VERTEX':
                    sps.VertexSource += line

                elif shadertype == 'FRAGMENT':
                    sps.FragmentSource += line

        return sps

    # Function called by self._CreateShader(): get shader source and compile
    # it. If an error occurs, the function displays it
    def _CompileShader(self, shadertype, source):
        id = gl.glCreateShader(shadertype)
        gl.glShaderSource(id, source)
        gl.glCompileShader(id)

        if gl.glGetShaderiv(id, gl.GL_COMPILE_STATUS) == gl.GL_FALSE:
            if shadertype == gl.GL_VERTEX_SHADER:
                print('Failed to compile vertex shader!')
            elif shadertype == gl.GL_FRAGMENT_SHADER:
                print('Failed to compile fragment shader!')

            raise RuntimeError(gl.glGetShaderInfoLog(id))
            gl.glDeleteShader(id)

            return 0

        return id

    # Third operation of Shader.__init__(filepath): create progra, compile both
    # shaders with self._CompileShader and attach them to the created program
    def _CreateShader(self):
        program = gl.glCreateProgram()
        vs = self._CompileShader(gl.GL_VERTEX_SHADER, self._Source.VertexSource)
        fs = self._CompileShader(gl.GL_FRAGMENT_SHADER, self._Source.FragmentSource)

        gl.glAttachShader(program, vs)
        gl.glAttachShader(program, fs)
        gl.glLinkProgram(program)
        gl.glValidateProgram(program)

        gl.glDeleteShader(vs)
        gl.glDeleteShader(fs)

        return program

    #Set and get uniforms

    def SetUniform1i(self, name, value):
        gl.glUniform1i(self._GetUniformLocation(name), value)

    def SetUniform1f(self, name, value):
        gl.glUniform1f(self._GetUniformLocation(name), value)

    def SetUniform4f(self, name, v0, v1, v2, v3):
        gl.glUniform4f(self._GetUniformLocation(name), v0, v1, v2, v3)

    def SetUniform2fv(self, name, vector):
        gl.glUniform2fv(self._GetUniformLocation(name), 1, vector)

    def SetUniformMat4f(self, name, matrix):
        gl.glUniformMatrix4fv(self._GetUniformLocation(name), 1, gl.GL_FALSE, matrix)

    def _GetUniformLocation(self, name):
        if name in self._UniformLocationCache:
            return self._UniformLocationCache[name]

        location = gl.glGetUniformLocation(self._RendererID, name)

        if location == -1:
            print('Warning: uniform "' + name + '" doesn\'t exist')

        self._UniformLocationCache[name] = location
        return location

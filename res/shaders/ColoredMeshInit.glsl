#shader vertex
#version 330 core


layout(location = 0) in vec4 position;


uniform mat4 u_MVP;


void main()
{
	gl_Position = u_MVP * position;
}



#shader fragment
#version 330 core


layout(location = 0) out vec4 dualDepth;


void main()
{
	// Since glBlendEquation() is set to GL_MAX, setting the x and y
	// components of StarDepth respectively to -gl_FragCoord.z and
	// gl_FragCoord.z, results, at the end of the blending proces, in
	// having the min rendered depth associated to the R channel and the
	// max rendered depth associated to the G channel
	dualDepth = vec4(-gl_FragCoord.z, gl_FragCoord.z, 0., 0.);
}

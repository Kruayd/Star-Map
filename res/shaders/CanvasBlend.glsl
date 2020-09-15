#shader vertex
#version 330 core


layout(location = 0) in vec4 position;
layout(location = 1) in vec2 texCoord;


out vec2 v_TexCoord;


void main()
{
	gl_Position = position;
	v_TexCoord = texCoord;
}



#shader fragment
#version 330 core


layout(location = 0) out vec4 color;


in vec2 v_TexCoord;


uniform sampler2D u_BackTemp;


void main()
{
	color = texture(u_BackTemp, v_TexCoord);
	if (color.a == 0)
	{
		discard;
	}
}

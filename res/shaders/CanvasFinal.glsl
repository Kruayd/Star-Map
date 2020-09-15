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


uniform sampler2D u_FrontBlender;
uniform sampler2D u_BackBlender;


void main()
{
	vec4 frontColor = texture(u_FrontBlender, v_TexCoord);
	vec4 backColor = texture(u_BackBlender, v_TexCoord);
	float alphaMultiplier = 1.0 - frontColor.w;
	
	color = frontColor + (backColor * alphaMultiplier);
}

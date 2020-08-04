#shader vertex
#version 330 core

layout(location = 0) in vec4 position;
layout(location = 1) in vec4 quadcolor; 

uniform mat4 u_MVP;

out vec4 v_QuadColor;

void main()
{
	gl_Position = u_MVP * position;

	v_QuadColor = quadcolor;
}

#shader fragment
#version 330 core

layout(location = 0) out vec4 color;

in vec4 v_QuadColor;

void main()
{
	color = v_QuadColor;
}

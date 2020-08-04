#shader vertex
#version 330 core

layout(location = 0) in vec4 position;
layout(location = 1) in vec4 starcolor;

uniform mat4 u_MVP;

out vec4 v_StarColor;

void main() {

	gl_Position = u_MVP * position;
	gl_PointSize = 100.;

	v_StarColor = starcolor;
}

#shader fragment
#version 330 core

layout(location = 0) out vec4 color;

in vec4 v_StarColor;

void main() {

	vec2 circCoord = (gl_PointCoord - 0.5) * 2;
	if (length(circCoord) > 0.1) {
		discard;
	}

	color = v_StarColor;

}

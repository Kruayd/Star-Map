#shader vertex
#version 330 core


layout(location = 0) in vec4 position;
layout(location = 1) in vec4 color;


uniform mat4 u_MVP;


out float v_Size;
out vec4 v_Color;


void main() {

	gl_Position = u_MVP * position;
	
	v_Size = 80/(gl_Position.w/5.);
	gl_PointSize = v_Size;

	v_Color = color;
}



#shader fragment
#version 330 core


layout(location = 0) out vec4 color;


in vec4 v_Color;
in float v_Size;


vec4 StarShape(vec4 StarColor, float pointsize){

	// gl_PointCoord has its origin on the low left corner
	// but we want it in the middle
	vec2 circCoord = (gl_PointCoord - 0.5) * 2;

	if (length(circCoord) > 1.) {
		discard;
	}

	// we want a constant "antialiasing" of 4 pixels on the border and,
	// since (pointsize - highstep) = 4 must be constant, it follows that:
	StarColor.a = smoothstep(1., 1 - (4/pointsize), length(circCoord));
	return StarColor;
}


void main() {

	color = StarShape(v_Color, v_Size);
}

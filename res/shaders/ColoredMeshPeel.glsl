#shader vertex
#version 330 core


layout(location = 0) in vec4 position;
layout(location = 1) in vec4 color;


uniform mat4 u_MVP;


out vec4 v_Color;


void main()
{
	gl_Position = u_MVP * position;

	v_Color = color;
}



#shader fragment
#version 330 core


layout(location = 0) out vec4 depthValue;
layout(location = 1) out vec4 forwardColor;
layout(location = 2) out vec4 backColor;


in vec4 v_Color;


uniform vec2 u_Res;
uniform sampler2D u_DepthTex;
uniform sampler2D u_FrontBlender;


void main()
{
	// Evaluating viewport normalized coordinates
	vec2 UV = gl_FragCoord.xy/u_Res;

	// Sampling Depth and Front Blending Textures
	vec4 depthBlender = texture(u_DepthTex, UV);
	vec4 forwardTemp = texture(u_FrontBlender, UV);

	// Since:
	// 1) Sampled forwardTemp values associated to fragments falling in
	//    the first or second depth case
	//    (fragDepth < nearestDepth || fragDepth > farthestDepth,
	//    nearestDepth < fragDepth && fragDepth < farthestDepth)
	//    should be preserved to the next passage
	// And since:
	// 2) Sampled forwardTemp values associated to fragments passing the
	//    depth test
	//    (fragment falls neither in the first case nor in the second)
	//    must be blended
	// forwardTemp is assigned to forwardColor, out on location 1
	forwardColor = forwardTemp;
	// The blending operation on the Back Temporary Texture is executed
	// outside this shader, thus we assign to backColor, out on location 2,
	// an empty vector, if the depth test is failed, or the object color
	// otherwise
	backColor = vec4(0., 0., 0., 0.);

	float fragDepth = gl_FragCoord.z;
	float nearestDepth = -depthBlender.x;
	float farthestDepth = depthBlender.y;
	float alphaMultiplier = 1.0 - forwardTemp.w;

	// If the following condition is satisfied, we have already peeled this
	// fragment, hence we reset the depth values of the current depth
	// texture. The MAX_BLENDING will take care of keeping or discarding
	// these values
	if (fragDepth < nearestDepth || fragDepth > farthestDepth)
	{
		depthValue = vec4(-1., -1., 0., 0.);
		return;
	}

	// If the following condition is satisfied, we have to peel again this
	// fragment. The MAX_BLENDING will take care of choosing the best
	// values
	if (nearestDepth < fragDepth && fragDepth < farthestDepth)
	{
		depthValue = vec4(-fragDepth, fragDepth, 0., 0.);
		return;
	}

	// If we made it here, this fragment is on the peeled layer, therefore
	// we need to shade it and make sure it is not peeled any farther
	vec4 color = v_Color;
	depthValue = vec4(-1., -1., 0., 0.);

	if (fragDepth == nearestDepth)
	{
		// Manual Blending described at
		// http://developer.download.nvidia.com/SDK/10/opengl/src/dual_depth_peeling/doc/DualDepthPeeling.pdf
		forwardColor.xyz += color.rgb * color.a * alphaMultiplier;
		forwardColor.w = 1 - alphaMultiplier * (1 - color.a);
	}
	else
	{
		backColor += color;
	}
}

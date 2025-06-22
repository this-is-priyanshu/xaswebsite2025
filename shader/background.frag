#version 100

precision highp float;

varying vec2 orig_uv;

uniform float uTime;
uniform float uDt;
uniform vec2 uResolution;

uniform vec4 uGlowColor;

uniform sampler2D uTexture0;

void main() {

	float aspect = uResolution.x / uResolution.y;
	vec2 uv = vec2(orig_uv.x * aspect, orig_uv.y);

	// TODO: this is a botch fix this with real math
	float hei = 3.; 
	float rad = sqrt(pow(aspect, 2.) + pow(hei - 1., 2.)) + exp(-aspect * 2.) / aspect;

	vec2 orig = vec2(0.0, -hei + 0.01 * sin(uTime/ 1000.)); 

	float dist = distance(uv, orig);

	if(dist > rad)
	{
		// Background

		float ang = uTime / 50000.;
		mat2 rot = mat2(cos(ang), sin(ang), -sin(ang), cos(ang));

		vec2 ruv = rot * (uv - orig) + orig;

		gl_FragColor = mix(texture2D(uTexture0, (ruv + vec2(1., aspect)) / 2.), vec4(uGlowColor.xyz * pow(rad / dist, 10.), 1.0), 0.3);
	}
	else
	{
		// The circle
		gl_FragColor = mix(uGlowColor, vec4(0.0, 0.0, 0.0, 1.0), pow(1. - dist / rad, 0.15));
	}

}

#version 100

precision highp float;

attribute vec3 aPos;

varying vec2 orig_uv;

void main() {
	gl_Position = vec4(aPos, 1.0);
	orig_uv = aPos.xy;
}

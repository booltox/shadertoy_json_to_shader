#!/usr/bin/env python3
import json
import sys
import argparse

if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")

# print("This is the name of the script: ", sys.argv[0])
# print("Number of arguments: ", len(sys.argv))
# print("The arguments are: ", str(sys.argv))
# print(f"Name of the script      : {sys.argv[1]=}")
# print(f"Arguments of the script : {sys.argv[1:]=}")

prefix = """
#version 150 core

uniform vec3      iResolution;           // viewport resolution (in pixels)
uniform float     iTime;                 // shader playback time (in seconds)
uniform float     iTimeDelta;            // render time (in seconds)
uniform int       iFrame;                // shader playback frame
uniform vec4      iMouse;                // mouse pixel coords. xy: current (if MLB down), zw: click
//uniform samplerXX iChannel0..3;          // input channel. XX = 2D/Cube
uniform sampler2D iChannel0;
uniform sampler2D iChannel1;
uniform sampler2D iChannel2;
uniform sampler2D iChannel3;
uniform vec4      iDate;                 // (year, month, day, time in seconds)
uniform float     iSampleRate;           // sound sample rate (i.e., 44100)

in vec2 fragCoord;
out vec4 fragColor;

"""

postfix = """

void main() {
    mainImage(fragColor, fragCoord);
}
"""

try:
    arg = sys.argv[1]
except IndexError:
    raise SystemExit("Usage: {sys.argv[0]} -f input.json")

parser = argparse.ArgumentParser()

parser.add_argument("--file", "-f", type=str, required=True)
args = parser.parse_args()

print(args.file)

with open(args.file) as f:
    json_decode = json.load(f)

print(json_decode['userName'])
result = []
for item in json_decode['shaders']:
    inf = item['info']
    shader_name = inf['name']
    print('-----------------')
    print(shader_name)
    rp = item["renderpass"]
    print("render pass:", len(rp))
    for p in rp:
        name = str(shader_name) + '_' + p['name']
        name = name.replace(" ", "_")
        print(name, ' type:', p['type'], ' id:', p['outputs'][0]['id'])
        inputs = p['inputs']
        for inp in inputs:
            print(' in:', inp['type'], ":", inp['id'])
        name += str('.fs')
        file = open(name, "w")
        file.write(prefix)
        file.write(p['code'])
        file.write(postfix)
        file.write
    print('-----------------')


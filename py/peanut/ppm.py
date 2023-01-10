#!/usr/bin/env python3

import os
import sys

def save_as_ppm(path, pixels, height, width) -> bool:
    with open(path, "wb") as ppm_out:
        ppm_out.write(f'P6\n{width} {height}\n255\n'.encode())
        for y in range(width):
            for x in range(height):
                pixel = pixels[y * width + x]
                color = bytearray([(pixel >> 16) & 0xFF, (pixel >> 8) & 0xFF, pixel & 0xFF])
                ppm_out.write(color)

def main():
    import random
    H = 256
    W = 256
    pixels = []
    for y in range(W):
        for x in range(H):
            pixel = (random.randint(0, 255) << 16) | (random.randint(0, 255) << 8) | (random.randint(0, 255) << 0)
            pixels.append(pixel)

    save_as_ppm("output.ppm", pixels, H, W)

if __name__ == "__main__":
    main()

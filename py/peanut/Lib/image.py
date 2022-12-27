#!/usr/bin/env python3

import os

class BufferedImage:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class ImageIO:
    __supported_exts = ['ppm']

    @staticmethod
    def read(path: str) -> BufferedImage:
        if not os.path.exists(path):
            raise OSError("File not found: " + path)
        ext = os.path.splitext(path)[1][1:]
        if ext not in ImageIO.__supported_exts:
            raise Exception(f"Can't read {ext} file")

        if ext == "ppm":
            return ImageIO.__read_ppm(path)

    @staticmethod
    def __read_ppm(path):
        PPM_MAGIC = b'P6'
        with open(path, "rb") as ppm:
            magic = ppm.read(2)
            if PPM_MAGIC != magic:
                raise IIOException("Image not PPM codec")

class IIOException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


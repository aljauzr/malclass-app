#!/usr/bin/env python3

import io
import math
import os
import sys
from tempfile import NamedTemporaryFile
from PIL import Image

class FileReader(object):
    def __init__(self, path_or_stream, file_backed=False):
        self.tmpfile = None
        if hasattr(path_or_stream, "name") and path_or_stream.name != "<stdin>":
            self.length = os.path.getsize(path_or_stream.name)
            self.file = path_or_stream
            self.name = path_or_stream.name
        else:
            if sys.version_info.major >= 3:
                infile = sys.stdin.buffer.read()
            else:
                infile = sys.stdin.read()
            self.length = len(infile)
            if file_backed:
                if sys.version_info.major >= 3:
                    file_mode = 'wb'
                    read_mode = 'rb'
                else:
                    file_mode = 'w'
                    read_mode = 'r'
                tmp = NamedTemporaryFile(delete=False, mode=file_mode)
                self.tmpfile = tmp.name
                tmp.write(infile)
                tmp.close()
                self.file = open(self.tmpfile, read_mode)
                self.name = self.tmpfile
            else:
                self.file = io.BytesIO(infile)
                self.name = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.tmpfile is not None:
            self.file.close()
            os.unlink(self.tmpfile)
            self.tmpfile = None
            self.file = None

    @staticmethod
    def new(path_or_stream, file_backed=False):
        if isinstance(path_or_stream, FileReader):
            return path_or_stream
        else:
            return FileReader(path_or_stream, file_backed=file_backed)

    def __len__(self):
        return self.length

    def read(self, n):
        if sys.version_info.major >= 3:
            return [i for i in self.file.read(n)]
        else:
            return map(ord, self.file.read(n))


def choose_file_dimensions(infile, input_dimensions=None):
    if input_dimensions is not None and len(input_dimensions) >= 2 and input_dimensions[0] is not None \
            and input_dimensions[1] is not None:
        return input_dimensions

    infile = FileReader.new(infile)
    num_bytes = len(infile)
    num_pixels = int(math.ceil(float(num_bytes) / 3.0))
    sqrt = math.sqrt(num_pixels)
    sqrt_max = int(math.ceil(sqrt))

    if input_dimensions is not None and len(input_dimensions) >= 1:
        if input_dimensions[0] is not None:
            if num_pixels % input_dimensions[0] == 0:
                return input_dimensions[0], num_pixels // input_dimensions[0]
            else:
                return input_dimensions[0], num_pixels // input_dimensions[0] + 1
        else:
            if num_pixels % input_dimensions[1] == 0:
                return num_pixels // input_dimensions[1], input_dimensions[1]
            else:
                return num_pixels // input_dimensions[1] + 1, input_dimensions[1]

    best_dimensions = None
    best_extra_bytes = None
    for i in range(int(sqrt_max), 0, -1):
        is_perfect = num_pixels % i == 0
        if is_perfect:
            dimensions = (i, num_pixels // i)
        else:
            dimensions = (i, num_pixels // i + 1)
        extra_bytes = dimensions[0] * dimensions[1] * 3 - num_bytes
        if dimensions[0] * dimensions[1] >= num_pixels and (best_dimensions is None or extra_bytes < best_extra_bytes):
            best_dimensions = dimensions
            best_extra_bytes = extra_bytes
        if is_perfect:
            break
    return best_dimensions


def file_to_png(infile, outfile, dimensions=None):
    reader = FileReader.new(infile)
    dimensions = choose_file_dimensions(reader, dimensions)
    dim = (int(dimensions[0]), int(dimensions[1]))
    img = Image.new('RGB', dim)
    pixels = img.load()
    row = 0
    column = -1
    while True:
        b = reader.read(3)
        if not b:
            break
        column += 1
        if column >= img.size[0]:
            column = 0
            row += 1
        if row >= img.size[1]:
            break
        color = [b[0], 0, 0]
        if len(b) > 1:
            color[1] = b[1]
        if len(b) > 2:
            color[2] = b[2]
        if not row >= img.size[1]:
            pixels[column, row] = tuple(color)
    img.save(outfile, format="PNG")
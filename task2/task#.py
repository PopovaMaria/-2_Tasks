import sys
from pathlib import Path
import math
import json
from collections import namedtuple


Coordinate = namedtuple('Coordinate', 'x y z')


class InputParser:
    @classmethod
    def parse(cls):
        file = sys.argv[1]
        file = file.strip()
        with Path(file).open() as stream:
            content = stream.read()
            return cls._transform_line_to_triangles_data(content)

    @staticmethod
    def _transform_line_to_triangles_data(line):
        line = line.replace('A', '"A"')
        line = line.replace('B', '"B"')
        line = line.replace('C', '"C"')
        line = line.replace('triangle1', '"triangle1"')
        line = line.replace('triangle2', '"triangle2"')
        return json.loads(line)


class Triangle:
    def __init__(self, a: Coordinate, b: Coordinate, c: Coordinate):
        self._a = a
        self._b = b
        self._c = c

    @classmethod
    def from_dict(cls, data: dict):
        coordinates = {name.lower(): Coordinate(*data[name]) for name in ('A', 'B', 'C')}

        obj = Triangle(**coordinates)
        return obj

    @property
    def sides_length(self):
        ab = self._side_length(self._a, self._b)
        ac = self._side_length(self._a, self._c)
        bc = self._side_length(self._b, self._c)
        return ab, ac, bc

    def is_same(self, other: 'Triangle'):
        result = {a / b for a, b in zip(self.sides_length, other.sides_length)}
        return len(result) == 1

    @staticmethod
    def _side_length(a: Coordinate, b: Coordinate):
        length = math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2)
        return length


if __name__ == '__main__':
    data = InputParser.parse()
    first_triangle_data = data.popitem()[1]
    second_triangle_data = data.popitem()[1]

    first_triangle = Triangle.from_dict(first_triangle_data)
    second_triangle = Triangle.from_dict(first_triangle_data)
    print(first_triangle.is_same(second_triangle))

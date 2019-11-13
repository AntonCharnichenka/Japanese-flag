"""
This module contains solution to Syberry task 'Japanese flag'.

As all the solution should be concentrated in flag.py module according to the task requirements,
all  the related logic is placed in this module, otherwise i would prefer to separate it into separate modules
within 'flag' package.

The size of a flag can optionally be passed as a command line argument: 'python3.7 flag.py 6'.
"""


import sys
import argparse
from dataclasses import dataclass


# Exceptions
class ArgumentError(Exception):
    pass


# Containers
@dataclass
class CharactersDTO:
    border: str
    body: str
    circle_border: str
    circle_body: str


@dataclass
class CircleCoordinatesDTO:
    left: int
    right: int


@dataclass
class CoordinatesDTO:
    body_width: int
    body_height: int
    border_width: int
    border_height: int
    circle_starting_row: int
    horizontal_center: int
    circle_coordinates: CircleCoordinatesDTO


# Utils
def create_parser():
    parser = argparse.ArgumentParser(
        prog='Japanese flag',
        description='solution to Syberry task'
    )
    parser.add_argument('n', nargs='?', default=None, help="flag size")

    return parser


def check_python_version():
    if sys.version_info[0] < 3 or (sys.version_info[0] == 3 and sys.version_info[1] < 7):
        print('This script should be run with Python3.7. Exit.')
        sys.exit(1)


def validate(n: int) -> None:
    message = None

    if not isinstance(n, int):
        message = 'The input argument "n" is of invalid type (should be "int".)'
    elif n % 2 != 0:
        message = 'The input argument "n" is not even integer number.'
    elif n < 0:
        message = 'The input argument "n" is not positive integer number.'

    if message:
        raise ArgumentError(message)


def calculate_coordinates(n: int) -> CoordinatesDTO:
    body_width = 3*n
    body_height = 2*n
    border_width = body_width + 2
    border_height = body_height + 2
    circle_starting_row = n//2 + 1
    horizontal_center = border_width//2
    circle_coordinates = CircleCoordinatesDTO(horizontal_center-1, horizontal_center)

    return CoordinatesDTO(
        body_width, body_height, border_width, border_height,
        circle_starting_row, horizontal_center, circle_coordinates
    )


def convert_to_str(flag_data: list) -> str:
    output_str = ''
    for row in flag_data:
        str_row = ''.join(row)
        output_str += str_row

    return output_str


def fill_circle_border(row: list, circle_coordinates: CircleCoordinatesDTO, circle_border_character: str) -> None:
    row[circle_coordinates.left] = circle_border_character
    row[circle_coordinates.right] = circle_border_character


def fill_circle_body(row: list, circle_coordinates: CircleCoordinatesDTO, circle_body_character: str) -> None:
    for index in range(circle_coordinates.left + 1, circle_coordinates.right):
        row[index] = circle_body_character


def mirror(half_flag_data: list) -> list:
    other_half_flag_data = half_flag_data[::-1]
    return half_flag_data + other_half_flag_data


# Main
def flag(n: int, characters=('#', ' ', '*', '0')):
    try:
        validate(n)
    except ArgumentError as exc:
        print(exc.args[0])
        sys.exit(1)

    characters = CharactersDTO(*characters)
    coordinates = calculate_coordinates(n)
    half_flag_data = []

    # build and add upper border row
    border_line = list(characters.border*coordinates.border_width) + ['\n']
    half_flag_data.append(border_line)

    # build and add upper body rows
    for _ in range(coordinates.body_height//2):
        half_flag_data.append(
            list(f'{characters.border}{characters.body*coordinates.body_width}{characters.border}') + ['\n']
        )

    # build and add inner circle
    for row in half_flag_data[coordinates.circle_starting_row:]:
        fill_circle_border(row, coordinates.circle_coordinates, characters.circle_border)
        fill_circle_body(row, coordinates.circle_coordinates, characters.circle_body)

        coordinates.circle_coordinates.left -= 1
        coordinates.circle_coordinates.right += 1

    # build full flag
    flag_data = mirror(half_flag_data)

    return convert_to_str(flag_data)


if __name__ == '__main__':
    check_python_version()

    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    n = namespace.n

    print('<Japanese flag>\n')
    if n:
        print(' - n={}'.format(n))
        print(flag(int(n)))
    else:
        print('- n=2:')
        print(flag(2))

        print('- n=4:')
        print(flag(4))

        print('- n=6:')
        print(flag(6))

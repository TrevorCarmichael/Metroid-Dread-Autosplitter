import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import pytest
import variables

from route import Route

route_data = [
    ["u", 0],
    ["u", 1],
    ["u", 2],
    ["l", 0, 1],
    ["l", 1, 2]
]

route = Route(route_data)

def test_get_current_split_1():
    assert route.get_current_split() == ["u", 0]

def test_progress_route():
    route.progress_route()
    assert route.get_current_split() == ["u", 1]

def test_is_complete_1():
    assert route.is_complete() == False

def test_get_split_text_1():
    assert route.get_split_text(0) == "Charge Beam"

def test_get_split_text_2():
    assert route.get_split_text(3) == "Transport from Artaria to Cataris"

def test_set_route_position_1():
    route.set_route_position(-10)
    assert route.route_pos == 0

def test_set_route_position_1():
    route.set_route_position(1000)
    assert route.route_pos == 4

def test_set_route_position_1():
    route.set_route_position(3)
    assert route.route_pos == 3







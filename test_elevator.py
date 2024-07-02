import pytest
import subprocess
from elevator import validate_input, move_to_floor, print_output

# constants
BASE_ARGS = ["program", "elevator"]

####################################
####        UNIT TESTING        ####
####################################

# VALIDATE_INPUT()
@pytest.mark.parametrize("args", [
    [*BASE_ARGS, "start=1", "floor=2,3,4"], # simple test
    [*BASE_ARGS, "start=12", "floor=2,9,1,32"], # provided test
    [*BASE_ARGS, "start=1", "floor=" + ",".join(map(str, range(2, 1001)))], # large floor list 
    [*BASE_ARGS, "start=1", "floor=10000000000,1"], # large floor numbers
    [*BASE_ARGS, "start=0", "floor=1,2,3"], # start at 0
    [*BASE_ARGS, "start=10", "floor=9,0,7"], # visit 0
    [*BASE_ARGS, "start=1", "floor=4"], # floors list is len 1
])
def test_validate_input_valid(args):
    assert validate_input(args) is None

@pytest.mark.parametrize("args", [
    [*BASE_ARGS, "floor=2,3,4,5"], # missing start input
    [*BASE_ARGS, "start=", "floor=2,3,4,5"], # missing start value
    [*BASE_ARGS, "start=a", "floor=2,3,4,5"], # non number start value
    [*BASE_ARGS, "start=1a", "floor=2,3,4,5"], # non number start value
    [*BASE_ARGS, "start=1,4", "floor=2,3,4,5"], # list start value
    [*BASE_ARGS, "start=1"], # missing floor input
    [*BASE_ARGS, "start=1", "floor="],# missing floor value
    [*BASE_ARGS, "start=1", "floor=a"], # non number floor value
    [*BASE_ARGS, "start=1", "floor=2,3,a,5"], # non number value in list
    [*BASE_ARGS, "start=1", "floor=2,3,1a,5"], # non number value in list
    [*BASE_ARGS, "start=1", "floor=2,3,,5"], # missing number in list
    [*BASE_ARGS, "start=1", "floor=2,-3,4,5"], # negative number in list
])
def test_validate_input_invalid(args):
    with pytest.raises(SystemExit):
        validate_input(args)

# MOVE_TO_FLOOR()
@pytest.mark.parametrize("floors_to_visit, expected_travel_time", [
    ([5, 1, 5, 3], 100), # simple test
    ([12, 2, 9, 1, 32], 560), # given test
    ([4, 4, 4, 4, 4, 4, 4], 0), # same floor
    (list(range(10000)), 99990), # large list test
    ([0, 2, 0, 2, 0], 80), # 0 in list 
])
def test_move_to_floor_valid(floors_to_visit, expected_travel_time):
    assert move_to_floor(floors_to_visit) == expected_travel_time

@pytest.mark.parametrize("floors_to_visit", [
    ([]), # empty list test
    ([1]), # single value list
    ([-1, 1, 3]), # negative numbers at list[0]
    ([1, -1, 3]), # negative numbers in list
    ([1, 1, -3]), # negative numbers at end of list
    ([1, "a", "b",]), # string in list
    ([1, 1.3, 3]), # double in list
    ([3, 1, True]), # boolean in list
    ("a"), # string
    (2), # int
    (True), # boolean
    (2.2), # double 
])
def test_move_to_floor_invalid(floors_to_visit):
    with pytest.raises(ValueError):
        move_to_floor(floors_to_visit)

# PRINT_OUTPUT()
@pytest.mark.parametrize("travel_time, floors_visited, expected_output", [
    (1, [1, 2, 3], "1 1,2,3\n"),
    (560, [12, 2, 9, 1, 32], "560 12,2,9,1,32\n"),
])     
def test_print_output_valid(travel_time, floors_visited, expected_output, capsys):
    print_output(travel_time, floors_visited)
    captured = capsys.readouterr()
    assert captured.out == expected_output

@pytest.mark.parametrize("travel_time, floors_visited", [
    (1.2, [1, 2, 3]),
    ("a", [1, 2, 3]),
    (20, [1, 2, 3.0]),
    (20, [1, 2, "a"]),
    (True, [1, 2, 3.0]),
    (20, [1, 2, False]),
    (20, 2),
    (20, 2.2),
    (20, False),
    (20, "a"),
])     
def test_print_output_invalid(travel_time, floors_visited):
    with pytest.raises(ValueError):
        print_output(travel_time, floors_visited)

####################################
####    INTEGRATION TESTING     ####
####################################

def run_elevator(args):
    result = subprocess.run(['python', 'Elevator.py'] + args, capture_output=True, text=True)
    return result.stdout.strip()
 
@pytest.mark.parametrize("args, expected_output", [
    (["elevator", "start=1", "floor=2,3,4"], "30 1,2,3,4"), # simple test
    (["elevator", "start=12", "floor=2,9,1,32"], "560 12,2,9,1,32"), # provided test
    (["elevator", "start=1", "floor=" + ",".join(map(str, range(2, 1001)))], "9990 1," + ",".join(map(str, range(2, 1001)))), # large floor list 
    (["elevator", "start=1", "floor=10000000000,1"], "199999999980 1,10000000000,1"), # large floor numbers
])
def test_input_valid(args, expected_output):
    assert run_elevator(args) == expected_output

@pytest.mark.parametrize("args, expected_output", [
    (["elevator", "start=0", "floor=1,2,3"], "30 0,1,2,3"), # start at 0
    (["elevator", "start=10", "floor=9,0,7"], "170 10,9,0,7"), # visit 0
    (["elevator", "start=1", "floor=4"], "30 1,4"), # floors list is len 1
])
def test_edge_cases(args, expected_output):
    assert run_elevator(args) == expected_output

@pytest.mark.parametrize("args", [
    ["elevator", "floor=2,3,4,5"], # missing start input
    ["elevator", "start=", "floor=2,3,4,5"], # missing start value
    ["elevator", "start=a", "floor=2,3,4,5"], # non number start value
    ["elevator", "start=1a", "floor=2,3,4,5"], # non number start value
    ["elevator", "start=1,4", "floor=2,3,4,5"], # list start value
    ["elevator", "start=1"], # missing floor input
    ["elevator", "start=1", "floor="],# missing floor value
    ["elevator", "start=1", "floor=a"], # non number floor value
    ["elevator", "start=1", "floor=2,3,a,5"], # non number value in list
    ["elevator", "start=1", "floor=2,3,1a,5"], # non number value in list
    ["elevator", "start=1", "floor=2,3,,5"], # missing number in list
    ["elevator", "start=1", "floor=2,-3,4,5"], # negative number in list
])
def test_invalid_inputs(args):
    result = subprocess.run(['python', 'Elevator.py'] + args, capture_output=True, text=True)
    assert "Usage:" in result.stdout
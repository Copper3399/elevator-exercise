import sys
import re

# constants
SINGLE_FLOOR_TRAVEL_TIME = 10

def main():
    try:
        validate_input(sys.argv)
    
        # add start floor to list
        floors_to_visit = [int(re.search(r'\d+', sys.argv[2]).group())]

        # add the other floors to list
        floors_string = re.search(r'\d+(?:,\d+)*', sys.argv[3]).group()
        floors_to_visit += [int(number) for number in floors_string.split(',')]

        # visit all floors
        travel_time = move_to_floor(floors_to_visit)

        print_output(travel_time, floors_to_visit)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def validate_input(argv) -> None:
    """
    Validates program arguments

    Args:
        argv (list): the sys.argv list.
    """
    if (len(argv) != 4):
        print("Invalid number of arguments.")
        print("Usage: python Elevator.py [start floor] [list of floors to visit]" + \
              "\ne.g. elevator start=12 floor=2,9,1,32")
        sys.exit(1)

    if (argv[1] != 'elevator' 
            or not re.match(r'start=\d+$', argv[2])
            or not re.match(r'floor=\d+(?:,\d+)*$', argv[3])):
        print("Invalid input format. Please provide valid arguments.")
        print("Usage: python Elevator.py [start floor] [list of floors to visit]" + \
              "\ne.g. elevator start=12 floor=2,9,1,32")
        sys.exit(1)


def move_to_floor(floors_to_visit) -> int:
    """
    Iteratively calculates total travel time for elevator from start to end of its floor list.

    Args:
        floors_to_visit (list): a list of ints representing the floors the elevator must visit.

    Returns:
        int: total travel time.
    """
    # verify input
    if (not isinstance(floors_to_visit, list)
            or not all(isinstance(num, int) and not isinstance(num, bool) for num in floors_to_visit)
            or len(floors_to_visit) < 2
            or any(num < 0 for num in floors_to_visit)):
        raise ValueError("input to move_to_floor: floors_to_visit must be a list containing all positive numbers and be have at least 2 indices")

    travel_time = 0
    
    for i in range(len(floors_to_visit) - 1):
        travel_time += (abs(floors_to_visit[i] - floors_to_visit[i + 1])) * SINGLE_FLOOR_TRAVEL_TIME
    
    return travel_time


# def moveToFloor(floors_to_visit, index = 0):
#     """
#     Recursively calculates total travel time for elevator from its current floor to the end of its floor list.

#     Args:
#         floors_to_visit (list): a list of ints representing the floors the elevator must visit.
#         index (int): the index into the floorsToVisit list. ie: the current floor.

#     Returns:
#         int: total travel time.
#     """
#     if (floors_to_visit.size() < 2
#             or any(num < 0 for num in floors_to_visit)):
#         raise ValueError("input to move_to_floor: floors_to_visit must contain all positive numbers and be have at least 2 indices")

#     travel_time = (abs(floors_to_visit[index] - floors_to_visit[index + 1])) * SINGLE_FLOOR_TRAVEL_TIME

#     if (index < len(floors_to_visit) - 2):    
#         travel_time += moveToFloor(floors_to_visit, index + 1)
    
#     return travel_time


def print_output(travel_time, floors_visited) -> None:
    """
    Prints the output of the elevator according to program specifications.

    Args:
        travel_time (int): the total travel time of the elevator.
        floors_visited (list): a list of ints representing the floors the elevator visited.
    """
    # verify input
    if (not isinstance(travel_time, int)):
        raise ValueError("input to print_output: travel_time must be an int")

    if (not isinstance(floors_visited, list)
            or not all(isinstance(num, int) and not isinstance(num, bool) for num in floors_visited)):
        raise ValueError("input to print_output: floors_visited must be a list of ints")

    print(str(travel_time), end=' ')
    print(*floors_visited, sep=',')


# call main function to start program
if __name__ == "__main__":
    main()
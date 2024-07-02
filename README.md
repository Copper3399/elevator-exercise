# elevator-exercise
This is a coding exercise for simulating an elevator

# Assumptions:
- Expected input should be \[list of floors to visit\] \(e.g. elevator start=12 floor=2,9,1,32\), as provided in the prompt
- Expected output should be \[total travel time, floors visited in order\] \(e.g. 560 12,2,9,1,32\), as provided in the prompt
- The single floor travel time is 10, as provided in the prompt
- Input must include:
  - Start floor
  - At least one floor in the floor list
- Floors can be in range \[0-infinity\)
- All floors are positive integers. Floors cannot include:
  - Negative numbers
  - Alpha characters
  - Decimal numbers
- Elevator always travels directly to the next floor in the list

# Unimplemented Features:
- Alternative floor shemes and a method to chose which sheme to use. ex:
  - Including negative number floors
  - Including alpha character floors
  - Including decimal number floors
- Smart algorithm to more efficiently traverse the floor list
- Adding a new floor to the floor list as the elevator runs

household = f'''
The environment is described by the following scene objects:
The size of the environmental site is (0,10,0,10). The active area of the car does not exceed this range.
Scene objects:
['name': 'RestRoom', 'color': 'yellow', 'position and size': (0, 3, 7.5, 10.0)]
['name': 'MasterBedroom', 'color': 'green', 'position and size': (7, 10, 5.5, 10.0)]
['name': 'RestRoom2', 'color': 'pink', 'position and size': (7, 10, 2, 4)]
['name': 'ExerciseRoom', 'color': 'deepblue', 'position and size': (4, 6, 8, 10)]
['name': 'LivingRoom', 'color': 'blue', 'position and size': (2, 5, 3, 6)]
['name': 'Kitchen', 'color': 'cyan', 'position and size': (0, 1, 0, 2)]
['name': 'DiningRoom', 'color': 'purple', 'position and size': (2, 4, 0, 1)]
['name': 'Bedroom', 'color': 'red', 'position and size': (5, 10, 0, 2)]

'''

examples_llm10='''
Examples:
Input:
initial position: [3,7]
instruction:'Go to restroom2 and then go to diningroom and always avoid livingroom and bedroom.'
STL:'eventually(x>5 and x<10 and y>0 and y<2) and ((x>5 and x<10 and y>0 and y<2) implies eventually(x>2 and x<4 and y>0 and y<1)) and always( not (x>2 and x<5 and y>3 and y<6)and not (x>7 and x<10 and y>2 and y<4))'
Output:
[[3, 7], [6, 7],[6, 1],[3, 0.5]]

Input:
initial position: [0,0]
instruction:'Going into livingroom and then entering masterbedroom.'
STL:'always((x>2 and x<5 and y>3 and y<6) implies eventually(x>7 and x<10 and y>5.5 and y<10))'
Output:
[[0,0], [4,5], [8,8]]

Input:
initial position: [6,2]
instruction:'Go to restroom and then go to kitchen and be careful not to go through livingroom.'
STL:always( not (x>2 and x<5 and y>3 and y<6)) and ((x>0 and x<3 and y>7.5 and y<10) implies eventually(x>0 and x<1 and y>0 and y<2))
Output:
[[6, 2],[6, 7],[2, 8],[0.5,1]]

'''

examples_llm11='''
Examples:
Input:
initial position: [3,7]
instruction:'Go to restroom2 and always avoid livingroom and bedroom.'
STL:'eventually(x>5 and x<10 and y>0 and y<2) and always( not (x>2 and x<5 and y>3 and y<6)and not (x>7 and x<10 and y>2 and y<4))'
Failure trajectory:[[3, 7], [4, 6],[5, 1]]

Output:
[[3, 7], [6, 7],[6, 1]]

Input:
initial position: [0,0]
instruction:'Going into livingroom and then entering masterbedroom.'
STL:'always((x>2 and x<5 and y>3 and y<6) implies eventually(x>7 and x<10 and y>5.5 and y<10))'
Failure trajectory:[[0, 0], [4, 6],[5, 1]]
Output:
[[0,0], [4,5], [8,8]]

Input:
initial position: [6,2]
instruction:'Go to restroom and then go to kitchen and be careful not to go through livingroom.'
STL:always( not (x>2 and x<5 and y>3 and y<6)) and ((x>0 and x<3 and y>7.5 and y<10) implies eventually(x>0 and x<1 and y>0 and y<2))
Failure trajectory:[[6, 2], [4, 6],[5, 1]]
Output:
[[6, 2],[6, 7],[2, 8],[0.5,1]]

'''

examples_llm12='''
Examples:
Input:
instruction:' Reach livingroom within 3 seconds, then get to bedroom within 5 seconds, and subsequently arrive at exerciseroom within 8 seconds. Do not pass through masterbedroom.'
target sequence: [[0,0.5],[3, 4],[8, 3],[6, 4],[ 6, 7],[ 5, 9]]
Output:
[[[0, 0.5],0],[[3, 4],2], [[8, 3],4], [[6, 4],5], [[6, 7],7], [[5, 9],8]]

Input:
instruction:'Make your path towards the room with a cyan hue, then migrate to the bedroom and hold there for 5 seconds, and finally, proceed to the restroom. Always remember, do not touch the two distinct areas shaded in blue.'
target sequence: [[1,4],[0.5, 1],[6, 1],[6, 7],[ 2, 8]]
Reasoning:In the natural language instruction it is required to stay in the bedroom for 5 seconds, so [[6, 1],4], [[6, 1],9] means stay in place in the bedroom for 5 seconds
Output:
[[[1,4],0],[[0.5, 1],2], [[6, 1],4], [[6, 1],9], [[6, 7],12], [[2, 8],14]]
'''

reprompt_llm14='The last time the generated code was wrong, please discard the inherent thinking and rethink it. '
# -*- coding: utf-8 -*-

EXTRACT_KEY_TRAJECTORY = """

I will give you a text about thinking and analyzing about path selection, please extract the final trajectory from the text.
e.g., if the text has statements like
"**Final Output:**
```json.
{{
    "trajectory": [
        [1, 4],
        [1.5, 8.75],
        [9, 8],
        [8.5, 7.75],
        [3, 5],
        [3.5, 4.5],
        [0.5, 1],
        [3, 0.5],
        [7.5, 1]
    ]
}}"     

Then output [[1, 4], [1.5, 8.75], [9, 8], [8.5, 7.75], [3.5, 4.5], [0.5, 1], [3, 0.5], [7.5, 1]]

The format of the output trajectories is:
[[a1, b1],[a2, b2][a3, b3]]
Here, [a1, b1], [a2, b2], [a3, b3] represent the coordinates.

The text is: {text_str}
Let us take a deep breath. Think carefully and logically.Please self-verification that whether it is the final trajectory of this text.

"""

EXTRACT_KEY_PWL = """
I will give you a text about thinking and analyzing about path and time selection, please extract the final trajectory from the text.
e.g., if the text has statements like
"**Final Output:**
```json.
{{
    "pwl": [
        [[1, 4],1],
        [[1.5, 8.75],3],
        [[9, 8],5],
        [[8.5, 7.75],8.5],
        [[3, 5],12],
        [[3.5, 4.5],16.3],
        [[0.5, 1],19.9],
        [[3, 0.5],21],
        [[7.5, 1],24]
    ]
}}"     

Then output [[[1, 4],1],[[1.5, 8.75],3],[[9, 8],5],[[8.5, 7.75],8.5],[[3, 5],12],[[3.5, 4.5],16.3],[[0.5, 1],19.9],[[3, 0.5],21],[[7.5, 1],24]]

The format of the output trajectories is:
[[[a1, b1],t1],[[a2, b2],t2],[[a3, b3],t3]]
Here, [a1, b1], [a2, b2], [a3, b3] represent the coordinates. t1,t2,t3 denote the moments at the corresponding coordinate points, respectively.

The text is: {text_str}
Let us take a deep breath. Think carefully and logically.Please self-verification that whether it is the final trajectory of this text.
"""


USER_PROMPT_10 = """
I will provide the position and size of each box in the environment, a natural language instruction to enter or avoid boxes, and a Signal Temporal Logic (STL) expression. Your task is to disregard any timing constraints present in the natural language instructions and generate a trajectory that meets the given conditions.
The position and size of each box are described by the coordinates: (x_start, x_end, y_start, y_end). The values x_start, x_end define the box's horizontal bounds, and y_start, y_end define the vertical bounds.
STL is an extension of propositional logic that incorporates time. STL operators include: and, or, not, implies, until, eventually, always, and next. The until, eventually, and always operators may include time constraints.
{env}

The generated trajectories should be in the following format:
[[a1, b1],[a2, b2][a3, b3]]
Here, [a1, b1], [a2, b2], [a3, b3] represent the coordinates of the robot at different points in its path.

Input:
The initial position of the robot is{initial_position}.
instruction:{input_instruction}
STL:{stl}

Task: 
(1)Disregard the timing constraints in the natural language instructions.
(2)Generate a trajectory that satisfies both the positional information constraints stated in the natural language instructions and the STL expression.
(3)Ensure that the line segment connecting each consecutive pair of points in the generated trajectory does not pass through any area that the robot is instructed to avoid.
(4)The generated trajectory should maintain a reasonable spatial distance from the areas to be avoided.

Visualize the state after each step of reasoning.Conduct a self-check to verify that the piecewise-linear trajectory formed by these points complies with the requirements of the natural language instructions (specifically, the positional information constraints).

{example}
"""

USER_PROMPT_10_navigation = """
I will provide the position and size of each box in the environment, a natural language instruction to enter or avoid boxes, and a Signal Temporal Logic (STL) expression. Your task is to disregard any timing constraints present in the natural language instructions and generate a trajectory that meets the given conditions.
The position and size of each box are described by the coordinates: (x_start, x_end, y_start, y_end). The values x_start, x_end define the box's horizontal bounds, and y_start, y_end define the vertical bounds.
STL is an extension of propositional logic that incorporates time. STL operators include: and, or, not, implies, until, eventually, always, and next. The until, eventually, and always operators may include time constraints.
{env}

The generated trajectory should be in the following format:
[[a1, b1],[a2, b2][a3, b3]]
Here, [a1, b1], [a2, b2], [a3, b3] represent the coordinates of the robot at different points in its path.

Input:
The initial position of the robot is{initial_position}.
instruction:{input_instruction}
STL:{stl}

Task: 
(1)Disregard the timing constraints in the natural language instructions.
(2)Generate a trajectory that satisfies both the positional information constraints stated in the natural language instructions and the STL expression.
(3)Ensure that the line segment connecting each consecutive pair of points in the generated trajectory does not pass through any area that the robot is instructed to avoid.
(4)The generated trajectory should maintain a reasonable spatial distance from the areas to be avoided.
(5)When you need to enter a area, go to the center of the area.
(6)Visualize the scene graph and the movement trajectory with each step. Determine whether an obstacle is crossed. If an obstacle is crossed, remember the position of the obstacle, replan the route and bypass the obstacle.

Let us take a deep breath. Think carefully and logically. Visualize the state after each reasoning step. Please self-verification that the piecewise linear trajectory composed of these trajectory points conforms to the requirements of the natural language instructions(positional information constraints).

{example}
"""


USER_PROMPT_11 = """
I will provide the position and size of each box in the environment, a natural language instruction to enter or avoid boxes, and a Signal Temporal Logic (STL) expression. Please ignore timing constraints in natural language instructions and generate a trajectory that satisfies the given conditions.
The position and size of each box are described by the coordinates: (x_start, x_end, y_start, y_end). The values x_start, x_end define the box's horizontal bounds, and y_start, y_end define the vertical bounds.
STL is an extension of propositional logic that incorporates time. STL operators include: and, or, not, implies, until, eventually, always, and next. The until, eventually, and always operators may include time constraints.
{env}

The output trajectory is represented in format:
[[a1, b1],[a2, b2][a3, b3]]
Here, [a1, b1], [a2, b2], [a3, b3] represent the robot's coordinates.

Input:
The initial position of the robot is {initial_position}.
instruction:{input_instruction}
STL:{stl}
Failure trajectory that do not meet the requirements of natural language and STL:{pwl}

The task is: Ignore timing constraints in natural language instructions. Generate the trajectory that satisfies the positional information constraints in natural language instructions and STL. And ensure that the line segment between each generated trajectory point does not pass through the area to be avoided. The generated trajectory tries to maintain an appropriate spatial distance from the area to be avoided. When you need to enter a area, go to the center of the area.
Let us take a deep breath. Thinking about the wrong reasons for failure trajectory. Think carefully and logically. Visualize the state after each reasoning step. Please self-verification that the piecewise linear trajectory composed of these trajectory points conforms to the requirements of the natural language instructions(positional information constraints).
Please do not return the json format.
{example}
"""

USER_PROMPT_12 = """
I will provide the position and size of each box in the environment, a natural language instruction, and a series of trajectory points. This series of trajectory points represents the coordinates that the robot will reach in sequence. It is crucial to carefully consider the time - related information provided in the natural language instruction. Your task is to determine the time at which the robot reaches each of these trajectory points.
The position and size of each box are described by the coordinates: (x_start, x_end, y_start, y_end). The values x_start, x_end define the box's horizontal bounds, and y_start, y_end define the vertical bounds.

{env}

The expected output format is: 
[[[a1, b1], t1] , [[a2, b2], t2] , [[a3, b3], t3]]
Here, [a1, b1], [a2, b2], [a3, b3] represent the coordinate positions of the robot at time t1, t2, and t3, respectively. 

Input:
Instruction:{input_instruction}
Target sequence: {target}
Task: 
(1)Analyze the time information present in the natural language instruction.
(2) For each coordinate point in the target sequence, determine its corresponding arrival time to one decimal place, where the number of decimal places can only be taken as 0 or 5. 
Assume that in this scenario, the unit of position distance is meters and the unit of time is seconds. The maximum speed of the robot is 3 meters per second, and the maximum angular speed is 5. Please ensure that the time interval between each pair of target points is large enough so that the robot can arrive on time.
(3)Mark each coordinate point in the target sequence with its respective arrival time.
(4)Please do not return the json format.
Let us take a deep breath. Let us think step by step. Please self-check that the arrival time of each coordinate trajectory point conforms to the requirements of the natural language instructions.
{add_navigation}
{example}
"""


USER_PROMPT_14 = """
You are a python code generator. 
You need to generate a controller program (python script).
Assume in a unicycle kinematic modeling system that does not consider balance issues, the state variables include two-dimensional plane coordinates x (horizontal axis), y (vertical axis), and θ (orientation Angle). The control input variables are linear velocity v and angular velocity w in the current direction. 
The function of the generated controller is to output the control variables that satisfy the constraints according to the current state variables and the desired goal state. The controller needs to calculate the linear and angular velocities according to the target position.

The unit of linear velocity is meters per second (m/s), the unit of orientation angle is radian(rad), and the unit of angular velocity is radians per second (rad/s). The position coordinates x and y are in meters. The time unit is seconds.

The azimuth angle θ is defined as the angle formed by rotating counter clockwise from the positive direction of the X - axis to the vehicle's traveling direction. The range of the azimuth angle is 0<=θ <2Π. 
This unicycle kinematic model is as follows.
dx/dt = v * cos(θ)
dy/dt = v * sin(θ)
dθ/dt = w
Here, dx/dt and dy/dt denote the speed of the car in the x and y directions, respectively. v is the linear velocity.θis the orientation angle. w is the angular velocity.

The generated v and w this time will be used in the Euler method of numerical analysis to update the values of state variables. The calculation process of the Euler method is as follows:
x' = x + cos(θ) * v * dt
y' = y + sin(θ) * v * dt
θ' = θ + w * dt
The obtained x', y', and θ' are the new state variable values, dt is the step size and is set to 0.1 seconds.

The position and size of each area are described by the coordinates: (x_start, x_end, y_start, y_end). The values x_start, x_end define the square area's horizontal bounds, and y_start, y_end define the vertical bounds. 
{env}

The natural language instruction:{nl}
The initial state is {initial_state}, and the list elements denote x,y,θ, respectively
The target trajectory that need to be reached in turn is :{target}
The maximum linear velocity was set to 5 m/s and the absolute value of the maximum angular velocity is 5 rad/s.

The format of the target trajectory is [[[a1, b1], t1] , [[a2, b2], t2] , [[a3, b3], t3]]
Here, [a1, b1], [a2, b2], [a3, b3] represent the target coordinate positions that need to be reached in turn at time t1, t2, and t3, respectively.

Task: Generate python code that functions as a controller. 
{reprompt}. Let us take a deep breath. Think carefully and logically, explaining your answer step by step. Please self-verification whether there are any mistakes. If there are mistakes, please rethink step by step.

The requirements of python code: 
(1) When calculating the values of the control variables, with respect to the angle, should consider min(angle_difference/dt, w_max).  (Angular velocity is calculated without considering time constraints)  . Regarding the distance, should consider the maximum linear velocity value and distance/time_remaining, try to satisfy the required time between two target trajectory points.
(2) The cars need to be sequentially realized to reach the corresponding target points at a given time.
(3) The criterion for determining whether the target trajectory point has been reached should be: the distance between the current point and the target trajectory point is less than dt * v_max.
(4) This python code only outputs the position coordinates in the format of [[[x,y],t],[[x,y],t],[[x,y],t]……], here, t is the time to accumulate from 0.
(5) import statements need to be at the beginning of the code.
(6) Avoid ZeroDivisionError: float division by zero. Avoid getting caught in a dead-end loop.Avoid SyntaxError(utf-8).
(7) A positive angular velocity indicates counterclockwise rotation and represents an increase within the range of the azimuth angle from 0 to 2π. A negative angular velocity indicates clockwise rotation and represents a decrease within the range of the azimuth angle from 0 to 2π. Angular velocity can be positive or negative in the code
(8) At the beginning of the code add the words "# -*- coding: utf-8 -*-"
    
Example of python code:
# -*- coding: utf-8 -*-
import math
class Controller:
    def __init__(self, x_init, y_init, theta_init, dt=0.1, v_max=5, w_max=5):
    ……
    ……
    def execute_trajectory(self, target_sequence):
    ……
    return self.trajectory
……


Example of output from python code:
[[[1.2, 4.0], 0.1], [[1.3, 4.1], 0.2], [[1.5, 4], 0.3], [[1, 4.5], 0.4], [[1.4, 4.7], 0.5], [[1.4, 4.9], 0.6], [[1.42, 5], 0.7], [[1.3, 5.3], 0.8], [[1.3, 5.5], 0.9], [[1.3, 5.8], 1.0],……]

"""

USER_PROMPT_15 = """
You are a python code generator. 
You need to generate a controller program (python script).
Suppose there is a car moving on a 2D environment, and this car follows the following kinematic constraints to sequentially complete the coordinate point tracking for a given time.
Assume in a unicycle kinematic modeling system that does not consider balance issues, the state variables include two-dimensional plane coordinates x (horizontal axis), y (vertical axis), and θ (orientation Angle). The control input variables are linear velocity v and angular velocity w in the current direction. 
The function of the generated controller is to output the control variables that satisfy the constraints according to the current state variables and the desired goal state. The controller needs to calculate the linear and angular velocities according to the target position.

The unit of linear velocity is meters per second (m/s), the unit of orientation angle is radian(rad), and the unit of angular velocity is radians per second (rad/s). The position coordinates x and y are in meters. The time unit is seconds.

The azimuth angle θ is defined as the angle formed by rotating counter clockwise from the positive direction of the X - axis to the vehicle's traveling direction. The range of the azimuth angle is 0<=θ <2Π. 
This unicycle kinematic model is as follows.
dx/dt = v * cos(θ)
dy/dt = v * sin(θ)
dθ/dt = w
Here, dx/dt and dy/dt denote the speed of the car in the x and y directions, respectively. v is the linear velocity.θis the orientation angle. w is the angular velocity.

The generated v and w this time will be used in the Euler method of numerical analysis to update the values of state variables. The calculation process of the Euler method is as follows:
x' = x + cos(θ) * v * dt
y' = y + sin(θ) * v * dt
θ' = θ + w * dt
The obtained x', y', and θ' are the new state variable values, dt is the step size and is set to 0.1 seconds.


The initial state is {initial_state}, and the list elements denote x,y,θ, respectively.
The target trajectory that need to be reached in turn is : target_sequence=[[[1.0, 4.0], 0.0], [[0.5, 1.0], 1.0], [[7.5, 1.0], 4.0], [[8.5, 8.0], 9.0], [[5.5, 1.0], 13.0]]
The maximum linear velocity was set to 5 m/s and the absolute value of the maximum angular velocity is 5 rad/s.

Task: Generate python code that functions as a controller. 
{reprompt}. Let us take a deep breath. Think slowly and carefully and logically, explaining your answer step by step. Please self-verification whether the angular velocity need to be positive or negative in the code. If there are mistakes, please rethink step by step.

The requirements of python code: 
(1) This code creates the 'Controller' class, which is called by passing the 'target_sequence' parameter through the ‘execute_trajectory’ method of the class, thus outputting the trajectory.
(2) The format of the 'target_sequence' is [[[a1, b1], t1] , [[a2, b2], t2] , [[a3, b3], t3]]. Here, [a1, b1], [a2, b2], [a3, b3] represent the target coordinate positions that need to be reached in turn at time t1, t2, and t3, respectively. The cars need to be sequentially realized to reach the corresponding target points at a given time.
(3) The criterion for determining whether the target trajectory point has been reached should be: the distance between the current point and the target trajectory point is less than dt * v_max.
(4) When calculating the values of the control variables, with respect to the angle, should consider min(angle_difference/dt, w_max).  (Angular velocity is calculated without considering time constraints)  . Regarding the distance, should consider the maximum linear velocity value and distance/time_remaining, try to satisfy the required time between two target trajectory points.
(5) Avoid ZeroDivisionError: float division by zero. Avoid getting caught in a dead-end loop. Avoid SyntaxError(utf-8).
(6) A positive angular velocity indicates counterclockwise rotation and represents an increase within the range of the azimuth angle from 0 to 2π. A negative angular velocity indicates clockwise rotation and represents a decrease within the range of the azimuth angle from 0 to 2π. Angular velocity can be positive or negative in the code.
(7) The format of the 'trajectory' is [[[a1, b1], t1] , [[a2, b2], t2] , [[a3, b3], t3]……]. t1=0.1, t2=0.2,t3=0.3, and so on in this order.

Example of python code:
# -*- coding: utf-8 -*-
import math
class Controller:
    def __init__(self, x_init, y_init, theta_init, dt=0.1, v_max=5, w_max=5):
    ……
    ……
    def execute_trajectory(self, target_sequence):
    ……
    return self.trajectory
……
……

"""


ADJUST_DATASET = """
I will provide you with a sentence and its corresponding STL expression. In the sentence, prop_i represents a hidden atomic predicate. The atomic predicates corresponding to prop_i are "in room_i" and "been to room_i", where i can be 1, 2, 3, 4, or 5. Please determine whether prop_i should be replaced by "in room_i" or "been to room_i" based on the semantics of the sentence, so that the sentence itself does not contain any contradictions.
For example, the sentence 'Globally, while (prop_1), and (prop_3), then the following condition holds: (prop_2).' corresponds to the STL expression 'always ((prop_1 and prop_3) implies prop_2)'. Here, prop_i should all be replaced by "been to room_i" so that the sentence does not contradict itself. If prop_i were replaced by "in room_i", the sentence would be contradictory, because being "in room_1" and "in room_3" and "in room_2" cannot happen simultaneously. Therefore, the output should be: 'Globally, while (been to room_1), and (been to room_3), then the following condition holds: (been to room_2)'. 
Another example, the sentence 'never (prop_1) and at some time (prop_2)' corresponds to the STL expression 'always (not prop_1 and eventually prop_2)'. Here, prop_2 should be replaced with "in room_2" for smoother semantics. prop_1 can be replaced with either "in room 1" or "been to room 1". Therefore, the output should be: 'never (been to room 1) and at some time (in room 2)'.
Yet another example, the sentence 'Remember to keep (prop_4) happen for at least between 4 to 8 time steps on your way to (prop_3), and don’t let (prop_2) if (prop_1) happens.' corresponds to the STL expression: '(((in room_4) until [4,8] (in room_3)) and ((in room 2) implies not (in room 1)))'. Here, prop_4 should be "been to room 4", prop_3 should be "in room 3", prop_2 should be "been to room 2", and prop_1 should be "been to room 1".Therefore, the output should be:'Remember to keep (been to room_4) happen for at least between 4 to 8 time steps on your way to (in room_3), and don‘t let (been to room_2) if (been to room_1) happens.'
Input sentence is:{input_instruction}, and the corresponding STL expression is:{stl}
let us think step by step. Only output the  sentence with the hidden atomic predicate replaced. Performing self-verification outputs only the sentence with the hidden atomic predicate replaced.

"""
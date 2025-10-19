# -*- coding: utf-8 -*-
import math

class Controller:
    def __init__(self, x_init, y_init, theta_init, dt=0.1, v_max=3, w_max=5):
        self.x = x_init
        self.y = y_init
        self.theta = theta_init
        self.dt = dt
        self.v_max = v_max
        self.w_max = w_max
        self.trajectory = []

    def compute_control(self, x_target, y_target, t_remain):
        # Calculate the angle to the target
        angle_to_target = math.atan2(y_target - self.y, x_target - self.x)
        angle_diff = angle_to_target - self.theta

        # Normalize angle_diff between 0 and 2��
        angle_diff = (angle_diff + math.pi) % (2 * math.pi) - math.pi

        # Compute the angular velocity
        w = min(max(angle_diff / self.dt, -self.w_max), self.w_max)

        # Compute the distance to the target
        distance_to_target = math.sqrt((x_target - self.x)**2 + (y_target - self.y)**2)

        # Compute the linear velocity
        if t_remain > self.dt:
            v = min(distance_to_target / t_remain, self.v_max)
        else:
            v = min(self.v_max, distance_to_target / self.dt)

        return v, w

    def update_state(self, v, w):
        # Update state using Euler method
        self.x += v * math.cos(self.theta) * self.dt
        self.y += v * math.sin(self.theta) * self.dt
        self.theta += w * self.dt
        # Normalize theta
        self.theta = self.theta % (2 * math.pi)

    def execute_trajectory(self, target_sequence):
        time_elapsed = 0
        for target_point, target_time in target_sequence:
            x_target, y_target = target_point
            while True:
                # Calculate remaining time to reach the target
                t_remain = target_time - time_elapsed
                if t_remain <= 0:
                    break
                
                # Calculate control variables
                v, w = self.compute_control(x_target, y_target, t_remain)

                # Update the state
                self.update_state(v, w)

                # Append the position and time to trajectory
                self.trajectory.append([[self.x, self.y], round(time_elapsed, 1)])

                # Check if the target point is reached
                if math.sqrt((x_target - self.x)**2 + (y_target - self.y)**2) < self.dt * self.v_max:
                    break

                # Increment time
                time_elapsed += self.dt

        return self.trajectory
if __name__ == '__main__':
    # Instantiating the controller with the initial position (1, 4, 0)
    controller = Controller(x_init=1, y_init=2, theta_init=1.3)

    # Define the target trajectory
    trajectory = controller.execute_trajectory([[[1.0, 2.0], 0.0], [[2.5, 3.4], 3.5], [[2.5, 3.4], 6.5], [[7.3, 4.0], 15.2], [[7.5, 7.5], 19.4], [[4.1, 6.5], 25.0], [[2.5, 8.25], 29.3]])

    # Print the resulting trajectory
    print(trajectory)
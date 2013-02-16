"""PySimiam
Author: John Alexander
ChangeDate: 8 FEB 2013; 2300EST
Description: Example PID implementation for goal-seek (incomplete)
"""
from controller import Controller
import math
import numpy

class AvoidObstacles(Controller):
    def __init__(self):
        '''read another .xml for PID parameters?'''
        self.kp=10
        self.ki=0
        self.kd=0

        self.E = 0
        self.error_1 = 0

    def set_parameters(self, params):
        """Set PID values
        @param: (float) kp, ki, kd
        """
        self.kp = params.kp
        self.ki = params.ki
        self.kd = params.kd

    #User-defined function
    def calculate_new_goal(ir_distances):
        #Normalize the angle values
        max_dist = 3960 #where does this number come from?
        ir_angles = [128, 75, 42, 13, -13, -42, -75, -128, 180]
        
        #travel orthogonally unless more then one point detected
        objlist = []
        for i in range(0, len(ir_distances)):
            if ir_distances < max_dist:
                objlist.append(i)
            
        numobjects = len(objlist)
        if numobjects == 0:
            return self.goalx, goaly
        elif numobjects > 1: # simple go 90 degrees from object
            angle = ir_angles(objlist[0]) + 90
            angle = math.radians(angle)
            angle = math.atan2(math.sin(angle), math.cos(angle))
            goalx = self.robotx + 100*math.cos(self.robottheta + angle)
            goaly = self.robotx + 100*math.sin(self.robottheta + angle)
            return goalx, goaly

    def calculate_new_velocity(ir_distances):
        #Compare values to range
        for dist in ir_distances:
            if dist < 100:
                return 10

        #if nothing found
        return 100

    def execute(self, state, dt):
        #Select a goal, ccw obstacle avoidance
        #Get distances from sensors 
        ir_distances = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  #placeholder

        self.robotx, self.roboty, self.robottheta = state.pose
        self.goalx, self.goaly = state.goalx, state.goaly
    
        #Non-global goal
        goalx, goaly = self.calculate_new_goal(ir_distances) #user defined function
        v_ = self.calculate_new_velocity(ir_distances) #user defined function

        #1. Calculate simple proportional error
        error = math.atan2(goaly - roboty, goalx - robotx) - robottheta 

        #2. Correct for angles (angle may be greater than PI)
        error = math.atan2(math.sin(error), math.cos(error))

        #3. Calculate integral error
        self.E += error*dt

        #4. Calculate differential error
        dE = error - self.error_1
        self.error_1 = error #updates the error_1 var

        #5. Calculate desired omega
        w_ = self.kp*error + self.ki*self.E + self.kd*dE

        #6. Return solution
        return [v_, w_]

import math

class Reward:
    def __init__(self, verbose=False, track_time=False):
        self.prev_steering_angle = 0
        self.prev_speed = 0
        
    def smooth_acceleration(self, params):
        reward = 0
        # Steering smoothness
        prev_steering_angle = self.prev_steering_angle
        steering_angle = params['steering_angle']
        self.prev_steering_angle = steering_angle
        steering_diff = abs(steering_angle - prev_steering_angle)
        reward_steering_smoothness = 10 * math.exp(-0.5 * steering_diff)
        
        # speed diff
        speed = params['speed']
        if (speed > self.prev_speed) and (self.prev_speed > 0):
            reward += 10
        self.prev_speed = speed  # update the previous speed
        
        return reward + reward_steering_smoothness

reward_obj = Reward()

def reward_function(params):

     # Read input parameters
    steering = abs(params["steering_angle"])
    progress = params['progress']
    all_wheels_on_track = params['all_wheels_on_track']
    isOfftrack = params["is_offtrack"]
    steps = params['steps']
    distance_from_center = params['distance_from_center']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    speed = params['speed']
    track_width = params['track_width']
    ABS_STEERING_THRESHOLD = 10
    center_variance = params["distance_from_center"] / params["track_width"]
    left_lane = [11,12,13,14,15,16,17,18, 45,46,47,48,49,50,51,52,53, 93,94,95 ,96,97,98,99,100,101,102,103,104,105,106,107, 133,134,135,136,137,138,139,140]
    center_lane= [1,2,3,4,5,6,7,8, 24,25,26,27,28,29,30,31,32,33,34, 59, 60, 61,62,63, 85,86,87,88,89,90,91,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127, 144,145,146,147,148,149,150,151,152,153,154]
    right_lane = [66,67,68,69,70,71,72,73,7,4,75,76]
    fast_speed = [1,2,3,4,5,6,7,8, 24,25,26,27,28,29,30,31,32,33,34, 59, 60, 61,62,63, 85,86,87,88,89,90,91,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127, 144,145,146,147,148,149,150,151,152,153,154]
    moderate_speed = [ 9,10,19,20,21,22,23,35,36,37,38,39,40,41,42,43,44]
    slow_speed = [11,12,13,14,15,16,17,18, 45,46,47,48,49,50,51,52,53, 93,94,9,96,97,98,99,100,101,102,103,104,105,106,107, 133,134,135,136,137,138,139,140,66,67,68,69,70,71,72,73,7,4,75,76]
    fifth_width = 0.05 * track_width
    tenth_width = 0.1 * track_width
    quarter_width = 0.25 * track_width
    half_width = 0.5 * track_width
    curb_width = 0.6 * track_width
    reward = 0
    
    w1 = 4.0
    w2 = 1.0
    
    if speed < 1.5:
        w2 = 0.5
    if speed > 3:
        w1 +=1

    if params["closest_waypoints"][1] in left_lane and params["is_left_of_center"]:
        reward += 10 + w1 * speed + w2 * center_variance
    elif params["closest_waypoints"][1] in right_lane and not params["is_left_of_center"]:
        reward += 10 + w1 * speed + w2 * center_variance
    elif params["closest_waypoints"][1] in center_lane and center_variance < 0.5:
        reward += 10 + w1 * speed + w2 * (1 - center_variance)
    else:
        reward *= 0.5
    
    reward += 2 * reward_obj.smooth_acceleration(params)

    if steering > ABS_STEERING_THRESHOLD:
        reward *= 0.3
    
    # Self motivator - reward for making progress in less steps and fast
    if steps > 0:
        reward += ((progress / steps) * 100  + speed ** 2)
    
    # Penalize reward if the car is off track
    if isOfftrack or distance_from_center > curb_width:
        reward = -1

    return float(reward)
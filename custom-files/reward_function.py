def reward_function(params):

     # Read input parameters
    steering = abs(params["steering_angle"])
    progress = params['progress']
    all_wheels_on_track = params['all_wheels_on_track']
    offtrack = params["is_offtrack"]
    steps = params['steps']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    speed = params['speed']
    TOTAL_NUM_STEPS = 293
    BENCHMARK_TIME = 19.0
    DIRECTION_THRESHOLD = 3.0
    ABS_STEERING_THRESHOLD = 10
    center_variance = params["distance_from_center"] / params["track_width"]
    left_lane = [11,12,13,14,15,16,17,18, 45,46,47,48,49,50,51,52,53, 93,94,95 ,96,97,98,99,100,101,102,103,104,105,106,107, 133,134,135,136,137,138,139,140]
    center_lane= [1,2,3,4,5,6,7,8, 24,25,26,27,28,29,30,31,32,33,34, 59, 60, 61,62,63, 85,86,87,88,89,90,91,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127, 144,145,146,147,148,149,150,151,152,153,154]
    right_lane = [66,67,68,69,70,71,72,73,7,4,75,76]
    fast_speed = [1,2,3,4,5,6,7,8, 24,25,26,27,28,29,30,31,32,33,34, 59, 60, 61,62,63, 85,86,87,88,89,90,91,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127, 144,145,146,147,148,149,150,151,152,153,154]
    moderate_speed = [ 9,10,19,20,21,22,23,35,36,37,38,39,40,41,42,43,44]
    slow_speed = [11,12,13,14,15,16,17,18, 45,46,47,48,49,50,51,52,53, 93,94,9,96,97,98,99,100,101,102,103,104,105,106,107, 133,134,135,136,137,138,139,140,66,67,68,69,70,71,72,73,7,4,75,76]
    reward = 30
    
    if params["closest_waypoints"][1] in left_lane and params["is_left_of_center"]:
        reward += 10
    elif params["closest_waypoints"][1] in right_lane and not params["is_left_of_center"]:
        reward += 10
    elif params["closest_waypoints"][1] in center_lane and center_variance < 0.5:
        reward += 20
    else:
        reward *= 0.5

    if params["closest_waypoints"][1] in fast_speed:
        if params["speed"] > 3.5 :
            reward += 30
        elif params["speed"] > 2.5:
            reward += 10
        else:
            reward *= 0.5
    elif params["closest_waypoints"][1] in moderate_speed:
        if params["speed"] > 1.5 and params["speed"] <= 2.5 :
            reward += 20
        else:
            reward *= 0.5
    elif params["closest_waypoints"][1] in slow_speed:
        if params["speed"] > 0.5 and params["speed"] <= 1.5 :
            reward += 20
        else:
            reward *= 0.5

    if params["steps"] > 0:
        reward += ((params["progress"] / params["steps"]) * 100  + params["speed"] ** 2)
    
    if params["is_offtrack"]:
        reward = -1

    if steering > ABS_STEERING_THRESHOLD:
        reward *= 0.3

    return float(reward)
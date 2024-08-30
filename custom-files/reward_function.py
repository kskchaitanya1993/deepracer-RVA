def reward_function(params):

    waypoints = params['waypoints']
    closest_waypoint = params['closest_waypoints'][1]
    speed = params['speed']

    center_variance = params["distance_from_center"] / params["track_width"]

    steering_angle = abs(params['steering_angle'])

    left_lane = [8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143]
    center_lane = [0,1,2,3,4,5,6,7,86,87,88,89,90,113,114,115,116,117,118,119,120,121,122,123,124,125,126,144,145,146,147,148,149,150,151,152,153,154,155]
    right_lane = [63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85]

    slow_speed = [10,11,12,13,14,15,16,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,131,132,133,134,135,136]
    medium_speed = [8,9,17,18,19,20,21,34,35,36,54,55,56,57,58,59,60,80,81,82,83,84,85,86,87,105,106,107,108,126,127,128,129,130,137,138,139,140]
    fast_speed = [0,1,2,3,4,5,6,7,22,23,24,25,26,27,28,29,30,31,32,33,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155]

    reward = 10
    
    if closest_waypoint in left_lane and params["is_left_of_center"]:
        reward += 40
    elif closest_waypoint in right_lane and not params["is_left_of_center"]:
        reward += 40
    elif closest_waypoint in center_lane and center_variance < 0.15:
        reward += 40
    else:
        reward *= 1e-3

    if closest_waypoint in fast_speed:
        if speed > 3.5:
            reward += 40
        elif speed > 3.0:
            reward += 30
        elif speed > 2.5:
            reward += 20
        elif speed > 2.0:
            reward += 10
        else:
            reward *= 1e-3
    elif closest_waypoint in medium_speed:
        if speed > 1.8 and speed <= 3.2:
            reward += 40
        else:
            reward *= 1e-3
    elif closest_waypoint in slow_speed:
        if speed > 0.6 and speed <= 2.0:
            reward += 40
        else:
            reward *= 1e-3

    ABS_STEERING_THRESHOLD = 10
    if steering_angle > ABS_STEERING_THRESHOLD:
        reward *= 1e-3
    else:
        reward += 5
    
    if params["is_offtrack"]:
        reward = 1e-6
    elif params["progress"] > 0 and params["steps"] > 0:
        reward += ((params["progress"] / params["steps"]) * 100) + (speed**2)
    else:
        reward *= 1e-3

    return float(reward)

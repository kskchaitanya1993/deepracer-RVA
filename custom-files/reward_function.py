import math


class Reward:
    def __init__(self, verbose=False):
        self.first_racingpoint_index = 0
        self.verbose = verbose

    def reward_function(self, params):

        # Import package (needed for heading)
        import math

        ################## HELPER FUNCTIONS ###################

        def dist_2_points(x1, x2, y1, y2):
            return abs(abs(x1-x2)**2 + abs(y1-y2)**2)**0.5

        def closest_2_racing_points_index(racing_coords, car_coords):

            # Calculate all distances to racing points
            distances = []
            for i in range(len(racing_coords)):
                distance = dist_2_points(x1=racing_coords[i][0], x2=car_coords[0],
                                         y1=racing_coords[i][1], y2=car_coords[1])
                distances.append(distance)

            # Get index of the closest racing point
            closest_index = distances.index(min(distances))

            # Get index of the second closest racing point
            distances_no_closest = distances.copy()
            distances_no_closest[closest_index] = 999
            second_closest_index = distances_no_closest.index(
                min(distances_no_closest))

            return [closest_index, second_closest_index]

        def dist_to_racing_line(closest_coords, second_closest_coords, car_coords):
            
            # Calculate the distances between 2 closest racing points
            a = abs(dist_2_points(x1=closest_coords[0],
                                  x2=second_closest_coords[0],
                                  y1=closest_coords[1],
                                  y2=second_closest_coords[1]))

            # Distances between car and closest and second closest racing point
            b = abs(dist_2_points(x1=car_coords[0],
                                  x2=closest_coords[0],
                                  y1=car_coords[1],
                                  y2=closest_coords[1]))
            c = abs(dist_2_points(x1=car_coords[0],
                                  x2=second_closest_coords[0],
                                  y1=car_coords[1],
                                  y2=second_closest_coords[1]))

            # Calculate distance between car and racing line (goes through 2 closest racing points)
            # try-except in case a=0 (rare bug in DeepRacer)
            try:
                distance = abs(-(a**4) + 2*(a**2)*(b**2) + 2*(a**2)*(c**2) -
                               (b**4) + 2*(b**2)*(c**2) - (c**4))**0.5 / (2*a)
            except:
                distance = b

            return distance

        # Calculate which one of the closest racing points is the next one and which one the previous one
        def next_prev_racing_point(closest_coords, second_closest_coords, car_coords, heading):

            # Virtually set the car more into the heading direction
            heading_vector = [math.cos(math.radians(
                heading)), math.sin(math.radians(heading))]
            new_car_coords = [car_coords[0]+heading_vector[0],
                              car_coords[1]+heading_vector[1]]

            # Calculate distance from new car coords to 2 closest racing points
            distance_closest_coords_new = dist_2_points(x1=new_car_coords[0],
                                                        x2=closest_coords[0],
                                                        y1=new_car_coords[1],
                                                        y2=closest_coords[1])
            distance_second_closest_coords_new = dist_2_points(x1=new_car_coords[0],
                                                               x2=second_closest_coords[0],
                                                               y1=new_car_coords[1],
                                                               y2=second_closest_coords[1])

            if distance_closest_coords_new <= distance_second_closest_coords_new:
                next_point_coords = closest_coords
                prev_point_coords = second_closest_coords
            else:
                next_point_coords = second_closest_coords
                prev_point_coords = closest_coords

            return [next_point_coords, prev_point_coords]

        def racing_direction_diff(closest_coords, second_closest_coords, car_coords, heading):

            # Calculate the direction of the center line based on the closest waypoints
            next_point, prev_point = next_prev_racing_point(closest_coords,
                                                            second_closest_coords,
                                                            car_coords,
                                                            heading)

            # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
            track_direction = math.atan2(
                next_point[1] - prev_point[1], next_point[0] - prev_point[0])

            # Convert to degree
            track_direction = math.degrees(track_direction)

            # Calculate the difference between the track direction and the heading direction of the car
            direction_diff = abs(track_direction - heading)
            if direction_diff > 180:
                direction_diff = 360 - direction_diff

            return direction_diff

        # Gives back indexes that lie between start and end index of a cyclical list 
        # (start index is included, end index is not)
        def indexes_cyclical(start, end, array_len):

            if end < start:
                end += array_len

            return [index % array_len for index in range(start, end)]

        # Calculate how long car would take for entire lap, if it continued like it did until now
        def projected_time(first_index, closest_index, step_count, times_list):

            # Calculate how much time has passed since start
            current_actual_time = (step_count-1) / 15

            # Calculate which indexes were already passed
            indexes_traveled = indexes_cyclical(first_index, closest_index, len(times_list))

            # Calculate how much time should have passed if car would have followed optimals
            current_expected_time = sum([times_list[i] for i in indexes_traveled])

            # Calculate how long one entire lap takes if car follows optimals
            total_expected_time = sum(times_list)

            # Calculate how long car would take for entire lap, if it continued like it did until now
            try:
                projected_time = (current_actual_time/current_expected_time) * total_expected_time
            except:
                projected_time = 9999

            return projected_time

        #################### RACING LINE ######################

        # Optimal racing line for Ross Raceway
        # Each row: [x,y,speed,timeFromPreviousPoint]
        racing_track = [[5.04771, 0.73385, 4.0, 0.04291],
                        [5.04771, 0.86385, 3.60911, 0.03602],
                        [5.0477, 0.99385, 3.19707, 0.04066],
                        [5.04768, 1.1655, 2.89347, 0.05932],
                        [5.04593, 1.46653, 2.66079, 0.11314],
                        [5.03895, 1.76564, 2.47353, 0.12096],
                        [5.02384, 2.06156, 2.31737, 0.12787],
                        [4.99798, 2.35298, 2.18259, 0.13404],
                        [4.959, 2.63848, 2.0642, 0.1396],
                        [4.90482, 2.91661, 1.92954, 0.14686],
                        [4.83368, 3.18587, 1.92954, 0.14433],
                        [4.74409, 3.44466, 1.92954, 0.14193],
                        [4.63476, 3.69126, 1.92954, 0.1398],
                        [4.5045, 3.92368, 1.92954, 0.13808],
                        [4.35223, 4.13958, 1.92954, 0.13692],
                        [4.17632, 4.33538, 2.00901, 0.13102],
                        [3.97987, 4.51132, 2.09535, 0.12586],
                        [3.76545, 4.66776, 2.18934, 0.12123],
                        [3.53521, 4.80509, 2.29315, 0.1169],
                        [3.29109, 4.92381, 2.40999, 0.11264],
                        [3.03483, 5.02452, 2.54279, 0.10828],
                        [2.76806, 5.10797, 2.69939, 0.10355],
                        [2.49238, 5.17514, 2.88686, 0.09829],
                        [2.20928, 5.22725, 3.11576, 0.09239],
                        [1.92021, 5.26577, 3.40944, 0.08554],
                        [1.62651, 5.29244, 3.79758, 0.07766],
                        [1.32942, 5.30924, 4.0, 0.07439],
                        [1.03001, 5.31831, 4.0, 0.07489],
                        [0.72919, 5.32199, 3.63022, 0.08287],
                        [0.42768, 5.32264, 3.2296, 0.09336],
                        [0.12603, 5.32269, 2.93569, 0.10275],
                        [-0.1753, 5.32032, 2.712, 0.11112],
                        [-0.47588, 5.31258, 2.52479, 0.11909],
                        [-0.77511, 5.29654, 2.38875, 0.12545],
                        [-1.07219, 5.26936, 2.26999, 0.13142],
                        [-1.36598, 5.22838, 2.16864, 0.13679],
                        [-1.65498, 5.17113, 2.08241, 0.14148],
                        [-1.93717, 5.09551, 2.00095, 0.14601],
                        [-2.21002, 4.99975, 1.92568, 0.15016],
                        [-2.47071, 4.88296, 1.85575, 0.15393],
                        [-2.7161, 4.74484, 1.7925, 0.15709],
                        [-2.94298, 4.58583, 1.72858, 0.16028],
                        [-3.1482, 4.40711, 1.66848, 0.16311],
                        [-3.32872, 4.21036, 1.6129, 0.16555],
                        [-3.48172, 3.99784, 1.55851, 0.16802],
                        [-3.60462, 3.77223, 1.5065, 0.17054],
                        [-3.69521, 3.53663, 1.45602, 0.17336],
                        [-3.75133, 3.29447, 1.45602, 0.17073],
                        [-3.77102, 3.0496, 1.45602, 0.16872],
                        [-3.75246, 2.80642, 1.45602, 0.16751],
                        [-3.69385, 2.57, 1.45602, 0.16728],
                        [-3.59354, 2.34656, 1.45602, 0.16822],
                        [-3.45039, 2.14404, 1.64965, 0.15034],
                        [-3.27546, 1.9629, 1.75293, 0.14366],
                        [-3.0734, 1.80435, 1.87188, 0.13721],
                        [-2.84832, 1.66879, 2.01693, 0.13028],
                        [-2.60402, 1.55572, 2.20091, 0.12231],
                        [-2.34411, 1.46376, 2.44653, 0.11269],
                        [-2.07198, 1.39059, 2.79759, 0.10073],
                        [-1.7908, 1.3329, 2.45286, 0.11702],
                        [-1.50352, 1.28663, 2.1832, 0.13328],
                        [-1.21285, 1.24708, 1.98474, 0.1478],
                        [-0.92738, 1.20293, 1.83094, 0.15777],
                        [-0.64789, 1.1487, 1.70496, 0.16699],
                        [-0.37774, 1.07993, 1.60185, 0.17403],
                        [-0.12038, 0.99315, 1.51145, 0.17969],
                        [0.12064, 0.88593, 1.43371, 0.18399],
                        [0.3417, 0.75697, 1.36324, 0.18774],
                        [0.53905, 0.60596, 1.3, 0.19115],
                        [0.70872, 0.43359, 1.3, 0.18605],
                        [0.84654, 0.24158, 1.3, 0.18181],
                        [0.94797, 0.03273, 1.3, 0.1786],
                        [1.00816, -0.18877, 1.3, 0.17656],
                        [1.02194, -0.41685, 1.3, 0.17577],
                        [0.98441, -0.64255, 1.4416, 0.15872],
                        [0.90575, -0.85904, 1.50749, 0.15279],
                        [0.79011, -1.06188, 1.57807, 0.14796],
                        [0.64117, -1.24774, 1.65777, 0.14367],
                        [0.46237, -1.4141, 1.75012, 0.13954],
                        [0.25707, -1.5591, 1.85675, 0.13537],
                        [0.02856, -1.68154, 1.98426, 0.13065],
                        [-0.21984, -1.78097, 2.14028, 0.12501],
                        [-0.48477, -1.85778, 2.3383, 0.11796],
                        [-0.76285, -1.91335, 2.60285, 0.10895],
                        [-1.05081, -1.95008, 2.89675, 0.10022],
                        [-1.3457, -1.97123, 2.57243, 0.11493],
                        [-1.64489, -1.98085, 2.33255, 0.12834],
                        [-1.94628, -1.98353, 2.14745, 0.14035],
                        [-2.24455, -1.99462, 1.99803, 0.14939],
                        [-2.53747, -2.01817, 1.87117, 0.15705],
                        [-2.82247, -2.05769, 1.76453, 0.16306],
                        [-3.09681, -2.1159, 1.66856, 0.16808],
                        [-3.3576, -2.19472, 1.62804, 0.16735],
                        [-3.60194, -2.29519, 1.56466, 0.16885],
                        [-3.82687, -2.4176, 1.50691, 0.16994],
                        [-4.02935, -2.56157, 1.44791, 0.17159],
                        [-4.20631, -2.72606, 1.44791, 0.16686],
                        [-4.35441, -2.9094, 1.44791, 0.16278],
                        [-4.47189, -3.10851, 1.44791, 0.15967],
                        [-4.55588, -3.3205, 1.44791, 0.15748],
                        [-4.60324, -3.54176, 1.44791, 0.15628],
                        [-4.61037, -3.7676, 1.46989, 0.15372],
                        [-4.57807, -3.99236, 1.47968, 0.15346],
                        [-4.5083, -4.21112, 1.47968, 0.15518],
                        [-4.40023, -4.41848, 1.47968, 0.15803],
                        [-4.25322, -4.6078, 1.57002, 0.15267],
                        [-4.07243, -4.77509, 1.73061, 0.14233],
                        [-3.86461, -4.91974, 1.84063, 0.13756],
                        [-3.63353, -5.04064, 1.97035, 0.13236],
                        [-3.38281, -5.13751, 2.1283, 0.12629],
                        [-3.11596, -5.21097, 2.33086, 0.11875],
                        [-2.83639, -5.26268, 2.60168, 0.10928],
                        [-2.54733, -5.29528, 2.99284, 0.0972],
                        [-2.25172, -5.31241, 3.63775, 0.0814],
                        [-1.95216, -5.31856, 4.0, 0.07491],
                        [-1.65075, -5.31873, 4.0, 0.07535],
                        [-1.34911, -5.31818, 4.0, 0.07541],
                        [-1.04746, -5.31762, 4.0, 0.07541],
                        [-0.74582, -5.31704, 4.0, 0.07541],
                        [-0.44418, -5.31646, 4.0, 0.07541],
                        [-0.14253, -5.31589, 4.0, 0.07541],
                        [0.15911, -5.31532, 4.0, 0.07541],
                        [0.46076, -5.31475, 3.59403, 0.08393],
                        [0.7624, -5.31418, 3.17034, 0.09515],
                        [1.06405, -5.31359, 2.86704, 0.10521],
                        [1.36507, -5.31127, 2.63158, 0.11439],
                        [1.66426, -5.30396, 2.44349, 0.12248],
                        [1.96025, -5.2886, 2.28965, 0.12945],
                        [2.25158, -5.2624, 2.15552, 0.1357],
                        [2.53669, -5.22291, 2.03966, 0.14112],
                        [2.81399, -5.16806, 1.93394, 0.14616],
                        [3.08184, -5.09611, 1.84034, 0.1507],
                        [3.33855, -5.00564, 1.84034, 0.1479],
                        [3.58236, -4.89548, 1.84034, 0.14537],
                        [3.81128, -4.76461, 1.84034, 0.14328],
                        [4.02307, -4.61211, 1.84034, 0.14181],
                        [4.21491, -4.43702, 1.84034, 0.14113],
                        [4.38328, -4.23854, 1.9884, 0.13089],
                        [4.53003, -4.0211, 2.08941, 0.12555],
                        [4.65579, -3.78715, 2.20535, 0.12044],
                        [4.76132, -3.53881, 2.34236, 0.1152],
                        [4.84756, -3.27803, 2.50145, 0.1098],
                        [4.91565, -3.00661, 2.69588, 0.1038],
                        [4.96702, -2.72631, 2.9409, 0.0969],
                        [5.00345, -2.43881, 3.26407, 0.08879],
                        [5.02712, -2.14574, 3.7201, 0.07904],
                        [5.04052, -1.84863, 4.0, 0.07435],
                        [5.04644, -1.54887, 4.0, 0.07495],
                        [5.04785, -1.24766, 4.0, 0.0753],
                        [5.04784, -0.94602, 4.0, 0.07541],
                        [5.04781, -0.64437, 4.0, 0.07541],
                        [5.04779, -0.34273, 4.0, 0.07541],
                        [5.04777, -0.04108, 4.0, 0.07541],
                        [5.04775, 0.26056, 4.0, 0.07541],
                        [5.04772, 0.56221, 4.0, 0.07541]]

        ################## INPUT PARAMETERS ###################

        # Read all input parameters
        all_wheels_on_track = params['all_wheels_on_track']
        x = params['x']
        y = params['y']
        distance_from_center = params['distance_from_center']
        is_left_of_center = params['is_left_of_center']
        heading = params['heading']
        progress = params['progress']
        steps = params['steps']
        speed = params['speed']
        steering_angle = params['steering_angle']
        track_width = params['track_width']
        waypoints = params['waypoints']
        closest_waypoints = params['closest_waypoints']
        is_offtrack = params['is_offtrack']

        ############### OPTIMAL X,Y,SPEED,TIME ################

        # Get closest indexes for racing line (and distances to all points on racing line)
        closest_index, second_closest_index = closest_2_racing_points_index(
            racing_track, [x, y])

        # Get optimal [x, y, speed, time] for closest and second closest index
        optimals = racing_track[closest_index]
        optimals_second = racing_track[second_closest_index]

        # Save first racingpoint of episode for later
        if self.verbose == True:
            self.first_racingpoint_index = 0 # this is just for testing purposes
        if steps == 1:
            self.first_racingpoint_index = closest_index

        ################ REWARD AND PUNISHMENT ################

        ## Define the default reward ##
        reward = 1

        ## Reward if car goes close to optimal racing line ##
        DISTANCE_MULTIPLE = 1
        dist = dist_to_racing_line(optimals[0:2], optimals_second[0:2], [x, y])
        distance_reward = max(1e-3, 1 - (dist/(track_width*0.5)))
        reward += distance_reward * DISTANCE_MULTIPLE

        ## Reward if speed is close to optimal speed ##
        SPEED_DIFF_NO_REWARD = 1
        SPEED_MULTIPLE = 2
        speed_diff = abs(optimals[2]-speed)
        if speed_diff <= SPEED_DIFF_NO_REWARD:
            # we use quadratic punishment (not linear) bc we're not as confident with the optimal speed
            # so, we do not punish small deviations from optimal speed
            speed_reward = (1 - (speed_diff/(SPEED_DIFF_NO_REWARD))**2)**2
        else:
            speed_reward = 0
        reward += speed_reward * SPEED_MULTIPLE

        # Reward if less steps
        REWARD_PER_STEP_FOR_FASTEST_TIME = 1 
        STANDARD_TIME = 37
        FASTEST_TIME = 19
        times_list = [row[3] for row in racing_track]
        projected_time = projected_time(self.first_racingpoint_index, closest_index, steps, times_list)
        try:
            steps_prediction = projected_time * 15 + 1
            reward_prediction = max(1e-3, (-REWARD_PER_STEP_FOR_FASTEST_TIME*(FASTEST_TIME) /
                                           (STANDARD_TIME-FASTEST_TIME))*(steps_prediction-(STANDARD_TIME*15+1)))
            steps_reward = min(REWARD_PER_STEP_FOR_FASTEST_TIME, reward_prediction / steps_prediction)
        except:
            steps_reward = 0
        reward += steps_reward

        # Zero reward if obviously wrong direction (e.g. spin)
        direction_diff = racing_direction_diff(
            optimals[0:2], optimals_second[0:2], [x, y], heading)
        if direction_diff > 30:
            reward = 1e-3
            
        # Zero reward of obviously too slow
        speed_diff_zero = optimals[2]-speed
        if speed_diff_zero > 0.5:
            reward = 1e-3
            
        ## Incentive for finishing the lap in less steps ##
        REWARD_FOR_FASTEST_TIME = 1000 # should be adapted to track length and other rewards
        STANDARD_TIME = 37  # seconds (time that is easily done by model)
        FASTEST_TIME = 27  # seconds (best time of 1st place on the track)
        if progress == 100:
            finish_reward = max(1e-3, (-REWARD_FOR_FASTEST_TIME /
                      (15*(STANDARD_TIME-FASTEST_TIME)))*(steps-STANDARD_TIME*15))
        else:
            finish_reward = 0
        reward += finish_reward
        
        ## Zero reward if off track ##
        if is_offtrack:
            reward = 1e-3

        ####################### VERBOSE #######################
        
        if self.verbose == True:
            print("Closest index: %i" % closest_index)
            print("Distance to racing line: %f" % dist)
            print("=== Distance reward (w/out multiple): %f ===" % (distance_reward))
            print("Optimal speed: %f" % optimals[2])
            print("Speed difference: %f" % speed_diff)
            print("=== Speed reward (w/out multiple): %f ===" % speed_reward)
            print("Direction difference: %f" % direction_diff)
            print("Predicted time: %f" % projected_time)
            print("=== Steps reward: %f ===" % steps_reward)
            print("=== Finish reward: %f ===" % finish_reward)
            
        #################### RETURN REWARD ####################
        
        # Always return a float value
        return float(reward)


reward_object = Reward() # add parameter verbose=True to get noisy output for testing


def reward_function(params):
    return reward_object.reward_function(params)

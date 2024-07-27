import math

class Reward:
    def __init__(self, verbose=False, track_time=False):
        self.prev_steering_angle = 0
        self.prev_speed = 0
        
    def fast_and_smooth(self, params):
        # Steering smoothness
        prev_steering_angle = self.prev_steering_angle
        steering_angle = params['steering_angle']
        self.prev_steering_angle = steering_angle
        steering_diff = abs(steering_angle - prev_steering_angle)
        reward_steering_smoothness = math.exp(-0.5 * steering_diff)
        
        # speed diff
        speed = params['speed']
        accl_reward = speed - self.prev_speed
        self.prev_speed = speed  # update the previous speed
        
        return 4 * accl_reward + 3 * reward_steering_smoothness

reward_obj = Reward()

def reward_function(params):

    def dist_bw_points(x1, x2, y1, y2):
        return abs(abs(x1-x2)**2 + abs(y1-y2)**2)**0.5
    
    def closest_indexes(racing_xy, car_xy):
        # Calculate all distances to racing points
        distances = []
        for i in range(len(racing_xy)):
            distance = dist_bw_points(x1=racing_xy[i][0], x2=car_xy[0],
                                        y1=racing_xy[i][1], y2=car_xy[1])
            distances.append(distance)
        
        closest_racing_index = distances.index(min(distances))
        distance_wo_closest = distances.copy()
        distance_wo_closest[closest_racing_index] = 1000
        sec_closest_racing_index = distance_wo_closest.index(min(distance_wo_closest))
        
        return [closest_racing_index, sec_closest_racing_index]
    
    def dist_to_racing_line(closest_coor, second_closest_coor, car_coor):
        # Calculate the distances between 2 closest racing points
        base = dist_bw_points(closest_coor[0], second_closest_coor[0], closest_coor[1], second_closest_coor[1])

        # Distances between car and closest and second closest racing point
        side1 = dist_bw_points(car_coor[0], closest_coor[0], car_coor[1], closest_coor[1])
        side2 = dist_bw_points(car_coor[0], second_closest_coor[0], car_coor[1], second_closest_coor[1])

        # Use Herons formula to calculate the height of triangle if racing line is the base
        # h = (0.5/b) * sqrt(a+b+c) * sqrt(-a+b+c) * sqrt(a-b+c) * sqrt(a+b-c)
        try:
            distance = (0.5/base) * (side1 + base + side2)**0.5 * (-side1 + base + side2)**0.5 * (side1 - base + side2)**0.5 * (side1 + base - side2)**0.5
        except:
            distance = side1
        
        return abs(distance)
    
    racing_track = [[ 5.04771315,  0.73385354],
       [ 5.04770565,  0.86385354],
       [ 5.04752488,  1.00379612],
       [ 5.04601829,  1.20414345],
       [ 5.03994307,  1.47311557],
       [ 5.02600116,  1.76191145],
       [ 5.00189401,  2.05172213],
       [ 4.96582171,  2.33698581],
       [ 4.91622468,  2.61553037],
       [ 4.85177041,  2.88595332],
       [ 4.77133984,  3.14700389],
       [ 4.67395059,  3.39739714],
       [ 4.55875699,  3.6357692 ],
       [ 4.42492216,  3.86054687],
       [ 4.27168295,  4.06991523],
       [ 4.09774347,  4.26110487],
       [ 3.90554285,  4.43449231],
       [ 3.69705278,  4.59044153],
       [ 3.47394098,  4.72931037],
       [ 3.23768799,  4.85148691],
       [ 2.98966154,  4.95743112],
       [ 2.73114063,  5.04767879],
       [ 2.46335206,  5.12287822],
       [ 2.18750733,  5.18385219],
       [ 1.90480595,  5.23162591],
       [ 1.61641802,  5.26742165],
       [ 1.32347122,  5.29266026],
       [ 1.02703794,  5.30896988],
       [ 0.72809709,  5.31812781],
       [ 0.42751795,  5.32204112],
       [ 0.1260345 ,  5.32269001],
       [-0.17538168,  5.32093302],
       [-0.47601888,  5.31358639],
       [-0.77521933,  5.29754077],
       [-1.07204545,  5.26980087],
       [-1.36516319,  5.22755939],
       [-1.65274271,  5.16831113],
       [-1.9324309 ,  5.09002486],
       [-2.2013603 ,  4.99121568],
       [-2.45635605,  4.87121954],
       [-2.69413698,  4.73020842],
       [-2.91162735,  4.56922464],
       [-3.10601215,  4.38991817],
       [-3.27486048,  4.19444706],
       [-3.41610707,  3.98530994],
       [-3.52798433,  3.76522914],
       [-3.60890395,  3.5370953 ],
       [-3.65743738,  3.30399517],
       [-3.67223309,  3.06925121],
       [-3.65179367,  2.83654502],
       [-3.59459533,  2.61013628],
       [-3.49892966,  2.39525451],
       [-3.3633466 ,  2.19872181],
       [-3.19776381,  2.02088656],
       [-3.00611602,  1.86291036],
       [-2.79196061,  1.72517113],
       [-2.55861142,  1.60730906],
       [-2.30924935,  1.50817011],
       [-2.04697933,  1.42575478],
       [-1.7748333 ,  1.35725225],
       [-1.49581087,  1.29907759],
       [-1.21285213,  1.24707933],
       [-0.93570951,  1.19187766],
       [-0.66503539,  1.12793126],
       [-0.40457428,  1.05103371],
       [-0.15792641,  0.95802559],
       [ 0.07149212,  0.8468814 ],
       [ 0.28039334,  0.71662137],
       [ 0.46557195,  0.5672239 ],
       [ 0.62378385,  0.39949873],
       [ 0.75162025,  0.21504164],
       [ 0.8455191 ,  0.01633875],
       [ 0.901376  , -0.19315507],
       [ 0.91460233, -0.40845905],
       [ 0.8805441 , -0.62211285],
       [ 0.8087429 , -0.82836943],
       [ 0.70236162, -1.02337644],
       [ 0.56427979, -1.20409612],
       [ 0.39718567, -1.36805544],
       [ 0.20367006, -1.51323014],
       [-0.01359087, -1.63811103],
       [-0.25174488, -1.74183706],
       [-0.50774609, -1.82435222],
       [-0.77839586, -1.88656104],
       [-1.0605201 , -1.93029929],
       [-1.35103   , -1.95843697],
       [-1.64709669, -1.97473126],
       [-1.94628298, -1.98353201],
       [-2.24098611, -2.00243066],
       [-2.52845734, -2.03492563],
       [-2.80593714, -2.08375666],
       [-3.07068421, -2.15079189],
       [-3.32009518, -2.2370279 ],
       [-3.55176264, -2.3426957 ],
       [-3.76346541, -2.46741111],
       [-3.9530907 , -2.61033015],
       [-4.11860792, -2.77020773],
       [-4.25800098, -2.94545682],
       [-4.36895309, -3.13425129],
       [-4.44897028, -3.33430465],
       [-4.49516841, -3.54275431],
       [-4.50413531, -3.75581058],
       [-4.47213169, -3.96808041],
       [-4.40594639, -4.17508205],
       [-4.30456706, -4.37236805],
       [-4.1668539 , -4.55429217],
       [-3.99975286, -4.71932704],
       [-3.80600624, -4.8652914 ],
       [-3.58840716, -4.99058499],
       [-3.34985862, -5.09425553],
       [-3.09342189, -5.17615585],
       [-2.82222521, -5.23700129],
       [-2.5394334 , -5.27851849],
       [-2.24811155, -5.30344756],
       [-1.95106624, -5.31540212],
       [-1.6507535 , -5.31872892],
       [-1.34910947, -5.31817913],
       [-1.04746497, -5.31761503],
       [-0.74582046, -5.31703806],
       [-0.44417594, -5.31646395],
       [-0.1425315 , -5.31589198],
       [ 0.15911295, -5.31531811],
       [ 0.46075745, -5.3147459 ],
       [ 0.76240206, -5.31417751],
       [ 1.06318784, -5.31144642],
       [ 1.36196134, -5.30388859],
       [ 1.65747443, -5.2889828 ],
       [ 1.94842516, -5.26444333],
       [ 2.23348727, -5.22825941],
       [ 2.51133861, -5.17872214],
       [ 2.78065951, -5.1143953 ],
       [ 3.04013545, -5.03410119],
       [ 3.28842729, -4.93686237],
       [ 3.52412161, -4.82183631],
       [ 3.74566065, -4.68825307],
       [ 3.95126641, -4.53538429],
       [ 4.13870953, -4.36240122],
       [ 4.30521967, -4.16853616],
       [ 4.4526025 , -3.95745961],
       [ 4.581401  , -3.73106306],
       [ 4.692197  , -3.49099281],
       [ 4.78563276, -3.23873508],
       [ 4.86247042, -2.97569186],
       [ 4.92363469, -2.70322012],
       [ 4.97030934, -2.42268499],
       [ 5.00397426, -2.13546103],
       [ 5.02640272, -1.84290848],
       [ 5.03963323, -1.54634031],
       [ 5.04595932, -1.24700049],
       [ 5.04784012, -0.94601676],
       [ 5.04781485, -0.64437172],
       [ 5.047791  , -0.34272665],
       [ 5.04776907, -0.04108161],
       [ 5.04774594,  0.26056334],
       [ 5.04772305,  0.56220838],
       [ 5.04771315,  0.73385354]]
    
    # Read input parameters
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    steering = abs(params['steering_angle']) # Only need the absolute steering angle
    car_xy = [params['x'], params['y']]
    is_offtrack = params['is_offtrack']
    is_left_of_center = params['is_left_of_center']
    closest_waypoints = params['closest_waypoints']
    progress = params['progress']
    steps = params["steps"]
    speed = params["speed"]
    all_wheels_on_track = params["all_wheels_on_track"]
    heading = params['heading']
    # Calculate 3 marks that are farther and father away from the center line
    fifth_width = 0.05 * track_width
    tenth_width = 0.1 * track_width
    quarter_width = 0.25 * track_width
    half_width = 0.5 * track_width
    curb_width = 0.6 * track_width
    ABS_STEERING_THRESHOLD = 10
    reward = 1
    
    closest_index, second_closest_index = closest_indexes(racing_track, car_xy)
    racing_first_coor = racing_track[closest_index]
    racing_second_coor = racing_track[second_closest_index]

    dist = dist_to_racing_line(racing_first_coor, racing_second_coor, car_xy)
    w1 = 4.0
    w2 = 2.0
    
    if speed < 1.5:
        w2 = 0.5
    if speed > 3:
        w1 +=1
        
    reward += w1 * speed + w2 * (1 - dist/quarter_width)
    reward += reward_obj.fast_and_smooth(params)
    
    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians and Convert to degree
    racing_direction = math.degrees(math.atan2(racing_track[closest_index+1][1] - racing_track[closest_index][1], racing_track[closest_index+1][0] - racing_track[closest_index][0]))
    # Calculate the difference between the racing direction and the heading direction of the car
    direction_diff = abs(racing_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff
    reward_alignment = math.cos(math.radians(direction_diff))
    reward += 2 * reward_alignment
    
    if steering > ABS_STEERING_THRESHOLD:
        reward *= 0.3
        
    # reward for making progress in less steps and fast
    # Penalize reward if the car is off track
    if is_offtrack or distance_from_center > curb_width:
        reward = -1
    elif steps > 0:
        reward += ((progress / steps) * 100  + speed ** 2)

    return float(reward)

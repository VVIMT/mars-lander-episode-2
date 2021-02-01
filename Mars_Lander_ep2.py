import sys
import math
import numpy as np

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

surface_n = int(input())  # the number of points used to draw the surface of Mars.
lst_land_x = []
lst_land_y = []

for i in range(surface_n):
    # land_x: X coordinate of a surface point. (0 to 6999)
    # land_y: Y coordinate of a surface point. By linking all the points together in a sequential fashion, you form the surface of Mars.
    land_x, land_y = [int(j) for j in input().split()]

    lst_land_x.append(land_x)
    lst_land_y.append(land_y)

def find_landing_site(lst_land_x, lst_land_y):

    flat_surface_coords = []
    flat_surface_found_signal = False
    flat_surface_len = 0

    i = 0
    while flat_surface_found_signal != True and i < len(lst_land_x):
        j = i + 1
        while lst_land_y[i] == lst_land_y[j] and lst_land_x[j] < 6999:
            j += 1
        if lst_land_x[j - 1] - lst_land_x[i] < 1000:
            pass
        else:
            flat_surface_len = lst_land_x[j - 1] - lst_land_x[i]
            flat_surface_coords = [lst_land_x[i], lst_land_y[i]]
            landing_site_coords = [lst_land_x[i] + flat_surface_len // 2, lst_land_y[i]]
            flat_surface_found_signal = True
            break
        i += 1

    return (flat_surface_len, flat_surface_coords, landing_site_coords)

flat_surface_len, flat_surface_coords, landing_site_coords = find_landing_site(lst_land_x, lst_land_y)

def compute_braking_distance(speed, acceleration, landing_phase):
    '''
    Calculate the distance required to stop the space shuttle \
    given its speed and maximum thrust power of deceleration.
    '''
    
    if landing_phase == 2 and abs(speed) > 5:
        speed = abs(speed) - 5
    time = abs(speed)/abs(acceleration)
    braking_distance = abs(abs(speed) * time + 1/2 * -abs(acceleration) * pow(time, 2))

    print("speed = " + str(abs(speed)), file=sys.stderr, flush=True)
    print("acceleration = " + str(abs(acceleration)), file=sys.stderr, flush=True)
    print("time = " + str(abs(time)), file=sys.stderr, flush=True)
    print("braking_distance = " + str(abs(braking_distance)), file=sys.stderr, flush=True)

    return (braking_distance)

def control_acceleration(params, landing_phase):
    """
    We calculate the desired acceleration according to the speed and 
    the distance of the space shuttle compared with the landing site position.
    """

    rotate = params["rotate"]
    power = params["power"]
    objective_distance = 0

    if x > landing_site_coords[0] - params["flat_surface_len"]//2 \
        and x < landing_site_coords[0] + params["flat_surface_len"]//2 \
        and params["h_speed"] >= -1 and params["h_speed"] <= 1:
        landing_phase = 2 # Land vertically when the shuttle is over the flat landing site.
    else:
        landing_phase = 1 # Move horizontally when the shuttle is not over the flat landing site.

    print("landing_phase = " + str(abs(landing_phase)), file=sys.stderr, flush=True)
    # The "objective" is a straight line
    if landing_phase == 1:
        position = x
        speed = params["h_speed"]
        objective = landing_site_coords[0]
        objective_distance = abs(objective - position)
        approach = params["x_approach"]
        max_acceleration = abs(4 * math.sin(math.acos(3.711/4)))
    elif landing_phase == 2: # When the shuttle is over the landing site
        position = y
        speed = params["v_speed"]
        objective = landing_site_coords[1]
        objective_distance = abs(objective - position)
        approach = params["y_approach"]
        max_acceleration = 4 - 3.711
    
    braking_distance = compute_braking_distance(speed, max_acceleration, landing_phase)
    # Variable "approach" takes value "1" when the shuttle is approaching the objective, 
    # "-1" when the shuttle is moving away from the objective, and "0" when it is static.
    if approach != -1: # Shuttle approaching the objective.
        power = 4
        rotate = math.degrees(math.acos(3.711/4))
        if x < objective and landing_phase == 1:
            if braking_distance <= objective_distance:
                rotate *= -1
            else:
                rotate *= 1
        elif x > objective and landing_phase == 1:
            if braking_distance <= objective_distance:
                rotate *= 1
            else:
                rotate *= -1
        if landing_phase == 1 and params["v_speed"] != 0 \
            and y < landing_site_coords[1] + abs(3000 - landing_site_coords[1])//2:
            rotate = 0
            if params["v_speed"] < 0:
                power = 4
            elif params["v_speed"] > 0:
                power = 0
        elif landing_phase == 2:
            rotate = 0
            if braking_distance < objective_distance:
                power = 0
            else:
                power = 4
    else: # Shuttle moving away from the objective.
        rotate = math.degrees(math.acos(3.711/4))
        if x < objective and landing_phase == 1:
            rotate *= -1
            power = 4
        elif x > objective and landing_phase == 1:
            rotate *= 1
        if landing_phase == 2:
            rotate = 0
            power = 0

    return (round(rotate), power, landing_phase)

tmp_h_speed = 0
tmp_v_speed = 0
tmp_x = 0
tmp_y = 0
h_acceleration = 0
v_acceleration = 0
first_loop = True
landing_phase = 1
# game loop
while True:
    # h_speed: the horizontal speed (in m/s), can be negative.
    # v_speed: the vertical speed (in m/s), can be negative.
    # fuel: the quantity of remaining fuel in liters.
    # rotate: the rotation angle in degrees (-90 to 90).
    # power: the thrust power (0 to 4).

    x, y, h_speed, v_speed, fuel, rotate, power = [int(i) for i in input().split()]
    if first_loop == True:
        h_acceleration = 0
        v_acceleration = 0
        x_approach = 0
        y_approach = 0
        first_loop = False
    h_acceleration = h_speed - tmp_h_speed
    v_acceleration = v_speed - tmp_v_speed
    tmp_h_speed = h_speed
    tmp_v_speed = v_speed
    x_approach = np.sign(abs(tmp_x - landing_site_coords[0]) - abs(x - landing_site_coords[0]))
    y_approach = np.sign(abs(tmp_y - landing_site_coords[1]) - abs(y - landing_site_coords[1]))
    tmp_x = x
    tmp_y = y

    params = {"x": x, "y": y, "landing_site_coords": landing_site_coords, "flat_surface_len": flat_surface_len, \
        "h_speed": h_speed, "v_speed": v_speed, "h_acceleration": h_acceleration, "v_acceleration": v_acceleration, \
        "rotate": rotate, "power": power, "x_approach": x_approach, "y_approach": y_approach}

    rotate, power, landing_phase = control_acceleration(params, landing_phase)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)


    # rotate power. rotate is the desired rotation angle. power is the desired thrust power.
    print(str(rotate) + " " + str(power))

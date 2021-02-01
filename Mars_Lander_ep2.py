import sys
import math

surface_n = int(input())  # the number of points used to draw the surface of Mars.
lst_land_x = []
lst_land_y = []

for i in range(surface_n):
    land_x, land_y = [int(j) for j in input().split()]

    lst_land_x.append(land_x)
    lst_land_y.append(land_y)

def find_landing_site(lst_land_x, lst_land_y):

    flat_surface_len = 0
    for i in range(len(lst_land_x) - 1):
        j = i + 1
        while lst_land_y[i] == lst_land_y[j] and lst_land_x[j] < 6999:
            j += 1
        if not (lst_land_x[j - 1] - lst_land_x[i] < 1000):
            flat_surface_len = lst_land_x[j - 1] - lst_land_x[i]
            landing_site_coords = [lst_land_x[i] + flat_surface_len//2, lst_land_y[i]]

    return (flat_surface_len, landing_site_coords)

def control_acceleration(params, landing_phase, rotate, power):

    landing_phase = 1 # Move horizontally when the shuttle is not over the flat landing site.
    position = x
    speed = params["h_speed"]
    objective_distance = abs(landing_site_coords[0] - position)
    max_acceleration = abs(4 * math.sin(math.acos(3.711/4)))
    if x > landing_site_coords[0] - params["flat_surface_len"]//2 \
        and x < landing_site_coords[0] + params["flat_surface_len"]//2 \
        and params["h_speed"] >= -5 and params["h_speed"] <= 5:
        landing_phase = 2 # Land vertically when the shuttle is over the flat landing site.
        position = y
        speed = params["v_speed"]
        objective_distance = abs(landing_site_coords[1] - position)
        max_acceleration = 4 - 3.711
    
    # We compute the distance required to stop the space shuttle 
    # given its speed and maximum thrust power of deceleration.
    braking_distance = (-pow(speed, 2)) / (2 * -abs(max_acceleration))

    if landing_phase == 1:
        rotate = math.degrees(math.acos(3.711/4))
        if x < landing_site_coords[0]:
            rotate *= -1
            power = 4
        elif x > landing_site_coords[0]:
            rotate *= 1
            power = 4
        if braking_distance >= objective_distance and \
            (speed > 0 and x < landing_site_coords[0] or \
                speed < 0 and x > landing_site_coords[0]):
            rotate *= -1
        elif objective_distance > flat_surface_len \
            and y < landing_site_coords[1] + abs(3000 - landing_site_coords[1])//2:
            rotate = 0
            if params["v_speed"] < 0:
                power = 4
    elif landing_phase == 2:
        rotate = 0
        if braking_distance < objective_distance:
            power = 0
        else:
            power = 4

    return (round(rotate), power, landing_phase)

landing_phase = 1
# game loop
while True:
    x, y, h_speed, v_speed, fuel, rotate, power = [int(i) for i in input().split()]
    
    flat_surface_len, landing_site_coords = find_landing_site(lst_land_x, lst_land_y)

    params = {"x": x, "y": y, "landing_site_coords": landing_site_coords, \
        "flat_surface_len": flat_surface_len, "h_speed": h_speed, \
            "v_speed": v_speed, "rotate": rotate, "power": power}

    rotate, power, landing_phase = control_acceleration(params, landing_phase, rotate, power)
    print(str(rotate) + " " + str(power))

import sys
from math import degrees, radians, cos, sin, acos, asin, hypot, copysign


def map_input():

    surface_n = int(input())  # Number of points to draw the surface of Mars.
    lst_land_x = []
    lst_land_y = []

    for i in range(surface_n):
        land_x, land_y = [int(j) for j in input().split()]

        lst_land_x.append(land_x)
        lst_land_y.append(land_y)

    return (lst_land_x, lst_land_y)


def find_landing_site(lst_land_x, lst_land_y):

    landing_site = {}
    flat_surface_len = 0
    for i in range(len(lst_land_x) - 1):
        j = i + 1
        while lst_land_y[i] == lst_land_y[j] and lst_land_x[j] < 6999:
            j += 1
        if not (lst_land_x[j - 1] - lst_land_x[i] < 1000):
            flat_surface_len = lst_land_x[j - 1] - lst_land_x[i]
            landing_site["x"] = lst_land_x[i] + flat_surface_len//2
            landing_site["y"] = lst_land_y[i]

    return (flat_surface_len, landing_site)


def control_acceleration(p, landing_stage, rotate, power):

    landing_stage = 1  # Move horizontally over the landing site.
    speed = p["h_speed"]
    target_distance = {"x": abs(landing_site["x"] - x), "y": y}

    brake_angle = abs(degrees(acos(3.711 / 4)))
    if hypot(p["h_speed"], p["v_speed"]) > 0:
        radian_angle = abs(p["h_speed"] / hypot(p["h_speed"], p["v_speed"]))
        brake_angle = copysign(1, speed) * (degrees(asin(radian_angle)))
    max_deceleration = abs(4 * sin(brake_angle))

    left_time_to_land = 7
    if p["v_speed"] != 0:
        left_time_to_land = abs(landing_site["y"] - y) / abs(p["v_speed"])

    if (abs(speed) <= 3 or left_time_to_land <= 6) \
            and x >= landing_site["x"] - p["flat_surface_len"] // 2 \
            and x <= landing_site["x"] + p["flat_surface_len"] // 2:
        landing_stage = 2  # Land vertically when over the landing site.
        brake_angle = 0
        max_deceleration = 4 - 3.711
        speed = p["v_speed"]
        target_distance["x"] = x
        target_distance["y"] = abs(landing_site["y"] - y)

    # We compute the distance required to stop the space shuttle
    # given its speed and maximum thrust power of deceleration.
    braking_distance = 0
    if max_deceleration != 0:
        t_dist = 4 * abs(speed)
        braking_distance = t_dist + -pow(speed, 2) / (2 * -max_deceleration)

    if landing_stage == 1:
        rotate = degrees(acos(3.711 / 4))
        power = 4
        if x < landing_site["x"]:
            rotate *= -1
        elif x > landing_site["x"]:
            rotate *= 1
        if braking_distance >= target_distance["x"] or abs(speed) > 100:
            rotate = brake_angle
        elif y < landing_site["y"] + abs(3000 - landing_site["y"]) // 2 \
                and target_distance["x"] > p["flat_surface_len"] // 2:
            rotate = 0
    elif landing_stage == 2:
        rotate = 0
        if braking_distance < target_distance["y"]:
            power = 0
        else:
            power = 4

    return (round(rotate), power, landing_stage)

lst_land_x, lst_land_y = map_input()
flat_surface_len, landing_site = find_landing_site(lst_land_x, lst_land_y)

landing_stage = 1
# game loop
while True:
    x, y, h_speed, v_speed, fuel, rotate, power = \
        [int(i) for i in input().split()]

    p = {
            "x": x,
            "y": y,
            "landing_site": landing_site,
            "flat_surface_len": flat_surface_len,
            "h_speed": h_speed,
            "v_speed": v_speed,
            "rotate": rotate,
            "power": power
        }

    rotate, power, landing_stage = control_acceleration(
                                                            p,
                                                            landing_stage,
                                                            rotate,
                                                            power
                                                       )

    print(str(int(rotate)) + " " + str(power))

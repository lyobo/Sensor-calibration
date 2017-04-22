# -*- coding: utf-8 -*-
# Joy wang
# 2017.04.21

import math
# it is a test data
def solar_location_cal(year,month,day,hour,minute,jingdu,weidu):
    # test data
    # year = 2017
    # month = 2
    # day = 17

    # jingdu = 116.35964512825012
    # weidu = 39.96041193087462
    # hour = 13
    # minute = 00

    N_temp = 79.6764 + 0.2422*(year-1985)-math.floor((year-1985)/4)

    A = year/4
    B = A - math.floor(A)
    C = 32.8
    if month <= 2:
        C = 30.6
    if (B == 0) and (month > 2):
        C = 31.8
    # 积日
    G = math.floor(30.6*month- C + 0.5) + day

    L = jingdu/15
    H =(hour - 8 + minute/60)
    N = G+ (H - L)/24

    # 日角
    theta = (2 * math.pi * (N - N_temp))/365.2422
    #theta = math.radians(theta)

    # 求赤纬
    delta = 0.3723+23.2567*math.sin(theta)+0.1149*math.sin(2*theta)-0.1712*math.sin(3*theta)-0.758*math.cos(theta)+0.3656*math.cos(2*theta)+0.0201*math.cos(3*theta)

    # 求时差
    Eq = 0.0028-1.9857*math.sin(theta)+9.9059*math.sin(2*theta)-7.0924*math.cos(theta)-0.6882*math.cos(2*theta)
    # 太阳时角
    LC = 4*(math.floor(jingdu) - 120)
    TT = hour + (minute + LC + Eq)/60
    omega = (TT-12)*15

    # 转弧度
    delta = math.radians(delta)
    phi = math.radians(weidu)
    omega = math.radians(omega)

    #太阳高度角
    solar_elevation = math.asin(math.sin(phi)*math.sin(delta) + math.cos(phi)*math.cos(delta)*math.cos(omega))
    solar_elevation_degree = math.degrees(solar_elevation)
    # 太阳方位角
    solar_azimuth_temp = (math.sin(solar_elevation)*math.sin(phi)-math.sin(delta))/(math.cos(solar_elevation)*math.cos(phi))
    solar_azimuth = math.acos(solar_azimuth_temp)
    solar_azimuth_degree_temp = math.degrees(solar_azimuth)
    if TT < 12:
        solar_azimuth_degree = 180 - solar_azimuth_degree_temp
    else:
        solar_azimuth_degree = 180 + solar_azimuth_degree_temp
    return solar_elevation_degree,solar_azimuth_degree

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件   :test.py
@说明   : 测试：
#         设置了道路的最高限速是100，那么我再把在这个路上走的车的
#         最大速度设置为110。那么这个车的限速是由谁决定呢？
@时间   :2021/08/10 16:38:57
@作者   :TaoHong
@版本   :v1.0
'''


import traci
import sumolib
from tqdm import tqdm
import pandas as pd


def main_test(car_speed, road_speed, use_gui= False):

    if use_gui:
        sb = sumolib.checkBinary('sumo-gui')
    else:
        sb = sumolib.checkBinary('sumo')

    traci.start([sb,
                "-n", "test.net.xml",
                "-r", "test.rou.xml",
                "-b", "0",
                "--no-warnings", "true",
                "--delay","100",
                "--start", "true",
                "--quit-on-end", "true" 
                ])
    
    edge_list = ['gneE1', 'gneE2', 'gneE3', 'gneE4'] # 只有两个路段
    

    ## 1 道路的限速
    for x in range(len(edge_list)):
        traci.edge.setMaxSpeed(edge_list[x], road_speed[x])
    

    ## 2 考虑 车自带的限速  
    if car_speed > 0: # # car_speed = 0 # 表示不给车限速
        traci.vehicle.setMaxSpeed('vehicle_0', car_speed)


    ## 3 收集参数
    sp_list = []

    pbar = tqdm(range(200))
    while traci.simulation.getMinExpectedNumber() > 0:
        sp = traci.vehicle.getSpeed('vehicle_0') # 没有车的时候就会报错了

        sp_list.append(sp)

        t = traci.simulation.getTime()
        traci.simulationStep()  # 仿真跑一秒
        pbar.set_description(f"Processing: {t} ")
        pbar.update(1)

    traci.close()
    
    return sp_list # 返回列表


if __name__ == "__main__":

    use_gui = False
    # use_gui = True

    
    ##  车 有 限速值
    car_speed = 18
    road_speed = range(15, 19) 
    sp_y = main_test(car_speed, road_speed, use_gui)  
    
    ##  车 没有 限速值
    car_speed = 11 
    road_speed = range(11,15)
    sp_n = main_test(car_speed, road_speed, use_gui) # car_speed <= 0 # 表示不给车限速 

    min_len = min(len(sp_y), len(sp_n))


    da = pd.DataFrame()
    da["with"] = sp_y[0: min_len] # 保证长度一样
    da["without"] = sp_n[0: min_len] 

    da.to_csv('speed.csv', index= None)


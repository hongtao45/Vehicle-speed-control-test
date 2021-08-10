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
import matplotlib.pyplot as plt


def main_test(use_gui= False):
    if use_gui:
        sb = sumolib.checkBinary('sumo-gui')
    else:
        sb = sumolib.checkBinary('sumo')


    traci.start([sb,
                "-n", "test.net.xml",
                "-r", "test.rou.xml",
                "-b", "0",
                "-e", "200",
                "--no-warnings", "true",
                "--delay","100",
                "--start", "true",
                "--quit-on-end", "true" 
                ])
    
    edge_list = ['gneE1', 'gneE2', 'gneE3', 'gneE4'] # 只有两个路段
    
    ## 1 道路的限速
    maxSp =[5, 7, 9, 11]
    for x in range(len(edge_list)):
        traci.edge.setMaxSpeed(edge_list[x], maxSp[x])
    
    ## 2 车自身的限速
    traci.vehicle.setMaxSpeed('vehicle_0', 8)

    ## 3 收集参数
    sp_list = []
    sp2_list = []

    
    pbar = tqdm(range(200))
    for x in pbar:
        sp = traci.vehicle.getSpeed('vehicle_0')
        sp2 = traci.vehicle.getSpeedWithoutTraCI('vehicle_0') # 欸有traci影响时的速度

        sp_list.append(sp)
        sp2_list.append(sp2)

        
        t = traci.simulation.getTime()
        traci.simulationStep()  # 仿真跑一秒
        pbar.set_description(f"Processing: {t} ")

    traci.close()

    da = pd.DataFrame(sp_list)
    da['sp2'] = sp2_list

    da.columns =['sp', 'sp2']
    da.to_csv('speed.csv', index= None)


if __name__ == "__main__":

    use_gui = False
    # use_gui = True
    main_test(use_gui)


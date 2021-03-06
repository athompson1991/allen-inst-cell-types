#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 15:28:37 2020

@author: briardoty
"""
import argparse
from modules.Visualizer import Visualizer
from modules.NetManager import nets

# general params with defaults
parser = argparse.ArgumentParser()
parser.add_argument("--data_dir", default="/home/briardoty/Source/allen-inst-cell-types/data/", type=str, help="Set value for data_dir")
parser.add_argument("--net_name", default="vgg11", type=str, help="Set value for net_name")
parser.add_argument("--n_classes", default=10, type=int, help="Set value for n_classes")

# required params
parser.add_argument("--case", type=str, help="Set value for case")


def main(data_dir, net_name, n_classes, case):
    
    # init visualizer
    visualizer = Visualizer(data_dir, net_name, n_classes, True)
    
    # plot
    visualizer.plot_type_specific_weights(case)
    
    print(f"vis_case.py completed")
    return

if __name__=="__main__":
    args = parser.parse_args()
    print(args)
    main(**vars(args))


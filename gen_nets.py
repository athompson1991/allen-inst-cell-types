#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 12:11:26 2020

@author: briardoty
"""
import argparse
from modules.NetManager import NetManager

# general params with defaults
parser = argparse.ArgumentParser()
parser.add_argument("--data_dir", default="/home/briardoty/Source/allen-inst-cell-types/data/", 
                    type=str, help="Set value for data_dir")
parser.add_argument("--net_name", default="vgg11", type=str, help="Set value for net_name")
parser.add_argument("--n_classes", default=10, type=int, help="Set value for n_classes")
parser.add_argument("--n_samples", default=10, type=int, help="Set value for n_samples")

# config params without defaults
parser.add_argument("--case", type=str, help="Set value for case")
parser.add_argument("--layer_names", type=str, nargs="+", help="Set value for layer_names")
parser.add_argument("--n_repeat", type=int, help="Set value for n_repeat")
parser.add_argument("--act_fns", type=str, nargs="+", help="Set value for act_fns")
parser.add_argument("--act_fn_params", type=str, nargs="+", help="Set value for act_fn_params")

# pretrained is a PITA since it's a bool
pretrained_parser = parser.add_mutually_exclusive_group(required=False)
pretrained_parser.add_argument('--pretrained', dest='pretrained', action='store_true')
pretrained_parser.add_argument('--untrained', dest='pretrained', action='store_false')
parser.set_defaults(pretrained=False)

def main(case, layer_names, n_repeat, act_fns, act_fn_params, data_dir, 
         net_name, n_classes, n_samples, pretrained):
    
    # init net manager
    manager = NetManager(net_name, n_classes, data_dir, pretrained=pretrained)
    
    # build and save nets
    for i in range(n_samples):

        # init net
        manager.init_net(case, i)
        
        # control nets are unmodified
        if (layer_names is not None and
            len(layer_names) > 0):
            manager.replace_layers(layer_names, n_repeat, act_fns, act_fn_params)
        
        # save
        manager.save_net_snapshot()

    print(f"gen_nets.py completed case {case}")
    return   

if __name__=="__main__":
    args = parser.parse_args()
    print(args)
    main(**vars(args))









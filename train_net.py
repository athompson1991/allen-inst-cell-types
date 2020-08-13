#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 17:22:40 2020

@author: briardoty
"""
import sys
import argparse
from modules.NetManager import NetManager
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler

parser = argparse.ArgumentParser()
parser.add_argument("--data_dir", default="/home/briardoty/Source/neuro511-artiphysiology/data/", type=str, help="Set value for data_dir")
parser.add_argument("--net_name", default="vgg11", type=str, help="Set value for net_name")
parser.add_argument("--n_classes", default=10, type=int, help="Set value for n_classes")
parser.add_argument("--epochs", default=10, type=int, help="Set value for epochs")
parser.add_argument("--train_frac", default=1., type=float, help="Set value for train_frac")
parser.add_argument("--lr", type=float, required=True)
parser.add_argument("--lr_step_size", type=int, required=True)
parser.add_argument("--lr_gamma", type=float, required=True)
parser.add_argument("--batch_size", type=int, required=True)
parser.add_argument("--net_filepath", type=str, help="Set value for net_filepath")
parser.add_argument("--scheme", type=str, help="Set scheme", required=True)


def create_optimizer(name, manager, lr):

    if name == "sgd":
        return optim.SGD(manager.net.parameters(), lr=lr)
    elif name == "adam":
        return optim.Adam(manager.net.parameters())
    else:
        print(f"Unknown optimizer configured: {name}")
        sys.exit(1)

def get_training_vars(name, manager, lr, lr_step_size, lr_gamma):
    
    criterion = nn.CrossEntropyLoss()
    optimizer = create_optimizer(name, manager, lr)

    if name == "adam":
        scheduler = None
    else:
        scheduler = lr_scheduler.StepLR(optimizer, step_size=lr_step_size, 
            gamma=lr_gamma)

    return (criterion, optimizer, scheduler)

def main(net_filepath, data_dir, net_name, n_classes, epochs, train_frac,
         lr, lr_step_size, lr_gamma, batch_size, scheme):
    
    # init net manager
    manager = NetManager(net_name, n_classes, data_dir, scheme)
    manager.load_dataset(batch_size)
    
    # load the proper net
    manager.load_net_snapshot_from_path(net_filepath)
    
    # training scheme vars
    (criterion, optimizer, scheduler) = get_training_vars(scheme, 
        manager, lr, lr_step_size, lr_gamma)
     
    # manually step lr scheduler up to current epoch to preserve training continuity
    if manager.epoch > 0 and scheduler is not None:
        for i in range(manager.epoch):
            scheduler.step()

    # train
    manager.run_training_loop(criterion, optimizer, scheduler, train_frac, 
        n_epochs=epochs)
    
    print("net_train.py completed")
    return


if __name__=="__main__":
    args = parser.parse_args()
    print(args)
    main(**vars(args))
    
    
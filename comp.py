# compare_specific_monitor
# compare_all_monitors
# exit

import os
import json
import sys
import argparse

class Compare():

    def __init__(self,monitor_name,base_dir):
        self.monitor_name = monitor_name
        self.base_dir=base_dir
        self.dev = 'dev'
        self.prod = 'prod'
        self.output = {}
        self.full_output = {}

    def compare_json(self,path1,path2,name):
        for filename in os.listdir(path1):
            if filename.endswith(".json"):
                if name not in self.output:
                    self.output[name]={}
                self.output[name][filename] = {'changes':{},'added':[],'removed':[]}
                full_path1 = os.path.join(path1, filename)
                full_path2 = os.path.join(path2, filename)
                if not os.path.exists(full_path2):
                    print('File not available in prod.')
                else:
                    with open(full_path1) as json_file:
                        d1 = json.load(json_file)
                    with open(full_path2) as json_file:
                        d2 = json.load(json_file)
                    for k in d2:
                        if (k not in d1):
                            self.output[name][filename]['added'].append(k)

                    self.findDiff(d1,d2,'',name,filename)
                    temp = self.output
                    self.full_output[name] = {filename:temp[name]}


    def findDiff(self,d1, d2, path="",name="",filename=""):
        for k in d1:
            if (k not in d2):
                if path == '':
                    self.output[name][filename]['removed'].append(k)
                else:
                    self.output[name][filename]['removed'].append(path+'->'+k)
            else:
                if type(d1[k]) is dict:
                    if path == "":
                        path = k
                    else:
                        path = path + "->" + k
                    self.findDiff(d1[k],d2[k], path,name,filename)
                else:
                    if d1[k] != d2[k]:
                        self.output[name][filename]['changes'][path+'->'+k] = {'old':d1[k],'new':d2[k]}

    def compare_monitor(self):
        self.dev_path = os.path.join(self.base_dir,self.dev,self.monitor_name)
        if self.monitor_name == 'all':
            dev_dir = os.path.join(self.base_dir,self.dev)
            print('Comparing all folders')
            output = [dI for dI in os.listdir(dev_dir) if os.path.isdir(os.path.join(dev_dir,dI))]
            # print(output)
            for folder in output:
                self.prod_path = os.path.join(self.base_dir,self.prod,folder)
                self.dev_path = os.path.join(self.base_dir,self.dev,folder)
                self.compare_json(self.dev_path,self.prod_path,folder)
        elif not os.path.isdir(self.dev_path):
            print('The folder specified does not exist')
            sys.exit()
        else:
            print('Comparing: {}'.format(self.monitor_name))
            self.prod_path = os.path.join(self.base_dir,self.prod,self.monitor_name)
            self.compare_json(self.dev_path,self.prod_path,self.monitor_name)
    def exit():
        pass

my_parser = argparse.ArgumentParser(description='Compare content')
my_parser.add_argument('Folder',metavar='folder',type=str,help='name of folder')
my_parser.add_argument('base_dir',metavar='base_dir',type=str,help='base dir')

args = my_parser.parse_args()
folder = args.Folder
base_dir = args.base_dir
if not os.path.isdir(base_dir):
    print('Incorrect Base Dir')
    sys.exit()
comp = Compare(folder,base_dir)
comp.compare_monitor()
print(json.dumps(comp.output, indent=4, sort_keys=True))

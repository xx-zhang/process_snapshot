# coding:utf-8 

import os
import sys
import json
import re
from datetime import datetime

filepath = "C:/Users/xxxxx/Downloads/go-audit.log"


import sys
from collections import defaultdict

class Process:
    def __init__(self, timestamp, pid, ppid, cmd):
        self.timestamp = timestamp
        self.pid = pid
        self.ppid = ppid
        self.cmd = cmd
        self.children = []

    def __str__(self):
        return f"{self.cmd}({self.pid})-{self.timestamp}"


def gen_process_data(pp, filterd_data):
    "通过父进程查询子进程形成数"
    # print(x)
    # print(f"输入类型 >>  {type(pp)}")
    __time_local, pid, ppid, cmd = pp['time_local'], pp['pid'], pp['ppid'], pp['cmdline']
    # sub_datas = [k for k in filterd_data if k['ppid'] == pid] # 找出当前进程的子进程
    process = Process(__time_local, pid, ppid, cmd)
    sub_datas = []
    for k in filterd_data:
        try:
            if k['ppid'] == pid:
                sub_datas.append(k)
        except Exception as e:
            pass 
    
    if len(sub_datas) < 1:
        pass
    else:
        for sub_pp in sub_datas:
            sub_process = gen_process_data(sub_pp, filterd_data)
            process.children.append(sub_process)
    return process


def print_tree(process, depth=0, prefix="   "):
    if depth == 0:
        print("┬─" + str(process)) 
    else:
        print(prefix[:-3] + "├─ " + str(process))
    if len(process.children) > 0:
        prefix += "│  "
    else:
        prefix += "   "
    for i, child in enumerate(process.children):
        if i == len(process.children) - 1:
            print_tree(child, depth + 1, prefix[:-3] + "└─ ")
        else:
            print_tree(child, depth + 1, prefix)


if __name__ == "__main__":
    with open(filepath, "r", encoding="utf-8") as f:
        datas = [json.loads(x) for x in f.readlines()]
        f.close()
    # https://github.com/torvalds/linux/blob/master/include/uapi/linux/audit.h
    audit_types = []
    cnts = 0
    process_datas = []
    for x in datas:
        # 这个地方应该是传递进去 type 后自己去寻找对应的方法，而不是一个个来便利方法，下面是一个简单的示例
        # for y in x["messages"]:
        #     audit_types.append(y["type"])
        #     # {1321, 1325, 1326, 1327, 1300, 1302, 1305, 1306, 1307, 1309}
        __temp = dict(cmdline="", )
        __temp['time_local'] = datetime.strftime(datetime.fromtimestamp(int(x['timestamp'].split('.')[0])), '%Y-%m-%d %H:%M:%S')
        if 1327 in [y["type"] for y in x["messages"]]:
            cnts += 1
            cmdline_og = [y["data"] for y in x["messages"] if y["type"]==1327][0]
            try:
                cmdline = bytes.fromhex(re.match("proctitle=(\w+)", cmdline_og).group(1)).decode().replace("\x00", " ")
            except AttributeError as e :
                cmdline = ""
            # print(cmdline)
            __temp["cmdline"] = cmdline
        if 1300 in [y["type"] for y in x["messages"]]:
            pid_og = [y["data"] for y in x["messages"] if y["type"]==1300][0]
            ppid_info = re.findall("(\w+)=([\w\"]+)", pid_og)
            pinfo_dict = {x[0]:x[1] for x in ppid_info}
            __temp = dict(__temp, **pinfo_dict)

        if 1307 in [y["type"] for y in x["messages"]]:
            cwd_og = [y["data"] for y in x["messages"] if y["type"]==1307][0]
            workdir = re.match("\s*cwd=\"(.*)\".*", cwd_og).group(1)
            __temp = dict(workdir=workdir, **__temp)

        if "pid" not in __temp.keys():
            continue

        if "time_local" not in __temp.keys():
                continue
        # print(json.dumps(__temp, indent=2) )
        process_datas.append(__temp)
    
    # 这个地方只是取到500条记录。还有一些没有取
    process_datas = process_datas[:500]
    # print(type(process_datas[1]))
    # print(json.dumps(process_datas[1], indent=2))
    # 开始向上寻找父亲节点
    process_results = []
    for x in process_datas:
        # print(type(x))
        __local_process_tree_data  = gen_process_data(x, process_datas)
        # process_results.append(__local_data)
        print_tree(__local_process_tree_data)
        print("\n\n")

    print("="*30)

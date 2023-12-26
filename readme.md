# 日志来源是来自
- https://github.com/slackhq/go-audit
    - `go build`


## 程序编写
- 读取所有的日志父子进程都输出
- 参考所有的类型有 [linux/audit.h](https://github.com/torvalds/linux/blob/master/include/uapi/linux/audit.h)


## 日志 tree 打印和查看
```python

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
```
#!/usr/bin/env python3
# _*_ coding: UTF-8 _*_

"""
update network resource of clash config

Usage:
    update_res.py -d <cfg_dir> [[-c <cfg_rel_path>] | [-f <profile_path>] [-n <cfg_name>]] [-p <proxy>]

Options:
    -h --help                 Get help.
    -d <cfg_dir>              clash 的配置路径。
    -c <cfg_rel_path>         clash 的配置的相对路径。如果不指定则会选择 `profiles/list.yml` 所选的配置文件。
    -f <profile_path>         profiles 的绝对路径。如果不指定则是默认的 profile 路径。
    -n <cfg_name>             clash 的配置文件的名称。会根据 `profiles/list.yml` 的 `name` 所对应的配置文件。`name` 可以同名，所以要注意。
    -p <proxy>                使用代理更新。比如：`-p socks5://127.0.0.1:7890`。

Examples:
    # 更新 list 所选的配置的资源。当加载出错时，list 的 index 会是 -1，所以要在没有出错前，运行该程序。
    update_res.py -d '/c/Users/johan/.config/clash' -p 'socks5://127.0.0.1:7890'
    # 更新 list 配置的 name 对应的配置的资源
    update_res.py -d '/c/Users/johan/.config/clash' -n 'myconfig' -p 'socks5://127.0.0.1:7890'
    # 更新 `config.yaml` 配置的资源
    update_res.py -d '/c/Users/johan/.config/clash' -c 'config.yaml' -p 'socks5://127.0.0.1:7890'
    # 非默认的 profile 路径
    update_res.py -d '/c/Users/johan/.config/clash' -f '/c/Users/johan/Desktop/profiles' -n 'config_mobile.yaml'

"""

import sys, os, getopt

from ruamel.yaml import YAML

def update_res(clash_cfg_dir, cfg_rel_path = None, profile_path = None, cfg_name = None, proxy = None):
    cfg_path = get_cfg_path(clash_cfg_dir, profile_path, cfg_rel_path, cfg_name)
    net_res = get_net_res(cfg_path)
    update_net_res(net_res, clash_cfg_dir, proxy)
    print(f"updated the resource needed by '{cfg_path}'")

def get_cfg_path(clash_cfg_dir, profile_path = None, cfg_rel_path = None, cfg_name = None):
    yaml = YAML(typ='safe')

    cfg_path = ''
    if not cfg_rel_path:
        # ### 从 list.yml 中选择配置
        # #### 读取 list.yml
        if not profile_path:
            # 选择 profile 的默认路径
            profile_path = os.path.join(clash_cfg_dir, './profiles')

        list_path = os.path.join(profile_path, './list.yml')
        if not os.path.exists(list_path):
            sys.stderr.write(f"list.yml: {list_path} isn't exist!\n")
            sys.exit(os.EX_USAGE)

        with open(list_path, 'r', encoding='utf-8') as f:
            list_data = yaml.load(f)

        # #### 如果指定 cfg_name 则使用 cfg_name 所对应的配置
        if cfg_name:
            for x in list_data['files']:
                if x['name'] == cfg_name:
                    cfg_path = os.path.join(clash_cfg_dir, f'profiles/{x["time"]}')
        # #### 如果没有指定 cfg_name 则当前选定的配置
        else:
            list_index = list_data['index']
            if list_index < 0:
                sys.stderr.write('Please select your profile.')
                sys.exit(os.EX_USAGE)
            cfg_rel_path = list_data['files'][list_index]['time']
            cfg_path = os.path.join(clash_cfg_dir, 'profiles/' + cfg_rel_path)
    else:
        cfg_path = os.path.join(clash_cfg_dir, cfg_rel_path)

    if not os.path.exists(cfg_path):
        sys.stderr.write(f"cfg_path: {cfg_path} isn't exists.")
        sys.exit(os.EX_USAGE)

    return cfg_path

def get_net_res(cfg_path):
    # ### 加载 cfg
    yaml = YAML(typ='safe')
    with open(cfg_path, 'r', encoding='utf-8') as f:
        cfg_data = yaml.load(f)

    # ### 取出 proxy_provider 的数据
    proxy_provider = cfg_data['proxy-providers']

    # ### 将 type == 'http' 的项的 url 和 path 放入 net_res
    # network resource
    net_res = []
    for i in proxy_provider.values():
        if i['type'] == 'http':
            net_res.append([i['url'], i['path']])

    return net_res

def update_net_res(net_res, clash_cfg_dir, proxy=None):
    # ### 下载 net_res 里的资源
    # 保存环境
    oldcwd = os.getcwd()
    os.chdir(clash_cfg_dir)

    timeout_param = '--connect-timeout 30'
    proxy_param = ''
    if proxy:
        proxy_param = 'ALL_PROXY=' + proxy

    for i in net_res:
        #  dirpath = os.path.dirname(i[1])
        #  if not os.path.exists(dirpath):
        #      os.makedirs(dirpath)
        cmd = f"/usr/bin/env {proxy_param} curl {timeout_param} -fLo '{i[1]}' --create-dirs '{i[0]}'"
        os.system(cmd)
        print(f'DONE: {i[1]}, {i[0]}')

    # 恢复环境
    os.chdir(oldcwd)

def usage():
    print(__doc__)

def main():
    # ### parse args
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'd:c:f:n:p:h', ['', '', '', '', '', 'help'])
    except getopt.GetoptError:
        usage()
        sys.exit(os.EX_USAGE)

    cfg_dir = None
    profile_path = None
    cfg_rel_path = None
    cfg_name = None
    proxy = None

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt in ('-d'):
            cfg_dir = arg
        elif opt in ('-f'):
            profile_path = arg
        elif opt in ('-c'):
            cfg_rel_path = arg
        elif opt in ('-n'):
            cfg_name = arg
        elif opt in ('-p'):
            proxy = arg
        else:
            usage()
            sys.exit(os.EX_USAGE)

    # ### 更新资源
    update_res(cfg_dir, cfg_rel_path = cfg_rel_path, profile_path = profile_path, cfg_name = cfg_name, proxy = proxy)

if __name__ == '__main__':
    main()

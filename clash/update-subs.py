#!/usr/bin/env python3
# _*_ coding: UTF-8 _*_

import os, re, sys
from ruamel.yaml import YAML
from update_res import update_res

def filter_proxies(net_res_files, clash_cfg_dir):
    # 保存环境
    oldcwd = os.getcwd()
    os.chdir(clash_cfg_dir)

    yaml = YAML(typ='safe')
    # pf: proxy_file
    for pf in net_res_files:
        with open(pf, 'r', encoding='utf-8') as f:
            proxy_data = yaml.load(f)
        # 过滤出有 `Mb` 字样的节点
        proxies = [x for x in proxy_data['proxies'] if re.search(r'\|.*[0-9]+\s*\.[0-9]+\s*Mb', x['name'])]

        # 如果为空
        if not proxies:
            # 保存原样
            continue

            # 插入一个 NULL 节点
            #  proxies.append({"name":"NULL","server":"NULL","port":11708,"type":"ssr","country":"NULL","password":"sEscPBiAD9K$\u0026@79","cipher":"aes-256-cfb","protocol":"origin","protocol_param":"NULL","obfs":"http_simple"})

        with open(pf, mode='w', encoding='utf-8') as f:
            yaml.dump({'proxies': proxies}, f)

    # 恢复环境
    os.chdir(oldcwd)

# net_res_files 的路径 src_clash_cfg_dir 是相对路径
def install_proxy_providers(net_res_files, src_clash_cfg_dir, dest_clash_cfg_dir):
    for x in net_res_files:
        src_file = os.path.join(src_clash_cfg_dir, x)
        dest_file = os.path.join(dest_clash_cfg_dir, x)
        if not os.path.exists(os.path.dirname(dest_file)):
            os.system(f'sudo -u nobody mkdir -p {os.path.dirname(dest_file)}')
        os.system(f'sudo install -o nobody -g nobody -m 0644 {src_file} {dest_file}')

def main():
    # 要注意 home_path 是否正确
    #  user=os.environ['USER']
    home_path=os.environ['HOME']
    clash_cfg_dir = os.path.join(home_path, '.config/clash_tun')

    cfg_rel_path = 'config.yaml'
    if len(sys.argv) > 1:
        cfg_rel_path = sys.argv[1]
    cfg_path = update_res.get_cfg_path(clash_cfg_dir, cfg_rel_path = cfg_rel_path)
    net_res = update_res.get_net_res(cfg_path)
    # 更新节点
    #  proxy='socks5://127.0.0.1:7890'
    proxy=None
    update_res.update_net_res(net_res, clash_cfg_dir, proxy=proxy)

    # ## 过滤节点
    net_res_files = [x[1] for x in net_res]
    #  filter_proxies(net_res_files, clash_cfg_dir)

    # ## install to /srv/clash
    src_clash_cfg_dir = clash_cfg_dir
    dest_clash_cfg_dir = '/srv/clash'
    install_proxy_providers(net_res_files, src_clash_cfg_dir, dest_clash_cfg_dir)

    os.system('sudo systemctl restart clash')
    #  print('Please reload your profile or config.')

if __name__ == '__main__':
    main()

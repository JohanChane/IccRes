# IccRes

Resources for Internet censorship circumvention

## Clash

### 准备

如果不能翻墙，则导入 `config_basic`。确保能翻墙后，再操作。

    https://cdn.jsdelivr.net/gh/JohanChane/IccRes@main/clash/config_basic.yaml

### Android 平台

用 Clash for Android。直接导入配置即可。

注意: 在 clash 的配置页面中更新配置时, 会更新配置文件但是不会更新配置中被墙的资源。解决办法是:

1.  更新配置
2.  进入"外部资源", 手动更新资源。如果更新失败, 重新导入配置即可。

### Windows 平台

使用 Clash for Windows

1.  [开启 tun 模式](https://docs.cfw.lbyczf.com/contents/tun.html#windows)。
2.  将 [yacd](https://github.com/haishanh/yacd/archive/gh-pages.zip) 解压到 `Users/<user>/.config/clash`, 并修改解压后的目录为 `yacd`。
3.  导入配置。比如：在 github 打开配置的文件，并点击 "Raw" 按钮，然后复制 url，再然后在 Clash for Windows 中导入该 url。
4.  切换到该配置。打开 [yacd](http://127.0.0.1:9090/ui/#/proxies)。

如果无法切换该配置时

1.  安装运行 linux shell 的工具。比如：msys64。
2.  找到导入配置的名称。比如：`config_yugogo.yaml`。并确保名称唯一。
3.  切换回一个可翻墙的配置。然后用 `update_res` 更新刚导入配置的资源。比如：`./update_res.py -d '/c/Users/johan/.config/clash' -n 'config_yugogo.yaml'`。

#### `update-subs.py` (optional)

用脚本更新订阅。

用法

1.  将 `update_res` 目录复制到当前目录
2.  复制 `update-subs-win.py` 到当前目录
3.  使用 `update-subs-win`

        # 比如：`./update-subs-win.py config.yaml`
        ./update-subs-win.py <cfg_name>

### Linux 平台

安装 [Kr328/clash-premium-installer](https://github.com/Kr328/clash-premium-installer)

安装之后

```shell
sudo chmod a+x /srv/clash
# 非 root 用户。用于存放 clash 配置。
mkdir ~/.config/clash_tun
将 [yacd](https://github.com/haishanh/yacd/archive/gh-pages.zip) 解压到 clash_tun, 并修改解压后的目录为 `yacd`。
ln -s /srv/clash/yacd ~/.config/clash_tun/yacd

sudo systemctl edit clash.service
    # 清除之前的 ExecStart
    ExecStart=
    # 添加 ExecStart
    ExecStart=/usr/bin/bypass-proxy /usr/bin/clash -d /srv/clash -f /home/<user>/.config/clash_tun/config.yaml
sudo systemctl restart clash.service
```

yacd

> 在浏览器中输入 `http://127.0.0.1:9090/ui/#/`

#### `update-subs.py` (optional)

用脚本更新订阅。

1.  将 `update_res` 目录复制到当前目录
2.  复制 `update-subs.py` 到当前目录
3.  使用 `update-subs`

        # 比如：`./update-subs.py config.yaml`
        ./update-subs.py <cfg_name>

### yacd

因为有些节点不支持 SSL, 所以可将延时测速 URL 改为 `https`, 即 `https://www.gstatic.com/generate_204`。这样可排除不支持 SSL 的节点。虽然节点的延时时间总体时间会增加一点, 但是实际延时和原来一样。

### `update_res`

[`update_res`](https://github.com/JohanChane/IccRes/tree/main/clash/update_res) 用于更新 clash 配置的资源。

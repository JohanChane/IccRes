# IccRes

Resources for Internet censorship circumvention

## Clash

### 准备

如果不能翻墙，则导入 `config_basic`。确保能翻墙后，再操作。

    https://cdn.jsdelivr.net/gh/JohanChane/IccRes@main/clash/config_basic.yaml

### Android 平台

用 Clash for Android。直接导入配置即可。

### Windows 平台

用 Clash for Windows, 并[开启 tun 模式](https://docs.cfw.lbyczf.com/contents/tun.html#windows)。

1.  安装运行 linux shell 的工具。比如：msys64。
2.  导入配置。比如：在 github 打开配置的文件，并点击 "Raw" 按钮，然后复制 url，再然后在 Clash for Windows 中导入该 url。
3.  找到导入配置的名称。比如：`config_yugogo.yaml`。并确保名称唯一。
4.  用 `update_res` 更新刚导入配置的资源。比如：`./update_res.py -d '/c/Users/johan/.config/clash' -n 'config_yugogo.yaml'`。
5.  切换到该配置。

#### `update-subs.py`

更新并过滤配置的节点。

用法

```shell
curl -fLo update-subs.py --create-dirs 'https://raw.githubusercontent.com/JohanChane/IccRes/main/clash/update-subs.py'
# 比如：`./update-subs.py config_yugogo.yaml`
./update-subs.py <cfg_name>
```

### `update_res`

[`update_res`](https://github.com/JohanChane/IccRes/tree/main/clash/update_res) 用于更新 clash 配置的资源。

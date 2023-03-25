# IccRes

Resources for Internet censorship circumvention

## Clash

### Android 平台

使用 Clash for Android。

### Windows 平台

使用 Clash for Windows

1.  [开启 tun 模式](https://docs.cfw.lbyczf.com/contents/tun.html#windows)。
2.  将 [yacd](https://github.com/haishanh/yacd/archive/gh-pages.zip) 解压到 `Users/<user>/.config/clash`, 并修改解压后的目录为 `yacd`。
3.  导入配置。比如：在 github 打开配置的文件，并点击 "Raw" 按钮，然后复制 url，再然后在 Clash for Windows 中导入该 url。
4.  切换到该配置。打开 [yacd](http://127.0.0.1:9090/ui/#/proxies)。

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

打开 [yacd](http://127.0.0.1:9090/ui/#/proxies)。

### yacd

因为有些节点不支持 SSL, 所以可将延时测速 URL 改为 `https`, 即 `https://www.gstatic.com/generate_204`。这样可排除不支持 SSL 的节点。虽然节点的延时时间总体时间会增加一点, 但是实际延时和原来一样。

### update_clashcfg_res

在 Windows 和 Linux 平台使用 Clash 时, 如果无法切换该配置时, 可以使用 [update_clashcfg_res](https://github.com/JohanChane/update-clash-resources.git) 来更新配置。前提有一个配置可以翻墙。

## 生成 Clash 配置

### 使用订阅转换

有些机场是提供 Clash 配置的, 可以在 url 之后添加 `&clash=1` 或 `flag=clash`, 具体情况要询问机场方。如果没有则可以使用订阅转换。有如下订阅转换站点:

-   [不被墙的订阅转换有推荐吗？](https://clashios.com/unblocked-subconvert-websites/)

将转换之后的链接加入 `config_template.yaml` 的 `proxy-providers url`。比如:

```
proxy-providers:
  main:
    type: http
    url: "<your url>"
    path: ./proxy-providers/NodeList/main.yaml
    interval: 3600
    health-check:
      enable: true
      interval: 600
      url: https://www.gstatic.com/generate_204
```

### (optional) 将 Clash 配置放到 gitlab 的私有库

1.  在 gitlab 上创建私有库。
2.  创建 "个人访问令牌" 有 `read_repository` 权限即可。
3.  找到仓库的 project id。`项目设置->通用->项目ID`。
4.  以这样的格式访问文件。

    ```
    https://gitlab.com/api/v4/projects/<project_id>/repository/files/<dir>%2F<file>/raw?ref=main&private_token=<your token>
    # 比如: 项目的 Clash 配置的路径是 `Clash/config.yaml`
    https://gitlab.com/api/v4/projects/<project_id>/repository/files/Clash%2Fconfig.yaml/raw?ref=main&private_token=<your token>
    ```

5.  clash 导入仓库的 clash 配置文件的链接即可。token 有 url 中, 要注意保护 token。

## `config_template` 的使用说明

LastMatch: 最后一条规则的流量入口。
    
-   DIRECT: 直连。表示黑名单模式。意为 "只有命中规则的网络流量，才使用代理"，适用于服务器线路网络质量不稳定或不够快，或服务器流量紧缺的用户。比较安全。
-   ENTRY: 代理。表示白名单模式。意为 "没有命中规则的网络流量，统统使用代理"。适用于服务器线路网络质量稳定、快速，不缺服务器流量的用户。

Entry 开头的表示是一个流量入口, 其中:

-   Entry-ChatGpt: 表示 ChatGpt 的流量入口。
-   Entry: 除了上面的流量的入口。

## 附加

-   [Clash doc](https://lancellc.gitbook.io/clash/)
-   [Clash for Windows doc](https://docs.cfw.lbyczf.com/)
-   [Clash cfg](https://github.com/Dreamacro/clash/wiki/configuration)

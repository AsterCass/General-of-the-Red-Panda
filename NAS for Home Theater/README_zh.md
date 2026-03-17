# 使用旧电脑搭建家庭影院

[English](README.md) | 中文

## 介绍

使用家中的旧电脑改装成NAS作为家庭影院，可以在家庭中其他手机，平板，电脑等等设备中直接观看以及管理视频。不需要手动下载任何虚拟机，也不需要修改操作系统，对电脑性能也几乎没有要求，只是要安装步骤输入一下字符就能轻松实现

## 具体文档

具体文档以及相关拓展更多内容可以访问：[点击此处](https://www.astercasc.com/article/detail?articleId=AT199028468800214220)

以及[家用网络下构建外网可访问的内网服务器（续篇）](https://www.astercasc.com/article/detail?articleId=AT203391896848146841)

如果有任何问题也可在该链接网址的最下方留言

## 相关资源下载地址

[点击此处](https://pan.baidu.com/s/5P4zJnQ1tJkycI24FEcJC4Q)

## 代码

### WSL相关内容

微软官网手动安装WSL：[点击此处](https://learn.microsoft.com/zh-cn/windows/wsl/install-manual)

```shell
# 查看当前WSL版本
wsl -v
# 安装WSL框架（如果你电脑使用 wsl -v 无法看到版本号的话）
wsl --install
# 切换到WSL2版本
wsl --set-default-version 2
# 查看当前宿主机已经安装WSL镜像容器以及状态
wsl --list --verbose
# 彻底删除某个容器
wsl --unregister Ubuntu-22.04
# 安装某个镜像容器
wsl --install Ubuntu-22.04
# 进入某个容器
wsl -d Ubuntu-22.04
# 指定文件安装外部镜像容器（修改安装地址和打包文件所在地址）
wsl --import Ubuntu-jjdyycm C:\Users\astercasc X:\red.panda\new\jjdyycm.tar
```

### Linux 相关（即你使用的是原生Linux或者已经使用【WSL -d 指定容器名】进入容器）

```shell
# 进入root身份，如果使用提供的镜像默认密码123456，如果是自己的容器就是你自己设置的密码
sudo su
# 安装docker
apt remove $(dpkg --get-selections docker.io docker-compose docker-compose-v2 docker-doc podman-docker containerd runc | cut -f1) \
&& apt update \
&& apt install -y ca-certificates curl gnupg \
&& install -m 0755 -d /etc/apt/keyrings \
&& curl -fsSL https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
&& echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null \
&& apt update \
&& apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
# 配置源
systemctl enable docker
cat <<'EOF' > /etc/docker/daemon.json
{
  "registry-mirrors": [
    "https://docker.xuanyuan.me",
    "https://docker.m.daocloud.io",
    "https://docker.1ms.run",
    "https://docker.1panel.live",
    "https://docker.hlmirror.com"
  ]
}
EOF
systemctl restart docker
# 安装 jellyfin
mkdir  -p /home/service/jellyfin/config
mkdir  -p /home/service/jellyfin/cache
mkdir  -p /home/service/jellyfin/data/videos
mkdir  -p /home/service/jellyfin/data/musics
mkdir  -p /home/service/jellyfin/data/pictures
mkdir  -p /home/service/jellyfin/data/fonts
cd /home/service/jellyfin
cat <<'EOF' > /home/service/jellyfin/docker-compose.yml
services:
  jellyfin:
    image: jellyfin/jellyfin
    container_name: jellyfin
    network_mode: "host"
    volumes:
      - /home/service/jellyfin/config:/config
      - /home/service/jellyfin/cache:/cache
      - type: bind
        source: /home/service/jellyfin/data/videos
        target: /videos
      - type: bind
        source: /home/service/jellyfin/data/musics
        target: /musics
      - type: bind
        source: /home/service/jellyfin/data/pictures
        target: /pictures
      - type: bind
        source: /home/service/jellyfin/data/fonts
        target: /fonts
        read_only: true

    restart: 'unless-stopped'
    extra_hosts:
      - 'host.docker.internal:host-gateway' 
EOF
docker compose up -d
```

### Windows相关命令

```shell

# 获取内网IP地址
ipconfig

# 傻瓜版本获取内网IP地址
Get-NetRoute -DestinationPrefix 0.0.0.0/0 |
  Sort-Object RouteMetric |
  Select-Object -First 1 |
  Get-NetIPAddress -AddressFamily IPv4 |
  Select-Object -ExpandProperty IPAddress
  
# 完全关闭防火墙
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False

# 开启防火墙
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True

# 写入脚本内容（下方 Ubuntu-jjdyycm 改成你的容器名称）
$script = @'
Start-Process powershell.exe -ArgumentList "-NoExit", "wsl -d Ubuntu-jjdyycm"
Start-Sleep -Seconds 10
$wslIp = wsl sh -c "ip -4 addr show eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'"
netsh interface portproxy delete v4tov4 listenport=8096 listenaddress=0.0.0.0
netsh interface portproxy add v4tov4 listenport=8096 listenaddress=0.0.0.0 connectaddress=$wslIp connectport=8096
netsh interface portproxy show all
if (-not (Get-NetFirewallRule -DisplayName "WSL 8096" -ErrorAction SilentlyContinue)) {
    New-NetFirewallRule `
      -DisplayName "WSL 8096" `
      -Direction Inbound `
      -Protocol TCP `
      -LocalPort 8096 `
      -Action Allow
}
'@
$path = "C:\Scripts\wsl-portproxy.ps1"
New-Item -ItemType Directory -Path C:\Scripts -Force | Out-Null
Set-Content -Path $path -Value $script -Encoding UTF8

# 设置开机启动
schtasks /create `
  /tn "WSL PortProxy 8096" `
  /tr "powershell.exe -ExecutionPolicy Bypass -File C:\scripts\wsl-portproxy.ps1" `
  /sc onlogon `
  /rl HIGHEST `
  /it `
  /f
  
# 测试脚本
schtasks /run /tn "WSL PortProxy 8096"
```

## 技术栈

- [Jellyfin官网](https://jellyfin.org/docs/)
- [WSL官网](https://learn.microsoft.com/en-us/windows/wsl/)
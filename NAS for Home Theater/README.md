# NAS for Home Theater

English | [中文](README_zh.md)

## Introduction

By repurposing an old computer at home into a NAS-based home theater, you can directly watch and manage videos from other devices in your household, such as smartphones, tablets, and computers.
There is no need to manually download any virtual machines, no need to modify the operating system, and the hardware performance requirements are minimal. You only need to type a few commands during installation to get everything up and running easily.

## 具体文档

For detailed documentation and more extended content, please visit:[Click here](https://www.astercasc.com/article/detail?articleId=AT199028468800214220)

If you have any questions, you can also leave a comment at the bottom of that page.

## 相关资源下载地址

[Click here](https://pan.baidu.com/s/5P4zJnQ1tJkycI24FEcJC4Q)

## Code

### WSL Related Commands

```shell
# Check current WSL version
wsl -v

# Install WSL framework (if wsl -v does not show a version)
wsl --install

# Switch default WSL version to WSL2
wsl --set-default-version 2

# List installed WSL distributions and their status
wsl --list --verbose

# Completely remove a distribution
wsl --unregister Ubuntu-22.04

# Install a specific distribution
wsl --install Ubuntu-22.04

# Enter a specific distribution
wsl -d Ubuntu-22.04

# Import an external distribution from a file
# (modify the install path and tar file path as needed)
wsl --import Ubuntu-jjdyycm C:\Users\astercasc X:\red.panda\new\jjdyycm.tar

```

### Linux Related (Native Linux or after entering a container using WSL -d <distro>)

```shell
# Switch to root user (default password is 123456 for the provided image)
sudo su

# Install Docker
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

# Enable Docker and configure registry mirrors
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

# Install Jellyfin
mkdir -p /home/service/jellyfin/config
mkdir -p /home/service/jellyfin/cache
mkdir -p /home/service/jellyfin/data/videos
mkdir -p /home/service/jellyfin/data/musics
mkdir -p /home/service/jellyfin/data/pictures
mkdir -p /home/service/jellyfin/data/fonts

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

### Windows Related Commands

```shell
# Get local network IP address
ipconfig

# Simplified way to get local network IP address
Get-NetRoute -DestinationPrefix 0.0.0.0/0 |
  Sort-Object RouteMetric |
  Select-Object -First 1 |
  Get-NetIPAddress -AddressFamily IPv4 |
  Select-Object -ExpandProperty IPAddress

# Disable firewall completely
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False

# Enable firewall
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True

# Write script content (replace Ubuntu-jjdyycm with your distribution name)
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

# Set script to run at startup
schtasks /create `
  /tn "WSL PortProxy 8096" `
  /tr "powershell.exe -ExecutionPolicy Bypass -File C:\scripts\wsl-portproxy.ps1" `
  /sc onlogon `
  /rl HIGHEST `
  /it `
  /f

# Test the scheduled task
schtasks /run /tn "WSL PortProxy 8096"

```


## Tech Stack

- [Jellyfin](https://jellyfin.org/docs/)
- [WSL](https://learn.microsoft.com/en-us/windows/wsl/)
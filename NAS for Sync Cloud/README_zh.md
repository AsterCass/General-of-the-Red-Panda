# 使用旧电脑搭建家庭网盘/同步云盘

[English](README.md) | 中文

## 介绍

使用家中的旧电脑改装成NAS作为家庭网盘/同步云盘，可以在其他手机，电脑等等设备中直接观看以及管理文件。不需要手动下载任何虚拟机，也不需要修改操作系统，对电脑性能也几乎没有要求，只是要安装步骤输入一下字符就能轻松实现

## 具体文档

具体文档以及相关拓展更多内容可以访问：[构建完全自定义的全屋智能系统（六）（娱乐篇-使用旧电脑构建NAS用于私有云）](https://www.astercasc.com/article/detail?articleId=AT203530254536227635)

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
    "https://docker.1ms.run",
    "https://docker.xuanyuan.me",
    "https://docker.m.daocloud.io",
    "https://docker.1panel.live",
    "https://docker.hlmirror.com"
  ]
}
EOF
systemctl restart docker


# 安装 nextcloud
mkdir  -p /home/service/nextcloud/data
mkdir  -p /home/service/nextcloud/html
mkdir  -p /home/service/nextcloud/postgresql
cd /home/service/nextcloud
cat <<'EOF' > /home/service/nextcloud/docker-compose.yml
---
services:
  # Note: PostgreSQL is an external service. You can find more information about the configuration here:
  # https://hub.docker.com/_/postgres
  db:
    # Note: Check the recommend version here: https://docs.nextcloud.com/server/latest/admin_manual/installation/system_requirements.html#server
    image: postgres:alpine
    restart: always
    volumes:
      - /home/service/nextcloud/postgresql:/var/lib/postgresql
    environment:
      - POSTGRES_DB=nextcloud
      - POSTGRES_USER=nextcloud
      - POSTGRES_PASSWORD=123456

  # Note: Redis is an external service. You can find more information about the configuration here:
  # https://hub.docker.com/_/redis
  redis:
    image: redis:alpine
    restart: always

  app:
    image: nextcloud:fpm-alpine
    restart: always
    ports:
      - "50010:9000"
    volumes:
      - /home/service/nextcloud/html:/var/www/html
      - /home/service/nextcloud/data:/var/www/html/data
    environment:
      - POSTGRES_HOST=db
      - REDIS_HOST=redis
      - POSTGRES_DB=nextcloud
      - POSTGRES_USER=nextcloud
      - POSTGRES_PASSWORD=123456
    depends_on:
      - db
      - redis

  cron:
    image: nextcloud:fpm-alpine
    restart: always
    volumes:
      - /home/service/nextcloud/html:/var/www/html
      - /home/service/nextcloud/data:/var/www/html/data
    entrypoint: /cron.sh
    depends_on:
      - db
      - redis

EOF
docker compose up -d


# 配置nginx
apt install -y nginx
cat <<'EOF' > /etc/nginx/nginx.conf
worker_processes auto;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include mime.types;
    default_type  application/octet-stream;
    types {
        text/javascript mjs;
    }

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    # Prevent nginx HTTP Server Detection
    server_tokens   off;

    keepalive_timeout  65;

    # Set the `immutable` cache control options only for assets with a cache busting `v` argument
    map $arg_v $asset_immutable {
        "" "";
    default ", immutable";
    }


    upstream php-handler {
                server 127.0.0.1:50010;
    }

    #gzip  on;



    server {
        listen 50011;

        # HSTS settings
        # WARNING: Only add the preload option once you read about
        # the consequences in https://hstspreload.org/. This option
        # will add the domain to a hardcoded list that is shipped
        # in all major browsers and getting removed from this list
        # could take several months.
        #add_header Strict-Transport-Security "max-age=15768000; includeSubDomains; preload;" always;

        # set max upload size and increase upload timeout:
        client_max_body_size 512M;
        client_body_timeout 300s;
        fastcgi_buffers 64 4K;

        # The settings allows you to optimize the HTTP2 bandwidth.
        # See https://blog.cloudflare.com/delivering-http-2-upload-speed-improvements/
        # for tuning hints
        client_body_buffer_size 512k;

        # Enable gzip but do not remove ETag headers
        gzip on;
        gzip_vary on;
        gzip_comp_level 4;
        gzip_min_length 256;
        gzip_proxied expired no-cache no-store private no_last_modified no_etag auth;
        gzip_types application/atom+xml text/javascript application/javascript application/json application/ld+json application/manifest+json application/rss+xml application/vnd.geo+json application/vnd.ms-fontobject application/wasm application/x-font-ttf application/x-web-app-manifest+json application/xhtml+xml application/xml font/opentype image/bmp image/svg+xml image/x-icon text/cache-manifest text/css text/plain text/vcard text/vnd.rim.location.xloc text/vtt text/x-component text/x-cross-domain-policy;

        # Pagespeed is not supported by Nextcloud, so if your server is built
        # with the `ngx_pagespeed` module, uncomment this line to disable it.
        #pagespeed off;

        # HTTP response headers borrowed from Nextcloud `.htaccess`
        add_header Referrer-Policy                      "no-referrer"       always;
        add_header X-Content-Type-Options               "nosniff"           always;
        add_header X-Frame-Options                      "SAMEORIGIN"        always;
        add_header X-Permitted-Cross-Domain-Policies    "none"              always;
        add_header X-Robots-Tag                         "noindex, nofollow" always;

        # Remove X-Powered-By, which is an information leak
        fastcgi_hide_header X-Powered-By;

        # Path to the root of your installation
        root /home/service/nextcloud/html;

        # Specify how to handle directories -- specifying `/index.php$request_uri`
        # here as the fallback means that Nginx always exhibits the desired behaviour
        # when a client requests a path that corresponds to a directory that exists
        # on the server. In particular, if that directory contains an index.php file,
        # that file is correctly served; if it doesn't, then the request is passed to
        # the front-end controller. This consistent behaviour means that we don't need
        # to specify custom rules for certain paths (e.g. images and other assets,
        # `/updater`, `/ocm-provider`, `/ocs-provider`), and thus
        # `try_files $uri $uri/ /index.php$request_uri`
        # always provides the desired behaviour.
        index index.php index.html /index.php$request_uri;

        # Rule borrowed from `.htaccess` to handle Microsoft DAV clients
        location = / {
            if ( $http_user_agent ~ ^DavClnt ) {
                return 302 /remote.php/webdav/$is_args$args;
            }
        }

        location = /robots.txt {
            allow all;
            log_not_found off;
            access_log off;
        }

        # Make a regex exception for `/.well-known` so that clients can still
        # access it despite the existence of the regex rule
        # `location ~ /(\.|autotest|...)` which would otherwise handle requests
        # for `/.well-known`.
        location ^~ /.well-known {
            # The rules in this block are an adaptation of the rules
            # in `.htaccess` that concern `/.well-known`.

            location = /.well-known/carddav { return 301 /remote.php/dav/; }
            location = /.well-known/caldav  { return 301 /remote.php/dav/; }

            location /.well-known/acme-challenge    { try_files $uri $uri/ =404; }
            location /.well-known/pki-validation    { try_files $uri $uri/ =404; }

            # Let Nextcloud's API for `/.well-known` URIs handle all other
            # requests by passing them to the front-end controller.
            return 301 /index.php$request_uri;
        }

        # Rules borrowed from `.htaccess` to hide certain paths from clients
        location ~ ^/(?:build|tests|config|lib|3rdparty|templates|data)(?:$|/)  { return 404; }
        location ~ ^/(?:\.|autotest|occ|issue|indie|db_|console)                { return 404; }

        # Ensure this block, which passes PHP files to the PHP process, is above the blocks
        # which handle static assets (as seen below). If this block is not declared first,
        # then Nginx will encounter an infinite rewriting loop when it prepends `/index.php`
        # to the URI, resulting in a HTTP 500 error response.
        location ~ \.php(?:$|/) {
            # Required for legacy support
            rewrite ^/(?!index|remote|public|cron|core\/ajax\/update|status|ocs\/v[12]|updater\/.+|ocs-provider\/.+|.+\/richdocumentscode(_arm64)?\/proxy) /index.php$request_uri;

            fastcgi_split_path_info ^(.+?\.php)(/.*)$;
            set $path_info $fastcgi_path_info;

            try_files $fastcgi_script_name =404;

            include fastcgi_params;
            #fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            fastcgi_param SCRIPT_FILENAME /var/www/html$fastcgi_script_name;
            fastcgi_param PATH_INFO $path_info;
            fastcgi_param HTTPS off;

            fastcgi_param modHeadersAvailable true;         # Avoid sending the security headers twice
            fastcgi_param front_controller_active true;     # Enable pretty urls
            fastcgi_pass php-handler;

            fastcgi_intercept_errors on;
            fastcgi_request_buffering on;                   # Required as PHP-FPM does not support chunked transfer encoding and requires a valid ContentLength header.

            fastcgi_max_temp_file_size 0;
        }

        # Serve static files
        location ~ \.(?:css|js|mjs|svg|gif|ico|jpg|png|webp|wasm|tflite|map|ogg|flac|mp4|webm)$ {
            try_files $uri /index.php$request_uri;
            add_header Cache-Control "public, max-age=15778463$asset_immutable";
            add_header Referrer-Policy                   "no-referrer"       always;
            add_header X-Content-Type-Options            "nosniff"           always;
            add_header X-Frame-Options                   "SAMEORIGIN"        always;
            add_header X-Permitted-Cross-Domain-Policies "none"              always;
            add_header X-Robots-Tag                      "noindex, nofollow" always;
            access_log off;     # Optional: Don't log access to assets
        }

        location ~ \.(otf|woff2?)$ {
            try_files $uri /index.php$request_uri;
            expires 7d;         # Cache-Control policy borrowed from `.htaccess`
            access_log off;     # Optional: Don't log access to assets
        }

        # Rule borrowed from `.htaccess`
        location /remote {
            return 301 /remote.php$request_uri;
        }

        location / {
            try_files $uri $uri/ /index.php$request_uri;
        }
    }
}
EOF
systemctl enable nginx
systemctl restart nginx
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
netsh interface portproxy delete v4tov4 listenport=50011 listenaddress=0.0.0.0
netsh interface portproxy add v4tov4 listenport=50011 listenaddress=0.0.0.0 connectaddress=$wslIp connectport=50011
netsh interface portproxy show all
if (-not (Get-NetFirewallRule -DisplayName "WSL 50011" -ErrorAction SilentlyContinue)) {
    New-NetFirewallRule `
      -DisplayName "WSL 50011" `
      -Direction Inbound `
      -Protocol TCP `
      -LocalPort 50011 `
      -Action Allow
}
'@
$path = "C:\Scripts\wsl-portproxy.ps1"
New-Item -ItemType Directory -Path C:\Scripts -Force | Out-Null
Set-Content -Path $path -Value $script -Encoding UTF8

# 设置开机启动
schtasks /create `
  /tn "WSL PortProxy 50011" `
  /tr "powershell.exe -ExecutionPolicy Bypass -File C:\scripts\wsl-portproxy.ps1" `
  /sc onlogon `
  /rl HIGHEST `
  /it `
  /f
  
# 测试脚本
schtasks /run /tn "WSL PortProxy 50011"
```


## 技术栈

- [Nextcloud](https://github.com/nextcloud)
- [WSL官网](https://learn.microsoft.com/en-us/windows/wsl/)
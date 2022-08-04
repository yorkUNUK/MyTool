### 一、简介



### 二、使用yum 安装NGINX服务

####   1、安装yum源

```javascript
wget http://nginx.org/packages/centos/7/noarch/RPMS/nginx-release-centos-7-0.el7.ngx.noarch.rpm
yum install  -y nginx-release-centos-7-0.el7.ngx.noarch.rpm
yum clean all && yum makecache
```

####   2、检查yum源中的nginx版本

```javascript
yum list|grep nginx
```

​    ![img](Linux安装PHP运行环境.assets/1568615614705327.png)

​    如上图，最后一列带有“@nginx”的行的软件表示已经安装了。如果有nginx-1.12版本的module等，需要卸载掉

```shell
yum remove nginx-mod-http-geoip
```

​    在这里如果不清理旧版本的NGINX相关软件包，会导致nginx-1.14版本，可以安装并成功但是无法正常启动，会产生报错显示某一个模块版本过低，不匹配已经安装的nginx版本，需要清理的nginx旧模块有以下命令中的rpm包；

```shell
yum remove  nginx-mod-stream nginx-mod-mail nginx-mod-http-xslt-filter  nginx-mod-http-perl nginx-mod-http-image-filter nginx-mod-http-geoip nginx-filesystem nginx-all-modules；
```

####   3、安装高版本NGINX

```shell
yum install -y nginx
```

####   4、检查NGINX是否正常启动

```shell
# 启动nginx
systemctl start nginx
# 开机自启
systemctl  enable nginx
# 重启
systemctl restart nginx
# 停止
systemctl stop nginx
# 检查nginx是否启动
systemctl status nginx
ps  -ef |grep nginx
# 检查nginx的版本以及可使用的模块等
nginx -V
# 修改配置文件后检查配置文件命令
nginx -t

# 使用curl（如果Linux80端口能被电脑访问，可以使用浏览器查看） 命令检查nginx页面，默认nginx端口80，如果不能启动请按照《Linux安装配置nginx》文章中的步骤排查

curl 127.0.0.1
```

如果以上没有问题，NGINX已经安装完成



### 三、使用yum 安装PHP服务

####   1、安装PHP的yum源

```javascript
rpm -Uvh  
##安装webtatic源，此源中包含php5.5-7.2等的版本，不过国外的源，下载可能会比较慢
rpm -Uvh https://mirror.webtatic.com/yum/el7/webtatic-release.rpm

yum clean all&&yum makecache
```

####  2、查看可安装的PHP版本

```javascript
yum list |grep php
```

​    通过上面命令会查看到很多关于PHP的软件，安装php7.2版本（如果要安装其他的版本，通过yum list 查找是否有相应的php版本，比如此源终就有php55w这个版本）

####   3、安装PHP

不知道上上签的demo是不是能在php7上运行，推荐php5

```javascript
yum -y install php56w
yum -y install php56w-cli php56w-common php56w-devel php56w-embedded php56w-fpm php56w-gd php56w-mbstring php56w-mysqlnd php56w-opcache php56w-pdo php56w-xml
```

如果在使用中发现缺少某功能时，比如报错无法使用php链接mysql ，则php72w-mysql没有安装，yum 安装上即可，缺少其他的，参照刚刚解决思路解决即可。

####   4、配置PHP并启动

​    PHP默认的配置文件路径为"/etc/php.ini",php-fpm 配置文件为/etc/php-fpm.conf。

​    如wordpress、zabbix等第一次使用的时候，会报一些错误，根据相应的错误修改即可。比如上传文件大小的修改：upload_max_filesize = 8M，修改此选项即可。

上上签的PHPdemo目前不需要修改这些。



启动PHP命令如下：

```shell
systemctl enable php-fpm
systemctl start php-fpm

# 验证php是否启动成功
systemctl status php-fpm

# 查看是否有php进程
ps -ef |grep  php

# 使用ss命令查看下是否启动9100端口
ss -luntp |grep php

```



#### 5、nginx配置PHP

```ini
#user  nobody;
worker_processes  1;

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;
#pid        logs/nginx.pid;
events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;

    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';

    #access_log  logs/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;
    gzip  on;

# nginx中配置PHP的配置段，配置https，再多谢一个server即可，配置成https格式。
    server {
        listen       80;#端口要修改
        server_name  域名记得修改;#域名要修改
        client_max_body_size 400m; # 上传文件的大小，默认是10m吧，可根据需求修改
        client_body_buffer_size 16k;
        client_header_buffer_size 1k;
        client_body_timeout 60s;
    
        charset koi8-r;
        access_log  logs/host.access.log  main;

        location / {
            root   html;#html等静态资源存放目录，yum安装的话，默认在/usr/share/nginx/html，就是此处写的html
            index  index index.php index.html index.htm;
        }
        
        if (!-e $request_filename) {
            rewrite ^(.*)$ /index.php$1 last;
        }

        # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
        location ~ .*\.php(\/.*)*$ {
            root /app/typecho;    #将/app/typecho替换为您的网站根目录
            fastcgi_pass 127.0.0.1:9000;   #Nginx通过本机的9000端口将PHP请求转发给PHP-FPM进行处理。
            fastcgi_index index.php;
            fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
            include fastcgi_params;   #Nginx调用fastcgi接口处理PHP请求。
        }
            error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
        location ~ /\.ht {
            deny  all;
        }

    }
}
```

6、验证PHP环境

在第五步的目录中/usr/share/nginx/html中编写一个文件，名称内容如下：

```
]# vim index.php

<?php
phpinfo();
?>
```

保存后，访问配置的域名，看下是否出现类似下图的php的信息页面。

![image-20220331175621848](Linux安装PHP运行环境.assets/image-20220331175621848.png)
## 一、简介

nginx的安装目前有两种：1、源码编译安装；2、使用包管理工具安装，比如yum、apt等。区别就是源码编译，可以根据自己需要定制自己想要的模块，使用包管理工具，大多模块能用，少部分是没有的。



## 二、使用包管理工具安装

1、yum安装nginx

```shell
# 下载官方rpm 源包
wget http://nginx.org/packages/centos/7/noarch/RPMS/nginx-release-centos-7-0.el7.ngx.noarch.rpm

yum install  -y nginx-release-centos-7-0.el7.ngx.noarch.rpm

# 如果上面的地址不能请求，可以使用一下命令安装低版本nginx
yum install  -y epel-release


yum clean all && yum makecache

yum list|grep nginx

# 安装，基础安装
yum install -y nginx
# 安装比较多的模块，自行选择。
yum install -y nginx nginx-debuginfo nginx-module-geoip nginx-module-geoip-debuginfo nginx-module-image-filter nginx-module-image-filter-debuginfo nginx-module-njs  nginx-module-njs-debuginfo nginx-module-perl nginx-module-perl-debuginfo nginx-module-xslt nginx-module-xslt-debuginfo


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

```





## 三、源码安装

1、因为目前CentOS还比较流行，此源码部分以CentOS为例进行安装

```shell
# 工作目录
cd /usr/local/src
# 安装 一些必备的包
yum install -y gcc gcc-c++ autoconf automake pcre pcre-devel openssl* zlib* libtool

# 新增用户nginx，后续配置文件可能会用此用户启动
useradd -s /sbin/nologin -M nginx

#下载tengine 源码，也可以下载nginx的，他们一样
cd /usr/local/src
wget http://tengine.taobao.org/download/tengine-2.2.3.tar.gz

tar xzf tengine-2.2.3.tar.gz
cd tengine-2.2.4

# 配置 目录指向/usr/local/nginx，安装后的目录
./configure --prefix=/usr/local/nginx  --user=nginx --group=nginx --with-debug --with-pcre --with-http_ssl_module --with-http_gzip_static_module --with-http_realip_module --with-http_stub_status_module --with-http_concat_module 
--with-pcre=/usr/local/src/pcre-8.41

#编译及安装
make&&make install


```



2、配置nginx的systemctl 文件，nginx 配置文件中有指定工作进程的用户，所以此处不再指定。

```shell
[Unit]
Description=The nginx HTTP and reverse proxy server
After=network-online.target remote-fs.target nss-lookup.target sshd-keygen.service
Wants=network-online.target

[Service]
Type=forking
EnvironmentFile=/etc/sysconfig/sshd
ExecStartPre=/usr/local/nginx/sbin/nginx -t -c /usr/local/nginx/conf/nginx.conf
ExecStart=/usr/local/nginx/sbin/nginx -c /usr/local/nginx/conf/nginx.conf
ExecReload=/usr/local/nginx/sbin/nginx -s reload
ExecStop=/usr/local/nginx/sbin/nginx -s stop
KillSignal=SIGQUIT
TimeoutStopSec=5
KillMode=process
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```



3、NGINX启动管理

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

# 修改配置文件后，检查配置文件是否正确
/usr/local/nginx/sbin/nginx -t
```




## 一、简介

Nginx和openResty配置内容可以一模一样的，openResty可以认为nginx的扩展加强版。

Nginx和openResty主要做负载均衡使用，本次示例呢，是nginx所在服务器直接绑定外网IP的，从公网访问直接访问NGINX，不过这种做法没有考虑安全的因素，单纯的为了演示架构，生产中NGINX前推荐加上安全设备等。

## 二、NGINX架构图

![image-20211124175124131](混合云使用NGINX.assets/image-20211124175124131.png)



此处有两种公网访问方法：1、nginx 服务器直接网卡绑定公网ip，就是访问形式就是https://公网ip：port/ ；2、路由交换设备中做公网端口映射内网NGINXssl服务端口，就是https://公网ip：port/

## 三、NGINX配置

​	这里介绍使用yum或apt方式部署，配置文件目录是：/etc/nginx ， 配置文件路径：/etc/nginx/nginx.conf

```shell
[root@VM-16-10-centos ~]# vim /etc/nginx/nginx.conf
# user  nginx;
worker_processes  auto;

error_log  /var/log/nginx/error.log notice;

events {
    worker_connections  1024;
}


http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"'
                      ' "请求时间:" "$upstream_response_time"'
                      '"$request_time" "$upstream_response_time" "$upstream_addr" "$upstream_status"';
                      #上面这个地方的配置是整个请求消耗多少时间，NGINX和后端交互耗时，后端服务ip，后端服务状态。

    access_log  /var/log/nginx/access.log  main;
    #默认nginx的日志是上面的，有些客户前端有slb ，用了head方式检查nginx的状态导致日志出现大量不需要的日志。替换为以下配置，日志中会过滤掉head请求和options请求，推荐在部署测试完毕之后，修改此配置，前期调试阶段不可去掉，会影响使用调试，map中 0表示不记录，1表示记录。
    #map $request_method $loggable {
    #    HEAD 0;
    #    OPTIONS 0;
    #    default 1;
    #}
    #access_log /var/log/nginx/access.log main if=$loggable;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;
    
	# 下面upstream 是负载均衡，默认是轮训，可以修改加权轮训，如果安装了健康检查模块（nginx_upstream_check_module），可以使用健康检查，百度用法吧。
	upstream bestsignjava {
		#ip_hash; 默认是轮训，这个配置是使用iphash的负载均衡策略。
		server 10.4.7.94:8433 weight=100; # 后端java服务的ip和端口，这里可以添加超时时间
		server 192.168.0.118:8080 weight=100; # weight越大，分配的请求越多。
    }

    server {

        client_max_body_size 20m; # 上传文件的大小，默认是10m吧，可根据需求修改
        client_body_buffer_size 16k;
        client_header_buffer_size 1k;
        client_body_timeout 60s;
        client_header_timeout 10s;

        listen 443 ssl;# 监听端口
        server_name 填写域名;#证书绑定的网站域名
        ssl_certificate /etc/nginx/cert/0.cer;#证书公钥
        ssl_certificate_key /etc/nginx/cert/0.com9920.key;#证书私钥
        ssl_session_timeout 5m;
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!3DES:!aNULL:!MD5:!ADH:!RC4;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_prefer_server_ciphers on;
        
        location / {
            proxy_pass  http://10.4.7.94:8433/; #对应上面upstream 处的名字
            proxy_redirect off;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
            proxy_set_header X-NginX-Proxy true;
            #以下proxy_xx_timeout防止后端超时超过默认60s后upstream做重试处理
            proxy_connect_timeout      150s;
            proxy_send_timeout         150s;
            proxy_read_timeout         150s;

        }
    }
}
```



## 四、openResty配置

这里配置示例是使用yum或apt方式安装的openresty的配置示例。

配置文件目录是：/usr/local/openresty/nginx/conf 

配置文件路径：/usr/local/openresty/nginx/conf /nginx.conf

```shell
[root@VM-16-10-centos ~]# vim /usr/local/openresty/nginx/conf /nginx.conf
# user  nginx;
worker_processes  auto;

error_log  /var/log/nginx/error.log notice;

events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;
    log_format main  escape=json '{ "@timestamp": "$time_local", '
                         '"remote_addr": "$remote_addr", '
                         '"remote_user": "$remote_user", '
                         '"body_bytes_sent": "$body_bytes_sent", '
                         '"upstream_addr": "$upstream_addr",'
                         '"upstream_status": "$upstream_status",'
                         '"upstream_response_time": "$upstream_response_time",'
                         '"request_time": "$request_time", '
                         '"status": "$status", '
                         '"request": "$request", '
                         '"request_method": "$request_method", '
                         '"http_referrer": "$http_referer", '
                         '"body_bytes_sent":"$body_bytes_sent", '
                         '"http_x_forwarded_for": "$http_x_forwarded_for", '
                         '"host":""$host",'
                         '"remote_addr":""$remote_addr",'
                         '"http_user_agent": "$http_user_agent",'
                         '"http_uri": "$uri",'
                         '"req_body":"$resp_body",'
                         '"http_host":"$http_host" }'

	# 这个地方配置access_log 就是http中的server全局的访问日志，可以配置在server中，针对某个server生效。
    # access_log  /usr/local/openresty/nginx/logs/access.log  main;
    #默认nginx的日志是上面的，有些客户前端有slb ，用了head方式检查nginx的状态导致日志出现大量不需要的日志。替换为以下配置，日志中会过滤掉head请求和options请求，推荐在部署测试完毕之后，修改此配置，前期调试阶段不可去掉，会影响使用调试，map中 0表示不记录，1表示记录。
    #map $request_method $loggable {
    #    HEAD 0;
    #    OPTIONS 0;
    #    default 1;
    #}
    #access_log /var/log/nginx/access.log main if=$loggable;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;
    
	# 下面upstream 是负载均衡，默认是轮训，可以修改加权轮训，如果安装了健康检查模块（nginx_upstream_check_module），可以使用健康检查，百度用法吧。
	upstream bestsignjava {
		#ip_hash; 默认是轮训，这个配置是使用iphash的负载均衡策略。
		server 10.4.7.94:8433 weight=100; # 后端java服务的ip和端口，这里可以添加超时时间
		server 192.168.0.118:8080 weight=100; # weight越大，分配的请求越多。
    }

    server {

        listen 443 ssl;# 监听端口
        server_name 填写域名;#证书绑定的网站域名
        ssl_certificate /etc/nginx/cert/0.cer;#证书公钥
        ssl_certificate_key /etc/nginx/cert/0.com9920.key;#证书私钥
        ssl_session_timeout 5m;
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!3DES:!aNULL:!MD5:!ADH:!RC4;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_prefer_server_ciphers on;
        
        # client请求相关配置。
		client_max_body_size 20m; # 上传文件的大小，默认是10m吧，可根据需求修改
        client_body_buffer_size 16k;
        client_header_buffer_size 1k;
        client_body_timeout 60s;
        client_header_timeout 10s;
        
        location / {
            # server中的access_log，lua记录请求返回值
            set $resp_body "";
            access_log  /usr/local/openresty/nginx/logs/test.log  main;# 定义日志的路径和日志级别，其中路径要有访问权限。
            # lua代码

                lua_need_request_body on;
            body_filter_by_lua '
                # 最大截取500字节返回体
                local resp_body = string.sub(ngx.arg[1], 1, 500)
                ngx.ctx.buffered = (ngx.ctx.buffered or"") .. resp_body
                # 判断response是否不为空
                if ngx.arg[2] then
                ngx.var.resp_body = ngx.ctx.buffered
                end
            ';
            
            proxy_pass  http://bestsignjava/; #对应上面upstream 处的名字
            proxy_redirect off;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
            proxy_set_header X-NginX-Proxy true;
            #以下proxy_xx_timeout防止后端超时超过默认60s后upstream做重试处理
            proxy_connect_timeout      150s;
            proxy_send_timeout         150s;
            proxy_read_timeout         150s;

        }
    }
}
```



## 五、安全配置

###### 1、Redhat系selinux

红帽系系统中比如rehl和centos，系统自带selinux，默认是开启的，如果碰到这种情况需要使用一下命令放开端口访问

```shell
#比如java启动端口是8075，需要在selinux中开通放行的动作：
semanage port -a -t http_port_t  -p tcp 443

## 如果不使用此防火墙
setenforce 0
# 上面临时关闭可能不生效，需要修改配置文件/etc/sysconfig/selinux ，将SELINUX配置项修改为disabled，如下
SELINUX=disabled
```

 linux系统中有的自带firewalld，有的iptables，有的ufw，碰到这种需要执行相关的命令将服务端口放开

###### 2、firewalld防火墙

```shell
#比如放开9930端口，使用一下命令，其他端口类比下；
firewall-cmd --zone=public --add-port=443/tcp --permanent
#重新加载使配置生效；
firewall-cmd --reload

##如果不使用 此防火墙，关闭命令如下：
systemctl stop firewalld
systemctl disable firewalld
```

###### 3、iptables防火墙

​	iptables防火墙可以使用命令添加规则，也可以直接编辑文件（/etc/sysconfig/iptables）。

```shell
/sbin/iptables -I INPUT -p tcp --dport 443 -j ACCEPT #开启8000端口

/etc/rc.d/init.d/iptables save #保存配置

/etc/rc.d/init.d/iptables restart #重启服务

/etc/init.d/iptables status # 查看端口是否已经开放 

##如果不使用 此防火墙，关闭命令如下：
systemctl stop iptables
systemctl disable iptables

```

###### 3.10.4、ufw防火墙

```shell
# 设置端口访问权限
ufw allow proto tcp from 192.168.0.0/24 to any port 443  允许指定的IP段访问特定端口

# 删除端口访问权限
ufw delete allow 443 

##如果不使用 此防火墙，关闭命令如下：

systemctl stop ufw
systemctl disable ufw
```





## 五、部署问题总结

1、访问nginx的https端口出现502报错

问题原因：nginx不能连接到配置在proxy_pass的服务，所以会出现这个报错；

解决方法：1、检查防火墙；2、检查proxy_pass服务是否启动并能被访问到；


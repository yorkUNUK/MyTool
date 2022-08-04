## 一、简介

只要是介绍mysql安装的方式：1、源码包编译安装；2、二进制包安装；3、使用相应linux系统平台的包管理器进行安装，比如rpm包，这部分有两种方法，第一种使用源，然后使用包管理器yum 或者apt 进行安装，第二种，下载相应的合集包，上传到服务器进行安装。

上上签使用的是系统平台的包管理器的方式进行安装。

因为目前大多平台是红帽系，所以在此文档中主要使用RHEL的yum包管理器进行安装。



## 二、Mysql安装

#### 1、使用官方Mysql的rpm源进行安装



```shell
cd /root/
# 安装一个yum扩展
yum install yum-utils
# 下载源rpm
wget -i -c  http://dev.mysql.com/get/mysql57-community-release-el7-10.noarch.rpm
# 安装源rpm包
yum install -y  mysql57-community-release-el7-10.noarch.rpm
yum clean all &&yum makecache 

# 查看可安装的mysql版本
yum repolist all|grep mysql
#禁用mysql5.7
yum-config-manager --disable mysql57-community
#启用mysql5.7，笔者选了5.7
yum-config-manager --enable mysql57-community

# 安装mysql 
yum install -y mysql-community-common mysql-community-libs mysql-community-libs-compat mysql-community-client mysql-community-server

```



#### 2、使用rpm合集离线安装

```shell
cd /usr/local/src/

# 下载msyql的rpm 离线包
wget  https://cdn.mysql.com/archives/mysql-5.7/mysql-5.7.35-1.el7.x86_64.rpm-bundle.tar

# 解压
tar xf mysql-5.7.35-1.el7.x86_64.rpm-bundle.tar

# 安装
 yum install -y ./mysql*rpm
 
```



#### 3、Mysql启动

通过以上两步安装的mysql ，启动命令都是一样的，如下

```shell
# 配置开机启动
systemctl enable  mysqld.service
# 启动mysql
systemctl start  mysqld.service
# 查看启动的状态，执行之后如下图表示启动成功
systemctl status mysqld.service
```

![img](Linux安装配置Mysql.assets/1079354-20170726202441687-1168874203.png)





三、Mysql初始化

Mysql安装之后需要一些初始化的操作，比如修改密码，比如配置一些可以远程连接的账户。

```shell
#  查找初始密码
grep "password" /var/log/mysqld.log

# 命令行连接mysql
mysql -uroot -p
# 输入密码之后，回车即可进入mysql 的命令行

# 修改mysql的默认密码，这里以新密码为例：BestSign_2019，mysql5.7 之后不允许弱密码，注意密码不要那么简单。
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'BestSign_2019';
 
# 如果mysql 要被其他主机的程序访问，需要执行一下命令
    mysql> grant all privileges on *.* to 'bestsign'@'%' identified by 'BestSign_2019' with grant option;
mysql> flush privileges;
# 解释一下上面命令 *.* 表示某个库的某个表 javauser 表示特定的用户，远程主机的java程序使用的user，%表示所有的主机类似0.0.0.0，这个地方可以根据需要定制，具体百度一下吧，应该是有192.168.1.0 这种 ，密码就是密码啦。

```



mysql8.0

高版本MySQL规则变了，需要创建用户然后再赋权。另尽量用普通用户吧，root好像不能被程序直接用了。

```

create user 'bestsign'@'%' identified by 'BestSign_2019';
grant all privileges on *.* to 'bestsign'@'%' with grant option;

flush privileges;


```





1、mysql 安装包下载

https://cdn.mysql.com/archives/mysql-5.7/mysql-5.7.35-1.el7.x86_64.rpm-bundle.tar
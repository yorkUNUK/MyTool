一、简述

目前常用的Linux服务器系统有Debian和Redhat系两种发行版本，其中Debian系的分支有Debian、Ubuntu等，Redhat系分支有RHEL(Redhat Enterprise Linux，也就是所谓的Redhat Advance Server，收费版本)、Fedora Core(由原来的Redhat桌面版本发展而来，免费版本)、CentOS。

此文将此两种发新版本安装字体的方法介绍下，希望会有借鉴意义。

同时为了应对可能有的容器镜像，最后也会简述下容器镜像安装字体的的方法。

特别说明：字体文件可能设计到收费，请自行百度确认哪些字体是收费那些不收费。

二、Debian系列

Debian系新版本（老版本碰到了应该是将命令apt 替换为apt-get）的安装字体方式如下：

```shell
#安装常用的操作字体命令
sudo apt install xfonts-utils ## 提供mkfontscale 和 mkfontdir 等命令
sudo apt-get install fontconfig ## 提供fc-cache 和  fc-list 等命令；
#创建字体目录
sudo mkdir -pv /usr/share/fonts/chinese/truetype

#将字体文件放到上一步创建的目录中；
~]# ls /usr/share/fonts/chinese/truetype
simsun.ttf
#执行以下命令-为了避免某些程序找不到字体。早期的程序是通过这样的东西索引字体的。
mkfontscale
mkfontdir
#重新生成字体缓存
fc-cache -fv 
#验证字体是否安装
fc-list :lang=zh-cn
```

三、Redhat系列

```shell
yum groupinstall Fonts -y #安装字体组件
yum install fontconfig xorg-x11-font-utils -y #安装fc-cache和fc-list工具
tar -xzvf fonts.tar.gz -C /usr/share/fonts #解压字体包到字体目录
mkfontscale //这样做是为了避免某些程序找不到字体。早期的程序是通过这样的东西索引字体的。
mkfontdir //这样做是为了避免某些程序找不到字体。早期的程序是通过这样的东西索引字体的。
fc-cache -fv            #重新生成字体缓存
fc-list :lang=zh-cn   #验证字体是否安装
```



四、容器中安装字体

因为容器中也是运行的微型的Debian或Redhat系系统，所以安装字体和正常安装字体有很大相似的地方。

以下代码仅为示例，具体需要根据客户情况进行修改

```yaml
# VERSION v1
 
FROM ubuntu
 
#MAINTAINER 维护者信息
LABEL maintainer="bestsign"
 

#修改apt 源，请自行选择合适的，souorces.list 和Dockerfile在同级目录；
COPY sources.list /etc/apt/sources.list
 
 
#将字体文件放入容器镜像中，会自动创建容器镜像中的目录
COPY fonts/ /usr/share/fonts/chinese/truetype
 
#安装 命令需要的包
RUN apt update && apt install -y   xfonts-utils  fontconfig  && mkfontscale && mkfontdir && fc-cache -fv && fc-list :lang=zh-cn
```


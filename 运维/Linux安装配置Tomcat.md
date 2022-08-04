### 一、简述

​	Linux有上百种不同的发行版，如基于社区开发的[debian](https://baike.baidu.com/item/debian/748667)、[archlinux](https://baike.baidu.com/item/archlinux/10857530)，和基于商业开发的[Red Hat Enterprise Linux](https://baike.baidu.com/item/Red Hat Enterprise Linux/10770503)、[SUSE](https://baike.baidu.com/item/SUSE/60409)、[Oracle Linux](https://baike.baidu.com/item/Oracle Linux/6876458)等。目前常用的发行版有以下几种：Debian、Ubuntu、RHEL、Centos、SUSE、Slackware等

​	在安装Tomcat时，各个发型版操作的步骤都是相同的，大致步骤是上传sunjdk二进制包、解压到指定目录、修改配置文件、验证是否安装成功，本文也将按照以上四个步骤进行。

指定相关用户、文件与路径：

​	username：bestsign（创建用户请查看《Linux基本操作命令》手册）

​	Tomcat二进制包存放路径：/usr/local/src/

​	Tomcat二进制包安装路径：/home/bestsign/bestsign-tomcat或/data/bestsign-tomcat

### 二、安装与配置

1. #### 上传二进制包

   可以使用《链接Linux服务器及文件上传下载》手册中的方式将Tomcat的二进制包上传到Linux服务器的/usr/lcoal/src/目录中

   ```shell
   [bestsign@bj-18-12 src]$ ls
   apache-tomcat-8.5.55.tar.gz
   ```

   

2. #### 解压二进制包至指定目录

   ```shell 
   [bestsign@bj-18-12 src]$ tar xzf apache-tomcat-8.5.55.tar.gz  -C /home/bestsign/
   [bestsign@bj-18-12 src]$ mv /home/bestsign/apache-tomcat-8.5.55  /home/bestsign/bestsign-tomcat
   ```

   

3. #### 修改配置文件

   Tomcat配置文件在/home/bestsign/bestsign-tomcat/conf目录下，如修改端口、配置ssl证书等都需要修改server.xml

   ```shell
   [bestsign@bj-18-12 ~]$ cd /home/bestsign/bestsign-tomcat/conf
   # 修改Tomcat的服务端口，只需要将以下内容修改即可
   [bestsign@bj-18-12 conf]$ vim server.xml
       <Connector port="8888" protocol="HTTP/1.1"
                  connectionTimeout="20000"
                  redirectPort="8443" />
   #ssl 实现方式一、 配置ssl证书，需要将以下内容注释去掉，然后修改端口以及证书相关内容
   [bestsign@bj-18-12 conf]$ vim server.xml
       <!--
       <Connector port="8443" protocol="org.apache.coyote.http11.Http11NioProtocol"
                  maxThreads="150" SSLEnabled="true">
           <SSLHostConfig>
               <Certificate certificateKeystoreFile="conf/localhost-rsa.jks"
                            type="RSA" />
           </SSLHostConfig>
       </Connector>
       -->
       
   # ssl 实现方式二、配置ssl证书，也可以在配置文件中增加以下内容
   <Connector port="8443" protocol="HTTP/1.1" SSLEnabled="true"  
                 maxThreads="150" scheme="https" secure="true"  
                 clientAuth="false" sslProtocol="TLS"   
          keystoreFile="g:\tomcat.keystore"  
          keystorePass="123456" />  
   ```

   

4. #### 验证是否安装成功

   ```shell
   [bestsign@bj-18-12 ~]$ cd /home/bestsign/bestsign-tomcat/bin
   
   # 因为以上操作都是在bestsign用户下操作的，所以启动后，tomcat的启动用户是bestsign
   [bestsign@bj-18-12 ~]$ ./start.sh
   
   # 访问Tomcat的端口，如果出现一下内容，就表示已经安装成功
   [bestsign@bj-18-12 bin]$ curl localhost:8080 -I
   HTTP/1.1 200
   Content-Type: text/html;charset=UTF-8
   Transfer-Encoding: chunked
   Date: Wed, 11 Aug 2021 09:43:23 GMT
   ```

   

   


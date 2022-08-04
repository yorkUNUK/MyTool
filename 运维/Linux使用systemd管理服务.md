### 一、简介

在linux系统中rhel/centos 7 之前的版本中都是使用initd 作为linux第一个进行启动linux系统，在rhel/centos 7之后的版本中采用了systemd

systemd 中字母d 是daemon的缩写，systemd名称的含义就是守护整个系统。

以往init启动的方式有两个缺点：

1. 串行启动，启动时间长；
2. 启动脚本复杂，init是调用启动脚本启动，不做其他事情，这样编写的脚本就千人千面了；

systemd 作为init的取代工具，取代了initd成为系统的第一个进程。

### 二、systemd的使用

systemd是一个系统管理守护进程、工具和库的集合，用于取代System V初始进程。Systemd的功能是用于集中管理和配置类UNIX系统。

Systemctl是一个systemd工具，主要负责控制systemd系统和服务管理器。



1. 检查systemd 是否运行

   ```shell
   ~]# ps -eaf |grep systemd
   root         1     0  0 6月28 ?       00:00:11 /usr/lib/systemd/systemd --switched-root --system --deserialize 22
   root       510     1  0 6月28 ?       00:00:01 /usr/lib/systemd/systemd-journald
   root       542     1  0 6月28 ?       00:00:00 /usr/lib/systemd/systemd-udevd
   dbus       894     1  0 6月28 ?       00:00:03 /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation
   root       959     1  0 6月28 ?       00:00:01 /usr/lib/systemd/systemd-logind
   root     11965  9828  0 15:48 pts/0    00:00:00 grep --color=auto systemd
   ```

   

2. 分析systemd启动进程

   ```shell
   ~]# systemd-analyze
   Startup finished in 28.644s (firmware) + 5.633s (loader) + 655ms (kernel) + 3.634s (initrd) + 18.496s (userspace) = 57.065s
   ```

   

3. 分析启动时各个进程花费的时间

   ```shell
   ~]# systemd-analyze  blame
             7.306s network.service
             4.237s lvm2-monitor.service
             3.150s vdo.service
             3.139s dev-mapper-centos\x2droot.device
             2.974s systemd-udev-settle.service
             2.302s kdump.service
             2.118s supervisord.service
             1.829s lvm2-pvscan@8:3.service
   ```

   

4. 分析启动时的关键链

   ```shell
   ~]# systemd-analyze critical-chain
   The time after the unit is active or started is printed after the "@" character.
   The time the unit takes to start is printed after the "+" character.
   
   multi-user.target @18.491s
   └─postfix.service @16.187s +1.444s
     └─network.target @16.186s
       └─network.service @8.878s +7.306s
         └─basic.target @7.659s
           └─sockets.target @7.658s
             └─rpcbind.socket @7.658s
               └─sysinit.target @7.657s
                 └─systemd-update-utmp.service @7.642s +14ms
                   └─auditd.service @7.310s +329ms
                     └─systemd-tmpfiles-setup.service @7.259s +48ms
                       └─rhel-import-state.service @7.113s +145ms
                         └─local-fs.target @7.090s
                           └─home.mount @6.967s +121ms
                             └─dev-mapper-centos\x2dhome.device @6.965s
   ```

   

5. 列出所有可用单元

   ```shell
   ~]# systemctl list-units
   UNIT                                                                                     LOAD   ACTIVE SUB       DESCRIPTION
   proc-sys-fs-binfmt_misc.automount                                                        loaded active waiting   Arbitrary Executable File Formats File System Automount Point
   sys-devices-pci0000:00-0000:00:01.0-0000:01:00.1-sound-card1.device                      loaded active plugged   High Definition Audio Controller
   sys-devices-pci0000:00-0000:00:17.0-ata4-host3-target3:0:0-3:0:0:0-block-sda-sda1.device loaded active plugged   ST1000DM010-2EP102 EFI\x20System\x20Partition
   sys-devices-pci0000:00-0000:00:17.0-ata4-host3-target3:0:0-3:0:0:0-block-sda-sda2.device loaded active plugged   ST1000DM010-2EP102 2
   rpcbind.service                                                                          loaded active running   RPC bind service
   rsyslog.service                                                                          loaded active running   System Logging Service
   smartd.service                                                                           loaded active running   Self Monitoring and Reporting Technology (SMART) Daemon
   sshd.service                                                                             loaded active running   OpenSSH server daemon
   ```

   

6. 检查某个单元是否启用

   ```shell
   systemctl is-enabled crond.service
   systemctl is-enabled sshd.service
   ```

   

7. 检查某个单元或服务是否运行

   ```shell
   systemctl status sshd.service
   ```

   

8. 列出所有服务

   ```shell
    ~]# systemctl list-unit-files
   UNIT FILE                                     STATE
   proc-sys-fs-binfmt_misc.automount             static
   dev-hugepages.mount                           static
   dev-mqueue.mount                              static
   proc-sys-fs-binfmt_misc.mount                 static
   sys-fs-fuse-connections.mount                 static
   sys-kernel-config.mount                       static
   sys-kernel-debug.mount                        static
   tmp.mount                                     disabled
   brandbot.path                                 disabled
   systemd-ask-password-console.path             static
   systemd-ask-password-plymouth.path            static
   systemd-ask-password-wall.path                static
   session-1339.scope                            static
   abrt-ccpp.service                             enabled
   abrt-oops.service                             enabled
   abrt-pstoreoops.service                       disabled
   ```

   

9. 使用systemctl启动、重启、停止、重载配置、检查服务状态和强制停止服务

   ```shell
    ~]# systemctl start sshd.service(sshd.service 可以简写为sshd,以下简写sshd) ~]# systemctl restart sshd ~]# systemctl stop sshd ~]# systemctl reload sshd ~]# systemctl status sshd#检查服务是否是启动状态，其实status就可以看到，但是还得找回显内容，一下命令可以直接显示 ~]# systemctl is-active sshdactive# 强制停止服务 ~]# systemctl kill sshd
   ```

   

10. 使用systemctl 检查服务是否启动

    ```shell
     ~]# systemctl is-enabled sshd ~]# systemctl disable sshd ~]# systemctl enable sshd
    ```

    

### 三、自定义service服务

自定义service配置文件的时候，可以将自定义文件存放在两个目录中：/lib/systemd/system/和/etc/systemd/system/，使用起来效果相当。

以下示例中，工作目录是/data/xxxxxx/

###### 1、无变量service文件写法

```shell
# 将变量放到service文件里面
 ~]# vim xxxxxx.service
[Unit]
Description=xxxxx.service
Documentation="http://documentation"
After=syslog.target
After=network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
User=java
WorkingDirectory=/data/xxxxxx/
ExecStart=/bin/bash -c 'java -jar xxxxxx.jar  2>&1 &'
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s QUIT $MAINPID

[Install]
WantedBy=multi-user.target
```

###### 2、有变量service文件写法

变量在service文件里面的写法。

```shell
# 将变量放到service文件里面

[Unit]
Description=xxxxxx
Documentation="Documentation"
After=syslog.target
After=network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
User=bestsign
WorkingDirectory=/data/xxxxxx/
Environment="LOG_PATH=/data/xxxxxx/logs"
Environment="JAVA_HOME=/usr/local/java"
Environment="JAVA_OPTS=-Xms4G -Xmx4G -Djava.security.egd=file:/dev/./urandom -XX:-UseBiasedLocking -XX:+UseConcMarkSweepGC -XX:AutoBoxCacheMax=20000 -XX:+PrintCommandLineFlags -XX:+PrintGCDetails -XX:+PrintGCDateStamps -Xloggc:./logs/gc.log"
ExecStart=/bin/bash -c '${JAVA_HOME}/bin/java ${JAVA_OPTS} -jar /data/xxxxxx/xxxxxx.jar >${LOG_PATH}/stdout.log  2>&1 &'
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s QUIT $MAINPID

[Install]
WantedBy=multi-user.target
```

变量写到单独的配置文件中，在service文件中引入的写法。

```shell
# 将变量放在文件里面，service文件引用变量文件
 ~]# vim /data/xxxxxx/xxxxxx.conf

JAVA_HOME="/usr/local/java"
WORK_PATH="/data/xxxxxx"
JAVA_OPTS="-Xms4G -Xmx4G -Djava.security.egd=file:/dev/./urandom -XX:-UseBiasedLocking -XX:+UseConcMarkSweepGC -XX:AutoBoxCacheMax=20000 -XX:+PrintCommandLineFlags -XX:+PrintGCDetails -XX:+PrintGCDateStamps -Xloggc:${WORK_PATH}/logs/gc.log"


 ~]# vim /etc/systemd/system/bestsign-hybrid.service

[Unit]
Description=xxxxxx
Documentation="http://Documentation"
After=syslog.target
After=network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
User=bestsign
WorkingDirectory=/data/xxxxxx/
EnvironmentFile=/data/xxxxxx/xxxxxx.conf
ExecStart=/bin/bash -c '${JAVA_HOME}/bin/java ${JAVA_OPTS} -jar /data/xxxxxx/xxxxxx.jar >${WORK_PATH}/logs/stdout.log  2>&1 &'
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s QUIT $MAINPID

[Install]
WantedBy=multi-user.target
```






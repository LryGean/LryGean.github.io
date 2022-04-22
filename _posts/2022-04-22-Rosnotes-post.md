---
layout: post
title: Ros-notes
category: tutorial
thumbnail: /style/image/头像.ico
icon: book
---

* content
{:toc}

<style>
    * {
        background: orange;
    }
</style>

###ROS操作

1. IP查询
(1) <span style='background: yellow'>ROS IP</span>：`ifconfig`

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%871.png "ROS IP")

(2) <span style='background: yellow'>查询主机 IP</span>：`ipconfig`

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%872.png "主机 IP")

2.虚拟机终端操作
(1)`sudo gedit /etc/hosts`打开<span style='background: yellow'>hosts</span>文件修改<span style='background: yellow'>ROS</span>的ip

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%873.png "hosts")

(2)ssh clbrobot@robot连接ROS

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%874.png "ssh")


<style>
    .ann>span {
        margin: 10px;
        background: yellow;
        color: red;
    }
</style>
<div class='ann'>
    <span>注释：Ctrl+Shift+T可在同一个终端窗口下打开多个终端界面</span>
    <br>
    <span>clear：清除界面内容</span>
    <br>
    <span>sudo halt:机器人关机命令</span>
    <br>
    <span>Sudo reboot:机器人重启指令</span>
</div>

(3)<span style='background: yellow'>ROS</span>和<span style='background: yellow'>虚拟机</span>终端都要执行命令`sudo gedit ~/.bashrc`，打开<span style='background: yellow'>bashrc</span>文件修改主节点
![图片已失效](../style/img/img/%E5%9B%BE%E7%89%875.png "修改主节点")

<span style='color: red'>注意</span>：将

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%876.png "细节")
改成<span style='background: #F0F0F0'>
export ROS_IP=`hostname -I | awk '{print $1}'`
export ROS_HOSTNAME=`hostname -I | awk '{print $1}'`
</span>

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%877.png "修改IP")

<span style='background: yellow; color: red'>注意：修改完以后一点要在ROS和虚拟机终端 <em style='color: black;'>source ~/.bashrc</em> 进行更新文件，并重启</span>

(4)打开底盘节点<span style='color: red'>（先）</span>和RVIZ建模界面<span style='color: red'>（后）</span>
命令：
`roslaunch clbrobot bringup.launch`
`rosrun rviz rviz`

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%878.png "rviz建模")

(5)打开`odometry.rviz`文件，并且<span style='background: yellow; color: red'>Ctrl+Shift+t</span>在同一终端下再打开一个终端界面进行ssh连接，输入命令：`rosrun teleop_twist_keyboard teleop_twist_keyboard.py`执行Python程序可实现主机控制机器人的移动 <span style='color: red'>（注：也可以不使用ssh连接，直接在机器人上输入打开底盘节点和此命令，利用无线键盘完成机器人的移动）</span>

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%879.png "keyboard")

此时当使用键盘控制小车移动时，`rviz`界面机会显示小车的动态

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8710.png "keyboard")

(6)ROS机器人`IMU`校正
①通过一系列命令
![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8711.png "机器人动态")

查看需要校准的参数

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8712.png "需要校准的参数")

②输入命令：`rosrun imu_calib do_calib`自动进行`x+`，`x-`，`y+`，`y-`，`z+`，`z-`校准计算

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8713.png "校准")

③查看校准后的`IMU`精度数值
输入命令：`rostopic echo /imu/data`

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8714.png "IMU精度数值")

(7)ROS机器人`角速度`校正
①在同一个窗口下打开两个终端界面并同时使用`ssh`连接，一个界面打开底盘节点，一个输入命令：`rosrun rikirobot_nav calibrate_angular.py` 启动角速度测试

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8715.png "启动角速度测试")

再打开一个虚拟机终端输入：`rosrun rqt_reconfigure rqt_reconfigure`打开`rqt`控制台

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8716.png "rqt控制台")

角速度校正界面：

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8717.png "角速度校正")

②其中`start_test`是对小车进行参数为`1`的`360°`的校正，观察小车是否旋转`360°`，通过偏差计算出比例因子：`n=(多旋转的角度+360)/360或(少旋转的角度+360)/360`，将结果修改至`oddm_angular_scale_correction`，实验所测小车经过旋转多旋转`5°`，因此比例因子为`374.4/360≈1.04`
③关闭底盘节点和rqt控制台，通过`vi`打开`bringup.launch`文件

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8718.png "bringup.launch")

找到角速度参数并修改<span style='background: yellow;color: red'>(注：i是进入编辑模式，Esc退出编辑模式，:q!或Shift+z+z退出文件)</span>：

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8719.png "修改角速度参数")

(8)ROS机器人`线速度`校正
①在同一个窗口下打开两个终端界面并同时使用`ssh`连接，一个界面打开底盘节点，一个输入命令：`rosrun rikirobot_nav calibrate_linear.py`启动线速度测试

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8720.png "启动线速度参数")

②再打开一个虚拟机终端输入：`rosrun rqt_reconfigure rqt_reconfigure`打开rqt控制台

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8721.png "rqt控制台")

测试小车在参数为`1`米时走过的路程大致为`1.04`米，因此类似的线速度测试的比例因子为`1.042/1.0=1.042`
然后输入命令通过`vim`打开`launch`文件

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8722.png "launch")

并找到校准线速度的位置进行修改比例因子

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8723.png "修改比例因子")

(9)建图
①打开两个终端界面分别`ssh`到`ROS`上
②打开激光雷达：`roslaunch clbrobot lidar_slam.launch`

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8724.png "打开激光雷达")

<span style='background: yellow; color: red'>注意：打开雷达前一定要对imu，角速度，线速度，进行一遍校正，否则建图会出现无边界等建图不成功的情况</span>
③打开`rviz`建模软件：`rosrun rviz rviz`
添加`slam.rviz`文件
<style>
        .slam {
            margin: 0;
            padding: 0;
            font-size: 0;
            width: 750px;
            height: 280px;
            text-align: center;
        }
        .slam img {
            width: 300px;
            height: 280px;
        }
        .slam .one {
            float: left;
        }
        .slam span {
            width: 100px;
            font-size: 20px;
            color: red;
            height: 280px;
            line-height: 280px;
        }
        .slam .two {
            float: right;
        }
</style>
<div class="slam" title='添加slam.rviz'>
    <img class="one" src='./img/图片25.png' alt='图片加载不出来'>
    <span>————></span>
    <img class="two" src='./img/图片26.png' alt='图片加载不出来'>
</div>

通过放大后的底盘坐标：

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8727.png "底盘坐标")

④`Ctrl+AIt+t`打开另一个终端界面输入键盘控制命令：`rosrun teleop_twist_keyboard teleop_twist_keyboard.py`
<span style='background: yellow; color: red'> 
注意：q/z：速度调节
      w/x：线速度调节
      e/c：角速度调节
</span>

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8728.png "keyboard")

`X：线速度调教至0.3左右`

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8729.png "线速度")

`C：角速度调节至0.5左右`

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8730.png "角速度")

⑤建模：
通过键盘控制机器人行走进行建模

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8731.png "建模")

最好让机器人将边缘走过是地图上呈现黑色线条的边框，使其规划路径时能避开障碍
⑥保存地图

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8732.png "保存地图")

或`rosrun map_server map_saver -f`
检查文件是否更新

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8733.png "检查更新")

(10)ROS自主导航与避障功能
①开启导航功能：`roslaunch clbrobot navigate.launch`

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8734.png "开启导航")

②启动完成标志

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8735.png "启动完成标志")

③打开rviz窗口
添加文件：`navigate.rviz`

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8736.png "添加navigate.rviz")

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8737.png "图片")


④校正ROS的位置和方向
通过![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8738.png "工具")工具来校正

<hr>



### 树莓派摄像头开启

###### 打开树莓派的命令行窗口：
输入以下指令进入树莓派的系统配置：
`sudo raspi-config`

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8739.png "系统配置")

`ls -al /dev/ | grep video`
如果配置成功，我们会有以下界面：

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8740.png "拍照")

找到`video0`，也就是我们的树莓派摄像头设备。
<span style='background: yellow; color: red'> 
【注】：可能提示这样的问题（如果在以上工作都完成的情况下，摄像头还是不能正常的使用或者驱动，请先检查硬件的连接的问题，可能是排线没有很好的插稳，或者是摄像头本身的问题。）
</span>

###### 拍照:

输入以下指令，可以使用树莓派摄像头的拍照功能
`raspistill -o imageDemo.jpg`

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8741.png "拍照")

然后在树莓派的应用界面打开文件夹，找到`imageDemo.jpg`

这里可以讲解一下`raspistill`命令的相关参数和实验的具体效果：
`-v：调试信息查看`
`-w：图像宽度`
`-h：图像高度`
`-rot：图像旋转角度，只支持 0、90、180、270 度（这里说明一下，测试发现其他角度的输入都会被转换到这四个角度之上）`
`-o：图像输出地址，例如image.jpg，如果文件名为“-”，将输出发送至标准输出设备`
`-t：获取图像前等待时间，默认为5000，即5秒`
`-tl：多久执行一次图像抓取`

###### 摄像+远程监控
首先下载和安装`motion`：
`motion` 是一款开源的支持多种摄像头的监控软件。本文也通过它来把树莓派变成监控摄像头~

不过官方的定义中，`motion` 是一款“运动检测”软件，因为它支持当图像中一部分发生变化时拍照，或者触发脚本。不过这些功能不在这次文章讨论的范围内。

打开树莓派的命令行窗口，输入以下指令：
`sudo apt-get install motion`

然后等待下载motion完成。
下载完成之后，就可以进行下一步配置`motion`。
输入以下指令，配置`motion daemon` 守护进程
`sudo nano /etc/default/motion`
将`start_motion_daemon=no`改为`start_motion_daemon=yes`，让他可以一直运行，修改完后按`^X`退出。
<span style='background: yellow; color: red'> （注意：^X表示Ctrl+X）</span>

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8742.png "yes")


输入以下指令，修改motion的配置文件：
`sudo vim /etc/motion/motion.conf`

<span style='background: yellow; color: red'>【注意】如果你是第一次使用树莓派的话，可能会提示vim指令错误，这是因为没有安装vim的缘故</span>，在树莓派的命令行输入
`sudo apt-get install motion安装vim之后，在执行上面的步骤。`

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8743.png "图片")

扣下`E`，进入编辑模式，然后将`11行`的`daemon off`改为`daemon on`，让`motion`后台运行，

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8744.png "daemon on")

到了`445行`，你可
以找到端口号`8081`，我们可以通过这个端口来读取视频数据，这里`无需修改！`

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8745.png "8081")

然后到第`461`行将`stream_localhost on`改成`off`，即关闭 `localhost` 的限制，允许通过非 `localhost` 来查看视频，如下：

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8746.png "off")

设定图片的分辨率，在第`79`行进行修改

![图片已失效](../style/img/img/%E5%9B%BE%E7%89%8747.png "分辨率")

改成`1280 x 720`的像素`（720P）`
`rotate` 旋转画面，如果需要`90°`、`180°`旋转，可以在这里配置

`framerate` 捕获的帧率，如修改为 `30`

`stream_maxrate` 修改流的帧率，如果需要实时查看的话，建议修改这个的值，因为这个默认值是 `1`，会导致画面非常卡顿，如修改为 `30`。

保存退出。

配置好了`motion`的基本设置之后，我们可以开始启动`motion`：
输入以下指令，其中第一条命令是启动服务，第二条命令是开启`motion`：
`sudo service motion start` 
`sudo motion`

然后我们就可以通过浏览器或者手机查看树莓派摄像头的内容了
打开网址`http://[你的树莓派IP地址]:8081`
such as:`http://192.168.2.156:8081`

<span style='background: yellow; color: red'>【注意】
可以修改画面分辨率来提高画质，但是画面分辨率越高越消耗资源！
如果画面非常卡，可以调整 stream_maxrate 和 framerate 找到一个合适你的值。
树莓派供电不足也会影响视频质量，就像我上面的视频不是很清楚，我是直接用笔记本的USB供电的，一般来说笔记本USB口电流一般为500mA，所以如果需要视频清晰的话建议使用移动电源进行供电，或者使用有源USB hub。
</span>

当 `motion` 运行以后，可以通过 `SIGHUP` 信号来重新加载配置文件
`sudo killall -SIGHUP motion`

也可以直接关闭掉，然后重新启动
`sudo killall -w motion sudo motion`

当你关闭`motion`时，可以输入如下指令，然后画面就会定格到最后一刻：
`sudo killall -TERM motion`
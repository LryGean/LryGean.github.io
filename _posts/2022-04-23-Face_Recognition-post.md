---
layout: post
title: Face Recognition Based on Python
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

### 环境配置

1. Python-version: 3.9.5
2. Visual Studio Code
3. OpenCV: https://opencv.org - version 4.5.4
4. model 
+ 下载工具：pip
+ opencv-python
+ numpy（python科学计算的基础包）
+ Pillow（PIL，图像处理库）
+ os（提供路径操作）
+ urllib（网络请求库）
+ hashlib（提供hash算法）

### 构建过程
#### 1. 导入库
+ import cv2
+ import numpy
+ import os
+ import urllib
+ import urllib.request
import hashlib
+ from PIL import Image
+ from typing import Text

#### 2.过程
(1) 人脸检测
(2) 人脸录入
(3) 数据训练
(4) 人脸识别

### 人脸检测
#### 1. 流程图
![图片已失效](../style/img/img1/Face%20Detection.png "人脸检测流程图")
#### 2. 图片检测
##### (1)代码实例
```
# 导入cv图片
import cv2 as cv
#监测函数
def face_detect_demo():
    #灰度转换
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    #加载分类器
    face_detect = cv.CascadeClassifier('cv/opencv/sources/data/haarcascades/haarcascade_frontalface_alt2.xml')
    # 参数含义:(图片,缩放倍数,检测次数)
    face = face_detect.detectMultiScale(gray,1.05,5,0,(10,10),(300,300))
    for x,y,w,h in face:
        cv.rectangle(img,(x,y),(x+w,y+h),color=(0,0,255),thickness=2)
    cv.imshow('result',img)
#读取图片
img = cv.imread('face/face10.png')
#建立检测函数
face_detect_demo()
#等待
while True:
    if ord('q') == cv.waitKey(0):
        break
# 释放内容
cv.destroyAllWindows()
```
##### (2)检测效果

<style>
    .picFace {
        margin: 10px;
        width: 500px;
    }
    .picFace img {
        margin: 0 10px;
    }
</style>
<div class='picFace'>
    <img src='../style/img/img1/f1.png' title='检测科比'>
    <img src='../style/img/img1/f2.png' title='检测杜兰特'>
    <img src='../style/img/img1/f3.png' title='检测多人'>
</div>

#### 3. 动态检测
##### (1) 代码示例

```
# 导入cv图片
import cv2 as cv
import time
import numpy as np

# 监测函数
def face_detect_demo(img):
    #灰度转换
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    #加载分类器
    face_detect = cv.CascadeClassifier('cv/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml')
    # 参数含义:(图片,缩放倍数,检测次数,0,最小,最大)
    face = face_detect.detectMultiScale(gray,1.1,5)
    for x,y,w,h in face:
        cv.rectangle(img,(x,y),(x+w,y+h),color=(0,0,255),thickness=2)
    #窗口可自由缩放
    cv.namedWindow('result',0)
    #cv.resizeWindow('result',600,600)
    cv.imshow('result',img)


# 读取摄像头
# 参数说明：0：默认摄像头
# cap = cv.VideoCapture(0)

# 读取机器人摄像头
# cap = cv.VideoCapture('http://192.168.2.156:8081/')

# 读取手机摄像头（软件：IP摄像头）
cap = cv.VideoCapture('http://admin:981222@192.168.137.25:8081/')
#cap = cv.VideoCapture('http://admin:981222@10.1.40.20:8081/')

# 读取网页摄像头
# cap = cv.VideoCapture('http://ivi.bupt.edu.cn/hls/cctv1hd.m3u8')


# 读取视频
# cap = cv.VideoCapture('mp4/王顺和王冰冰.mp4')

# read:def read(self,image: Any =None) -> None
# 当self本身有视频内容的时候，有值并且返回值为true,image表示当前真的图像
# cap.read()

cap.set(cv.CAP_PROP_FRAME_WIDTH,1920)
cap.set(cv.CAP_PROP_FRAME_HEIGHT,1080)

#获取cap的视频帧（帧：每秒多少张图片）
fps = cap.get(cv.CAP_PROP_FPS)
print(fps)
#获取cap视频流的每帧大小
size = (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))
print(size)


# 循环
while True:
    flag,frame = cap.read()
    # 如果播放不成立的时候，假设不成立
    if not flag:
        break
    face_detect_demo(frame)
    # 保持画面持续：1
    # 保持静止持续：0
    if ord('q') == cv.waitKey(1):
        break
# 释放内容
cv.destroyAllWindows()
# 释放摄像头
cap.release()
```

##### (2) 检测效果

+ 各种摄像机调取检测人脸

<div class='picFace'>
    <img src='../style/img/img1/f4.png' title='检测me'>
    <img src='../style/img/img1/f5.png' title='检测科比'>
    <img src='../style/img/img1/f6.png' title='检测多人'>
</div>

+ 读取视频文件检测人脸

<div class='picFace'>
    <img src='../style/img/img1/f7.png' title='检测视频1'>
    <img src='../style/img/img1/f8.png' title='检测视频2'>
    <img src='../style/img/img1/f9.png' title='检测王冰冰'>
</div>

### 人脸录入
#### 1. 流程图

![图片已失效](../style/img/img1/Face%20Entry.png "人脸录入流程图")

#### 2. 代码示例

```
#导入模块
import cv2 as cv
#摄像头
cap = cv.VideoCapture('http://admin:981222@192.168.2.190:8081/') 

falg = 1
num = 1

while(cap.isOpened()): #检测是否在开启状态
    ret__flag,Vshow = cap.read() #得到每帧图像
    #窗口可自由缩放
    cv.namedWindow('Capture_Test',0)
    cv.imshow('Capture_Test',Vshow) #显示图像
    k = cv.waitKey(1) & 0xFF #按键判断 0xFF=1B
    if k == ord('s'): #保存
        cv.imwrite('save/'+str(num)+'.lena'+'.png',Vshow)
        print("Success to save"+str(num)+".jpg")
        print("-------------------------------")
        num += 1
    elif ord('q') == k: #退出
        break
# 释放摄像头
cap.release()
# 释放内存
cv.destroyAllWindows()
```

#### 3. 检测效果

<style>
    .picFace1 {
        margin: 10px;
        width: 500px;
    }
    .picFace1 img {
        margin: 0 10px;
    }
</style>
<div class='picFace1'>
    <img src='../style/img/img1/f10.png' title='1.lena.png'>
    <img src='../style/img/img1/f11.png' title='2.Gean.png'>
    <img src='../style/img/img1/f12.png' title='3.Kevin Durant.png'>
    <img src='../style/img/img1/f13.png' title='4.Kobe Bean Bryant.png'>
</div>

### 数据训练

#### 1. 流程图

![图片已失效](../style/img/img1/The%20Train%20Data.png "数据训练流程图")

#### 2. 代码示例

```
import os
import cv2 as cv
from PIL import Image
import numpy as np

def getImageAndLabels(path):
    # 存储人脸数据:二维列表，二维数组
    facesSamples = []
    # 存储姓名数据
    ids = []
    # 储存图片信息
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    # 加载分类器
    face_detector = cv.CascadeClassifier('cv/opencv/sources/data/haarcascades/haarcascade_frontalface_alt2.xml')
    # 遍历列表中的图片：保存身份信息
    for imagePath in imagePaths:
        # 打开图片，灰度化PIL有九种不同模式：1(黑白，有像素为1，没像素为0), L(灰度图像，把每个像素点变成0-255的数值，颜色越深，值越大),P, RGB, RGBA, CMYK, YCbCr, I, F.
        PIL_img = Image.open(imagePath).convert('L')
        # 图片灰度化处理后进行向量化处理，将图像转换为数组（把每个像素点变成数值），以黑白深浅
        # img_numpy:列表
        img_numpy = np.array(PIL_img,'uint8')
        # 通过分类器提取人脸特征，获取图片人脸特征，将人脸的特征数组存储在faces中
        faces = face_detector.detectMultiScale(img_numpy)
        # 获取每张图片的id和姓名
        id = int(os.path.split(imagePath)[1].split('.')[0])
        # 预防无面容照片
        # 将所画的方框添加到facesSamples列表中，所以每一个ids(0)和facesSamples(0)它们对应的是同一个人和同一个人向量下的特征
        for x,y,w,h in faces:
            ids.append(id)
            facesSamples.append(img_numpy[y:y+h,x:x+w])
    #打印脸部特征和id
    print('id:',id)
    print('fs:',facesSamples)
    return facesSamples,ids


if __name__ == '__main__':
    # 图片路径
    path = './data/jm/'
    # 获取图像数组id标签数组和姓名
    faces,ids = getImageAndLabels(path)
    # 加载识别器:加载LBPH识别器将面部和身份信息通过训练整合在一起，最后写入.yml文件中
    # 最后面部信息和身份信息就一一对应保存于文件中，在识别人脸时调用关系文件即可完成识别
    recognizer = cv.face.LBPHFaceRecognizer_create()
    # 训练
    recognizer.train(faces,np.array(ids))
    # 保存文件：生成一个一一对应的关系文件
    recognizer.write('trainer/trainer.yml')
```
#### 3. error

##### 报错信息 

+    ① AttributeError: module 'cv2' has no attribute 'detectMultiScale'
+    ② AttributeError: module 'cv2' has no attribute 'face'

##### 出错原因：

①可能cv2相关包没有安装完
②没有下载contrib库

##### 解决方法：

①pip uninstall opencv-python
②安装wheel包，在https://www.lfd.uci.edu/~gohlke/pythonlibs/下载相应Python版本的opencv最新库
③下载contrib库：pip install opencv-contrib-python

##### 训练模型文件

![图片已失效](../style/img/img1/datamodel.png "trainer.yml")

<style>
    p {
        color: #fff;
    }
</style>
<p>YML文件介绍：</p>
<p>
    YAML是一种直观的能够被电脑识别的数据序列化格式，容易被人类阅读，并且容易和脚本语言交互。YAML类似于XML，但是语法比XML简单得多，对于转化成数组或可以hash的数据时是很简单有效的。
    功能：
    YAML 的语法和其他高级语言类似，并且可以简单表达清单、散列表，标量等数据形态。 它使用空白符号缩进和大量依赖外观的特色，特别适合用来表达或编辑数据结构、各种配置文件、倾印调试内容、文件大纲（例如：许多电子邮件标题格式和 YAML 非常接近）。尽管它比较适合用来表达层次结构式（hierarchical model）的数据结构，不过也有精致的语法可以表示关系性（relational model）的数据。由于 YAML 使用空白字符和分行来分隔数据，使得它特别适合用 grep／Python／Perl／Ruby 操作。其让人最容易上手的特色是巧妙避开各种封闭符号，如：引号、各种括号等，这些符号在嵌套结构时会变得复杂而难以辨认
</p>

### 人脸识别

#### 1. 流程图

![图片已失效](../style/img/img1/Face%20Recognition.png "人脸识别流程图")

#### 2. 代码示例

```
from typing import Text
import cv2
import numpy as np
import os
# coding=utf-8
import urllib
import urllib.request
import hashlib
from PIL import Image,ImageFont,ImageDraw
from playsound import playsound

#加载训练数据集文件
recogizer=cv2.face.LBPHFaceRecognizer_create()
# 可执行评分依靠训练数据集文件
recogizer.read('trainer/trainer.yml')
# 储存名字
names=[]

#------------------------------------------------------------------------------#

# 报警全局变量：防治检测到未训练人员，若有，发送短信提醒
warningtime = 0
abc = 0

def md5(str):
    import hashlib
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()

statusStr = {
    '0': '短信发送成功',
    '-1': '参数不全',
    '-2': '服务器空间不支持,请确认支持curl或者fsocket,联系您的空间商解决或者更换空间',
    '30': '密码错误',
    '40': '账号不存在',
    '41': '余额不足',
    '42': '账户已过期',
    '43': 'IP地址限制',
    '50': '内容含有敏感词'
}

def warning():
    smsapi = "http://api.smsbao.com/"
    # 短信平台账号
    user = 'Gean'
    # 短信平台密码
    password = md5('lry981222')
    # 要发送的短信内容
    content = '【安全提示】尊敬的主人，发现未知人员在实验室，请注意！'
    # 要发送短信的手机号码
    phone = '17302254866'

    data = urllib.parse.urlencode({'u': user, 'p': password, 'm': phone, 'c': content})
    send_url = smsapi + 'sms?' + data
    response = urllib.request.urlopen(send_url)
    the_page = response.read().decode('utf-8')
    print(statusStr[the_page])

#------------------------------------------------------------------------------#
#准备识别的图片
def face_detect_demo(img):
    # 导入图片灰度化
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    face_detector=cv2.CascadeClassifier('cv/opencv/sources/data/haarcascades/haarcascade_frontalface_alt2.xml')
    face=face_detector.detectMultiScale(gray,1.1,5,cv2.CASCADE_SCALE_IMAGE,(100,100),(300,300))
    #face=face_detector.detectMultiScale(gray)
    for x,y,w,h in face:
        # 绘制矩形和圆形将人脸锁定
        cv2.rectangle(img,(x,y),(x+w,y+h),color=(0,0,255),thickness=2)
        cv2.circle(img,center=(x+w//2,y+h//2),radius=w//2,color=(0,255,0),thickness=1)
        # 人脸识别：人脸预测并评分（confidence）
        ids, confidence = recogizer.predict(gray[y:y + h, x:x + w])
        #print('标签id:',ids,'置信评分：', confidence)
        
        # 若评分大于80，说明人脸不可信，警报+1
        if confidence > 80:
            global warningtime
            warningtime += 1
            # 当警报超过100，说明该人脸不是所录入的人脸
            if warningtime > 100:
               warning()
               warningtime = 0
            # 创建一个可以在给定图像上绘图的对象
            # draw = ImageDraw.Draw(img)    
            # 设置中文格式
            # fontstyle = ImageFont.truetype("simsun.ttc",20,encoding="utf-8")
            # 绘制文本
            # draw.text((x + 10, y - 10),'不认识的陌生人',(0,255,0),font = fontstyle)

            cv2.putText(img, 'who?', (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 1)
        #如果评分低于80分，说明为可信人员，将其姓名显示在方框上
        else:
            cv2.putText(img,str(names[ids-1]), (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 1)
    cv2.namedWindow('result',0)
    cv2.imshow('result',img)
    #print('bug:',ids)

def name():
    path = './data/jm/'
    #names = []
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    for imagePath in imagePaths:
       name = str(os.path.split(imagePath)[1].split('.',2)[1])
       names.append(name)


cap=cv2.VideoCapture(0)
# cap = cv2.VideoCapture('http://admin:981222@192.168.137.209:8081/')

#默认分辨率为640x480,设置成1920x1080
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)

name()
while True:
    flag,frame=cap.read()
    if not flag:
        break
    face_detect_demo(frame) 
    if ord(' ') == cv2.waitKey(10):
        break
print("over!")
cv2.destroyAllWindows()
cap.release()
playsound('./mp3/1.mp3')#输出音频
#print(names)
```

#### 3. 检测效果

<video controls height='100%' width='100%' src="../style/img/img1/last.webm"></video>
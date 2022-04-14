---
layout: post
title: jekyll安装
category: tutorial
thumbnail: /style/image/头像.ico
icon: book
---

* content
{:toc}

安装指令 ：`gem install bundler jekyll`


创建项目目录
1. 新建项目文件夹 `cd 文件夹`

2. 生成项目文件：`jekyll new ./`

3. 第一次打开：`bundle exec jekyll serve`
![图片已失效](../style/img/%E6%8A%A5%E9%94%991.png "报错信息")

4. 添加webrick：`bundle add webrick`

5. 再次启动jekyll服务：`bundle exec jekyll serve`

6. 浏览器打开jekyll网站：`127.0.0.1:4000/` 或 `localhost:4000`

7. 进入指定模板文件夹

8. 下载bundle：`bundle install`(显示版本过老需要更新)

9. 更新bundle：`bundle update`

10. 若缺少rexml：`bundle add rexml`
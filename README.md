# 基于Django的博客框架  

本项目为一个基于Django的博客框架（A blog frame depend on Django），计划的特性有：  
1. 主题可定制、更换（心情不好就换个主题，但不需要重新设置models）；
2. 快速搭建博客，能让只有几小时Python基础的小伙伴也快速上手；
3. Views与APP分离，将Views置于主题中，便于维护管理；  

这是作为一个初学者新建的坑，主要是想把学到的东西想方设法放到实际项目中从而加深记忆与提高技能。  
目前还是很原始，很基础的版本，陆续完善中，其中参考了hexo搭建的博客的效果，特此感谢[yilia](https://github.com/litten/hexo-theme-yilia.git) 。  
希望各位大佬轻喷，如果有啥建议给我发邮件或者加我QQ：470657570，谢谢！  

## 一、To do list:
▢ 1. 编写日志页面；  
▢ 2. 编写管理日志页面；  
√ 3. 注册及登陆页面；  
▢ 4. 评论页面；  
▢ 5. 增加导入一键markdown文件功能；  
## 二、以下是开发日志，倒序书写： 
### 2018.06.20
1. 部署到了阿里云，欢迎访问：[明月不归尘](https://fslong.xyz) ；
2. 编写用户管理页；
3. 加入使用Ajax验证账户密码；
4. 由于django使用了csrf_token，用Ajax直接发送post请求会被拒绝，因此需要在使用Ajax之前加入以下代码（不能在文件中，必须在要使用Ajax的地方）：  
```javascript
$.ajaxSetup({
    data: {
        csrfmiddlewaretoken: '{{ csrf_token }}'
    },
});
```
### 2018.06.18
1. 完成了登陆和注册页面；
2. 完成了发表评论和显示评论；
3. 继续完善models和写完的页面；
### 2018.06.13  
1. 完善了博客编辑页面，增加了富文本编辑器；  
2. 完善了注册及登陆页面模板；  
3. 将登陆界面放在弹出框里面；  
### 2018.06.10  
最近在考驾照，推送时间不定，各位见谅。
1. 继续完善models；
2. 继续完善views；
3. 继续完善admin；
4. 总之就是东写一下西写一下，是时候建立一个To do list了！
### 2018.06.07
1. 将代码托管到Github上，开启交友之旅！
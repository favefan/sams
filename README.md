# Student-Activity-Management-System_background

Graduation works (in group).

## 开发环境
Python 3.7 64bit

Django 2.2

MySQL 10.3

## 系统功能设置:
普通用户： 
1. 个人活动（查看参与的活动数量√，对应加分项目的总得分，已报名的活动列表以及活动分别获得的奖项和加分） 
2. 公开活动（查看所有公开的活动列表√，并可报名√） 
3. 信息修改（修改密码√）

活动管理用户： 
1. 公开活动（*）√
2. 活动管理（创建活动√√√，生成并发布活动报名页面，查看当前帐号已创建的活动详情，并可修改活动详情，添加导入报名学生，设置活动参与学生获得奖项及加分） 
3. 信息修改（*）√

系统管理用户： 
1. 公开活动（*）√
2. 活动管理（*，删除活动√，删除活动中报名人员√，修改活动加分）
3. 学生管理（查看√√√，创建√√√，<修改:delete>，删除√√√学生对象以及对应普通用户）
4. 账号管理（查看√√√，创建√√√，修改√√√，删除√√√活动管理用户）
5. 信息修改（*）√
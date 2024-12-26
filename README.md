<div align="center">
<h1>Go Ldap Admin</h1>

Fork from [go-ldap-admin](https://github.com/opsre/go-ldap-admin)
<br>
Fork time: 2024-11-14 11:19

<p> 🌉 基于Go+Vue实现的openLDAP后台管理项目 🌉</p>

</div><br>

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->



## 变更点

- 赋予角色ID为2的子管理员拥有修改用户状态权限
- 新增脚本add_posixAccount.py，可以给用户添加posixAccount，解决LDAP client获取不到用户问题（需要配合定时任务执行）

## 手动配置
需要手动配置创建子管理员角色
- 角色名称：子管理员
- 关键字：subadmin
- 等级：2


## 构建
提前下载前端代码构建包：[dist.zip](https://github.com/Fsiyuetian/go-ldap-admin-ui/releases/download/v1.0/dist.zip)

```bash
# 修改Dockerfile
RUN release_url=$(curl -s https://api.github.com/repos/eryajf/go-ldap-admin-ui/releases/latest | grep "browser_download_url" | grep -v 'dist.zip.md5' | cut -d '"' -f 4); wget $release_url && unzip dist.zip && rm dist.zip && mv dist public/static
# 改为：
RUN unzip dist.zip && rm dist.zip && mv dist public/static

# 重新构建镜像
docker build -t go-ldap-admin:v1.0 .
```


<!-- readme: collaborators,contributors -end -->

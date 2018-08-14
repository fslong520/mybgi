echo "开始执行脚本..."
echo "由于一些操作需要最高权限，请使用sudo su切换到root账号下再执行source命令..."
echo "切换到mybgi工程目录..."
cd /home/fslong/projects/mybgi
echo "赋予www-data用户读写数据库权限..."
chgrp www-data db.sqlite3
chmod g+w db.sqlite3
echo "重启apache2服务..."
service apache2 restart
echo "脚本执行完毕,谢谢使用."

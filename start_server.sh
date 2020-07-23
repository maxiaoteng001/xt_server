echo 'git 开始拉取'
git pull
echo 'git 拉取结束'

echo '开启虚拟环境'
source venv/bin/activate

echo '安装依赖'
python3 -m pip install -r requirements.txt

echo '杀掉之前进程'
ps -efww|grep -w 'gevent_run.py'|grep -v grep|cut -c 9-15|xargs kill -9

echo '启动服务'
nohup python3 gevent_run.py >nohup.server 2>&1 &
echo '启动服务完成'

deactivate
echo '退出虚拟环境'


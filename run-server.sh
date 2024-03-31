# 激活虚拟环境
. venv/bin/activate

# 编译安装 F2 模块
WORKSPACE=${PWD}
cd ../f2
pip install -e .
cd ${WORKSPACE}

# 启动 docker 环境
cd Server
pip install -r ./requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.tuna.tsinghua.edu.cn
python3 Server.py
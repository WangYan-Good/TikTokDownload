#!/bin/bash

# 激活虚拟环境
if test -n "$VIRTUAL_ENV"
then
    echo "你处于Python虚拟环境中，路径为：$VIRTUAL_ENV"
else
    echo "激活Python虚拟环境"
    if . venv/bin/activate  1
    then
        echo "激活成功！"
    else
        echo "激活失败！"
    fi
fi

# 获取pip3的版本信息
pip3_version=$(pip3 --version 2>/dev/null | awk '{print $2}')

# 判断是否需要更新 pip
if [[ -z "$pip3_version" ]]; 
then
    echo "pip3 未安装或命令不存在。"
    exit 1
fi

echo "当前pip3的版本是：$pip3_version"

# # 获取最新的pip3版本信息
# latest_version=$(pip3 install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.tuna.tsinghua.edu.cn 2>&1 | grep -o 'Successfully installed pip-[0-9.]*' | awk -F'-' '{print $2}')

# if [[ "$pip3_version" == "$latest_version" ]]; 
# then
#     echo "当前pip3版本已是最新。"
# else
#     echo "当前pip3版本不是最新，正在更新..."
#     pip3 install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.tuna.tsinghua.edu.cn
#     echo "pip3 更新完成，新版本为：$latest_version"
# fi

# # 编译安装 F2 模块
if [[ -x "$(command -v f2)" ]];
then
    echo "f2 已成功安装！"
else
    echo "未检测到安装 f2， 正在编译安装..."
    WORKSPACE=${PWD}
    cd ./f2
    pip install -e .
    cd ${WORKSPACE}
fi

# 启动 docker 环境
echo "cd Server"
cd Server

echo "检查安装依赖"
pip install -r ./requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.tuna.tsinghua.edu.cn

echo "启动 docker 环境"
python3 Server.py
# 使用官方的 Python 作为基础镜像
FROM python:3.9-slim

# 设置环境变量，防止 Python 写入缓存文件并确保控制台输出
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 设置工作目录
WORKDIR /app

# 安装系统依赖和服务（nginx, keepalived, redis, rabbitmq, mysql, supervisor）
RUN apt-get update && apt-get install -y nginx
RUN apt-get install -y keepalived
RUN apt-get install -y redis-server
RUN apt-get install -y rabbitmq-server
RUN apt-get install -y supervisor
#RUN apt-get install -y mysql-server
RUN apt-get install -y default-libmysqlclient-dev
RUN rm -rf /var/lib/apt/lists/*

# 安装必要的编译工具和开发库
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    default-libmysqlclient-dev \
    libmariadb-dev-compat \
    libcups2-dev \
    libdbus-1-dev \
    pkg-config \
    --no-install-recommends

RUN apt-get install -y libmariadb-dev-compat
RUN apt-get update
RUN apt-get install -y vim

# 安装 Python 依赖 (例如 Celery)
COPY requirements.txt .
RUN pip3 install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制配置文件到容器中
COPY nginx.conf /etc/nginx/nginx.conf
COPY keepalived.conf /etc/keepalived/keepalived.conf
COPY supervisord.conf /etc/supervisor/supervisord.conf
COPY redis.conf /etc/redis/redis.conf
COPY . /app/

# 暴露必要的端口  
EXPOSE 80 6379 5672 3306 16379 25672 15672 4369 443 112

# 启动 supervisor 来管理所有进程
CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]


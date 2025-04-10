# 使用Python官方镜像
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 设置Python环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 安装系统依赖
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements.txt
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 创建uploads目录
RUN mkdir -p app/static/uploads && chmod 777 app/static/uploads

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["python", "run.py"]
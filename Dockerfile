# 使用 uv 官方镜像进行多阶段构建
FROM astral-sh/uv:python3.10-alpine AS builder

# 设置工作目录
WORKDIR /app

# 启用字节码编译，减少启动时间
ENV UV_COMPILE_BYTECODE=1
# 禁用 uv 缓存以减小镜像体积
ENV UV_NO_CACHE=1

# 首先只复制依赖定义文件，利用 Docker 缓存
COPY pyproject.toml uv.lock ./

# 安装依赖（不包含开发依赖）
RUN uv sync --no-dev --no-install-project

# 复制源代码
COPY src ./src
COPY README.md ./

# 安装项目本身
RUN uv sync --no-dev

# 运行阶段
FROM python:3.10-alpine

WORKDIR /app

# 从构建阶段复制安装好的环境
COPY --from=builder /app/.venv /app/.venv

# 设置环境变量，使用 .venv 中的 Python
ENV PATH="/app/.venv/bin:$PATH"

# 复制业务代码（如果是以包形式运行，也可以只复制 venv）
COPY src ./src

# 设置默认启动命令
CMD ["python", "-m", "app.main"]

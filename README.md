# Agent Enterprise Boilerplate

面向企业级 Agent 项目的 Python 起手式。模板默认使用 `src/app` 作为唯一代码包，并把打包、命令入口、测试覆盖率、Docker 启动和 README 全部指向同一个包，避免新项目一开始就出现入口漂移。

## 核心特性

- `uv` 管理依赖和锁文件
- `src/app` 布局
- `ruff`、`mypy`、`pytest`、`pytest-cov`
- `pre-commit` 和 GitHub Actions CI
- Docker 多阶段构建
- 基于 `pydantic-settings` 的强类型配置
- 基于 `loguru` 的日志和 trace id
- Agent 生命周期与 LLM provider 容器预留

## 目录结构

```text
src/app/
├── api/               API 或工具路由预留
├── config/            配置、枚举和环境变量加载
├── core/              容器、生命周期、日志和启动辅助
└── main.py            应用主入口
tests/                 自动化测试
skills/                Agent prompt 模板
Dockerfile             容器镜像定义
Makefile               常用指令集
pyproject.toml         项目定义与工具链配置
.pre-commit-config.yaml Git 提交前自动校验
```

## 快速开始

```bash
uv sync --extra dev
cp .env.example .env
```

运行应用：

```bash
make run
# 或
uv run python -m app.main
```

默认 provider 是 `openai`。启动前会校验当前 provider 所需的 API key，例如 `OPENAI_API_KEY`。

## 开发指令

| 指令 | 说明 |
| :--- | :--- |
| `make install` | 安装依赖 |
| `make run` | 运行应用入口 |
| `make test` | 运行测试和覆盖率 |
| `make lint` | 自动修复 Ruff 问题并格式化 |
| `make check` | 运行 Ruff、格式检查和 Mypy |
| `make clean` | 清理缓存和构建产物 |

## Docker

```bash
docker-compose up --build
```

## 模板生成建议

如果要把它扩展成团队级模板，建议下一步引入 Copier 或 Cookiecutter，并把这些变量集中管理：

- `project_name`
- `package_name`
- `python_version`
- `app_type`
- `with_docker`
- `with_agent`

当前仓库已先固定为 `src/app`，保证这个版本开箱时所有入口一致。

## License

MIT

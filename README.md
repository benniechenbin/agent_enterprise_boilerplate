# Python 项目开局模板 (Enhanced)

这是一个现代化、生产就绪的 Python 项目模板，采用了工业界的最佳实践。

## 核心特性

- **uv 驱动**：使用目前最快的 Python 依赖管理工具。
- **src 布局**：防止意外导入，确保测试环境与安装环境一致。
- **严格类型**：内置 `mypy` 配置，支持静态类型检查。
- **极致检测**：集成 `ruff` (Linter & Formatter)、`pytest` (Tests & Coverage)。
- **自动化**：提供 `Makefile`、`pre-commit` 钩子和 GitHub Actions CI 流程。
- **容器化**：提供多阶段构建的 `Dockerfile` 和 `docker-compose.yml`。
- **健壮配置**：基于 `pydantic-settings` 的强类型配置管理。

## 目录结构

```text
src/python_project/    核心代码空间 (需重命名为你的项目名)
├── config/            配置与环境变量加载
├── core/              项目启动与初始化入口
├── observability/     日志与可观测性辅助模块
└── main.py            应用主入口
tests/                 自动化测试
docs/                  (预留) 文档目录
Dockerfile             容器镜像定义
Makefile               常用指令集
pyproject.toml         项目定义与工具链配置
.pre-commit-config.yaml Git 提交前自动校验
```

## 快速开始

### 1. 环境准备 (推荐使用 uv)

```powershell
# 安装依赖并创建虚拟环境
uv sync

# 复制配置文件
cp .env.example .env
```

### 2. 运行应用

```powershell
# 使用 Makefile 命令
make run

# 或直接运行
uv run python -m python_project.main
```

## 开发常用指令

| 指令 | 说明 |
| :--- | :--- |
| `make install` | 安装所有依赖 |
| `make test` | 运行测试并查看覆盖率 |
| `make lint` | 运行 Ruff 自动修复并格式化代码 |
| `make check` | 运行 Ruff 检查和 Mypy 类型检查 |
| `make clean` | 清理缓存和临时文件 |

## Docker 运行

```bash
docker-compose up --build
```

## 进阶建议

1. **重命名包名**：将 `src/python_project` 文件夹重命名为你自己的项目包名（如 `src/my_awesome_app`），并同步修改 `pyproject.toml` 中的相关引用。
2. **启用 pre-commit**：运行 `uv run pre-commit install`，这样在每次 `git commit` 时都会自动执行代码风格和类型检查。
3. **扩展配置**：在 `src/python_project/config/settings.py` 中添加你的业务特定配置项。

## License

MIT

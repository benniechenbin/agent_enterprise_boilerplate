import os
from pathlib import Path

def main():
    env_file = Path(".env")
    example_file = Path(".env.example")

    if not env_file.exists():
        # 如果没有 .env 文件，直接跳过
        return

    with open(env_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    example_lines = []
    for line in lines:
        line = line.strip()
        # 保留空行和注释
        if not line or line.startswith("#"):
            example_lines.append(line)
        # 脱敏处理：只保留等号左边的 Key
        elif "=" in line:
            key = line.split("=", 1)[0]
            example_lines.append(f"{key}=")
        else:
            example_lines.append(line)

    # 写入 .env.example
    with open(example_file, "w", encoding="utf-8") as f:
        f.write("\n".join(example_lines) + "\n")
        
    print("✅ 成功从 .env 生成脱敏的 .env.example 文件！")

if __name__ == "__main__":
    main()
# -*- coding: utf-8 -*-
"""
Merge all python files in second_ui/ into one single python file.

- No logic changes
- Keep original code
- Add clear file boundary markers
"""

import os
from datetime import datetime

# ===== 可配置项 =====
SRC_DIR = "second_ui"
OUT_FILE = "second_ui_merged.py"
ENCODING = "utf-8"


def is_python_file(filename: str) -> bool:
    return filename.endswith(".py") and not filename.startswith("__")


def read_file(path: str) -> str:
    with open(path, "r", encoding=ENCODING) as f:
        return f.read()


def main():
    if not os.path.isdir(SRC_DIR):
        raise FileNotFoundError(f"Directory not found: {SRC_DIR}")

    py_files = sorted(
        f for f in os.listdir(SRC_DIR)
        if is_python_file(f)
    )

    if not py_files:
        raise RuntimeError("No python files found in second_ui/")

    merged_lines = []

    # ===== 文件头 =====
    merged_lines.append("#" * 80)
    merged_lines.append("# AUTO-GENERATED FILE - DO NOT EDIT MANUALLY")
    merged_lines.append("#")
    merged_lines.append("# Source directory : second_ui/")
    merged_lines.append(f"# Generated at    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    merged_lines.append("#")
    merged_lines.append("# Included files:")
    for f in py_files:
        merged_lines.append(f"#   - {f}")
    merged_lines.append("#" * 80)
    merged_lines.append("\n\n")

    # ===== 合并各文件 =====
    for idx, filename in enumerate(py_files, start=1):
        file_path = os.path.join(SRC_DIR, filename)
        content = read_file(file_path)

        merged_lines.append("\n" + "=" * 80)
        merged_lines.append(f"# FILE {idx}/{len(py_files)} : {filename}")
        merged_lines.append(f"# PATH   : {file_path}")
        merged_lines.append("=" * 80 + "\n")

        # 防止多重编码声明
        content = content.replace("# -*- coding: utf-8 -*-", "").lstrip()

        merged_lines.append(content.rstrip() + "\n")

    # ===== 写入文件 =====
    with open(OUT_FILE, "w", encoding=ENCODING) as f:
        f.write("\n".join(merged_lines))

    print("Merge completed successfully.")
    print(f"Output file : {OUT_FILE}")
    print("Merged files:")
    for f in py_files:
        print(f"  - {f}")


if __name__ == "__main__":
    main()

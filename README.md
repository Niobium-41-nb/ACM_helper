# ACM_helper

由 vanadium-23(Niobium-41-nb) 开发的 ACM 竞赛辅助工具包。

## 项目简介

`ACM_helper` 是一个模块化的 ACM 竞赛辅助工具库，旨在为算法竞赛选手提供常用算法、数据结构实现，以及自动化测试用例生成等实用功能。通过本工具包，用户可以更高效地进行算法调试、性能测试和竞赛准备。

## 主要功能

- **算法与数据结构实现**：核心算法、常用数据结构等，便于直接调用。
- **测试用例生成**：支持 C++ 标准程序与数据生成器的自动编译、运行、清理，批量生成测试数据。
- **辅助工具函数**：如输入输出处理、调试工具、性能测试等。
- **模块化设计**：按需动态导入，提升性能和易用性。

## 目录结构

```
ACM_helper/
    core.py         # 核心算法与数据结构
    utils.py        # 辅助工具与测试用例生成
    __init__.py     # 包初始化与动态导入
tests/
    test_core.py    # 单元测试
requirements.txt    # 依赖说明
setup.py           # 安装脚本
```

## 安装与使用

1. 克隆仓库到本地：
   ```
   git clone https://github.com/Niobium-41-nb/ACM_helper.git
   ```
2. 安装依赖：
   ```
   pip install -r requirements.txt
   ```
3. 在你的 Python 项目中导入并使用：
   ```python
   from ACM_helper import core, utils
   ```

## 适用人群

- ACM/ICPC/算法竞赛选手
- 算法学习者
- 需要批量生成测试用例的开发者

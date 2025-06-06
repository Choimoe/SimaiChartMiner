# SimaiChartMiner

一个用于挖掘、分析和探索音乐游戏谱面数据的模板项目，从海量谱面中发掘有趣的模式和统计数据！

本项目中的示例脚本 (`main.py`) 将统计所有谱面中真绝赞（不带 `x` 修饰的无判定保护绝赞），并按数量排序输出结果。你可以基于此脚本进行修改，以实现你自己的分析逻辑。

## ✨ 功能

- **模块化代码**: 将文件查找、数据处理、结果打印等逻辑拆分为独立函数，易于理解和维护。
- **开箱即用**: 提供一个完整的分析示例，帮助你快速上手。
- **易于定制**: 清晰的代码结构让你能轻松修改核心处理逻辑，以满足不同的分析需求。

## 📁 项目结构

项目已预先配置好推荐的目录结构：

```
SimaiChartMiner/
├── data/
├── main.py
└── README.md
```

## 🚀 如何开始

请按照以下步骤来配置和运行本项目。

### 1. 克隆项目与数据

获取本项目和其中预先配置的谱面数据 `submodule`，你有以下两种选择：

**方式一：克隆时一并下载 (推荐)**

```
git clone --recurse-submodules https://github.com/Choimoe/SimaiChartMiner.git
cd SimaiChartMiner
```

这条命令会在克隆主项目的同时，自动初始化并下载 `data` 目录下的谱面数据。

**方式二：分开下载**

如果你已经克隆了项目但未下载数据，可以执行以下命令：

```
git clone https://github.com/Choimoe/SimaiChartMiner.git
cd SimaiChartMiner
git submodule update --init --recursive
```

### 2. 配置环境与安装依赖

（建议创建一个独立的 Python 虚拟环境，以避免包冲突。）

安装所有必要的依赖：

```
pip install PySimaiParser
```

## 💻 如何使用

所有准备工作就绪后，你可以直接运行分析脚本。

```
python main.py
```

脚本会默认扫描 `data` 目录。你也可以指定一个不同的目录：

```
python main.py /path/to/your/chart/data
```

运行后，你将在终端看到类似如下格式的输出：

```
--- Chart Analysis Results (Top 50) ---
ID       | Song Title                   | Diff Idx | Total Breaks | Special Breaks | Ratio
-------------------------------------------------------------------------------------------
102      | Oshama Scramble!             | 5        | 12           | 10             | 83.33%
8        | TRUELOVESONG                 | 4        | 5            | 4              | 80.00%
...
```

## 🛠️ 如何自定义

本模板的核心价值在于其易于定制。要实现你自己的分析逻辑，你主要需要关注和修改 `main.py` 中的 `process_chart_file` 函数。

```
def process_chart_file(chart_file_path):
    """
    分析单个谱面文件，并返回其统计结果。
    """
    # ... 省略部分代码 ...

    for fumen in chart.processed_fumens_data:
        # ...

        # ▼▼▼ 在这里修改你的核心分析逻辑 ▼▼▼
        for note_event in fumen.get("note_events", []):
            for note in note_event.get("notes", []):
                # 示例: 判断 note.get("is_break") 和 note.get("is_ex")
                # 你可以在这里添加任何你想要的判断条件
                # 例如: note.get("is_hanabi"), note.get("note_type") == "SLIDE" 等
                pass 
        # ▲▲▲ 在这里修改你的核心分析逻辑 ▲▲▲

        # ...
        # 你也可以修改 fumen_results.append({}) 中的字典结构，以存储你需要的不同数据
    
    return fumen_results
```

例如，如果你想统计每个谱面的星星数量，你可以这样修改：

1. 在 `process_chart_file` 中添加一个新的计数器 `slide_note_count = 0`。
2. 在循环中，判断 `note.get("note_type") == "SLIDE"`，如果为真，则计数器加一。
3. 将 `slide_note_count` 添加到返回的 `fumen_results` 字典中。
4. 最后，修改 `print_results` 函数以展示新的统计数据。
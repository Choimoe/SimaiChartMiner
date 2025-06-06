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
├── util.py
├── main.py
└── README.md
```

## 🚀 如何开始

请按照以下步骤来配置和运行本项目。


### 0. 使用本项目作为模板（可选）

使用右上角 Use this template - Create a new repository 来基于本模板创建您自己的项目。

### 1. 克隆本项目及子模块

地址请修改为您基于本模板创建的新项目地址：

```
git clone https://github.com/Choimoe/SimaiChartMiner.git
cd SimaiChartMiner
```

下载谱面文件：

```
git submodule update --init --recursive
```

请注意，谱面文件子模块仓库体积较大，请确认您已经成功下载，否则后续 `main.py` 会找不到谱面文件。


### 2. 配置环境与安装依赖

（建议创建一个独立的 Python 虚拟环境，以避免包冲突。）

安装所有必要的依赖：

```
pip install -r requirements.txt
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

运行后，你将在终端看到带有进度条的分析过程，以及对齐整洁的输出结果：

```
开始扫描目录: data
正在分析谱面: 100%|████████████████████| 1621/1621 [00:32<00:00, 50.45it/s, 840_IMPERISHABLENIGHT20062016REFINE]

--- Chart Analysis Results (Top 50) ---
ID       | Song Title                     | Diff Idx | Total Breaks | Special Breaks | Ratio   
-----------------------------------------------------------------------------------------------
111222   | [光]BREaK! BREaK! BREaK![宴]   | 6        | 918          | 918            | 100.00% 
140227   | [某]Garakuta Doll Play[宴]     | 6        | 341          | 341            | 100.00% 
130227   | [玉]Garakuta Doll Play[宴]     | 6        | 253          | 253            | 100.00% 
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

关于 `fumen` 具体的结构可以参考：[PySimaiParser - Wiki](https://github.com/Choimoe/PySimaiParser/wiki)。

## 贡献

欢迎参与贡献！如果您想为项目做出贡献，请考虑以下几点：

- Fork 本仓库。
- 为您的新功能或错误修复创建一个新的分支。
- 为您的更改编写测试。
- 确保所有测试都通过。
- 提交一个 Pull Request，并清晰描述您的更改。

## 许可证

本项目采用 MIT 许可证。详情请参阅 `LICENSE` 文件。
import os
import re
import argparse
import sys
from SimaiParser import SimaiChart
from tqdm import tqdm
from wcwidth import wcswidth

from util import ljust_cjk


def find_chart_files(data_directory):
    """
    遍历指定目录，返回所有maidata.txt文件的路径列表。

    Args:
        data_directory (str): 包含谱面数据的根目录。

    Returns:
        list: maidata.txt 文件的完整路径列表。
    """
    chart_files = []
    print(f"开始扫描目录: {data_directory}")
    for partition in os.listdir(data_directory):
        partition_path = os.path.join(data_directory, partition)
        if not os.path.isdir(partition_path):
            continue

        for song_folder in os.listdir(partition_path):
            song_path = os.path.join(partition_path, song_folder)
            chart_file_path = os.path.join(song_path, 'maidata.txt')

            if os.path.isfile(chart_file_path):
                chart_files.append(chart_file_path)
    return chart_files


def process_chart_file(chart_file_path):
    """
    分析单个谱面文件，并返回其统计结果。

    Args:
        chart_file_path (str): maidata.txt 文件的路径。

    Returns:
        list: 包含该文件各难度谱面分析结果的字典列表。
    """
    song_folder = os.path.basename(os.path.dirname(chart_file_path))
    match = re.match(r'^(\d+)', song_folder)
    song_id = match.group(1) if match else 'N/A'

    fumen_results = []

    try:
        with open(chart_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        chart = SimaiChart()
        chart.load_from_text(content)

        song_title = chart.metadata.get("title", "未知标题")

        for fumen in chart.processed_fumens_data:
            if not fumen.get("note_events") and not fumen.get("level_info"):
                continue

            difficulty_index = fumen.get("difficulty_index", -1)
            total_break_notes = 0
            special_break_notes = 0  # is_ex is False and is_break is True

            for note_event in fumen.get("note_events", []):
                for note in note_event.get("notes", []):
                    if note.get("is_break"):
                        total_break_notes += 1
                        if not note.get("is_ex"):
                            special_break_notes += 1

            if total_break_notes > 0:
                ratio = special_break_notes / total_break_notes
                fumen_results.append({
                    "song_id": song_id,
                    "song_title": song_title,
                    "difficulty_index": difficulty_index,
                    "total_breaks": total_break_notes,
                    "special_breaks": special_break_notes,
                    "ratio": ratio
                })
    except Exception as e:
        print(f"\n处理文件失败 '{chart_file_path}': {e}", file=sys.stderr)

    return fumen_results


def print_results(results):
    """
    格式化并打印分析结果到控制台，确保CJK字符正确对齐。

    Args:
        results (list): 包含所有谱面分析结果的列表。
    """
    results.sort(key=lambda x: x["special_breaks"], reverse=True)

    print("\n--- Chart Analysis Results (Top 50) ---")

    # 打印表头
    header = (f"{ljust_cjk('ID', 8)} | {ljust_cjk('Song Title', 30)} | "
              f"{ljust_cjk('Diff Idx', 8)} | {ljust_cjk('Total Breaks', 12)} | "
              f"{ljust_cjk('Special Breaks', 14)} | {ljust_cjk('Ratio', 8)}")
    print(header)
    print("-" * wcswidth(header))

    if not results:
        print("在指定目录中没有找到任何谱面数据或符合条件的Note。")
        return

    for res in results[:50]:
        title = res['song_title']

        # 对过长的标题进行截断，同时考虑CJK字符宽度
        display_title = title
        if wcswidth(title) > 30:
            current_width = 0
            for i, char in enumerate(title):
                char_width = wcswidth(char)
                if current_width + char_width > 27:
                    display_title = title[:i] + '...'
                    break
                current_width += char_width

        # 使用CJK对齐函数
        id_str = ljust_cjk(res['song_id'], 8)
        title_str = ljust_cjk(display_title, 30)
        diff_str = ljust_cjk(str(res['difficulty_index']), 8)
        total_b_str = ljust_cjk(str(res['total_breaks']), 12)
        special_b_str = ljust_cjk(str(res['special_breaks']), 14)
        ratio_str = ljust_cjk(f"{res['ratio']:.2%}", 8)

        print(f"{id_str} | {title_str} | {diff_str} | {total_b_str} | {special_b_str} | {ratio_str}")


def main():
    """
    脚本主入口，处理命令行参数并调用分析函数。
    """
    parser = argparse.ArgumentParser(
        description="分析Simai谱面目录，统计特定类型的Break Note。",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "data_directory",
        nargs='?',
        default="data",
        help="包含谱面数据的根目录。\n"
             "目录结构应为: data/[分区]/[歌曲id]_[歌曲名称]/maidata.txt\n"
             "(默认值: 'data')"
    )

    args = parser.parse_args()

    if not os.path.isdir(args.data_directory):
        print(f"错误: 目录 '{args.data_directory}' 不存在或不是一个有效的目录。", file=sys.stderr)
        sys.exit(1)

    all_results = []
    chart_files = find_chart_files(args.data_directory)

    if not chart_files:
        print("在指定目录中未找到任何 'maidata.txt' 文件。")
        sys.exit(0)

    # 使用tqdm来显示进度条
    with tqdm(total=len(chart_files), desc="正在分析谱面", bar_format="{l_bar}{bar:20}{r_bar}") as pbar:
        for chart_file in chart_files:
            pbar.set_postfix_str(os.path.basename(os.path.dirname(chart_file)), refresh=True)
            all_results.extend(process_chart_file(chart_file))
            pbar.update(1)

    print_results(all_results)


if __name__ == "__main__":
    main()

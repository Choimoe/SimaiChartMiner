import os
import re
import argparse
import sys
from SimaiParser import SimaiChart


def find_chart_files(data_directory):
    """
    遍历指定目录，生成所有maidata.txt文件的路径。

    Args:
        data_directory (str): 包含谱面数据的根目录。

    Yields:
        str: maidata.txt 文件的完整路径。
    """
    print(f"开始扫描目录: {data_directory}")
    for partition in os.listdir(data_directory):
        partition_path = os.path.join(data_directory, partition)
        if not os.path.isdir(partition_path):
            continue

        for song_folder in os.listdir(partition_path):
            song_path = os.path.join(partition_path, song_folder)
            chart_file_path = os.path.join(song_path, 'maidata.txt')

            if os.path.isfile(chart_file_path):
                yield chart_file_path


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
        print(f"处理文件失败 '{chart_file_path}': {e}", file=sys.stderr)

    return fumen_results


def print_results(results):
    """
    格式化并打印分析结果到控制台。

    Args:
        results (list): 包含所有谱面分析结果的列表。
    """
    results.sort(key=lambda x: x["special_breaks"], reverse=True)

    print("\n--- Chart Analysis Results (Top 50) ---")
    print(
        f"{'ID':<8} | {'Song Title':<30} | {'Diff Idx':<8} | {'Total Breaks':<12} | {'Special Breaks':<14} | {'Ratio':<8}")
    print("-" * 95)

    if not results:
        print("在指定目录中没有找到任何谱面数据或符合条件的Note。")
        return

    for res in results[:50]:
        title = res['song_title']
        display_title = (title[:27] + '...') if len(title) > 30 else title
        print(f"{res['song_id']:<8} | {display_title:<30} | {res['difficulty_index']:<8} | "
              f"{res['total_breaks']:<12} | {res['special_breaks']:<14} | "
              f"{res['ratio']:.2%}:<8")

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
            for chart_file in find_chart_files(args.data_directory):
                all_results.extend(process_chart_file(chart_file))

            print_results(all_results)

        if __name__ == "__main__":
            main()

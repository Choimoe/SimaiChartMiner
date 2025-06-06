from wcwidth import wcswidth


def ljust_cjk(text, width):
    """
    一个能够正确处理中日韩 (CJK) 字符的左对齐函数。
    它会根据字符串在终端的实际显示宽度进行空格填充。

    Args:
        text (str): 需要对齐的文本。
        width (int): 期望的总显示宽度。

    Returns:
        str: 填充空格后对齐的字符串。
    """
    text_width = wcswidth(text)
    if text_width == -1:  # wcswidth 返回 -1 表示包含不可打印字符
        text_width = len(text)  # 回退到使用字符长度

    padding_needed = width - text_width
    return text + ' ' * padding_needed

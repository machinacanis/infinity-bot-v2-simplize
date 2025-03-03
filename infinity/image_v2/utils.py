from PIL import ImageDraw, ImageFont

sans_35_font = ImageFont.truetype("./assets/font/SourceHanSans_35.otf", 42)
sans_15_font = ImageFont.truetype("./assets/font/SourceHanSans_15.otf", 26)
sans_15_font_28 = ImageFont.truetype("./assets/font/SourceHanSans_15.otf", 28)
sans_17_font = ImageFont.truetype("./assets/font/SourceHanSans_17.ttf", 28)
ntlgpro_B = ImageFont.truetype("./assets/font/FOT-RodinNTLGPro-B.otf", 32)
ntlgpro_EB = ImageFont.truetype("./assets/font/FOT-RodinNTLGPro-EB.otf", 32)
sans_37_font = ImageFont.truetype("./assets/font/SourceHanSans_37.ttf", 28)
ntlgpro_B_18 = ImageFont.truetype("./assets/font/FOT-RodinNTLGPro-B.otf", 18)
sans_35_font_28 = ImageFont.truetype("./assets/font/SourceHanSans_35.otf", 28)
ntlgpro_EB_48 = ImageFont.truetype("./assets/font/FOT-RodinNTLGPro-EB.otf", 48)


def generate_maimai_filename(song_id: int):
    # 将ID转换为字符串，并在左侧补足0，使其总长度为6位
    padded_id = f"{song_id:06}"
    # 生成文件名
    filename = f"UI_Jacket_{padded_id}.png"
    return filename


def generate_chunithm_filename(song_id: int):
    # 将ID转换为字符串，并在左侧补足0，使其总长度为6位
    padded_id = f"{song_id:04}"
    # 生成文件名
    filename = f"CHU_UI_Jacket_{padded_id}.png"
    return filename


def draw_centered_text(
    draw: ImageDraw, text: str, position: tuple, font: ImageFont, fill: str
):
    # 计算文本的边界框
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]

    # 计算水平居中的起始位置
    x = position[0] - text_width // 2
    y = position[1]

    # 绘制文本
    draw.text((x, y), text, font=font, fill=fill)


def draw_wrapped_text(
    draw: ImageDraw,
    text: str,
    position: tuple,
    font: ImageFont,
    fill: str,
    max_width: int,
):
    # 拆分文本为单词列表
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        # 计算当前行加上新单词后的宽度
        test_line = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font)
        width = bbox[2] - bbox[0]  # 获取文本的宽度

        if width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    # 添加最后一行
    if current_line:
        lines.append(current_line)

    # 绘制每一行文本
    x, y = position
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        bbox = draw.textbbox((0, 0), line, font=font)
        y += bbox[3] - bbox[1]  # 移动到下一行


def get_maimai_real_song_id(song_id: int):
    if 100000 <= song_id <= 110000:
        return song_id - 100000
    elif 110000 <= song_id:
        return song_id - 100000
    elif 1000 <= song_id <= 10000:
        return 10000 + song_id
    else:
        return song_id


def get_maimai_shortest_song_id(song_id: int):
    if 100000 <= song_id <= 110000:
        return song_id - 100000
    elif 110000 <= song_id:
        return song_id - 110000
    elif song_id >= 10000:
        return song_id - 10000
    else:
        return song_id

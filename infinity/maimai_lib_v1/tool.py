import math
import time
from io import BytesIO
import base64
import json
import textwrap
from PIL.ImageFont import FreeTypeFont

from .music import total_list
from .plate_map import NOW_VERSION
from .. import *



def hash(qq: int):
    days = int(time.strftime("%d", time.localtime(time.time()))) + 31 * int(
        time.strftime("%m", time.localtime(time.time()))) + 77
    return (days * qq) >> 8


def get_cover_len6_id(mid: str) -> str:
    mid = int(mid)
    if mid > 10000:
        mid -= 10000
    return f'{mid:06d}'

def get_cover_len4_id(mid: str) -> str:
    mid = int(mid)
    mid += 10000
    return f'{mid:05d}'

def image_path_to_base64(byte_data: bytes) -> str:
    base64_str = base64.b64encode(byte_data).decode()
    return 'base64://' + base64_str


def image_to_base64_gif(imgPath):
    with open(imgPath, "rb") as f:
        base64_data = base64.b64encode(f.read())
        f.close()
    return base64_data

def hash(qq: int):
    days = int(time.strftime("%y", time.localtime(time.time()))) + 9 * int(time.strftime("%d", time.localtime(time.time()))) + 31 * int(
        time.strftime("%m", time.localtime(time.time())))
    return (days * qq) >> 8

def is_pro_group(group_id):
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pro_groups.json')
    if os.path.exists(file):
        with open(file, 'r') as f:
            group_pro = json.load(f)
    else:
        group_pro = {}
        with open(file, 'w') as f:
            json.dump(group_pro, f)

    return group_pro.get(str(group_id), {}).get('pro', False)

# def wrap_text(title, max_width):
#     wrapper = textwrap.TextWrapper(width=max_width)
#     wrapped_title = wrapper.fill(text=title)
#     return wrapped_title
def wrap_text(text, font, max_width):
    lines = []
    line = ''
    for char in text:
        if font.getsize(line + char)[0] <= max_width:
            line += char
        else:
            lines.append(line)
            line = char
    lines.append(line)  # 添加最后一行
    return lines

def truncate_text(text, font, max_width):
    if font.getsize(text)[0] <= max_width:
        return text
    else:
        for i in range(len(text), 0, -1):
            if font.getsize(text[:i] + '...')[0] <= max_width:
                return text[:i] + '...'
        return '...'
    

def computeRaB50(ds: float, achievement:float) -> int:
    baseRa = 22.4
    if achievement == 0:
        baseRa = 0
    elif achievement < 20:
        baseRa = 1.6
    elif achievement < 30:
        baseRa = 3.2
    elif achievement < 40:
        baseRa = 4.8
    elif achievement < 50:
        baseRa = 6.4
    elif achievement < 60:
        baseRa = 8
    elif achievement < 70:
        baseRa = 9.6
    elif achievement < 75:
        baseRa = 11.2
    elif achievement < 79.9999:
        baseRa = 12
    elif achievement == 79.9999:
        baseRa = 12.8
    elif achievement < 90:
        baseRa = 13.6
    elif achievement < 94:
        baseRa = 15.2
    elif achievement < 96.9999:
        baseRa = 16.8
    elif achievement == 96.9999:
        baseRa = 17.6
    elif achievement < 98:
        baseRa = 20.0 
    elif achievement < 98.9999:
        baseRa = 20.3
    elif achievement == 98.9999:
        baseRa = 20.6
    elif achievement < 99.5:
        baseRa = 20.8
    elif achievement < 99.9999:
        baseRa = 21.1
    elif achievement == 99.9999:
        baseRa = 21.4
    elif achievement < 100.4999:
        baseRa = 21.6
    elif achievement == 100.4999:
        baseRa = 22.2
    return math.floor(ds * (min(100.5, achievement) / 100) * baseRa)

def get_font_size(font: FreeTypeFont, content: str) -> tuple[float, float]:
    x0, y0, x1, y1 = font.getbbox(content)
    w, h = x1 - x0, y1 - y0
    return w, h

type_map = {
    "SD":"standard",
    "DX":"dx"
}

def translate_df_to_lx(player_data):
    best = []
    for score in player_data:
        id = score['song_id']
        music_type = type_map.get(score['type'])
        if music_type == 'dx':
            id-=10000
        song_name = score['title']
        level = score['level']
        level_index = score['level_index']
        achievements = score['achievements']
        fc = score['fc'] if score['fc'] != "" else None
        fs = score['fs'] if score['fs'] != "" else None
        dx_score = score['dxScore']
        dx_rating = score['ra']
        rate = score['rate']
        best.append({
            "id": id,
            "song_name": song_name,
            "level": level,
            "level_index": level_index,
            "achievements": achievements,
            "fc": fc,
            "fs": fs,
            "dx_score": dx_score,
            "dx_rating": dx_rating,
            "rate": rate,
            "type": music_type
        })
    return best

def image_to_base64(img, format='PNG'):
    output_buffer = BytesIO()
    img.save(output_buffer, format)
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str

def filter_all_perfect_records(records):
    b15_all_perfect_records = []
    b35_all_perfect_records = []
    for item in records:
      if item['fc'] in ['ap', 'app']:
        if total_list.by_id(str(item['song_id'])).version == NOW_VERSION:
            b15_all_perfect_records.append(item)
        else:
            b35_all_perfect_records.append(item)

    b35_sorted_data = sorted(b35_all_perfect_records,
                             key=lambda x: x['ra'], reverse=True)
    b15_sorted_data = sorted(b15_all_perfect_records,
                             key=lambda x: x['ra'], reverse=True)
    return b35_sorted_data[:35], b15_sorted_data[:15]
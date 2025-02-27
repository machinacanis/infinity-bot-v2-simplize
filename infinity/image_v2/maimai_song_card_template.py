import os
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from .utils import get_maimai_shortest_song_id, generate_maimai_filename, sans_35_font, sans_15_font, ntlgpro_B, \
    ntlgpro_EB, draw_centered_text, sans_15_font_28, sans_37_font, ntlgpro_B_18, draw_wrapped_text, sans_35_font_28, \
    sans_17_font, ntlgpro_EB_48
from .. import connection


async def maimai_song_card_img(song_id: int) -> BytesIO | None:
    """
    根据歌曲ID获取歌曲信息图片
    :param song_id: 歌曲ID
    :return: 歌曲信息
    """
    # 查找缓存中是否包含该歌曲的图片缓存，如果有则直接返回
    if os.path.exists(f"./cache/maimai_song_{song_id}.png"):
        with open(f"./cache/maimai_song_{song_id}.png", "rb") as f:
            return BytesIO(f.read())

    # 没有缓存则开始生成图片
    # 首先通过数据库获取这首曲目的完整信息
    song = await connection.query_maimai_song_by_id(get_maimai_shortest_song_id(song_id) if song_id <= 100000 else song_id)
    print(song)
    # 判断是否获取到了歌曲信息
    if song is None:
        return None
    # 判断谱面类型
    is_dx = False
    is_remaster = False
    is_utage = False
    if song.version >= 20000:  # 大于20000为DX及以上版本
        is_dx = True
    # 判断是否存在白谱
    if is_dx:
        if len(song.dx_charts) == 5:
            is_remaster = True
    else:
        if len(song.sd_charts) == 5:
            is_remaster = True
    # 判断是否为宴谱
    if song_id >= 100000:
        is_utage = True

    if not is_utage:
        # 根据是否包含白谱来选择不同的图片模板
        cover = Image.open(f"./assets/cover/mai/{generate_maimai_filename(get_maimai_shortest_song_id(song_id))}")
        cover = cover.resize((300, 300))
        badge = Image.open(f"./assets/img/{'id-deluxe' if is_dx else 'id-standard'}.png").convert("RGBA")
        badge = badge.resize((90, 30))
        if is_remaster:
            tp = Image.open("./assets/img/mai-id-5.png")
        else:
            tp = Image.open("./assets/img/mai-id-4.png")
        draw = ImageDraw.Draw(tp)
        tp.paste(cover, (130, 130))
        tp.paste(badge, (133, 400), badge)
        draw.text((460, 140), song.title, font=sans_35_font, fill="#1E3663")
        draw.text((460, 265), song.artist, font=sans_15_font, fill="#1E3663")
        draw.text((460, 395), f"ID {song_id}          {song.genre_cn}          BPM: {song.bpm}", font=sans_17_font,
                  fill="#1E3663")
        # 开始绘制谱面数据信息
        charts = song.dx_charts if is_dx else song.sd_charts
        draw_centered_text(draw, f"{charts[0].level} ({charts[0].level_value:.1f})", (181, 668), ntlgpro_B, "#FFFFFF")
        draw_centered_text(draw, f"{charts[1].level} ({charts[1].level_value:.1f})", (181, 748), ntlgpro_B, "#FFFFFF")
        draw_centered_text(draw, f"{charts[2].level} ({charts[2].level_value:.1f})", (181, 828), ntlgpro_B, "#FFFFFF")
        draw_centered_text(draw, f"{charts[3].level} ({charts[3].level_value:.1f})", (181, 908), ntlgpro_B, "#FFFFFF")
        if is_remaster:
            draw_centered_text(draw, f"{charts[4].level} ({charts[4].level_value:.1f})", (181, 1008), ntlgpro_B,
                               "#C346E7")

        # 绘制TOTAL列
        draw_centered_text(draw, str(charts[0].notes.total), (370, 655), ntlgpro_EB, "#1E3663")
        draw_centered_text(draw, str(charts[1].notes.total), (370, 735), ntlgpro_EB, "#1E3663")
        draw_centered_text(draw, str(charts[2].notes.total), (370, 815), ntlgpro_EB, "#1E3663")
        draw_centered_text(draw, str(charts[3].notes.total), (370, 895), ntlgpro_EB, "#1E3663")
        if is_remaster:
            draw_centered_text(draw, str(charts[4].notes.total), (370, 995), ntlgpro_EB, "#1E3663")

        # 绘制TAP列
        draw_centered_text(draw, str(charts[0].notes.taps), (550, 655), ntlgpro_B, "#1E3663")
        draw_centered_text(draw, str(charts[1].notes.taps), (550, 735), ntlgpro_B, "#1E3663")
        draw_centered_text(draw, str(charts[2].notes.taps), (550, 815), ntlgpro_B, "#1E3663")
        draw_centered_text(draw, str(charts[3].notes.taps), (550, 895), ntlgpro_B, "#1E3663")
        if is_remaster:
            draw_centered_text(draw, str(charts[4].notes.taps), (550, 995), ntlgpro_B, "#1E3663")

        # 绘制HOLD列
        draw_centered_text(draw, str(charts[0].notes.holds), (730, 655), ntlgpro_B, "#1E3663")
        draw_centered_text(draw, str(charts[1].notes.holds), (730, 735), ntlgpro_B, "#1E3663")
        draw_centered_text(draw, str(charts[2].notes.holds), (730, 815), ntlgpro_B, "#1E3663")
        draw_centered_text(draw, str(charts[3].notes.holds), (730, 895), ntlgpro_B, "#1E3663")
        if is_remaster:
            draw_centered_text(draw, str(charts[4].notes.holds), (730, 995), ntlgpro_B, "#1E3663")

        # 绘制SLIDE列
        draw_centered_text(draw, str(charts[0].notes.slides), (910, 655), ntlgpro_B, "#1E3663")
        draw_centered_text(draw, str(charts[1].notes.slides), (910, 735), ntlgpro_B, "#1E3663")
        draw_centered_text(draw, str(charts[2].notes.slides), (910, 815), ntlgpro_B, "#1E3663")
        draw_centered_text(draw, str(charts[3].notes.slides), (910, 895), ntlgpro_B, "#1E3663")
        if is_remaster:
            draw_centered_text(draw, str(charts[4].notes.slides), (910, 995), ntlgpro_B, "#1E3663")

        # 绘制TOUCH列
        draw_centered_text(draw, str("-" if not is_dx else str(charts[0].notes.touchs)), (1090, 655), ntlgpro_B,
                           "#1E3663")
        draw_centered_text(draw, str("-" if not is_dx else str(charts[1].notes.touchs)), (1090, 735), ntlgpro_B,
                           "#1E3663")
        draw_centered_text(draw, str("-" if not is_dx else str(charts[2].notes.touchs)), (1090, 815), ntlgpro_B,
                           "#1E3663")
        draw_centered_text(draw, str("-" if not is_dx else str(charts[3].notes.touchs)), (1090, 895), ntlgpro_B,
                           "#1E3663")
        if is_remaster:
            draw_centered_text(draw, str("-" if not is_dx else str(charts[4].notes.touchs)), (1090, 995), ntlgpro_B,
                               "#1E3663")

        # 绘制BREAK列
        draw_centered_text(draw, str(charts[0].notes.breaks), (1270, 655), ntlgpro_B, "#1E3663")
        draw_centered_text(draw, str(charts[1].notes.breaks), (1270, 735), ntlgpro_B, "#1E3663")
        draw_centered_text(draw, str(charts[2].notes.breaks), (1270, 815), ntlgpro_B, "#1E3663")
        draw_centered_text(draw, str(charts[3].notes.breaks), (1270, 895), ntlgpro_B, "#1E3663")
        if is_remaster:
            draw_centered_text(draw, str(charts[4].notes.breaks), (1270, 995), ntlgpro_B, "#1E3663")

        # 绘制谱师和版本信息
        if is_remaster:
            draw.text((300, 1118), charts[2].note_designer, font=sans_15_font_28, fill="#1E3663")
            draw.text((300, 1178), charts[3].note_designer, font=sans_15_font_28, fill="#1E3663")
            draw.text((300, 1238), charts[4].note_designer, font=sans_15_font_28, fill="#1E3663")
            draw_centered_text(draw, song.version_name, (1180, 1208), sans_37_font, "#1E3663")
        else:
            draw.text((300, 1018), charts[2].note_designer, font=sans_15_font_28, fill="#1E3663")
            draw.text((300, 1078), charts[3].note_designer, font=sans_15_font_28, fill="#1E3663")
            draw_centered_text(draw, song.version_name, (1180, 1078), sans_37_font, "#1E3663")
    else:
        cover = Image.open(f"./assets/cover/mai/{generate_maimai_filename(get_maimai_shortest_song_id(song_id))}")
        cover = cover.resize((300, 300))
        # 获取谱面的buddy数据
        is_buddy = song.utage_charts[0].is_buddy
        if is_buddy:
            tp = Image.open("./assets/img/mai-utage-2.png")
        else:
            tp = Image.open("./assets/img/mai-utage-1.png")
        draw = ImageDraw.Draw(tp)
        tp.paste(cover, (130, 180))
        draw.text((1148, 116), song.utage_charts[0].kanji, font=ntlgpro_B_18, fill="#FFFFFF")
        draw_wrapped_text(draw, song.title, (460, 190), sans_35_font, "#FFFFFF", 840)
        draw_wrapped_text(draw, song.artist, (460, 315), sans_15_font, "#FFFFFF", 840)
        draw.text((460, 445), f"ID {song_id}          {song.genre_cn}          BPM: {song.bpm}", font=sans_17_font,
                  fill="#FFFFFF")
        draw_centered_text(draw, song.utage_charts[0].description, (720, 625), sans_35_font_28, "#FFFFFF")

        # 绘制谱面数据
        # TOTAL列
        draw_centered_text(draw, str(
            song.utage_charts[0].normal_notes.total if not is_buddy else song.utage_charts[0].left_notes.total),
                           (370, 865), ntlgpro_EB, "#FFFFFF")
        if is_buddy:
            draw_centered_text(draw, str(song.utage_charts[0].right_notes.total), (370, 945), ntlgpro_EB, "#FFFFFF")

        # TAP列
        draw_centered_text(draw, str(
            song.utage_charts[0].normal_notes.taps if not is_buddy else song.utage_charts[0].left_notes.taps),
                           (550, 865), ntlgpro_B, "#FFFFFF")
        if is_buddy:
            draw_centered_text(draw, str(song.utage_charts[0].right_notes.taps), (550, 945), ntlgpro_B, "#FFFFFF")

        # HOLD列
        draw_centered_text(draw, str(
            song.utage_charts[0].normal_notes.holds if not is_buddy else song.utage_charts[0].left_notes.holds),
                           (730, 865), ntlgpro_B, "#FFFFFF")
        if is_buddy:
            draw_centered_text(draw, str(song.utage_charts[0].right_notes.holds), (730, 945), ntlgpro_B, "#FFFFFF")

        # SLIDE列
        draw_centered_text(draw, str(
            song.utage_charts[0].normal_notes.slides if not is_buddy else song.utage_charts[0].left_notes.slides),
                           (910, 865), ntlgpro_B, "#FFFFFF")
        if is_buddy:
            draw_centered_text(draw, str(song.utage_charts[0].right_notes.slides), (910, 945), ntlgpro_B, "#FFFFFF")

        # TOUCH列
        draw_centered_text(draw, str(
            song.utage_charts[0].normal_notes.slides if not is_buddy else song.utage_charts[0].left_notes.touchs),
                           (1090, 865), ntlgpro_B, "#FFFFFF")
        if is_buddy:
            draw_centered_text(draw, str(song.utage_charts[0].right_notes.touchs), (1090, 945), ntlgpro_B, "#FFFFFF")

        # BREAK列
        draw_centered_text(draw, str(
            song.utage_charts[0].normal_notes.slides if not is_buddy else song.utage_charts[0].left_notes.breaks),
                           (1270, 865), ntlgpro_B, "#FFFFFF")
        if is_buddy:
            draw_centered_text(draw, str(song.utage_charts[0].right_notes.breaks), (1270, 945), ntlgpro_B, "#FFFFFF")

        # 难度标注
        if is_buddy:
            draw_centered_text(draw, song.utage_charts[0].level, (540, 1110), ntlgpro_EB_48, "#FFFFFF")
            draw_centered_text(draw, song.version_name, (820, 1140), sans_37_font, "#FFFFFF")
        else:
            draw_centered_text(draw, song.utage_charts[0].level, (540, 1040), ntlgpro_EB_48, "#FFFFFF")
            draw_centered_text(draw, song.version_name, (820, 1070), sans_37_font, "#FFFFFF")

    # 将绘制结果存入文件缓存，以供复用
    if os.path.exists("./cache") is False:
        os.mkdir("./cache")
    tp.save(f"./cache/maimai_song_{song_id}.png")
    res_byte = BytesIO()
    tp.save(res_byte, format="PNG")
    return res_byte
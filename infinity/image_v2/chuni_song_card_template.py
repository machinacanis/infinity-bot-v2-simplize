import os
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from .utils import (
    get_maimai_shortest_song_id,
    generate_maimai_filename,
    sans_35_font,
    sans_15_font,
    ntlgpro_B,
    ntlgpro_EB,
    draw_centered_text,
    sans_15_font_28,
    sans_37_font,
    ntlgpro_B_18,
    draw_wrapped_text,
    sans_35_font_28,
    sans_17_font,
    ntlgpro_EB_48,
    generate_chunithm_filename,
)
from .. import connection


async def chunithm_song_card_img(song_id: int):
    """
    根据歌曲ID获取歌曲信息图片
    :param song_id: 歌曲ID
    :return: 歌曲信息
    """
    # 查找缓存中是否包含该歌曲的图片缓存，如果有则直接返回
    if os.path.exists(f"./cache/chunithm_song_{song_id}.png"):
        with open(f"./cache/chunithm_song_{song_id}.png", "rb") as f:
            return BytesIO(f.read())

    # 没有缓存则开始生成图片
    # 首先通过数据库获取这首曲目的完整信息
    song = await connection.query_chunithm_song_by_id(song_id)
    # 判断是否获取到了歌曲信息
    if song is None:
        return None
    # 判断谱面类型
    is_ultima = False
    is_worldend = False
    # 判断是否存在ULTIMA谱
    if len(song.charts) == 5:
        is_ultima = True
    # 判断是否为宴谱
    if song_id >= 8000:
        is_worldend = True

    if not is_worldend:
        # 根据是否包含ULTIMA谱来选择不同的图片模板
        cover = Image.open(f"./assets/cover/chu/{generate_chunithm_filename(song_id)}")
        cover = cover.resize((300, 300))
        if is_ultima:
            tp = Image.open("./assets/img/chu-id-5.png")
        else:
            tp = Image.open("./assets/img/chu-id-4.png")
        draw = ImageDraw.Draw(tp)
        tp.paste(cover, (130, 130))
        draw.text((460, 140), song.title, font=sans_35_font, fill="#1E3663")
        draw.text((460, 265), song.artist, font=sans_15_font, fill="#1E3663")
        draw.text(
            (460, 395),
            f"ID {song_id}          {song.genre}          BPM: {song.bpm}",
            font=sans_17_font,
            fill="#1E3663",
        )
        # 开始绘制谱面数据信息
        charts = song.charts
        draw_centered_text(
            draw,
            f"{charts[0].level} ({charts[0].level_value:.1f})",
            (181, 668),
            ntlgpro_B,
            "#FFFFFF",
        )
        draw_centered_text(
            draw,
            f"{charts[1].level} ({charts[1].level_value:.1f})",
            (181, 748),
            ntlgpro_B,
            "#FFFFFF",
        )
        draw_centered_text(
            draw,
            f"{charts[2].level} ({charts[2].level_value:.1f})",
            (181, 828),
            ntlgpro_B,
            "#FFFFFF",
        )
        draw_centered_text(
            draw,
            f"{charts[3].level} ({charts[3].level_value:.1f})",
            (181, 908),
            ntlgpro_B,
            "#FFFFFF",
        )
        if is_ultima:
            draw_centered_text(
                draw,
                f"{charts[4].level} ({charts[4].level_value:.1f})",
                (181, 1008),
                ntlgpro_B,
                "#FFFFFF",
            )

        # 绘制TOTAL列
        draw_centered_text(
            draw, str(charts[0].notes.total), (370, 655), ntlgpro_EB, "#1E3663"
        )
        draw_centered_text(
            draw, str(charts[1].notes.total), (370, 735), ntlgpro_EB, "#1E3663"
        )
        draw_centered_text(
            draw, str(charts[2].notes.total), (370, 815), ntlgpro_EB, "#1E3663"
        )
        draw_centered_text(
            draw, str(charts[3].notes.total), (370, 895), ntlgpro_EB, "#1E3663"
        )
        if is_ultima:
            draw_centered_text(
                draw, str(charts[4].notes.total), (370, 995), ntlgpro_EB, "#1E3663"
            )

        # 绘制TAP列
        draw_centered_text(
            draw, str(charts[0].notes.taps), (550, 655), ntlgpro_B, "#1E3663"
        )
        draw_centered_text(
            draw, str(charts[1].notes.taps), (550, 735), ntlgpro_B, "#1E3663"
        )
        draw_centered_text(
            draw, str(charts[2].notes.taps), (550, 815), ntlgpro_B, "#1E3663"
        )
        draw_centered_text(
            draw, str(charts[3].notes.taps), (550, 895), ntlgpro_B, "#1E3663"
        )
        if is_ultima:
            draw_centered_text(
                draw, str(charts[4].notes.taps), (550, 995), ntlgpro_B, "#1E3663"
            )

        # 绘制HOLD列
        draw_centered_text(
            draw, str(charts[0].notes.holds), (730, 655), ntlgpro_B, "#1E3663"
        )
        draw_centered_text(
            draw, str(charts[1].notes.holds), (730, 735), ntlgpro_B, "#1E3663"
        )
        draw_centered_text(
            draw, str(charts[2].notes.holds), (730, 815), ntlgpro_B, "#1E3663"
        )
        draw_centered_text(
            draw, str(charts[3].notes.holds), (730, 895), ntlgpro_B, "#1E3663"
        )
        if is_ultima:
            draw_centered_text(
                draw, str(charts[4].notes.holds), (730, 995), ntlgpro_B, "#1E3663"
            )

        # 绘制SLIDE列
        draw_centered_text(
            draw, str(charts[0].notes.slides), (910, 655), ntlgpro_B, "#1E3663"
        )
        draw_centered_text(
            draw, str(charts[1].notes.slides), (910, 735), ntlgpro_B, "#1E3663"
        )
        draw_centered_text(
            draw, str(charts[2].notes.slides), (910, 815), ntlgpro_B, "#1E3663"
        )
        draw_centered_text(
            draw, str(charts[3].notes.slides), (910, 895), ntlgpro_B, "#1E3663"
        )
        if is_ultima:
            draw_centered_text(
                draw, str(charts[4].notes.slides), (910, 995), ntlgpro_B, "#1E3663"
            )

        # 绘制Air列
        draw_centered_text(
            draw, str(charts[0].notes.airs), (1090, 655), ntlgpro_B, "#1E3663"
        )
        draw_centered_text(
            draw, str(charts[1].notes.airs), (1090, 735), ntlgpro_B, "#1E3663"
        )
        draw_centered_text(
            draw, str(charts[2].notes.airs), (1090, 815), ntlgpro_B, "#1E3663"
        )
        draw_centered_text(
            draw, str(charts[3].notes.airs), (1090, 895), ntlgpro_B, "#1E3663"
        )
        if is_ultima:
            draw_centered_text(
                draw, str(charts[4].notes.airs), (1090, 995), ntlgpro_B, "#1E3663"
            )

        # 绘制Flick列
        draw_centered_text(
            draw, str(charts[0].notes.flicks), (1270, 655), ntlgpro_B, "#1E3663"
        )
        draw_centered_text(
            draw, str(charts[1].notes.flicks), (1270, 735), ntlgpro_B, "#1E3663"
        )
        draw_centered_text(
            draw, str(charts[2].notes.flicks), (1270, 815), ntlgpro_B, "#1E3663"
        )
        draw_centered_text(
            draw, str(charts[3].notes.flicks), (1270, 895), ntlgpro_B, "#1E3663"
        )
        if is_ultima:
            draw_centered_text(
                draw, str(charts[4].notes.flicks), (1270, 995), ntlgpro_B, "#1E3663"
            )

        # 绘制谱师和版本信息
        if is_ultima:
            draw.text(
                (300, 1118),
                charts[2].note_designer,
                font=sans_15_font_28,
                fill="#1E3663",
            )
            draw.text(
                (300, 1178),
                charts[3].note_designer,
                font=sans_15_font_28,
                fill="#1E3663",
            )
            draw.text(
                (300, 1238),
                charts[4].note_designer,
                font=sans_15_font_28,
                fill="#1E3663",
            )
            draw_centered_text(
                draw, song.version_name, (1180, 1208), sans_37_font, "#1E3663"
            )
        else:
            draw.text(
                (300, 1018),
                charts[2].note_designer,
                font=sans_15_font_28,
                fill="#1E3663",
            )
            draw.text(
                (300, 1078),
                charts[3].note_designer,
                font=sans_15_font_28,
                fill="#1E3663",
            )
            draw_centered_text(
                draw, song.version_name, (1180, 1078), sans_37_font, "#1E3663"
            )
    else:
        # worldend谱面
        cover = Image.open(
            f"./assets/cover/chuwe/{generate_chunithm_filename(song_id)}"
        )
        cover = cover.resize((300, 300))
        tp = Image.open("./assets/img/chu-id-we.png")
        draw = ImageDraw.Draw(tp)
        tp.paste(cover, (130, 130))
        draw_wrapped_text(draw, song.title, (460, 140), sans_35_font, "#1E3663", 840)
        draw_wrapped_text(draw, song.artist, (460, 265), sans_15_font, "#1E3663", 840)
        draw.text(
            (460, 395),
            f"ID {song_id}          {song.genre}          BPM: {song.bpm}",
            font=sans_17_font,
            fill="#1E3663",
        )

        # 歌曲信息
        draw_centered_text(
            draw,
            f"{song.charts[0].kanji} ☆{song.charts[0].star}",
            (181, 668),
            ntlgpro_B,
            "#FFFFFF",
        )

        # 绘制谱面数据
        # TOTAL列
        draw_centered_text(
            draw, str(song.charts[0].notes.total), (370, 655), ntlgpro_EB, "#1E3663"
        )
        # TAP列
        draw_centered_text(
            draw, str(song.charts[0].notes.taps), (550, 655), ntlgpro_B, "#1E3663"
        )

        # HOLD列
        draw_centered_text(
            draw, str(song.charts[0].notes.holds), (730, 655), ntlgpro_B, "#1E3663"
        )

        # SLIDE列
        draw_centered_text(
            draw, str(song.charts[0].notes.slides), (910, 655), ntlgpro_B, "#1E3663"
        )

        # Air列
        draw_centered_text(
            draw, str(song.charts[0].notes.airs), (1090, 655), ntlgpro_B, "#1E3663"
        )

        # Flick列
        draw_centered_text(
            draw, str(song.charts[0].notes.flicks), (1270, 655), ntlgpro_B, "#1E3663"
        )

        # 谱面作者
        draw_wrapped_text(
            draw,
            song.charts[0].note_designer,
            (300, 780),
            sans_15_font_28,
            "#1E3663",
            1035,
        )

    # 将绘制结果存入文件缓存，以供复用
    if os.path.exists("./cache") is False:
        os.mkdir("./cache")
    tp.save(f"./cache/chunithm_song_{song_id}.png")
    res_byte = BytesIO()
    tp.save(res_byte, format="PNG")
    return res_byte

from dataclasses import dataclass
from typing import List, Union

# 版本信息
versions = [
    {"id": 0, "title": "CHUNITHM", "version": 10000},
    {"id": 1, "title": "CHUNITHM PLUS", "version": 10500},
    {"id": 2, "title": "AIR", "version": 11000},
    {"id": 3, "title": "AIR PLUS", "version": 11500},
    {"id": 4, "title": "STAR", "version": 12000},
    {"id": 5, "title": "STAR PLUS", "version": 12500},
    {"id": 6, "title": "AMAZON", "version": 13000},
    {"id": 7, "title": "AMAZON PLUS", "version": 13500},
    {"id": 8, "title": "CRYSTAL", "version": 14000},
    {"id": 9, "title": "CRYSTAL PLUS", "version": 14500},
    {"id": 10, "title": "PARADISE", "version": 15000},
    {"id": 11, "title": "PARADISE LOST", "version": 15500},
    {"id": 12, "title": "NEW", "version": 20000},
    {"id": 13, "title": "NEW PLUS", "version": 20500},
    {"id": 14, "title": "SUN", "version": 21000},
    {"id": 15, "title": "SUN PLUS", "version": 21500},
    {"id": 16, "title": "LUMINOUS", "version": 22000},
    {"id": 17, "title": "LUMINOUS PLUS", "version": 22500},
]

version_dict = {version["version"]: version["title"] for version in versions}


def return_ver_name(song_version: int) -> str:
    for version in versions:
        if version["version"] == song_version:
            return version["title"]


@dataclass
class Notes:
    total: int
    taps: int
    holds: int
    slides: int
    airs: int
    flicks: int

    def to_dict(self):
        return {
            "total": self.total,
            "tap": self.taps,
            "hold": self.holds,
            "slide": self.slides,
            "air": self.airs,
            "flick": self.flicks,
        }

    @staticmethod
    def from_dict(data: dict) -> "Notes":
        return Notes(
            total=data.get("total", 0),
            taps=data.get("tap", 0),
            holds=data.get("hold", 0),
            slides=data.get("slide", 0),
            airs=data.get("air", 0),
            flicks=data.get("flick", 0),
        )


# 常规谱面数据类
@dataclass
class ChuniChartData:
    difficulty: int
    level: str
    level_value: float
    note_designer: str
    version: int
    origin_id: int
    kanji: str
    star: int
    notes: Notes

    def to_dict(self):
        return {
            "difficulty": self.difficulty,
            "level": self.level,
            "level_value": self.level_value,
            "note_designer": self.note_designer,
            "version": self.version,
            "origin_id": self.origin_id,
            "kanji": self.kanji,
            "star": self.star,
            "notes": self.notes.to_dict(),
        }

    @staticmethod
    def from_dict(data: dict) -> "ChuniChartData":
        return ChuniChartData(
            difficulty=data.get("difficulty", 0),
            level=data.get("level", ""),
            level_value=data.get("level_value", 0),
            note_designer=data.get("note_designer", ""),
            version=data.get("version", 0),
            origin_id=data.get("origin_id", 0),
            kanji=data.get("kanji", ""),
            star=data.get("star", 0),
            notes=Notes.from_dict(data.get("notes", {})),
        )


# 特殊谱面 WORLDEND 类型
@dataclass
class ChuniWorldEndChartData:
    difficulty: int
    level: str
    level_value: float
    note_designer: str
    version: int
    origin_id: int
    kanji: str
    star: int
    notes: Notes
    worldend_specific_field: str  # 特殊字段

    def to_dict(self):
        return {
            "difficulty": self.difficulty,
            "level": self.level,
            "level_value": self.level_value,
            "note_designer": self.note_designer,
            "version": self.version,
            "origin_id": self.origin_id,
            "kanji": self.kanji,
            "star": self.star,
            "notes": self.notes.to_dict(),
            "worldend_specific_field": self.worldend_specific_field,
        }

    @staticmethod
    def from_dict(data: dict) -> "ChuniWorldEndChartData":
        return ChuniWorldEndChartData(
            difficulty=data.get("difficulty", 0),
            level=data.get("level", ""),
            level_value=data.get("level_value", 0),
            note_designer=data.get("note_designer", ""),
            version=data.get("version", 0),
            origin_id=data.get("origin_id", 0),
            kanji=data.get("kanji", ""),
            star=data.get("star", 0),
            notes=Notes.from_dict(data.get("notes", {})),
            worldend_specific_field=data.get("worldend_specific_field", ""),
        )


# 主歌单数据类
@dataclass
class ChuniSongData:
    id: int
    title: str
    artist: str
    genre: str
    bpm: int
    version: int
    version_name: str
    rights: str
    charts: List[
        Union[ChuniChartData, ChuniWorldEndChartData]
    ]  # 允许普通和特殊谱面共存

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "genre": self.genre,
            "bpm": self.bpm,
            "version": self.version,
            "version_name": return_ver_name(self.version),
            "rights": self.rights,
            "charts": [chart.to_dict() for chart in self.charts],
        }

    @staticmethod
    def from_dict(data: dict) -> "ChuniSongData":
        charts = []
        for chart in data.get("charts", []):
            if chart.get("worldend_specific_field"):  # 判断是否是WORLDEND类型
                charts.append(ChuniWorldEndChartData.from_dict(chart))
            else:
                charts.append(ChuniChartData.from_dict(chart))
        return ChuniSongData(
            id=data.get("id", 0),
            title=data.get("title", ""),
            artist=data.get("artist", ""),
            genre=data.get("genre", ""),
            bpm=data.get("bpm", 0),
            version=data.get("version", 0),
            version_name=return_ver_name(data.get("version", 0)),
            rights=data.get("rights", ""),
            charts=charts,
        )


# 创建谱面数据的函数，区分普通谱面和WORLDEND谱面
def create_chuni_chart_data(data):
    if data.get("worldend_specific_field"):  # 如果是WORLDEND类型
        return ChuniWorldEndChartData(
            difficulty=int(data.get("difficulty", 0)),
            level=data.get("level", ""),
            level_value=data.get("level_value", 0.0),
            note_designer=data.get("note_designer", ""),
            version=data.get("version", 0),
            origin_id=data.get("origin_id", 0),
            kanji=data.get("kanji", ""),
            star=data.get("star", 0),
            notes=Notes.from_dict(data.get("notes", {})),
            worldend_specific_field=data.get("worldend_specific_field", ""),
        )
    else:  # 常规谱面
        return ChuniChartData(
            difficulty=int(data.get("difficulty", 0)),
            level=data.get("level", ""),
            level_value=data.get("level_value", 0.0),
            note_designer=data.get("note_designer", ""),
            version=data.get("version", 0),
            origin_id=data.get("origin_id", 0),
            kanji=data.get("kanji", ""),
            star=data.get("star", 0),
            notes=Notes.from_dict(data.get("notes", {})),
        )


# 创建歌曲数据的函数
def create_chuni_song_data(json_data: list[dict]) -> list[ChuniSongData]:
    songs = []

    for song in json_data:
        charts = []

        for chart in song.get("difficulties", []):
            charts.append(create_chuni_chart_data(chart))

        song_data = ChuniSongData(
            id=song.get("id", 0),
            title=song.get("title", ""),
            artist=song.get("artist", ""),
            genre=song.get("genre", ""),
            bpm=song.get("bpm", 0),
            version=song.get("version", 0),
            version_name=return_ver_name(song.get("version", 0)),
            rights=song.get("rights", ""),
            charts=charts,
        )
        songs.append(song_data)

    return songs


class ChuniDifficulty:
    difficult: int = -1

    def __init__(self, diffculty: int | str):
        if isinstance(diffculty, str):
            match diffculty:
                case "BASIC":
                    self.difficult = 0
                case "ADVANCED":
                    self.difficult = 1
                case "EXPERT":
                    self.difficult = 2
                case "MASTER":
                    self.difficult = 3
                case "REMASTER":
                    self.difficult = 4
                case "ALTIMA":
                    self.difficult = 4
                case "Basic":
                    self.difficult = 0
                case "Advanced":
                    self.difficult = 1
                case "Expert":
                    self.difficult = 2
                case "Master":
                    self.difficult = 3
                case "Altima":
                    self.difficult = 4
                case "basic":
                    self.difficult = 0
                case "advanced":
                    self.difficult = 1
                case "expert":
                    self.difficult = 2
                case "master":
                    self.difficult = 3
                case "altima":
                    self.difficult = 4
                case "绿":
                    self.difficult = 0
                case "黄":
                    self.difficult = 1
                case "红":
                    self.difficult = 2
                case "紫":
                    self.difficult = 3
                case "黑":
                    self.difficult = 4
                case _:
                    self.difficult = -1
        elif isinstance(diffculty, int):
            if diffculty < 0 or diffculty > 4:
                self.difficult = -1
            self.difficult = diffculty

    def __str__(self):
        match self.difficult:
            case 0:
                return "BASIC"
            case 1:
                return "ADVANCED"
            case 2:
                return "EXPERT"
            case 3:
                return "MASTER"
            case 4:
                return "ALTIMA"
            case -1:
                return "UNKNOWN"

    def __int__(self):
        return self.difficult

    def str(self):
        return str(self)

    def int(self):
        return int(self)

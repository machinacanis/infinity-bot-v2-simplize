from dataclasses import dataclass
from typing import List

# 定义字典
genre_dict = {"maimai": "舞萌", "オンゲキCHUNITHM": "音击/中二节奏", "ゲームバラエティ": "其他游戏",
              "東方Project": "东方Project", "niconicoボーカロイド": "niconico＆VOCALOID™", "POPSアニメ": "流行&动漫",
              "宴会場": "宴会场"}

version_dict = {24000: "舞萌DX 2024", 23000: "舞萌DX 2023", 22000: "舞萌DX 2022", 21000: "舞萌DX 2021", 20000: "舞萌DX",
                19900: "FiNALE", 19500: "MiLK PLUS", 19000: "MiLK"
    , 18500: "MURASAKi PLUS", 18000: "MURASAKi", 17000: "PiNK PLUS", 16000: "PiNK", 15000: "ORANGE PLUS",
                14000: "ORANGE", 13000: "GreeN PLUS"
    , 12000: "GreeN", 11000: "maimai PLUS", 10000: "maimai"}


def return_ver_name(song_version: int) -> str:
    for target_version in version_dict.keys():
        if target_version <= song_version:
            return version_dict[target_version]
    return "NoneVersion"


@dataclass
class Notes:
    total: int
    taps: int
    holds: int
    slides: int
    touchs: int
    breaks: int
    
    def to_dict(self):
        return {
            "total": self.total,
            "taps": self.taps,
            "holds": self.holds,
            "slides": self.slides,
            "touchs": self.touchs,
            "breaks": self.breaks
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Notes':
        return Notes(
            total=data.get('total', 0),
            taps=data.get('taps', 0),
            holds=data.get('holds', 0),
            slides=data.get('slides', 0),
            touchs=data.get('touchs', 0),
            breaks=data.get('breaks', 0)
        )


@dataclass
class MaimaiChartData:
    type: str
    difficulty: int
    level: str
    level_value: float
    note_designer: str
    version: int
    version_name: str
    notes: Notes
    
    def to_dict(self):
        return {
            "type": self.type,
            "difficulty": self.difficulty,
            "level": self.level,
            "level_value": self.level_value,
            "note_designer": self.note_designer,
            "version": self.version,
            "version_name": self.version_name,
            "notes": self.notes.to_dict()
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'MaimaiChartData':
        return MaimaiChartData(
            type=data.get('type', ''),
            difficulty=data.get('difficulty', 0),
            level=data.get('level', ''),
            level_value=data.get('level_value', 0.0),
            note_designer=data.get('note_designer', ''),
            version=data.get('version', 0),
            version_name=data.get('version_name', ''),
            notes=Notes.from_dict(data.get('notes', {}))
        )


@dataclass
class UtageChartData:
    type: str
    difficulty: int
    level: str
    level_value: float
    note_designer: str
    version: int
    version_name: str
    kanji: str
    description: str
    is_buddy: bool
    normal_notes: Notes
    left_notes: Notes = None  # 默认为 None
    right_notes: Notes = None  # 默认为 None
    
    def to_dict(self):
        data = {
            "type": self.type,
            "difficulty": self.difficulty,
            "level": self.level,
            "level_value": self.level_value,
            "note_designer": self.note_designer,
            "version": self.version,
            "version_name": self.version_name,
            "kanji": self.kanji,
            "description": self.description,
            "is_buddy": self.is_buddy,
            "normal_notes": self.normal_notes.to_dict()
        }
        
        if self.is_buddy:
            # 如果是 buddy 类型，将 left 和 right 的音符数据也存储
            data["left_notes"] = self.left_notes.to_dict() if self.left_notes else None
            data["right_notes"] = self.right_notes.to_dict() if self.right_notes else None
        
        return data
    
    @staticmethod
    def from_dict(data: dict) -> 'UtageChartData':
        normal_notes = Notes.from_dict(data.get('normal_notes', {}))
        left_notes = Notes.from_dict(data.get('left_notes', {})) if 'left_notes' in data else None
        right_notes = Notes.from_dict(data.get('right_notes', {})) if 'right_notes' in data else None
        
        return UtageChartData(
            type=data.get('type', ''),
            difficulty=data.get('difficulty', 0),
            level=data.get('level', ''),
            level_value=data.get('level_value', 0.0),
            note_designer=data.get('note_designer', ''),
            version=data.get('version', 0),
            version_name=return_ver_name(data.get('version', 0)),
            kanji=data.get('kanji', ''),
            description=data.get('description', ''),
            is_buddy=data.get('is_buddy', False),
            normal_notes=normal_notes,
            left_notes=left_notes,
            right_notes=right_notes
        )


@dataclass
class MaimaiSongData:
    id: int
    title: str
    artist: str
    genre_jp: str
    genre_cn: str
    bpm: int
    version: int
    version_name: str
    rights: str
    sd_charts: List[MaimaiChartData]
    dx_charts: List[MaimaiChartData]
    utage_charts: List[UtageChartData]
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "genre_jp": self.genre_jp,
            "genre_cn": self.genre_cn,
            "bpm": self.bpm,
            "version": self.version,
            "version_name": self.version_name,
            "rights": self.rights,
            "sd_charts": [chart.to_dict() for chart in self.sd_charts],
            "dx_chart": [chart.to_dict() for chart in self.dx_charts],
            "utage_chart": [chart.to_dict() for chart in self.utage_charts]
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'MaimaiSongData':
        # 从字典中构造 MaimaiSongData 实例
        sd_charts = [MaimaiChartData.from_dict(chart) for chart in data.get('sd_charts', [])]
        dx_charts = [MaimaiChartData.from_dict(chart) for chart in data.get('dx_chart', [])]
        utage_charts = [UtageChartData.from_dict(chart) for chart in data.get('utage_chart', [])]
        
        return MaimaiSongData(
            id=data.get('id', 0),
            title=data.get('title', ''),
            artist=data.get('artist', ''),
            genre_jp=data.get('genre_jp', ''),
            genre_cn=genre_dict.get(data.get('genre_jp', ''), ''),
            bpm=data.get('bpm', 0),
            version=data.get('version', 0),
            version_name=return_ver_name(data.get('version', 0)),
            rights=data.get('rights', ''),
            sd_charts=sd_charts,
            dx_charts=dx_charts,
            utage_charts=utage_charts
        )


def create_notes(data):
    return Notes(
        total=data.get('total', 0),
        taps=data.get('tap', 0),
        holds=data.get('hold', 0),
        slides=data.get('slide', 0),
        touchs=data.get('touch', 0),
        breaks=data.get('break', 0)
    )


def create_maimai_chart_data(data, type_str):
    return MaimaiChartData(
        type=type_str,
        difficulty=int(data.get('difficulty', 0)),
        level=data.get('level', ''),
        level_value=data.get('level_value', 0),
        note_designer=data.get('note_designer', ''),
        version=data.get('version', 0),
        version_name=return_ver_name(data.get('version', 0)),
        notes=create_notes(data.get('notes', {}))
    )


def create_utage_chart_data(data, type_str):
    normal_notes = create_notes(data.get('notes', {}))
    left_notes = create_notes(data.get('notes', {}).get('left', {})) if 'left' in data.get('notes', {}) else None
    right_notes = create_notes(data.get('notes', {}).get('right', {})) if 'right' in data.get('notes', {}) else None
    
    return UtageChartData(
        type=type_str,
        difficulty=int(data.get('difficulty', 0)),
        level=data.get('level', ''),
        level_value=data.get('level_value', 0),
        note_designer=data.get('note_designer', ''),
        version=data.get('version', 0),
        version_name=return_ver_name(data.get('version', 0)),
        kanji=data.get('kanji', ''),
        description=data.get('description', ''),
        is_buddy=data.get('is_buddy', False),
        normal_notes=normal_notes,
        left_notes=left_notes,
        right_notes=right_notes
    )


def create_maimai_song_data(json_data: list[dict]) -> list[MaimaiSongData]:
    songs = []
    
    for song in json_data:
        # 为每首歌准备相关的难度数据
        sd_charts = []
        dx_charts = []
        utage_charts = []
        
        for difficulty in song.get('difficulties', {}).get('standard', []):
            sd_charts.append(create_maimai_chart_data(difficulty, 'standard'))
        
        for difficulty in song.get('difficulties', {}).get('dx', []):
            dx_charts.append(create_maimai_chart_data(difficulty, 'dx'))
        
        for difficulty in song.get('difficulties', {}).get('utage', []):
            utage_charts.append(create_utage_chart_data(difficulty, 'utage'))
        
        song_data = MaimaiSongData(
            id=song.get('id', 0),
            title=song.get('title', ''),
            artist=song.get('artist', ''),
            genre_jp=song.get('genre', ''),
            genre_cn=genre_dict.get(song.get('genre', '')),
            bpm=song.get('bpm', 0),
            version=song.get('version', 0),
            version_name=return_ver_name(song.get('version', 0)),
            rights=song.get('rights', ''),
            sd_charts=sd_charts,
            dx_charts=dx_charts,
            utage_charts=utage_charts
        )
        songs.append(song_data)
    
    return songs

class MaiDifficulty:
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
                case "RE:MASTER":
                    self.difficult = 4
                case "Basic":
                    self.difficult = 0
                case "Advanced":
                    self.difficult = 1
                case "Expert":
                    self.difficult = 2
                case "Master":
                    self.difficult = 3
                case "Remaster":
                    self.difficult = 4
                case "Re:Master":
                    self.difficult = 4
                case "basic":
                    self.difficult = 0
                case "advanced":
                    self.difficult = 1
                case "expert":
                    self.difficult = 2
                case "master":
                    self.difficult = 3
                case "remaster":
                    self.difficult = 4
                case "re:master":
                    self.difficult = 4
                case "绿":
                    self.difficult = 0
                case "黄":
                    self.difficult = 1
                case "红":
                    self.difficult = 2
                case "紫":
                    self.difficult = 3
                case "白":
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
                return "RE:MASTER"
            case -1:
                return "UNKNOWN"

    def __int__(self):
        return self.difficult

    def str(self):
        return str(self)

    def int(self):
        return int(self)

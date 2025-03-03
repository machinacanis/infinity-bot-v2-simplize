import infinity
from infinity.model.chunithm_song import ChuniDifficulty


def svdxin_version(version: int | ChuniDifficulty) -> int:
    if isinstance(version, ChuniDifficulty):
        version = version.int
    # 对版本号进行除二并取整，然后加一，得到sdvx.in网站使用的版本号格式
    version = (version // 2) + 1
    return version


class SDVXinClient:
    uri = infinity.sdvxin_api

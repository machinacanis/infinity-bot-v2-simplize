class MaiVersion:
    def __init__(self, version: str):
        full_name, kanji = self._get_full_version_name(version)
        self.version = full_name
        self.kanji = kanji

    @staticmethod
    def _get_full_version_name(version: str):
        if version in ["maimaiplus", "真", "真代", "真极", "真神", "真将", "真舞舞"]:
            return "maimai PLUS", "真"
        elif version in ["maimaigreen", "超", "超代", "超极", "超神", "超将", "超舞舞"]:
            return "maimai GREEN", "超"
        elif version in ["maimaigreenplus", "檄", "檄代", "檄极", "檄神", "檄将", "檄舞舞"]:
            return "maimai GREEN PLUS", "檄"
        elif version in ["maimaiorange", "橙", "橙代", "橙极", "橙神", "橙将", "橙舞舞"]:
            return "maimai ORANGE", "橙"
        elif version in ["maimaiorangeplus", "晓", "暁", "晓代", "暁代", "晓极", "暁极", "晓神", "暁神", "晓将", "暁将", "晓舞舞", "暁舞舞"]:
            return "maimai ORANGE PLUS", "晓"
        elif version in ["maimaipink", "桃", "桃代", "桃极", "桃神", "桃将", "桃舞舞"]:
            return "maimai PINK", "桃"
        elif version in ["maimaipinkplus", "樱", "櫻", "樱代", "櫻代", "樱极", "櫻极", "樱神", "櫻神", "樱将", "櫻将", "樱舞舞", "櫻舞舞"]:
            return "maimai PINK PLUS", "樱"
        elif version in ["maimaimurasaki", "紫", "紫代", "紫极", "紫神", "紫将", "紫舞舞"]:
            return "maimai MURASAKI", "紫"
        elif version in ["maimaimurasakiplus", "堇", "菫", "堇代", "菫代", "堇极", "菫极", "堇神", "菫神", "堇将", "菫将", "堇舞舞", "菫舞舞"]:
            return "maimai MURASAKI PLUS", "堇"
        elif version in ["maimaimilk", "白", "白代", "白极", "白神", "白将", "白舞舞"]:
            return "maimai MILK", "白"
        elif version in ["milkplus", "雪", "雪代", "雪极", "雪神", "雪将", "雪舞舞"]:
            return "MiLK PLUS", "雪"
        elif version in ["maimaifinale", "辉", "輝", "辉代", "輝代", "辉极", "輝极", "辉神", "輝神", "辉将", "輝将", "辉舞舞", "輝舞舞"]:
            return "maimai FiNALE", "辉"
        elif version in ["allfinale", "舞", "霸", "霸者", "舞极", "舞神", "舞将", "舞舞舞"]:
            return "ALL FiNALE", "舞"
        elif version in ["dx", "熊", "DX", "熊代", "无印", "熊极", "熊神", "熊将", "熊舞舞"]:
            return "maimai でらっくす", "熊"
        elif version in ["dxplus", "华", "華", "华代", "華代", "华极", "華极", "华神", "華神", "华将", "華将", "华舞舞", "華舞舞"]:
            return "maimai でらっくす PLUS", "华"
        elif version in ["splash", "爽", "爽代", "爽极", "爽神", "爽将", "爽舞舞"]:
            return "maimai でらっくす Splash", "爽"
        elif version in ["splashplus", "煌", "煌代", "煌极", "煌神", "煌将", "煌舞舞"]:
            return "maimai でらっくす Splash PLUS", "煌"
        elif version in ["universe", "宙", "宙代", "宙极", "宙神", "宙将", "宙舞舞"]:
            return "maimai でらっくす UNiVERSE", "宙"
        elif version in ["universeplus", "星", "星代", "星极", "星神", "星将", "星舞舞"]:
            return "maimai でらっくす UNiVERSE PLUS", "星"
        elif version in ["festival", "祭", "祭代", "祭极", "祭神", "祭将", "祭舞舞"]:
            return "maimai でらっくす FESTiVAL", "祭"
        elif version in ["festivalplus", "祝", "祝代", "祝极", "祝神", "祝将", "祝舞舞"]:
            return "maimai でらっくす FESTiVAL PLUS", "祝"
        elif version in ["buddies", "双", "双代", "双极", "双神", "双将", "双舞舞"]:
            return "maimai でらっくす BUDDiES", "双"
        elif version in ["buddiesplus", "宴", "宴代", "宴极", "宴神", "宴将", "宴舞舞"]:
            return "maimai でらっくす BUDDiES PLUS", "宴"
        else:
            return "Unknown", ""
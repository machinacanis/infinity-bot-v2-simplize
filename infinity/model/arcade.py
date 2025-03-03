class ArcadeInfo:
    def __init__(self):
        # 通过初始化时不传递参数，而是通过 from_dict 方法来设置属性
        self.place_id = None
        self.machine_count = None
        self.arcade_id = None
        self.province = None
        self.arcade_name = None
        self.mall = None
        self.address = None

    @classmethod
    def from_dict(cls, data):
        """从字典数据创建 Arcade 实例并填充属性"""
        arcade = cls()
        arcade.place_id = data.get("placeId")
        arcade.machine_count = data.get("machineCount")
        arcade.arcade_id = data.get("id")
        arcade.province = data.get("province")
        arcade.arcade_name = data.get("arcadeName")
        arcade.mall = data.get("mall")
        arcade.address = data.get("address")
        return arcade

    def to_dict(self):
        """将 Arcade 实例转换为字典"""
        return {
            "placeId": self.place_id,
            "machineCount": self.machine_count,
            "id": self.arcade_id,
            "province": self.province,
            "arcadeName": self.arcade_name,
            "mall": self.mall,
            "address": self.address,
        }

import io
from io import BytesIO

from PIL.Image import Image
from PIL.ImageFile import ImageFile

# code from github.com/machinacanis/kikaiken-bot

infinity_system_message_prefix = ">>> 「Infinity Bot」 \n" # 暂时不需要这个消息内容，占个位置先
infinity_global_exception = "发生了意料之外的异常。\n请稍后重试，或联系开发者。"
infinity_result_not_found = "没有搜索到任何结果。"
infinity_need_no_paging = "共找到 %d 条结果\n%s"
infinity_need_paging = "共找到 %d 条结果，第 %d/%d 页：\n%s\n使用参数 -p [页码] 来翻页"
infinity_too_much_paged = "你翻太多页啦！总共可请求 %d 页。"
infinity_command_not_found = "指令 %s 不存在"
infinity_permission_denied = "你没有执行此操作的权限"


class InfinityUniMessage:
    """
    用于构造跨平台文本消息的存储类
    """
    def __init__(self):
        self._content = []  # 内容负载
        self._image = []  # 图片负载，一般只建议存入一张
        self._is_system_message = False  # 是否为系统消息，决定是否显示系统消息抬头，默认为False
        self.is_paged = False  # 消息是否需要分页，默认为False
        self._row_per_page = 15  # 每页显示的行数，默认为15
        self._prefix = ""  # 消息抬头，默认为空，构建时显示在消息内容上方一行，系统信息抬头下方一行
        self._suffix = ""  # 消息尾，默认为空，构建时显示在消息内容下方一行
        self._disable_content = False  # 取消内容显示，此时不会将content列表作为内容构建，一般用于保证仅显示异常信息
        self._exception = ""  # 异常信息内容
        self.permisson = 0
        self.is_reply = True
        self.status = False

    def set_system_message_flag(self):
        # 设置系统消息
        self._is_system_message = True
        return self

    def enable_paging(self):
        # 开启分页
        self.is_paged = True
        return self

    def set_row_per_page(self, row_per_page: int):
        # 设置每页显示的行数
        self._row_per_page = row_per_page
        return self

    def set_prefix(self, prefix: str):
        # 设置消息抬头
        self._prefix = prefix
        return self

    def set_suffix(self, suffix: str):
        # 设置消息尾
        self._suffix = suffix
        return self

    def set_disable_content_flag(self):
        # 取消内容显示
        self._disable_content = True
        return self

    def set_exception(self, exception: str):
        # 设置异常信息
        self._exception = exception
        return self

    def set_permission(self, permisson: int):
        # 设置权限等级
        self.permisson = permisson
        return self

    def get_content_length(self):
        # 获取内容总数
        return len(self._content)

    def get_page_count(self):
        # 获取分页数量
        return int(len(self._content) / self._row_per_page) + 1

    def get_page_start(self, page_num: int):
        # 计算每页的起始位置
        return (page_num - 1) * self._row_per_page

    def add_content(self, content: str):
        # 添加内容
        self._content.append(content)
        return self

    def add_image(self, image: BytesIO | ImageFile | Image):
        # 添加图片
        self._image.append(image)
        return self

    def shortcut_permission_denied(self):
        self.add_content(infinity_permission_denied)

    def build(self, page_num: int = 1) -> str:
        result = ""  # 新建结果字符串

        if self._is_system_message:
            result += infinity_system_message_prefix + "\n"  # 添加系统消息抬头
        if self._prefix != "":
            result += self._prefix + "\n" if not self._disable_content else self._prefix

        # 不启用分页模式，直接将内容添加到结果字符串中
        if not self._disable_content:
            if self.is_paged:
                # 计算页码是否超出范围
                if page_num > self.get_page_count():
                    result += infinity_too_much_paged % self.get_page_count()
                else:
                    # 计算内容总量
                    if self.get_content_length() == 0:
                        result += infinity_result_not_found
                    elif self.get_content_length() <= self._row_per_page:
                        result += infinity_need_no_paging % (self.get_content_length(), "\n".join(self._content))
                    elif self.get_content_length() > self._row_per_page:
                        result += infinity_need_paging % (self.get_content_length(), page_num,
                                                          self.get_page_count(), "\n".join(self._content[
                                                                                           self.get_page_start(
                                                                                               page_num):self.get_page_start(
                                                                                               page_num) + self._row_per_page]))
            else:
                for content in self._content:
                    result += content + "\n"
                # 最后一行不需要换行符，去除结尾的换行符
                result = result[:-1]


        if self._exception != "":
            result += "\n" + "异常：" + self._exception + "\n" + infinity_global_exception

        if self._suffix != "":
            result += "\n" + self._suffix

        return result

    def get_image(self, index: int = 0):
        if isinstance(self._image[index], ImageFile):
            byte_io = io.BytesIO()
            self._image[index].save(byte_io, format='PNG')
            byte_io.seek(0)
            return byte_io
        if isinstance(self._image[index], Image):
            byte_io = io.BytesIO()
            self._image[index].save(byte_io, format='PNG')
            byte_io.seek(0)
            return byte_io
        return self._image[index]

    def success(self):
        self.status = True
        return self


def create_infinity_message():
    """
    创建一个InfinityMessage对象
    :return: InfinityMessage对象
    """
    return InfinityUniMessage()

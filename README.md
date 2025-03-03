# infinity-bot-v2-simplize

## 速览

开发文档：
<https://docs.qq.com/aio/DTWVJTk1uQVl2eExk?p=S3fHhKvG1nplUvmsq09UbA>

测试单：
<https://docs.qq.com/sheet/DTUVpYUpFdGVTS3V2?scene=ab9286dadf1307a6c2b6c4cc7WZRt1&tab=gu3qpt>

目录功能速查：

- infinity | 核心代码
- - image_template | pillow图片模板
- - models | 数据模型
- plugins | nonebot插件
- - infinity_plugin_hello | 测试插件
- - infinity_plugin_manager | 机器人全局管理相关功能

绝大部分消息的构建都在`infinity_api.py`中完成，输出成统一消息格式，以防日后需要跨平台处理

## 开始

### 快速部署

使用github action自动打包docker镜像：

```shell
# 还没做这个，有空写个action脚本把lagrange和mongodb之类的玩意都打包进来
```

使用pdm运行：

```shell
git clone xxx.git
cd infinity-bot-v2-simplize/
pdm install

odm run bot.py
```

### 配置文件

`.env`文件用于配置，参考如下：

```dotenv
HOST=0.0.0.0  # 配置 NoneBot 监听的 IP / 主机名
PORT=8081  # 配置 NoneBot 监听的端口
LOG_LEVEL=DEBUG
COMMAND_START=["/"]  # 配置命令起始字符
COMMAND_SEP=[" "]  # 配置命令分割字符
SUPERUSERS=[]  # 配置超级用户
SUPERGROUPS=[] # 配置集散群组

MONGO_URL="mongodb://localhost:27017/"
MONGO_DB="infinity"
MONGO_USER=""
MONGO_PASSWORD=""

DIVING_FISH_API="https://www.diving-fish.com/api/"
LXNS_API="https://maimai.lxns.net/api/v0/"
FANYU_API="https://download.fanyu.site/"
WAHLAP_ARCADES_API="https://wc.wahlap.net/"
SDVXIN_API="https://sdvx.in/"
DIVING_FISH_TOKEN="Ol3pAoaD9NFuUMxdsAg1dwtT1zjGH2Jy"
LXNS_TOKEN="pCx9K3Sta3034GljtbR6ykfQfbR12uZbnbYdePcQKGM="

TIPPY_TAG=[]

SEND_START_MESSAGE=True
SEND_SHUTDOWN_MESSAGE=True
```

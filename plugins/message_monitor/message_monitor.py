import plugins
from common.log import logger
from plugins.plugin import Plugin
from plugins.event import Event, EventContext, EventAction
from bridge.context import ContextType

@plugins.register(
    name="MessageMonitor",
    desire_priority=1,
    hidden=False,
    enabled=True,
    desc="monitor message",
    version="0.1",
    author="seanliu",
)

class MessageMonitor(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_RECEIVE_MESSAGE] = self.on_receive_message
        logger.info("[MessageMonitor] 插件已加载")

    def on_receive_message(self, e_context: EventContext):
        context = e_context["context"]
        msg_type = context.type

        type_desc = {
            ContextType.TEXT: "文本消息",
            ContextType.VOICE: "语音消息",
            ContextType.IMAGE: "图片消息",
            ContextType.FILE: "文件消息",
            ContextType.VIDEO: "视频消息",
            ContextType.SHARING: "分享消息",
            ContextType.IMAGE_CREATE: "图片创建命令",
            ContextType.ACCEPT_FRIEND: "好友请求",
            ContextType.JOIN_GROUP: "加入群聊",
            ContextType.PATPAT: "拍一拍",
            ContextType.FUNCTION: "函数调用",
            ContextType.EXIT_GROUP: "退出群聊",
            ContextType.NON_USER_MSG: "非用户消息",
            ContextType.STATUS_SYNC: "状态同步"
        }

        msg_desc = type_desc.get(msg_type, "未知类型消息")
        logger.info(f"[MessageMonitor] 收到{msg_desc}，内容：{context.content}")

        # 继续交给下个插件处理
        return EventAction.CONTINUE
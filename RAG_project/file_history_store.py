


class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self,session_id,storage_path):
        self.session_id = session_id
        self.storage_path = storage_path
        self.file_path = os.path.join(self.storage_path,self.session_id)

        os.makedirs(os.path.dirname(self.file_path),exist_ok=True)

    def add_message(self, message: Sequence[BaseMessage]) -> None:
        all_messages = list(self.message)
        all_messages.extend(message)

        new_messages = [message_to_dict(message) for message in all_message]
        #将数据写入文件
        with open(self.file_path,'w',encoding='utf-8') as f:
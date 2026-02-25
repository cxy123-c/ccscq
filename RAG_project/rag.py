from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_core.runnables import RunnableWithMessageHistory
from file_history_store import get_history

from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi




def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)

    return prompt

class RagService(object):
    def __init__(self):
        self.vector_service = VectorStoreService(
            embedding=DashScopeEmbeddings(
                model=config.embedding_model_name, 
                dashscope_api_key=config.dashscope_api_key)
        )
        self.prompt_templete = ChatPromptTemplate.from_messages(
            [
                ('system',"以我提供的已知参考资料为主"
                 "简洁和专业的回答用户问题，参考资料：{context}。"),
                 ("system","并且我提供历史会话记录,如下:"),
                 MessagesPlaceholder("history"),
                 ("user","请回答用户问题：{input}")
            ]
        )
        self.chat_model = ChatTongyi(model=config.chat_model_name,dashscope_api_key=config.dashscope_api_key)
        self.chain = self.__get_chain()

    def __get_chain(self):
        """获取最终的执行链"""
        retriever = self.vector_service.get_retriever()
        
        def format_document(docs: list[Document]):
            if not docs:
                return "没有相关的知识内容"

            formatted_str = ""
            for doc in docs:
                formatted_str += f"文档片段：{doc.page_content}\n文档元数据：{doc.metadata}\n\n"

            return formatted_str

        chain = (
            {
            "input":RunnablePassthrough(),
            "context":retriever | format_document
            } | self.prompt_templete | self.chat_model | StrOutputParser()
        )

        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_message_key="input",
            history_messages_key="history",
        )

        return chain

if __name__ == '__main__':
    res = RagService().chain.invoke("我的体重180斤，尺码推荐")
    print(res)

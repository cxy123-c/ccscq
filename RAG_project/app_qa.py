import streamlit as st
import time

#标题
st.title("问答服务")
st.divider()            #分隔符



#在页面最下方提供用户输入栏
prompt = st.chat_input()

if prompt:

    #在页面输出用户的提问
    st.chat_message('user').write(prompt)

    with st.spinner("AI正在思考..."):
        time.sleep(1),
        st.chat_message('assistant').write("这是一个基于RAG架构的问答系统，正在努力回答你的问题，请稍等...")

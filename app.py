from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# ------------------------
# 関数：LLMから回答を得る
# ------------------------
def get_expert_response(user_input: str, expert_type: str) -> str:
    # 専門家ごとのシステムプロンプト
    expert_prompts = {
        "心理カウンセラー": "あなたは優しい心理カウンセラーです。心の悩みを持つ人に寄り添い、的確なアドバイスを行ってください。",
        "栄養士": "あなたは知識豊富な管理栄養士です。食事や健康に関する相談に、わかりやすく丁寧に答えてください。"
    }

    system_msg = SystemMessage(content=expert_prompts[expert_type])
    human_msg = HumanMessage(content=user_input)

    # Chatモデルの設定（APIキーは環境変数で設定）
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    response = llm([system_msg, human_msg])

    return response.content

# ------------------------
# Streamlit UI
# ------------------------
st.set_page_config(page_title="専門家AIアシスタント", layout="centered")

st.title("専門家AIに相談してみよう")

# アプリの概要説明
st.markdown("""
このアプリでは、あなたの入力内容に対して、選択した専門家（AI）が回答を行います。  
下記の入力欄に相談したい内容を入力し、「心理カウンセラー」または「栄養士」を選んで送信してください。
""")

# ラジオボタンで専門家を選択
expert_type = st.radio("相談したい専門家を選んでください", ["心理カウンセラー", "栄養士"])

# ユーザーの入力フォーム
user_input = st.text_area("相談内容を入力してください", height=150)

# 送信ボタン
if st.button("相談する"):
    if user_input.strip() == "":
        st.warning("相談内容を入力してください。")
    else:
        with st.spinner("AI専門家が考え中..."):
            response = get_expert_response(user_input, expert_type)
            st.success("専門家からの回答")
            st.markdown(response)

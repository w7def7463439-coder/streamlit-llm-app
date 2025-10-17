from dotenv import load_dotenv

load_dotenv()
# app.py

import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import os
from dotenv import load_dotenv


# -----------------------------
# 1. Webアプリ概要
# -----------------------------
st.title("大学受験コンサルアプリ")
st.markdown("""
このアプリでは、入力テキストを元に大規模言語モデル(LLM)が回答を生成します。
1. テキストを入力してください。
2. ラジオボタンで専門家の種類を選択してください。
3. 「送信」ボタンを押すと回答が表示されます。
""")

# -----------------------------
# 2. ユーザー入力フォーム
# -----------------------------
user_input = st.text_area("質問を入力してください")
expert_type = st.radio(
    "専門家の種類を選択してください",
    ("進路アドバイザー", "勉強法アドバイザー")
)

# -----------------------------
# 3. LLMに渡す関数
# -----------------------------
def generate_response(input_text, expert_type):
    # 選択された専門家に応じてsystemメッセージを変更
    if expert_type == "進路アドバイザー":
        system_prompt = "あなたは大学受験の進路に関する専門家です。正確で的確なアドバイスを提供してください。"
    elif expert_type == "勉強法アドバイザー":
        system_prompt = "あなたは大学受験の勉強法に関する専門家です。効果的な学習方法を提案してください。"
    else:
        system_prompt = "あなたは有能なアシスタントです。"

    # ChatOpenAIインスタンスを生成
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5)

    # LangChainでのメッセージ作成
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=input_text)
    ]

    # LLMに渡して回答を取得
    result = llm(messages)
    return result.content

# -----------------------------
# 4. ボタン押下時の処理
# -----------------------------
if st.button("送信"):
    if user_input.strip() == "":
        st.warning("質問を入力してください")
    else:
        with st.spinner("回答生成中..."):
            answer = generate_response(user_input, expert_type)
        st.subheader("LLMの回答")
        st.write(answer)


# Pyhton外部モジュールのインポート
import streamlit as st
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage

# タイトル
st.title("Let's compare the AWS services!")
st.write("AWSソリューションアーキテクトの役割を持つ生成AIエージェントが、2つのサービスの比較議論を行います。")

BEDROCK_LLM_MODEL_ID = "anthropic.claude-3-5-sonnet-20240620-v1:0"
MAX_TOKENS = 4000

# モデルの呼び出し
chat = ChatBedrock(
    model_id=BEDROCK_LLM_MODEL_ID,
    model_kwargs={"max_tokens": MAX_TOKENS},
    streaming=True,
)

# モデルの初期化
messages = [
    SystemMessage(content="あなたのタスクはユーザーの質問に明確に答えることです。"),
]

# 事前指示プロンプト
predefined_instructions = '''
        # 指示
        - SA1、SA2、SA3は優れたAWSソリューションアーキテクトです。
        - 1人目のSA1は、テーマを肯定する主張をして、その理由を説明してください。
        - 2人目のSA2は、テーマを肯定する主張をして、その理由を説明してください。
        - その後、SA1は、SA2の主張に対する批判を述べ、SA2はそれに反論してください。
        - 次に、SA2は、SA1の主張に対する批判を述べ、SA1はそれに反論してください。
        - 最後に、3人目のSA3は、2人の意見をまとめ、論理的に分析して、最終的にどちらの主張に賛成するか判定してください。
        - SA3は、AWS Well-Architected Frameworkの6本の柱の観点、運用性、セキュリティ、信頼性、パフォーマンス効率、コスト最適化、持続可能性から論理的な分析を行なって下さい。
        # 出力
        - 上記を、日本語で、Markdown記法に変換してください。
        ```
        
        ```
    '''
if prompt := st.chat_input("「ECS vs EKS」「ECSはEKSより優れていますか？」等"):
    messages.append(HumanMessage(content=predefined_instructions+prompt))

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        st.write_stream(chat.stream(messages))
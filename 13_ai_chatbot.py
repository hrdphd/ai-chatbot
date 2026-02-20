# google 에서 제공하는 LLM API 를 사용하기
# Google AI Studio 플랫폼 사이트에서 키발급

# 라이브러리 설치
#pip install -q -U google-genai

#0. api key 는 노출되면 안됨. 그래서 별도의 환경변수파일 .env 에 저장하여 dotenv모듈로 불러서 적용
# 단, 우리의 챗봇을 streamlit cloud 에 배포할 예정. 애석하게 이곳은 .env 를 설정할 수 없음
# 그래서 streamlit에서 제공하는 비밀값을 저장하는 속성 secrets 를 활용 [secrets에 등록될 값들은 .streamlit폴더 안에 secrets.toml 파일로 등록. 이 파일을 GitHub를 통해 배포되면 안됨. 노출되면 일정시간 후에 정지됨. 다시 키발급 필요]
import streamlit as st
if "GEMINI_API_KEY" in st.secrets:
    api_key= st.secrets["GEMINI_API_KEY"]

#1. 라이브러리 사용
from google import genai
#2. 요청 사용자 객체 생성
client= genai.Client(api_key=api_key)

#3. 채팅 UI 만들기

#1) 페이지 기본 설정 -- 브라우저의 탭영역에 표시되는 내용.
st.set_page_config(
    page_title='AI 불량봇',
    page_icon='./logo/logo_chatbot.png'
)

#2) HEADER 영역 (레이아웃 : 이미지 + 제목 영역 가로 배치)
col1, col2= st.columns([1.2, 4.8])

with col1:
    st.image("./logo/logo_chatbot.png", width=200)

with col2:
    #제목(h1)+서브안내글씨(p) [색상을 다르게.. 하려면 HTML코드로 구현]
    st.markdown(
        """
        <h1 style='margin-bottom:0;'>AI 불량봇</h1>
        <p style='margin-top:0; color:gray'>이 챗봇은 모든 답변을 불량 고등학생처럼 합니다. 상처받지 마세요.</p>
        """,
        unsafe_allow_html=True
    )

#구분선
st.markdown("---")

#3) 채팅 UI 구현

#a. messages 라는 이름의 변수가  session_state에 존재하는지 확인. 후 없으면 첫 문자 지정
if "messages" not in st.session_state:
    st.session_state.messages= [
        {'role':'assistant', 'content':'무엇이든 물어봐!'},
    ]

#b. sesstion_state에 저장된 "messages"의 메세지들을 채팅 UI로 그려내기
for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

#c. 사용자 채팅메세지를 입력받아 session_state에 저장하고 UI 갱신
question= st.chat_input('질문을 입력해보든가.')
if question:
    question= question.replace('\n','  \n')
    st.session_state.messages.append({'role':'user','content':question})
    st.chat_message('user').write(question)

    



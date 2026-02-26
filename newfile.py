import streamlit as st
import requests

# Настройка страницы
st.set_page_config(page_title="Personal AI", page_icon="💬")
st.title("🤖 Мой личный ИИ-ассистент")

# Сюда вставь свой токен или добавь его в секреты Streamlit
API_TOKEN = "ТВОЙ_ТОКЕН_ЗДЕСЬ"
MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.3" # Мощная модель
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Инициализация истории
if "messages" not in st.session_state:
    st.session_state.messages = []

# Отображение чата
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Ввод текста
if prompt := st.chat_input("Напиши мне что-нибудь..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Думаю..."):
            # Отправка запроса к API
            output = query({
                "inputs": f"<s>[INST] {prompt} [/INST]",
                "parameters": {"max_new_tokens": 500, "return_full_text": False}
            })
            
            # Обработка ответа
            if isinstance(output, list) and len(output) > 0:
                answer = output[0].get('generated_text', 'Ошибка ответа')
            else:
                answer = "ИИ сейчас занят, попробуй через минуту."
            
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

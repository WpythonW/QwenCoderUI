import streamlit as st
from huggingface_hub import InferenceClient
import ast
import dotenv, os

dotenv.load_dotenv()

def init_client():
    """Инициализация клиента Hugging Face"""
    api_key = api_key = os.getenv("API_KEY_HUGGINGFACE")
    return InferenceClient(api_key=api_key)

def validate_syntax(code):
    """Проверка синтаксиса кода"""
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False

def complete_code(client, incomplete_code):
    """Отправка запроса на дополнение кода"""
    messages = [
        {
            "role": "system",
            "content": "You are an expert code completion assistant. Complete the code by replacing [...] or <...> with appropriate code. Respond ONLY with the completed code, no explanations."
        },
        {
            "role": "user",
            "content": f"Complete this code:\n{incomplete_code}"
        }
    ]
    
    try:
        completion = client.chat.completions.create(
            model="Qwen/Qwen2.5-Coder-32B-Instruct",  # или другая подходящая модель
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

def main():
    st.title("Code Completion Tool")
    st.write("Enter code with [...] or <...> placeholders for completion")
    
    # Инициализация клиента при первом запуске
    if 'client' not in st.session_state:
        st.session_state.client = init_client()
    
    # Пример кода для демонстрации
    example_code = '''def calculate_sum(a, b):
    [...]
    return result'''
    
    # Ввод кода
    incomplete_code = st.text_area(
        "Your code:",
        value=example_code,
        height=200
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Complete Code"):
            if incomplete_code:
                # Базовая проверка синтаксиса
                placeholder_filled = incomplete_code.replace('[...]', 'pass').replace('<...>', 'pass')
                if not validate_syntax(placeholder_filled):
                    st.error("Invalid code syntax")
                    return
                
                with st.spinner("Generating completion..."):
                    completed = complete_code(st.session_state.client, incomplete_code)
                    
                    if completed:
                        st.code(completed, language='python')
                        
                        # Проверяем синтаксис результата
                        if validate_syntax(completed):
                            st.success("Generated code is syntactically correct!")
                        else:
                            st.warning("Generated code might have syntax errors")
    
    with col2:
        st.button("Clear", on_click=lambda: st.session_state.clear())

if __name__ == "__main__":
    main()
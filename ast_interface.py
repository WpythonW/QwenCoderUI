import streamlit as st
from huggingface_hub import InferenceClient
import ast
import dotenv, os

# Настройка страницы на широкий формат
st.set_page_config(layout="wide", page_title="AI Code Completion", page_icon="🤖")

# Добавление CSS для улучшения внешнего вида
st.markdown("""
    <style>
        .stTextArea textarea {
            font-family: 'Courier New', Courier, monospace;
        }
        .stButton button {
            width: 100%;
        }
        .success-message {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }
        .warning-message {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: #fff3cd;
            border: 1px solid #ffeeba;
            color: #856404;
        }
    </style>
""", unsafe_allow_html=True)

def init_client():
    """Инициализация клиента Hugging Face"""
    api_key = os.getenv("API_KEY_HUGGINGFACE")
    return InferenceClient(api_key=api_key)

def validate_syntax(code):
    """Проверка синтаксиса кода"""
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False

def complete_code(client, incomplete_code, max_tokens, temperature):
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
            model="Qwen/Qwen2.5-Coder-32B-Instruct",
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

def main():
    # Заголовок с описанием
    st.title("AI Code Completion Tool")
    st.markdown("""
        This tool helps you complete code snippets using AI. Simply enter your code with 
        `[...]` or `<...>` placeholders where you want the AI to fill in the code.
    """)
    
    # Инициализация клиента при первом запуске
    if 'client' not in st.session_state:
        st.session_state.client = init_client()
    
    # Создаем две колонки: основную для кода и боковую для параметров
    main_col, sidebar = st.columns([3, 1])
    
    with sidebar:
        st.subheader("Generation Parameters")
        
        # Параметры генерации
        max_tokens = st.slider(
            "Max Tokens",
            min_value=100,
            max_value=1000,
            value=500,
            step=50,
            help="Maximum number of tokens to generate"
        )
        
        temperature = st.slider(
            "Temperature",
            min_value=0.1,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Higher values make the output more random, lower values make it more focused"
        )
        
        # Примеры кода
        st.subheader("Code Templates")
        example_templates = {
            "Function Template": '''def calculate_sum(a, b):
    [...]
    return result''',
            
            "Class Template": '''class DataProcessor:
    def __init__(self, data):
        self.data = data
    
    def process(self):
        [...]''',
            
            "Loop Template": '''for item in items:
    <...>'''
        }
        
        selected_template = st.selectbox(
            "Select a template",
            list(example_templates.keys())
        )
        
        if st.button("Use Template"):
            st.session_state.current_code = example_templates[selected_template]
    
    with main_col:
        # Ввод кода с увеличенной высотой
        if 'current_code' not in st.session_state:
            st.session_state.current_code = example_templates["Function Template"]
            
        incomplete_code = st.text_area(
            "Your code:",
            value=st.session_state.current_code,
            height=400,
            key="code_input"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 Complete Code", use_container_width=True):
                if incomplete_code:
                    # Базовая проверка синтаксиса
                    placeholder_filled = incomplete_code.replace('[...]', 'pass').replace('<...>', 'pass')
                    if not validate_syntax(placeholder_filled):
                        st.error("❌ Invalid code syntax")
                        return
                    
                    with st.spinner("🔄 Generating completion..."):
                        completed = complete_code(
                            st.session_state.client,
                            incomplete_code,
                            max_tokens,
                            temperature
                        )
                        
                        if completed:
                            st.markdown("### Completed Code:")
                            st.code(completed, language='python')
                            
                            # Проверяем синтаксис результата
                            if validate_syntax(completed):
                                st.markdown('<div class="success-message">✅ Generated code is syntactically correct!</div>', unsafe_allow_html=True)
                            else:
                                st.markdown('<div class="warning-message">⚠️ Generated code might have syntax errors</div>', unsafe_allow_html=True)
        
        with col2:
            if st.button("🔄 Clear", use_container_width=True):
                st.session_state.current_code = ""
                st.experimental_rerun()

if __name__ == "__main__":
    main()
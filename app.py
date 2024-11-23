import streamlit as st
import asyncio
import aiohttp
import logging
from llms_api_client import CodeGenerationAPI
import dotenv, io, os

dotenv.load_dotenv()
# Get api_key
api_key = os.getenv("API_KEY_HUGGINGFACE")

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('streamlit_app')

# Инициализация состояния сессии
if 'params' not in st.session_state:
    st.session_state.params = {
        "max_tokens": 500,
        "temperature": 0.7,
        "top_p": 0.95  # оставляем дефолтное значение 0.95
    }

if 'prompt' not in st.session_state:
    st.session_state.prompt = ''


def update_params():
    st.session_state.params = {
        "max_tokens": st.session_state.form_max_tokens,
        "temperature": st.session_state.form_temperature,
        "top_p": st.session_state.form_top_p
    }
    st.session_state.prompt = st.session_state.form_prompt

# Add this class before main()
class PromptFormatter:
    LANGUAGE_TEMPLATES = {
        "python": """Write Python code for the following task.
Requirements:
- Use Pythonic conventions
- Format Markdown
- Include comments for complex logic
- Handle edge cases
- Use type hints where appropriate

Task description:
{prompt}

Please provide only the code without explanation:""",
        
        "javascript": """Write JavaScript code for the following task.
Requirements:
- Use modern ES6+ syntax
- Format Markdown
- Follow JavaScript best practices
- Include error handling
- Add JSDoc comments for functions

Task description:
{prompt}

Please provide only the code without explanation:""",
        
        "cpp": """Write C++ code for the following task.
Requirements:
- Follow modern C++ conventions
- Format Markdown
- Include proper error handling
- Use appropriate STL containers
- Add comments for complex logic

Task description:
{prompt}

Please provide only the code without explanation:"""
    }
    
    @staticmethod
    def format_prompt(prompt: str, language: str) -> str:
        """Format the prompt for specific programming language."""
        template = PromptFormatter.LANGUAGE_TEMPLATES.get(
            language, 
            "Write code in {language} for the following task:\n{prompt}"
        )
        return template.format(prompt=prompt, language=language)

async def generate_code_async(session: aiohttp.ClientSession, api: CodeGenerationAPI, 
                            prompt: str, model: str, language: str, params: dict):
    logger.info(f"Generating code: language={language}, model={model}")
    try:
        # Format the prompt according to language
        formatted_prompt = PromptFormatter.format_prompt(prompt, language)
        logger.debug(f"Formatted prompt for {language}:\n{formatted_prompt}")
        
        response = await api.generate_code_async(
            session, 
            prompt=formatted_prompt, 
            model=model, 
            language=language, 
            **params
        )
        logger.debug(f"Response status: {response.status}")
        return response
    except Exception as e:
        logger.error(f"Error in generate_code_async: {str(e)}", exc_info=True)
        raise

def main():
    st.set_page_config(layout="wide", page_title="AI Code Generation")
    
    st.title("Генерация кода с помощью ИИ")
    
    # Создаем контейнер с рамкой
    with st.container():
        st.markdown("""
        <style>
        .stContainer {
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
        }
        </style>
        """, unsafe_allow_html=True)
        
        with st.form(key="params_form"):
            # Большое поле для ввода запроса
            st.text_area(
                "Введите ваш запрос для генерации кода:",
                value=st.session_state.prompt,
                height=200,
                key="form_prompt"
            )
            
            # Центрированные ползунки
            col1, col2, col3, col4, col5 = st.columns([4, 1, 2, 1, 4])
            with col3:
                st.slider(
                    "Максимум токенов",
                    100, 1000, st.session_state.params["max_tokens"],
                    key="form_max_tokens"
                )
                
                st.slider(
                    "Temperature",
                    0.1, 1.0, st.session_state.params["temperature"],
                    step=0.1,
                    key="form_temperature"
                )
                
                st.slider(
                    "Top P",
                    0.1, 0.99, st.session_state.params["top_p"],  # максимум теперь 0.99 вместо 1.0
                    step=0.05,
                    key="form_top_p"
                )
            
            # Пустое пространство перед кнопкой
            st.write("")
            
            # Кнопка генерации по центру (уменьшенная)
            col1, col2, col3, col4, col5 = st.columns([5, 2, 1, 2, 5])
            with col3:
                submit_button = st.form_submit_button(
                    "Сгенерировать",  # Укоротил текст кнопки
                    type="primary",
                    on_click=update_params
                )
    
    # Инициализация API
    api = CodeGenerationAPI(api_key=api_key)
    
    # Генерация кода после отправки формы
    if submit_button and st.session_state.prompt:
        with st.spinner("Генерируем код..."):
            languages = ["python", "javascript", "cpp"]
            models = ["qwen", "starcoder"]
            
            # Создаем табы для языков
            lang_tabs = st.tabs(["Python", "JavaScript", "C++"])
            
            async def generate_all():
                async with aiohttp.ClientSession() as session:
                    tasks = []
                    for lang in languages:
                        for model in models:
                            tasks.append(generate_code_async(
                                session,
                                api,
                                st.session_state.prompt,
                                model,
                                lang,
                                st.session_state.params
                            ))
                    return await asyncio.gather(*tasks)
            
            try:
                results = asyncio.run(generate_all())
                
                # Отображаем результаты в табах
                for idx, tab in enumerate(lang_tabs):
                    with tab:
                        # Создаем две колонки для моделей
                        col1, col2 = st.columns(2)
                        
                        # Qwen результат
                        with col1:
                            st.subheader("Qwen")
                            result = results[idx * 2]
                            if result.status:
                                st.markdown(result.generated_text)
                            else:
                                st.error(f"Ошибка: {result.error}")
                        
                        # StarCoder результат
                        with col2:
                            st.subheader("StarCoder")
                            result = results[idx * 2 + 1]
                            if result.status:
                                st.markdown(result.generated_text)
                            else:
                                st.error(f"Ошибка: {result.error}")
                            
            except Exception as e:
                st.error(f"Ошибка при генерации: {str(e)}")

if __name__ == "__main__":
    main()
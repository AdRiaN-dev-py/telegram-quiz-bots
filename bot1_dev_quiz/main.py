import telebot
from telebot import types
from dotenv import load_dotenv
import os
print(os.listdir())

#загрузка токена
load_dotenv()

token = os.getenv('TOKEN')
print(repr(token))
if not token:
    print("Ошибка: создай .env с TOKEN")
    print(os.getenv('TOKEN'))
    exit()
bot = telebot.TeleBot(token)


#Основная часть - вопросы
QUESTIONS = [
    {
        "id": 1,
        "text": "Какой язык программирования тебе ближе?",
        "options": ["Python", "JavaScript", "Java", "C++"],
        "scores": {
            "Python": {"backend": 10, "data": 5},
            "JavaScript": {"frontend": 10, "fullstack": 7},
            "Java": {"backend": 7, "enterprise": 10},
            "C++": {"systems": 10, "gamedev": 8}
        }
    },
    {
        "id": 2,
        "text": "Что тебе интереснее?",
        "options": ["Серверная логика", "Интерфейсы", "Оба направления", "Системное программирование"],
        "scores": {
            "Серверная логика": {"backend": 10},
            "Интерфейсы": {"frontend": 10},
            "Оба направления": {"fullstack": 10},
            "Системное программирование": {"systems": 10}
        }
    },
    {
        "id": 3,
        "text": "Предпочитаешь работать?",
        "options": ["Один", "В команде", "Зависит от задачи"],
        "scores": {
            "Один": {"backend": 5, "data": 7},
            "В команде": {"frontend": 7, "fullstack": 8},
            "Зависит от задачи": {"fullstack": 5}
        }
    },
    {
        "id": 4,
        "text": "Как относишься к дизайну?",
        "options": ["Важна красота", "Важна функциональность", "Баланс"],
        "scores": {
            "Важна красота": {"frontend": 10},
            "Важна функциональность": {"backend": 10, "systems": 8},
            "Баланс": {"fullstack": 10}
        }
    },
    {
        "id": 5,
        "text": "Что бы ты выбрал?",
        "options": ["Базы данных", "Анимации", "Архитектура", "Игровая физика"],
        "scores": {
            "Базы данных": {"backend": 10, "data": 8},
            "Анимации": {"frontend": 10, "gamedev": 5},
            "Архитектура": {"backend": 8, "enterprise": 10},
            "Игровая физика": {"gamedev": 10, "systems": 5}
        }
    }
]

# Описания результатов
RESULTS = {
    "backend": {
        "title": "Backend-разработчик",
        "emoji": "🖥️",
        "description": "Тебе нравится серверная логика, базы данных, API. Ты предпочитаешь работать с данными и бизнес-логикой, а не с интерфейсами."
    },
    "frontend": {
        "title": "Frontend-разработчик",
        "emoji": "🎨",
        "description": "Тебе нравятся интерфейсы, UX/UI, визуальная часть. Ты любишь создавать красивые и удобные приложения."
    },
    "fullstack": {
        "title": "Fullstack-разработчик",
        "emoji": "🚀",
        "description": "Ты универсал! Можешь работать и с сервером и с клиентом. Тебе интересны разные стороны разработки."
    },
    "data": {
        "title": "Data Scientist",
        "emoji": "📊",
        "description": "Тебе интересны данные, анализ, машинное обучение. Ты любишь находить закономерности и делать выводы из данных."
    },
    "systems": {
        "title": "Systems Programmer",
        "emoji": "⚙️",
        "description": "Тебе интересен низкий уровень, производительность, операционные системы. Ты любишь понимать как всё работает изнутри."
    },
    "gamedev": {
        "title": "Game Developer",
        "emoji": "🎮",
        "description": "Тебе интересна разработка игр, графика, физика. Ты любишь создавать интерактивные миры."
    },
    "enterprise": {
        "title": "Enterprise Developer",
        "emoji": "🏢",
        "description": "Тебе интересны корпоративные системы, сложная архитектура, масштабируемость."
    }
}

# Хранение данных пользователей (в памяти)
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    
    # Инициализация данных пользователя
    user_data[user_id] = {
        "current_question": 0,
        "scores": {}
    }
    
    # Приветствие
    welcome_text = """Привет! 👋

Я помогу тебе определить твой тип разработчика.

Ответь на 5 вопросов и узнай кто ты:
• Backend-разработчик 🖥️
• Frontend-разработчик 🎨
• Fullstack-разработчик 🚀
• Data Scientist 📊
• И другие варианты!

Готов начать?"""
    
    # Кнопка "Начать"
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("Начать опрос", callback_data="start_quiz")
    markup.add(btn)
    
    bot.send_message(user_id, welcome_text, reply_markup=markup)

def ask_question(user_id):
    """Задать следующий вопрос"""
    user = user_data[user_id]
    question_index = user["current_question"]
    
    # Проверка: все вопросы пройдены?
    if question_index >= len(QUESTIONS):
        show_result(user_id)
        return
    
    question = QUESTIONS[question_index]
    
    # Создаем inline-кнопки с вариантами ответов
    markup = types.InlineKeyboardMarkup(row_width=1)
    for option in question["options"]:
        btn = types.InlineKeyboardButton(
            option,
            callback_data=f'answer_{question_index}_{option}'
        )
        markup.add(btn)
    
    # Отправляем вопрос
    question_text = f"Вопрос {question_index + 1}/{len(QUESTIONS)}\n\n{question['text']}"
    bot.send_message(user_id, question_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "start_quiz")
def start_quiz(call):
    """Начать опрос"""
    user_id = call.message.chat.id
    
    # Убираем кнопку "Начать"
    bot.edit_message_reply_markup(
        chat_id=user_id,
        message_id=call.message.message_id,
        reply_markup=None
    )
    
    # Задаем первый вопрос
    ask_question(user_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('answer_'))
def handle_answer(call):
    """Обработка ответа на вопрос"""
    user_id = call.message.chat.id
    
    # Парсим callback_data: 'answer_0_Python'
    parts = call.data.split('_', 2)
    question_index = int(parts[1])
    answer = parts[2]

    print(f'Пользователь {user_id} выбрал: {answer} на вопрос {question_index}')

    question = QUESTIONS[question_index]
    
    # Обновляем баллы
    scores_for_answer = question["scores"][answer]
    for category, points in scores_for_answer.items():
        if category not in user_data[user_id]["scores"]:
            user_data[user_id]["scores"][category] = 0
        user_data[user_id]["scores"][category] += points
    
    # Показываем что выбрано
    bot.edit_message_text(
        f"Вопрос {question_index + 1}/{len(QUESTIONS)}\n\n{question['text']}\n\n✅ Выбрано: {answer}",
        user_id,
        call.message.message_id
    )
    
    # Переходим к следующему вопросу
    user_data[user_id]["current_question"] += 1
    ask_question(user_id)

def show_result(user_id):
    """Показать результат опроса"""
    scores = user_data[user_id]["scores"]
    
    # Находим категорию с максимальным баллом
    if not scores:
        bot.send_message(user_id, "Ошибка: нет данных. Попробуй /start")
        return
    
    max_category = max(scores, key=scores.get)
    max_score = scores[max_category]
    
    # Получаем описание результата
    result = RESULTS.get(max_category, {
        "title": "Разработчик",
        "emoji": "💻",
        "description": "Твой тип: " + max_category
    })
    
    # Формируем текст результата
    result_text = f"""🎉 Результат готов!

{result['emoji']} Ты — {result['title']}!

{result['description']}

📊 Твои баллы:
"""
    
    # Добавляем баллы по категориям (топ-3)
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for i, (category, score) in enumerate(sorted_scores[:3], 1):
        category_name = RESULTS.get(category, {}).get("title", category)
        result_text += f"{i}. {category_name}: {score} баллов\n"
    
    bot.send_message(user_id, result_text)
    
    # Кнопка "Пройти еще раз"
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("Пройти еще раз", callback_data="start_quiz")
    markup.add(btn)
    
    bot.send_message(user_id, "Хочешь пройти опрос еще раз?", reply_markup=markup)
    
    # Сбрасываем данные пользователя
    user_data[user_id] = {
        "current_question": 0,
        "scores": {}
    }

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """ℹ️ Помощь:
      Этот бот определяет твой тип разработчика.

Команды:
/start - Начать опрос
/help - Показать эту справку

Просто ответь на 5 вопросов и получи результат!"""
    
    bot.send_message(message.chat.id, help_text)

# Запуск бота
if __name__ =='__main__': 
    print("Бот запущен...")
    bot.infinity_polling()
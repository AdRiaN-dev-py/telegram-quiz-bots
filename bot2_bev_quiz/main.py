import telebot
from telebot import types
from dotenv import load_dotenv
import os

#Загрузка токена с проверкой
load_dotenv()

token = os.getenv('BOT_TOKEN')
if not token:
    print('Ошибка: создай .env с BOT_TOKEN')
    exit()

bot = telebot.TeleBot(token)

# Основная часть
QUESTIONS = [
    {
        'id': 1,
        'text': "Как ты относишься к тренировкам?",
        'options': [
            'Люблю, когда тяжело и через боль (много повторений, отказ)',
            'Хочу красивые мышцы и рельеф, но без фанатизма',
            'Мне важно быть выносливым и не уставать в жизни',
            'Тренируюсь только когда настроение есть или друг позовет'
        ],
        'scores': {
            'Люблю, когда тяжело и через боль (много повторений, отказ)': {'strength': 3, 'pull-ups': 3},
            'Хочу красивые мышцы и рельеф, но без фанатизма': {'aesthetics': 3},
            'Мне важно быть выносливым и не уставать в жизни': {'endurance': 3},
            'Тренируюсь только когда настроение есть или друг позовет': {'lazybones': 3}
        }
    },
    {
        'id': 2,
        'text': 'Что для тебя важнее всего в результате тренировок?',
        'options': [
            'Сильные руки, спина и умение подтягиваться много раз',
            "Красивое тело",
            "Выносливость, чтобы работать весь день без усталости",
            "Просто быть в форме и не толстеть"
        ],
        'scores': {
            'Сильные руки, спина и умение подтягиваться много раз':{'pull-ups': 3},
            "Красивое тело": {'aesthetics': 3},
            "Выносливость, чтобы работать весь день без усталости": {'functionality': 3},
            "Просто быть в форме и не толстеть": {'lazybones': 2, 'aesthetics': 1}
        }
    },
    {
        'id': 3,
        'text': 'Как ты обычно тренируешься?',
        'options': [
            "В основном на турнике и брусьях (или хочу так)",
            "Хожу в зал",
            "Легкая атлетика, кардио или единоборства",
            "Ничего не делаю (или редко)"
        ],
        'scores': {
            "В основном на турнике и брусьях (или хочу так)": {'pull-ups': 3},
            "Хожу в зал": {'aesthetics': 2, 'strength': 1},
            "Легкая атлетика, кардио или единоборства": {'endurance': 3},
            "Ничего не делаю (или редко)": {'lazybones': 3}
        }
    },
    {
        'id': 4,
        'text': 'Как ты реагируешь на боль и дискомфорт во время тренировки?',
        'options': [
            "Боль - это рост, терплю и иду дальше",
            "Если больно - стараюсь делать легче или менять упражнение",
            "Боль в мышцах меня мотивирует, но в суставах - сразу останавливаюсь",
            "Если тяжело или больно - лучше пропущу тренировку"
        ],
        'scores': {
            "Боль - это рост, терплю и иду дальше": {'pull-ups': 3},
            "Если больно - стараюсь делать легче или менять упражнение": {'aesthetics': 3},
            "Боль в мышцах меня мотивирует, но в суставах - сразу останавливаюсь": {'endurance': 3},
            "Если тяжело или больно - лучше пропущу тренировку": {'lazybones': 3}
        }
    },
    {
        'id': 5,
        'text': 'Какая у тебя мотивация заниматься спортом?',
        'options': [
            "Стать сильным и уметь делать сложные элементы",
            "Выглядеть круто, иметь сухое тело и рельеф",
            "Быть здоровым, выносливым и готовым к любой жизненной нагрузке",
            "Просто не толстеть и иногда поддерживать форму"
        ],
        'scores': {
            "Стать сильным и уметь делать сложные элементы": {'pull-ups': 3},
            "Выглядеть круто, иметь сухое тело и рельеф": {'aesthetics': 3},
            "Быть здоровым, выносливым и готовым к любой жизненной нагрузке": {'functionality': 3, 'endurance': 3},
            "Просто не толстеть и иногда поддерживать форму": {'lazybones': 3}
        }
    },
]

# Описание результатов
RESULTS = {
        'pull-ups': {
        'title': "Турник-мен",
        'emoji': "🏋️",
        "description": "Ты любишь работать со своим весом тела, подтягивания и брусья. Тебе комфортно тренироваться на улице или дома. Скорее всего, ты уже неплохо подтягиваешься и хочешь прогрессировать дальше в калистенике."
    },
    'strength': {
        'title': "Зальный парень",
        'emoji': "💪",
        "description": "Тебе нравится зал, железо, гантели и штанга. Ты хочешь увеличивать веса и видеть, как растут мышцы. Классический подход к тренировкам — твой"
    },
    'aesthetics': {
        'title': "Эстет",
        'emoji': "🎨",
        "description": " Главная цель — красивое, пропорциональное тело, рельеф и чёткие мышцы. Тебе важно, как ты выглядишь в зеркале и в одежде. Скорее всего, тебе подойдёт программа на рельеф и сухость."
    },
    'functionality': {
        'title': "Функциональщик",
        'emoji': "⚡️",
        "description": " Ты хочешь быть не только сильным, но и выносливым, ловким и готовым к реальной жизни (драка, работа, экстренные ситуации). Тебе ближе кроссфит, единоборства или функциональные тренировки."
    },
    'endurance': {
        'title': "Выносливый",
        'emoji': "🏃",
        "description": "Тебе нравится ощущение, когда ты можешь долго бежать, ехать на велосипеде или работать без быстрой усталости. Кардио и тренировки на выносливость — твоя сильная сторона."
    },
    'lazybones': {
        'title': "Домашний минималист",
        'emoji': "🏠",
        "description": "Ты понимаешь пользу спорта, но не хочешь сложных программ и зала. Тебе хватает коротких домашних тренировок 3–4 раза в неделю (отжимания, приседания, планка). Главное — регулярность, а не рекорды."
    },
    'Newbie': {
        'title': "Новичок в процессе",
        'emoji': "🌱",
        "description": "Ты только начинаешь или часто пропускаешь тренировки. У тебя есть желание, но пока не хватает дисциплины или понимания, с чего начать. Тебе нужны простые, короткие и понятные тренировки, чтобы не бросить."
    }
}


# Хранение данных пользователя (в памяти)
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id

    # Инициализация данных пользователя
    user_data[user_id] = {
        'current_question': 0,
        'scores': {}
    }

    # Приветствие
    welcome_text = """Привет! 👋

Я помогу определить какой ты спортсмен.

Ответь на 5 вопросов и узнай кто ты:
• Турник-мен
• Зальный парень
• Эстет
• Домашний минималист
• И другие Варианты!

Готов начать?"""

    # Кнопка "начать"
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton('Начать опрос', callback_data='start_quiz')
    markup.add(btn)

    bot.send_message(user_id, welcome_text, reply_markup=markup)

def ask_question(user_id):
    '''задать следующий вопрос'''
    user = user_data[user_id]
    question_index = user['current_question']

    # Проверка: все ли вопросы пройдены? 
    if question_index >= len(QUESTIONS):
        show_result(user_id)
        return
    
    question = QUESTIONS[question_index]

    # Создаем Inline-кнопки с вариантами ответов
    markup = types.InlineKeyboardMarkup(row_width=1)
    for i, option in enumerate(question['options']):
        btn = types.InlineKeyboardButton(
            option,
            callback_data=f'answer_{question_index}_{i}'
        )
        markup.add(btn)
    
    # отправляем вопрос
    question_text = f"Вопрос{question_index + 1}/{len(QUESTIONS)}\n\n{question['text']}"
    bot.send_message(user_id, question_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'start_quiz')
def start_quiz(call):
    '''Начать опрос'''
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
def handler_answer(call):
    '''Обработка ответа на вопрос'''
    user_id = call.message.chat_id

    # Парсим Callback_data: 'answer_0_pull-ups'
    parts = call.data.split('_', 2)
    question_index = int(parts[1])
    answer_index = int(parts[2])


    question = QUESTIONS[question_index]
    answer_text = question['options'][answer_index]

    print(f'Пользователь {user_id} выбрал: {answer_index} на вопрос {question_index}')
    
    # Обновляем баллы
    scores_for_answer = question['scores'][answer_index]
    for category, points in scores_for_answer.items():
        if category not in user_data[user_id]['scores']:
            user_data[user_id]['scores'][category] = 0
        user_data[user_id]['scores'][category] += points

    # Показываем что выбрано
    bot.edit_message_text(
        f"Вопрос {question_index + 1}/{len(QUESTIONS)}\n\n{question['text']}\n\n✅ Выбрано: {answer_text}",
        user_id,
        call.message.message_id
    )

    # Переходим к следующему вопросу
    user_data[user_id]['current_question'] += 1
    ask_question(user_id)

def show_result(user_id):
    '''Показать результат опроса'''
    scores = user_data[user_id]['scores']

    #Находи категорию максимальным баллом
    if not scores:
        bot.send_message(user_id, 'Ошибка: нет данных. Попробуй /start')
        return
    
    max_category = max(scores, key=scores.get)
    max_score = scores[max_category]

    # Получаем описание результата
    result = RESULTS.get(max_category, {
        'title': 'Спортсмен',
        'emoji': '💪',
        'description': 'Твой тип: ' + max_category
    })

    # Формируем текст результата
    result_text = f'''🎉 Результат готов!

{result['emoji']} **Ты - {result['title']}!**

{result['description']}

📊 Твои баллы: 
'''

    # Добавляем баллы по категориям (топ-3)
    sorted_scores =  sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for i, (category, score) in enumerate(sorted_scores[:3], 1):
        category_name = RESULTS.get(category, {}).get('title', category)
        emoji = RESULTS.get(category, {}).get('emoji', '•')
        result_text += f"{i}. {emoji} {category_name}: {score} баллов\n"

    bot.send_message(user_id, result_text)

    # Кнопка "Пройти еще раз"
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton('Пройти еще раз', callback_data='start_quiz')
    markup.add(btn)

    bot.send_message(user_id, 'Хочешь пройти опрос еще раз?', reply_markup=markup)

    # Сбрасываем данные пользователя
    user_data[user_id] = {
        'current_question': 0,
        'scores': {}
    }

@bot.message_handler(commands=['help'])
def help_commands(message):
    help_text = """ℹ️ Помощь:
    Этот бот определяет какой тип тренировок тебе подходит.

Команды: 
/start - Начать опрос
/help - Показать эту справку

Просто ответь на 5 вопросов и получи результат!"""

    bot.send_message(message.chat.id, help_text)

@bot.message_handler(func=lambda message: True)
def handle_unknown(message):
    bot.send_message(
        message.chat.id,
        'Я не понимаю эту команду. Используйте /start для начала опроса или /help для справки.'
    )

# Запуск бота
if __name__ == '__main__':
    print('Бот запущен...')
    bot.infinity_polling()
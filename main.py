import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import google.generativeai as genai

# --- БАПТАУЛАР ---
TOKEN = "8763271423:AAGGGfyeJpFG0MeKY4kaPTT_tjQZ1Ikt5NA"
AI_API_KEY = "AIzaSyDWQP3LwhjJpwcbKVvKXOamu0DKT_iMlWkAIzaSyDWQP3LwhjJpwcbKVvKXOamu0DKT_iMlWk" # Осы жерге Gemini кілтін қой

genai.configure(api_key=AI_API_KEY)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- ATAKSHOP "МИЫ" (SYSTEM PROMPT) ---
SYSTEM_PROMPT = """
Сен — 'ATAKSHOP' киім және кроссовкалар дүкенінің кәсіби сатушы-консультантысың. 

БІЗДІҢ МЕКЕН-ЖАЙЛАРЫМЫЗ:
📍 Астана, Мәңгілік Ел 40
📍 Алматы, Назарбаев 174А
📍 Қарағанды, Бұхар Жырау 55
📍 Бішкек, Қалық Ақиев 11

ТАУАРЛАР ЖӘНЕ БАҒАЛАР:
- Nike x Corteiz Ветровка — 18 990 kzt
- Nike x Corteiz Штаны — 12 990 kzt
- Ветровки Nike (басқа түрлері) — 15 990 kzt
- Ремень Gucci — 4 990 kzt
- Кроссовкалар — бағасы модельге байланысты (орташа 25 000 - 45 000 kzt)

ЕРЕЖЕЛЕР:
1. Сөйлеу мәнері: Сабырлы, кәсіби және көмектесуге дайын.
2. Жеткізу: СДЭК немесе Қазпочта арқылы бүкіл Қазақстанға жібереміз.
3. Тапсырыс беру: Клиент сатып алғысы келсе, оған @atak_dostavka менеджеріне жазу керектігін айт.
4. Каталог: Толық каталогты t.me/atakshop каналынан көруге болатынын ескерт.
"""

async def call_ai(user_text):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        full_query = f"{SYSTEM_PROMPT}\n\nКлиент: {user_text}"
        response = model.generate_content(full_query)
        if response and response.text:
            return response.text
        return "Кешіріңіз, қазір жауап бере алмай тұрмын. Сәлден соң қайталаңыз."
    except Exception as e:
        print(f"Gemini Error: {e}")
        return "Байланыс үзілді, бірақ біз жұмыс істеп тұрмыз! Сұрағыңызды қайта жазыңызшы."

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Қайырлы күн! ATAKSHOP дүкеніне қош келдіңіз! 🔥\n\n"
        "Бізде ең сәнді киімдер мен кроссовкалар бар.\n"
        "Не қызықтырады? Бағасын немесе адресімізді сұрасаңыз болады."
    )

@dp.message()
async def chat(message: types.Message):
    # Бот ойланып жатқанын көрсету
    status_msg = await message.answer("Ойланып жатырмын... ⏳")
    
    ai_response = await call_ai(message.text)
    
    # "Ойланып жатырмын" дегенді нақты жауаппен ауыстыру
    await status_msg.edit_text(ai_response)

async def main():
    print("Бот іске қосылды...")
    await dp.start_polling(bot)

if __name__ == "__main__":
     asyncio.run(main())

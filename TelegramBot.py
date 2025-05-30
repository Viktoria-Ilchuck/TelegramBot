import asyncio

from aiogram import Bot
import paho.mqtt.client as mqtt
import asyncio
from aiogram import Bot
import paho.mqtt.client as mqtt
import json

TOKEN = "7751997779:AAFHJTDZVQ1OwSulVRlOLhqL0et8igcnr98"
CHAT_ID = 1727886974
TOPIC = "/Vika/itstep"
BROKER = "broker.mqtt.cool"
PORT = 1883

bot = Bot(token=TOKEN)
loop = asyncio.get_event_loop()

def format_json_string(json_string):
    try:
        data = json.loads(json_string)
        content = data.get("content", {})
        temp = content.get("temp", "N/A")
        hum = content.get("hum", "N/A")
        light = content.get("light", "N/A")

        message = (
            f"🌡 Температура: {temp} °C\n"
            f"💧 Вологість: {hum} %\n"
            f"💡 Освітлення: {light} %"
        )
        return message
    except Exception as e:
        print(f"Помилка обробки JSON: {e}")
        return "❌ Помилка отримання даних"

async def send_telegram_message(message):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
        print(f"Повідомлення надіслано: {message}")
    except Exception as e:
        print(f"Помилка надсилання: {e}")

def on_connect(client, userdata, flags, rc):
    print(f"Підключено з кодом: {rc}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    text = msg.payload.decode()
    print(f"Отримано повідомлення: {text}")

    formatted = format_json_string(text)
    asyncio.run_coroutine_threadsafe(send_telegram_message(formatted), loop)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_start()

print("Бот запущено. Чекаю повідомлення...")

try:
    loop.run_forever()
except KeyboardInterrupt:
    print("Зупинка Бота...")
finally:
    client.loop_stop()
    client.disconnect()
    loop.run_until_complete(bot.session.close())
    loop.close()
import asyncio
import json



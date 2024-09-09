from telethon import TelegramClient, events
from dotenv import load_dotenv
import asyncio
import random
import os
import datetime


load_dotenv ()
# Вставьте сюда свои данные
api_id = str(os.getenv('id'))
api_hash = str(os.getenv('hash'))
phone_number = str(os.getenv('number'))

# Список каналов. Для супергрупп с топиками используйте кортеж: (имя канала, ID топика)
channels = [
    str(os.getenv('channel')),  # Обычный канал
    (str(os.getenv('channelTwo')), 2637)  # Супергруппа с топиком (имя канала, ID топика)
]

# Добавляем параметры для эмуляции устройства
client = TelegramClient(
    str(os.getenv('suka')), api_id, api_hash,
    system_version='4.16.30-vxCUSTOM',  # Версия системы
    device_model='PC',                  # Модель устройства
    app_version='7.2.1'                 # Версия приложения
)

def generate_random_series():
    """Генерирует случайную серию для текущей даты."""
    today = datetime.datetime.now().strftime('%Y%m%d')
    random_number = random.randint(1000, 9999)
    return f"{today}-{random_number}"

async def main():
    try:
        await client.start(phone_number)
        print("Клиент запущен.")
        
        while True:
            now = datetime.datetime.now()

            # Проверка времени: запускаем отправку сообщений в 16:20
            if now.hour == 16 and now.minute == 20:
                print("Наступило время 16:20, начинаем отправку сообщений...")
                
                # Получаем последние 1000 сообщений из первого канала
                messages = await client.get_messages(channels[0], limit=1000)
                print(f"Получено сообщений: {len(messages)}")
                
                # Фильтруем сообщения для нахождения видео
                video_messages = [msg for msg in messages if msg.video]
                
                if video_messages:
                    # Рандомизация среди сообщений с видео
                    random_video = random.choice(video_messages)
                    print(f"Выбрано видео ID: {random_video.id}")
                    
                    # Получаем текстовое содержимое сообщения
                    message_text = random_video.text or ""
                    print(f"Текст сообщения: {message_text}")
                    
                    # Генерируем случайную серию
                    random_series = generate_random_series()
                    print(f"Случайная серия: {random_series}")
                    
                    # Формируем новый текст сообщения
                    new_message_text = f"{message_text}\n\nСлучайная серия на сегодня\n\n[Все серии южного парка](https://t.me/southsparkvse)"
                    new_message_textTwo = f"{message_text}\n\nСлучайная серия на сегодня\n\n[Наш другой канал с фильмами и сериалами](https://t.me/apelsinovypodval)"
                    
                    for channel in channels:
                        if isinstance(channel, tuple):
                            # Если это супергруппа с топиком
                            channel_name, topic_id = channel
                            await client.send_message(
                                channel_name,  # Назначение (супергруппа)
                                new_message_text,  # Новый текст сообщения
                                file=random_video.video,  # Пересылаем видео
                                reply_to=topic_id  # Отправляем в конкретный топик
                            )
                            print(f"Сообщение с видео и текстом переслано в топик {topic_id} супергруппы {channel_name}.")
                        else:
                            # Если это обычный канал
                            await client.send_message(
                                channel,  # Назначение (канал)
                                new_message_textTwo,  # Новый текст сообщения
                                file=random_video.video  # Пересылаем видео
                            )
                            print(f"Сообщение с видео и текстом переслано в {channel}.")
                    
                    break  # Выход из цикла после успешной пересылки
                else:
                    print("Видео не найдено, пробуем снова.")
                    await asyncio.sleep(10)  # Ожидание перед новой попыткой
            else:
                print("Ждем наступления времени 16:20...")
                await asyncio.sleep(60)  # Ожидание 1 минуты перед проверкой времени
    
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    
    finally:
        await client.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

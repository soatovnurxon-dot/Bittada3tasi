import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

# BotFather'dan olgan tokeningizni shu yerga yozing
TOKEN = "9019949541:AAHi0qY5dHHyZf4_Tl3f8z5CKO_JmXTIrkk"

# 3 ta guruhning ID raqamlari (manfiy sonlar bilan boshlanadi)
GROUP_IDS = [-1003018040083, -1002986742269,  -1002129889527]

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(F.chat.type.in_({"group", "supergroup"}))
async def sync_groups(message: Message):
    # Agar xabar biz ko'rsatgan 3 ta guruhning biridan kelgan bo'lsa
    if message.chat.id in GROUP_IDS:
        # Qolgan ikki guruhga xabarni nusxalaymiz
        for group_id in GROUP_IDS:
            if group_id != message.chat.id:
                try:
                    await bot.copy_message(
                        chat_id=group_id,
                        from_chat_id=message.chat.id,
                        message_id=message.message_id
                    )
                except Exception as e:
                    logging.error(f"Xatolik {group_id} guruhga yuborishda: {e}")

async def main():
    logging.basicConfig(level=logging.INFO)
    print("Sinxronizatsiya boti ishga tushdi...")
    # Eski xabarlarni tashlab yuborib, yangilaridan boshlash
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
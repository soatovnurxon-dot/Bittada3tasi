import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from fastapi import FastAPI
import uvicorn

# Token va guruh ID'larini Render muhitidan o'qiymiz
TOKEN = os.getenv("TOKEN")
GROUP_IDS_STR = os.getenv("GROUP_IDS", "")
GROUP_IDS = [int(gid.strip()) for gid in GROUP_IDS_STR.split(",") if gid.strip()]

bot = Bot(token=TOKEN)
dp = Dispatcher()

# FastAPI serverini yaratamiz
app = FastAPI()

@app.get("/")
async def index():
    return {"status": "Bot 24/7 ishlayapti!"}

@dp.message(F.chat.type.in_({"group", "supergroup"}))
async def sync_groups(message: Message):
    if message.chat.id in GROUP_IDS:
        # Yuboruvchi ismini aniqlaymiz
        sender_name = message.from_user.full_name if message.from_user else "Foydalanuvchi"
        
        for group_id in GROUP_IDS:
            if group_id != message.chat.id:
                try:
                    # Agar matn bo'lsa, uni yuboruvchi ismi bilan birga yuboramiz
                    if message.text:
                        caption_text = f"{message.text}\n\n👤 <i>{sender_name}</i>"
                        await bot.send_message(chat_id=group_id, text=caption_text, parse_mode="HTML")
                    else:
                        # Rasm, video yoki boshqa media bo'lsa o'z holicha nusxalaymiz
                        await bot.copy_message(
                            chat_id=group_id,
                            from_chat_id=message.chat.id,
                            message_id=message.message_id
                        )
                except Exception as e:
                    logging.error(f"Xatolik {group_id} guruhga yuborishda: {e}")

# FastAPI ishga tushganda botni fon rejimida ishga tushiramiz
@app.on_event("startup")
async def startup_event():
    logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook(drop_pending_updates=True)
    asyncio.create_task(dp.start_polling(bot))
    print("Sinxronizatsiya boti ishga tushdi...")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)

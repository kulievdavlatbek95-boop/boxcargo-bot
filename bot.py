from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio

TOKEN = '9096400625:AAFj_x9x3gCtmjnqu6gp3jfPKDXJqDcajg'
CHANNEL_ID = '@BoxCargoofficial'
INSTAGRAM_URL = 'https://www.instagram.com/yoko_zfd?psln=MTA1dZe3EdU0Zmchdg=='

dp = Dispatcher()

async def check_sub_channel(bot: Bot, user_id: int):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status not in ['left', 'kicked']:
            return True
    except Exception:
        pass
    return False

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    is_subscribed = await check_sub_channel(message.bot, user_id)

    if not is_subscribed:
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(text="📢 Подписаться на наш Telegram-канал", url="https://t.me/BoxCargoofficial"))
        builder.row(types.InlineKeyboardButton(text="📸 Подписаться на наш Instagram", url=INSTAGRAM_URL))
        builder.row(types.InlineKeyboardButton(text="🔄 Я всё подписался", callback_data="check_sub"))

        await message.answer(
            "Здравствуйте! 👋 Добро пожаловать в службу доставки **BOXCARGO**.\n\n"
            "Чтобы начать пользоваться ботом, пожалуйста, подпишитесь на наши социальные сети:",
            reply_markup=builder.as_markup(),
            parse_mode="Markdown"
        )
    else:
        await message.answer("Спасибо, что вы с нами! Добро пожаловать в BOXCARGO. Чем мы можем вам помочь?")

@dp.callback_query(lambda c: c.data == "check_sub")
async def process_check_sub(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    is_subscribed = await check_sub_channel(callback.bot, user_id)

    if is_subscribed:
        await callback.message.edit_text(
            "✅ Спасибо за подписку! Теперь вам доступен весь функционал бота BOXCARGO.\n\n"
            "Оварга расонидан дар муддати 15-25 руз. Нарх: 1кг то 10кг — 25 сомони, 10кг+ — 23 сомони."
        )
    else:
        await callback.answer(
            "❌ Вы еще не подписались на Telegram-канал! Пожалуйста, подпишитесь.", 
            show_alert=True
        )

async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

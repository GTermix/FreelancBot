import logging
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from keyboards.inline.subscription import check_subs
from utils.misc.subscription import check as subscription_check
from data.config import CHANNELS
from utils.misc import subscription
from loader import bot


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            user = update.message.from_user.id
            logging.info(user)
            if update.message.text in ['/start', 'Bot ishga tushdi']:
                return
        elif update.callback_query:
            user = update.callback_query.from_user.id
            logging.info(user)
            if update.callback_query.data in ['check_subs', ]:
                return
        logging.info(user)
        channels_format = list()
        final_status = True
        for channel in CHANNELS:
            status = await subscription_check(user_id=user, channel=channel)
            final_status *= status
            channel = await bot.get_chat(chat_id=channel)
            if not status:
                invite_link = await channel.export_invite_link()
                channels_format.append(invite_link)
        if not final_status:
            await update.message.answer(f"Quyidagi kanallarga obuna bo'ling 👇",
                                        reply_markup=check_subs(channels_format))
            raise CancelHandler()

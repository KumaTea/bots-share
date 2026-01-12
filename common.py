import pyrogram


pyrogram_version = tuple(map(int, pyrogram.__version__.split('.')))
is_old_pyrogram = pyrogram_version <= (2, 0, 106)


# disable webpage preview option
# usage: await client.send_message(chat_id, text, **no_preview)
if is_old_pyrogram:
    no_preview = {'disable_web_page_preview': True}
else:
    # from pyrogram.types import LinkPreviewOptions
    from pyrogram.types.messages_and_media.link_preview_options import LinkPreviewOptions
    no_preview = {'link_preview_options': LinkPreviewOptions(is_disabled=True)}


# old `quote` parameter is deprecated
# because Telegram has assigned "quote" as a new feature
if is_old_pyrogram:
    no_quote = {'quote': False}
    do_quote = {'quote': True}
else:
    # from pyrogram.types import ReplyParameters
    from pyrogram.types.messages_and_media.reply_parameters import ReplyParameters
    no_quote = {'reply_parameters': ReplyParameters(message_id=None)}
    do_quote = {}  # default behavior is to reply

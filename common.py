import pyrogram


pyrogram_version = tuple(map(int, pyrogram.__version__.split('.')))
is_old_pyrogram = pyrogram_version <= (2, 0, 106)


# disable webpage preview option
# usage: await client.send_message(chat_id, text, **no_preview)
if is_old_pyrogram:
    no_preview = {'disable_web_page_preview': True}
else:
    from pyrogram.types.messages_and_media.link_preview_options import LinkPreviewOptions
    no_preview = {'link_preview_options': LinkPreviewOptions(is_disabled=True)}

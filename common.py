import pyrogram


pyrogram_version = tuple(map(int, pyrogram.__version__.split('.')))
is_old_pyrogram = pyrogram_version <= (2, 0, 106)

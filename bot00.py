import sys
import glob
import gzip
import zipfile
import json
import yaml
import logging
import platform
import asyncio
from aiogram import (
    Bot, Dispatcher, types,
    __version__ as aiogram__version__, __api_version__ as aiogram__api_version__)
from aiohttp import __version__ as aiohttp__version__
from bot_config import TELEGRAM_BOT_TOKENs


async def re_start_handler(event: types.Message):
    event_example = {
        "message_id": 1706,
        "from": {
            "id": 120752770,
            "is_bot": False,
            "first_name": "Alexandr",
            "last_name": "Avramchikov",
            "username": "Alexandr_Avramchikov",
            "language_code": "ru"
        },
        "chat": {
            "id": 120752770,
            "first_name": "Alexandr",
            "last_name": "Avramchikov",
            "username": "Alexandr_Avramchikov",
            "type": "private"},
        "date": 1601559739,
        "text": "/start",
        "entities": [
            {"offset": 0, "length": 6, "type": "bot_command"}
        ]}
    print("debug", event)
    await event.answer(
        f"Hello, {event.from_user.get_mention(as_html=True)} 👋!",
        parse_mode=types.ParseMode.HTML,
    )


async def main(bot_token: str):
    bot = Bot(token=bot_token)
    try:
        disp = Dispatcher(bot=bot)
        disp.register_message_handler(re_start_handler, commands={"start", "restart"})
        # disp.register_message_handler(re_start_handler, content_types=)
        await disp.start_polling()
    finally:
        await bot.close()


#
#
#
def list_from_file_mask_gz(file_mask_gz: str = './config/*.gz', encoding: str = "utf-8") -> list:
    """ Получить список из содержимого в архивных gz-файлах """

    buffer_list = list()
    files_list = glob.glob(file_mask_gz)
    files_list.sort()  # соблюсти очередность от сортировки по имени файла
    for filename in files_list:
        try:
            if filename[-9:] in (".json.zip", ):
                with zipfile.ZipFile(filename) as zf:
                    for zfn in zf.filelist:
                        with zf.open(zfn) as f:
                            buffer_list.append({
                                "filename": zfn.filename, "path": filename, "type": "json.zip",
                                "_": json.loads(f.read().decode(encoding=encoding)), })
            elif filename[-8:] in (".json.gz", ):
                with gzip.open(filename, 'rb') as f:
                    buffer_list.append({
                        "filename": f.filename, "path": filename, "type": "json.gz",
                        "_": json.loads(f.read().decode(encoding=encoding)), })
            elif filename[-5:] in (".json", ):
                with open(filename, 'rb') as f:
                    buffer_list.append({
                        "filename": filename, "path": filename, "type": "json",
                        "_": json.loads(f.read().decode(encoding=encoding)), })
            elif filename[-9:] in (".yaml.zip", ):
                with zipfile.ZipFile(filename) as zf:
                    for zfn in zf.filelist:
                        with zf.open(zfn) as f:
                            buffer_list.append({
                                "filename": zfn.filename, "path": filename, "type": "yaml.zip",
                                "_": [x for x in yaml.safe_load_all(f.read().decode(encoding=encoding))], })
            elif filename[-8:] in (".yaml.gz", ):
                with gzip.open(filename, 'rb') as f:
                    buffer_list.append({
                        "filename": f.filename, "path": filename, "type": "yaml.gz",
                        "_": [x for x in yaml.safe_load_all(f.read().decode(encoding=encoding))], })
            elif filename[-5:] in (".yaml", ):
                with open(filename, 'rb') as f:
                    buffer_list.append({
                        "filename": filename, "path": filename, "type": "yaml",
                        "_": [x for x in yaml.safe_load_all(f.read().decode(encoding=encoding))], })
        except Exception as e:
            buffer_list.append({"error": True, "filename": filename, "message": f"in {filename}: {str(e)}", })
    return buffer_list


def norm_f(fl: list) -> list:
    """ Провести нормализацию в единый словарь """
    nn = list()
    for x in fl:
        if x.get("error", False) is False:
            nn.append(x["_"])
    return nn


if __name__ == '__main__':

    if True:
        event_example = {
            "message_id": 1706,
            "from": {
                "id": 120752770,
                "is_bot": False,
                "first_name": "Alexandr",
                "last_name": "Avramchikov",
                "username": "Alexandr_Avramchikov",
                "language_code": "ru"
            },
            "chat": {
                "id": 120752770,
                "first_name": "Alexandr",
                "last_name": "Avramchikov",
                "username": "Alexandr_Avramchikov",
                "type": "private"},
            "date": 1601559739,
            "text": "/start",
            "entities": [
                {"offset": 0, "length": 6, "type": "bot_command"}
            ]}
        # print(yaml.dump(event_example))
        import pprint
        fff = list_from_file_mask_gz(file_mask_gz='./config/*.*')
        pprint.pprint(fff)
        # print(fff)
        ggg = norm_f(fff)
        pprint.pprint(ggg)
        exit(0)
        pass

    logging.basicConfig(level=logging.DEBUG)
    print(
        f"OS {platform.platform()}"
        f", Python {sys.version}"
        f", Released API {aiogram__api_version__}"
        f", aiogram {aiogram__version__}"
        f", aiohttp {aiohttp__version__}")
    asyncio.run(main(bot_token=TELEGRAM_BOT_TOKENs["telegram_debug"][0]["token"]))

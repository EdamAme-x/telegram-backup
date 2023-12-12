from telethon import TelegramClient, events, functions

import time
import json
import asyncio

print('\033[93mWelcome to Telegram backup script!\033[0m')
print('\033[93m[Control+C] to exit\033[0m')
print('\033[93mバグ報告は @amex2189 まで\033[0m')

async def main():
    try:
        print("\033[94mhttps://my.telegram.org/apps でAPI IDとAPI Hashを取得してください！\033[0m")
        api_id = 0
        try:
            api_id = int(input('\033[94mApi ID: \033[0m'))
        except ValueError:
            print('\033[91mApi IDは数値で入力してください！\033[0m')
            exit()
        api_hash = input('\033[94mApi Hash: \033[0m')
        client = TelegramClient('client', api_id, api_hash)
        await client.start()
        dialogs = await client.get_dialogs()

        data = { "ユーザー": [], "チャンネル": [], "グループ": [], "未保存": { "チャンネル": [], "グループ": [] } }

        for dialog in dialogs:
            if dialog.is_user and not (dialog.name == '' and not dialog.entity.phone and not dialog.entity.phone):
                data['users'].append({
                    "name": dialog.name,
                    "username": dialog.entity.username,
                    "phone": dialog.entity.phone,
                    "bot": dialog.entity.bot
                })
            elif dialog.is_group:
                try:
                    result = await client(functions.messages.ExportChatInviteRequest(dialog.entity.id))
                    data['groups'].append({
                        "name": dialog.name,
                        "title": dialog.entity.title,
                        "link": result.link
                    })
                except:
                    data['unsaved']['groups'].append({
                        "name": dialog.name,
                    })
            elif dialog.is_channel:
                if not dialog.entity.username:
                    data['unsaved']['channels'].append({
                        "name": dialog.name
                    })
                else:
                    data['channels'].append({
                        "name": dialog.name,
                        "username": dialog.entity.username,
                        "link": f'https://t.me/{dialog.entity.username}',
                        "participants_count": dialog.entity.participants_count
                    })


        filename = f'tg-backup-{round(time.time())}.json'
        with open(filename, "w") as fs:
            fs.write(json.dumps(data, indent=4))

        print(f'\033[92mSaved to: {filename}\033[0m')
    except Exception as e:
        print(e)
        print("電話番号、API ID、API Hashが正しいか確認してください 電話番号は国際形式で入力して下さい！(eg: +819012345678)")

asyncio.run(main())

# Forked by https://github.com/Normalizex/telegram-backup# を元に改造

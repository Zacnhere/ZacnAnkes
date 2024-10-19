import re

from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import *

from Teiko import *



def ikb(rows=[]):
    lines = []
    for row in rows:
        line = []
        for button_data in row:
            if isinstance(button_data, str):
                match = re.match(r"\| ([^|]+) - ([^|]+) \|", button_data)
                if match:
                    text, action = match.groups()
                    button = InlineKeyboardButton(text=text.strip(), url=action.strip() if action.startswith("http") else None, callback_data=action.strip() if not action.startswith("http") else None)
                    line.append(button)
                else:
                    raise ValueError("Invalid button data format.")
            elif isinstance(button_data, tuple) and len(button_data) == 2:
                button = InlineKeyboardButton(text=button_data[0], url=button_data[1] if isinstance(button_data[1], str) and button_data[1].startswith("http") else None, callback_data=button_data[1] if isinstance(button_data[1], str) and not button_data[1].startswith("http") else None)
                line.append(button)
            else:
                raise ValueError("Invalid button data format.")
        lines.append(line)
    return InlineKeyboardMarkup(inline_keyboard=lines)



class BTN:
    def START(message):
        button = ikb([
            ["| Menu Help - AH |"],
            [
              "| Group - https://t.me/Zacn_Support |",
              "| Owner - https://t.me/ZacnBoys |",
            ]
        ])
        return button
            

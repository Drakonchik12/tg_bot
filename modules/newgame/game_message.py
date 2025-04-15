import json
import random
import os



def load_role_messages(role):
    try:
        filename = os.path.join("data", f"{role}.json")

        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("messages", [])
    except Exception as e:
        print(f"Помилка при завантаженні фраз для ролі {role}: {e}")
        return []


def assign_messages_to_npcs(npc_list, user_nickname):
    npc_messages = []
    
    for npc in npc_list:
        if npc.role == "Мафія":
            messages = load_role_messages("mafia")
        elif npc.role == "Мирний":
            messages = load_role_messages("peaceful")
        elif npc.role == "Комісар":
            messages = load_role_messages("commissioner")
        elif npc.role == "Лікар":
            messages = load_role_messages("doctor")
        else:
            messages = []

        if messages:
            # Вибираємо випадкове повідомлення
            npc_message = random.choice(messages)
            
            # Випадково вирішуємо, чи замінити [персонаж] на ім'я NPC чи на нік користувача
            if "[персонаж]" in npc_message:
                replacement_name = random.choice(npc_list).name if random.random() > 0.3 else user_nickname
                npc_message = npc_message.replace("[персонаж]", replacement_name)

            npc_messages.append((npc.name, npc_message))
        else:
            npc_messages.append((npc.name, "Не вдалося знайти повідомлення для цієї ролі."))

    return npc_messages


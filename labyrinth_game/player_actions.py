from labyrinth_game.constants import ROOMS


def get_input(prompt="> "):
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def show_inventory(game_state):
    if game_state["player_inventory"]:
        print("\nВаш инвентарь:")
        for item in game_state["player_inventory"]:
            print(f"  - {item}")
    else:
        print("\nВаш инвентарь пуст.")


def move_player(game_state, direction):
    from labyrinth_game.utils import describe_current_room, random_event

    current_room = game_state["current_room"]
    room_data = ROOMS[current_room]

    if direction in room_data["exits"]:
        next_room = room_data["exits"][direction]
        
        if next_room == "treasure_room":
            if "rusty_key" in game_state["player_inventory"]:
                print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.")
                game_state["current_room"] = next_room
                game_state["steps_taken"] += 1
                describe_current_room(game_state)
                random_event(game_state)
            else:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
        else:
            game_state["current_room"] = next_room
            game_state["steps_taken"] += 1
            describe_current_room(game_state)
            random_event(game_state)
    else:
        print("Нельзя пойти в этом направлении.")


def take_item(game_state, item_name):
    current_room = game_state["current_room"]
    room_data = ROOMS[current_room]

    if item_name == "treasure_chest":
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return

    if item_name in room_data["items"]:
        room_data["items"].remove(item_name)
        game_state["player_inventory"].append(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state, item_name):
    if item_name not in game_state["player_inventory"]:
        print("У вас нет такого предмета.")
        return

    if item_name == "torch":
        print(
            "Вы зажигаете факел. Вокруг стало намного светлее, "
            "и вы чувствуете себя увереннее."
        )
    elif item_name == "sword":
        print("Вы сжимаете рукоять меча. Чувство уверенности наполняет вас.")
    elif item_name == "bronze_box":
        print("Вы открываете бронзовую шкатулку...")
        if "rusty_key" not in game_state["player_inventory"]:
            print("Внутри лежит ржавый ключ!")
            game_state["player_inventory"].append("rusty_key")
        else:
            print("Шкатулка пуста.")
    elif item_name == "lantern":
        print("Фонарь освещает путь перед вами, раскрывая скрытые детали.")
    elif item_name == "ancient_book":
        print(
            "Вы листаете древнюю книгу. Страницы содержат старинные карты "
            "и криптические записи."
        )
    elif item_name == "crystal":
        print(
            "Кристалл начинает светиться в ваших руках, излучая мягкое голубое сияние."
        )
    else:
        print(f"Вы не знаете, как использовать {item_name}.")

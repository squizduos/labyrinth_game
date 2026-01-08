from labyrinth_game.constants import ROOMS
from labyrinth_game.player_actions import get_input


def describe_current_room(game_state):
    current_room = game_state["current_room"]
    room_data = ROOMS[current_room]

    print(f"\n== {current_room.upper().replace('_', ' ')} ==")
    print(room_data["description"])

    if room_data["items"]:
        print("\nЗаметные предметы:")
        for item in room_data["items"]:
            print(f"  - {item}")

    print("\nВыходы:", ", ".join(room_data["exits"].keys()))

    if room_data["puzzle"]:
        print("\nКажется, здесь есть загадка (используйте команду solve).")


def solve_puzzle(game_state):
    current_room = game_state["current_room"]
    room_data = ROOMS[current_room]

    if current_room == "treasure_room" and "treasure_chest" in room_data["items"]:
        attempt_open_treasure(game_state)
        return

    if not room_data["puzzle"]:
        print("Загадок здесь нет.")
        return

    question, correct_answer = room_data["puzzle"]
    print(f"\n{question}")

    answer = get_input("Ваш ответ: ")

    if answer == correct_answer:
        print("\nПравильно! Загадка решена!")
        room_data["puzzle"] = None

        if current_room == "hall":
            print("Пьедестал открывается, и вы находите серебряный медальон!")
            game_state["player_inventory"].append("silver_medallion")
        elif current_room == "trap_room":
            print("Плиты успокаиваются, путь безопасен!")
        elif current_room == "library":
            print("Один из свитков раскрывается, показывая тайную карту!")
            game_state["player_inventory"].append("secret_map")
        elif current_room == "secret_chamber":
            print("Стена отодвигается, открывая тайник с золотым ключом!")
        elif current_room == "ancient_cave":
            print("Пещера содрогается, открывая скрытый проход!")
    else:
        print("Неверно. Попробуйте снова.")


def attempt_open_treasure(game_state):
    if "treasure_key" in game_state["player_inventory"]:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        current_room = game_state["current_room"]
        room_data = ROOMS[current_room]
        if "treasure_chest" in room_data["items"]:
            room_data["items"].remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
        return

    print("Сундук заперт. Нужен особый ключ, но можно попробовать ввести код.")
    choice = get_input("Ввести код? (да/нет): ")

    if choice == "да":
        current_room = game_state["current_room"]
        room_data = ROOMS[current_room]
        if room_data["puzzle"]:
            question, correct_answer = room_data["puzzle"]
            print(f"\n{question}")
            code = get_input("Введите код: ")

            if code == correct_answer:
                print("\nКод верный! Замок открывается!")
                if "treasure_chest" in room_data["items"]:
                    room_data["items"].remove("treasure_chest")
                print("В сундуке сокровище! Вы победили!")
                game_state["game_over"] = True
            else:
                print("Неверный код. Сундук остается закрытым.")
    else:
        print("Вы отступаете от сундука.")


def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")

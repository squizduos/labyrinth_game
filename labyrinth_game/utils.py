import math

from labyrinth_game.constants import ROOMS
from labyrinth_game.player_actions import get_input


def pseudo_random(seed, modulo):
    print(seed, modulo)
    x = math.sin(seed * 12.9898) * 43758.5453
    fractional_part = x - math.floor(x)
    result = int(fractional_part * modulo)
    return result


def trigger_trap(game_state):
    print("Ловушка активирована! Пол стал дрожать...")
    
    inventory = game_state["player_inventory"]
    
    if inventory:
        item_count = len(inventory)
        random_index = pseudo_random(game_state["steps_taken"], item_count)
        lost_item = inventory.pop(random_index)
        print(f"Вы потеряли: {lost_item}")
    else:
        random_value = pseudo_random(game_state["steps_taken"], 10)
        print(random_value)
        if random_value < 3:
            print("Ловушка оказалась смертельной! Вы не смогли выжить...")
            game_state["game_over"] = True
        else:
            game_state["steps_taken"] += 1
            print("Вы чудом уцелели, но были близки к гибели!")


def random_event(game_state):
    event_chance = pseudo_random(game_state["steps_taken"], 10)
    
    if event_chance == 0:
        event_type = pseudo_random(game_state["steps_taken"] + 1, 3)
        current_room = game_state["current_room"]
        room_data = ROOMS[current_room]
        
        if event_type == 0:
            print("Вы нашли на полу монетку!")
            if "coin" not in room_data["items"]:
                room_data["items"].append("coin")
        elif event_type == 1:
            print("Вы слышите странный шорох...")
            if "sword" in game_state["player_inventory"]:
                print("Вы достаете меч, и существо отступает!")
        elif event_type == 2:
            if current_room == "trap_room" and "torch" not in game_state["player_inventory"]:
                print("Опасность! Без света вы не заметили ловушку!")
                trigger_trap(game_state)


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

    answer = get_input("Ваш ответ: ").strip()

    is_correct = False
    if answer == correct_answer:
        is_correct = True
    else:
        alternative_answers = {
            "10": ["десять", "ten"],
            "12": ["двенадцать", "twelve"],
        }
        if correct_answer in alternative_answers:
            if answer in alternative_answers[correct_answer]:
                is_correct = True

    if is_correct:
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
        if current_room == "trap_room":
            trigger_trap(game_state)


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


def show_help(COMMANDS):
    print("\nДоступные команды:")
    for command, description in COMMANDS.items():
        print(f"  {command:<16} - {description}")

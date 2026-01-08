#!/usr/bin/env python3

from labyrinth_game.constants import COMMANDS
from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle,
)


def process_command(game_state, command_line):
    """Обрабатывает команду игрока и выполняет соответствующее действие."""
    parts = command_line.split(maxsplit=1)
    if not parts:
        return

    command = parts[0]
    argument = parts[1] if len(parts) > 1 else None

    match command:
        case "look":
            describe_current_room(game_state)
        case "go":
            if argument:
                move_player(game_state, argument)
            else:
                print("Куда идти? Укажите направление (north/south/east/west).")
        case "north" | "south" | "east" | "west":
            move_player(game_state, command)
        case "take":
            if argument:
                take_item(game_state, argument)
            else:
                print("Что взять? Укажите название предмета.")
        case "use":
            if argument:
                use_item(game_state, argument)
            else:
                print("Что использовать? Укажите название предмета.")
        case "inventory" | "inv":
            show_inventory(game_state)
        case "solve":
            if game_state["current_room"] == "treasure_room":
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case "help":
            show_help(COMMANDS)
        case "quit" | "exit":
            print("Спасибо за игру!")
            game_state["game_over"] = True
        case _:
            print("Неизвестная команда. Введите 'help' для списка команд.")


def main() -> None:
    """Главная функция игры, инициализирует состояние и запускает игровой цикл."""
    game_state = {
        "player_inventory": [],
        "current_room": "entrance",
        "game_over": False,
        "steps_taken": 0,
    }

    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    while not game_state["game_over"]:
        command_line = get_input()
        if command_line:
            process_command(game_state, command_line)


if __name__ == "__main__":
    main()

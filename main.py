#!/usr/bin/python

import random
import urllib.parse
import requests
from time import sleep
import os, signal, sys
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich.style import Style
import pystyle
from pystyle import Colors, Colorate

from carparktool import CarParkTool


def обработчик_сигнала(sig, frame):
    print("\n Пока Пока...")
    sys.exit(0)


def градиентный_текст(текст, цвета):
    строки = текст.splitlines()
    высота = len(строки)
    ширина = max(len(строка) for строка in строки)
    красочный_текст = Text()
    for y, строка in enumerate(строки):
        for x, символ in enumerate(строка):
            if символ != " ":
                индекс_цвета = int(
                    (
                        (x / (ширина - 1 if ширина > 1 else 1))
                        + (y / (высота - 1 if высота > 1 else 1))
                    )
                    * 0.5
                    * (len(цвета) - 1)
                )
                индекс_цвета = min(
                    max(индекс_цвета, 0), len(цвета) - 1
                )  # Гарантируем, что индекс в пределах границ
                стиль = Style(color=цвета[индекс_цвета])
                красочный_текст.append(символ, style=стиль)
            else:
                красочный_текст.append(символ)
        красочный_текст.append("\n")
    return красочный_текст


def баннер(консоль):
    os.system("cls" if os.name == "nt" else "clear")
    название_бренда = "Подпишись на канал @dark_tool_cpm"
    название_бренда = "Подпишись на канал @dark_tool_cpm Пополнение баланса: @sad_sad2"

    текст = Text(название_бренда, style="bold black")

    консоль.print(текст)
    консоль.print(
        "[bold white] ============================================================[/bold white]"
    )
    консоль.print(
        "[bold yellow]      Пожалуйста, войдите в CPM перед использованием этого инструмента[/bold yellow]"
    )
    консоль.print("[bold red]      Совместное использование ключа доступа запрещено и будет заблокировано[/bold red]")
    консоль.print(
        "[bold white] ============================================================[/bold white]"
    )


def загрузить_данные_игрока(cpm):
    ответ = cpm.get_player_data()

    if ответ.get("ok"):
        данные = ответ.get("data")

        if all(key in данные for key in ["floats", "localID", "money"]):
            консоль.print(
                "[bold][red]========[/red][ ДАННЫЕ ИГРОКА ][red]========[/red][/bold]"
            )

            консоль.print(
                f"[bold white]   >> Имя        : {данные.get('Name', 'НЕ ОПРЕДЕЛЕНО')}[/bold white]"
            )
            консоль.print(
                f"[bold white]   >> LocalID     : {данные.get('localID', 'НЕ ОПРЕДЕЛЕНО')}[/bold white]"
            )
            консоль.print(
                f"[bold white]   >> Деньги      : {данные.get('money', 'НЕ ОПРЕДЕЛЕНО')}[/bold white]"
            )
            консоль.print(
                f"[bold white]   >> Монеты       : {данные.get('coin', 'НЕ ОПРЕДЕЛЕНО')}[/bold white]"
            )
        else:
            консоль.print(
                "[bold red] '! ОШИБКА: новые аккаунты должны хотя бы раз войти в игру (✘)[/bold red]"
            )
            exit(1)
    else:
        консоль.print(
            "[bold red] '! ОШИБКА: похоже, ваш логин не настроен правильно (✘)[/bold red]"
        )
        exit(1)


def загрузить_данные_ключа(cpm):
    данные = cpm.get_key_data()

    консоль.print(
        "[bold][red]========[/red][ ДАННЫЕ КЛЮЧА ДОСТУПА ][red]========[/red][/bold]"
    )

    консоль.print(
        f"[bold white]   >> Ключ доступа  [/bold white]: [black]{данные.get("access_key")}[/black]"
    )

    консоль.print(
        f"[bold white]   >> Telegram ID : {данные.get('telegram_id')}[/bold white]"
    )

    консоль.print(
        f"[bold white]   >> Баланс     : {данные.get('coins') if not данные.get('is_unlimited') else 'Безлимитный'}[/bold white]"
    )


def запросить_корректное_значение(содержание, тег, пароль=False):
    while True:
        значение = Prompt.ask(содержание, password=пароль)
        if not значение or значение.isspace():
            консоль.print(
                f"[bold red]{тег} не может быть пустым или состоять только из пробелов. Пожалуйста, попробуйте снова (✘)[/bold red]"
            )
        else:
            return значение


def загрузить_данные_клиента():
    ответ = requests.get("http://ip-api.com/json")
    данные = ответ.json()
    консоль.print(
        "[bold red] =============[bold white][ ЛОКАЦИЯ ][/bold white]=============[/bold red]"
    )
    консоль.print(
        f"[bold white]    >> Страна    : {данные.get('country')} {данные.get('zip')}[/bold white]"
    )
    консоль.print(
        "[bold red] ===============[bold white][ МЕНЮ ][/bold white]===========[/bold red]"
    )


def интерполировать_цвет(начальный_цвет, конечный_цвет, доля):
    start_rgb = tuple(int(начальный_цвет[i : i + 2], 16) for i in (1, 3, 5))
    end_rgb = tuple(int(конечный_цвет[i : i + 2], 16) for i in (1, 3, 5))
    интерполированный_rgb = tuple(
        int(начало + доля * (конец - начало)) for начало, конец in zip(start_rgb, end_rgb)
    )
    return "{:02x}{:02x}{:02x}".format(*интерполированный_rgb)


def радужный_градиент(имя_клиента):
    модифицированная_строка = ""
    количество_символов = len(имя_клиента)
    начальный_цвет = "{:06x}".format(random.randint(0, 0xFFFFFF))
    конечный_цвет = "{:06x}".format(random.randint(0, 0xFFFFFF))
    for i, символ in enumerate(имя_клиента):
        доля = i / max(количество_символов - 1, 1)
        интерполированный_цвет = интерполировать_цвет(начальный_цвет, конечный_цвет, доля)
        модифицированная_строка += f"[{интерполированный_цвет}]{символ}"
    return модифицированная_строка


if __name__ == "__main__":
    консоль = Console()
    signal.signal(signal.SIGINT, обработчик_сигнала)
    while True:
        баннер(консоль)
        почта_аккаунта = запросить_корректное_значение(
            "[bold][?] Почта аккаунта[/bold]", "Почта", password=False
        )
        пароль_аккаунта = запросить_корректное_значение(
            "[bold][?] Пароль аккаунта[/bold]", "Пароль", password=False
        )
        ключ_доступа = запросить_корректное_значение(
            "[bold][?] Ключ доступа[/bold]", "Ключ доступа", password=False
        )
        консоль.print("[bold yellow][%] Попытка входа[/bold yellow]: ", end=None)
        cpm = CarParkTool(ключ_доступа)
        ответ_входа = cpm.login(почта_аккаунта, пароль_аккаунта)
        if ответ_входа != 0:
            if ответ_входа == 100:
                консоль.print("[bold red]АККАУНТ НЕ НАЙДЕН (✘)[/bold red]")
                sleep(2)
                continue
            elif ответ_входа == 101:
                консоль.print("[bold red]НЕВЕРНЫЙ ПАРОЛЬ (✘)[/bold red]")
                sleep(2)
                continue
            elif ответ_входа == 103:
                консоль.print("[bold red]НЕДЕЙСТВИТЕЛЬНЫЙ КЛЮЧ ДОСТУПА (✘)[/bold red]")
                sleep(2)
                continue
            else:
                консоль.print("[bold red]ПОПРОБУЙТЕ СНОВА[/bold red]")
                консоль.print(
                    "[bold yellow] '! Примечание: убедитесь, что вы заполнили все поля![/bold yellow]"
                )
                sleep(2)
                continue
        else:
            консоль.print("[bold green]УСПЕШНО (✔)[/bold green]")
            sleep(1)
        while True:
            баннер(консоль)
            загрузить_данные_игрока(cpm)
            загрузить_данные_ключа(cpm)
            загрузить_данные_клиента()
            варианты = [
                "00",
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
                "16",
                "17",
                "18",
                "19",
                "20",
                "21",
                "22",
                "23",
                "24",
                "25",
                "26",
            ]
            консоль.print(
                "[bold yellow][bold white](01)[/bold white]: Увеличить Деньги                 [bold red]1.5K[/bold red][/bold yellow]"
            )
            консоль.print(
                "[bold yellow][bold white](02)[/bold white]: Увеличить Монеты                 [bold red]1.5K[/bold red][/bold yellow]"
            )
            консоль.print(
                "[bold yellow][bold white](03)[/bold white]: Ранг Короля                      [bold red]8K[/bold red][/bold yellow]"
            )
            консоль.print(
                "[bold yellow][bold white](04)[/bold white]: Изменить ID                      [bold red]4.5K[/bold red][/bold yellow]"
            )
            консоль.print(
                "[bold yellow][bold white](05)[/bold white]: Изменить Имя                    [bold red]100[/bold red][/bold yellow]"
            )
            консоль.print(
                "[bold yellow][bold white](06)[/bold white]: Изменить Имя (Радуга)          [bold red]100[/bold red][/bold yellow]"
            )
            консоль.print(
                "[bold yellow][bold white](07)[/bold white]: Номерные Знаки                  [bold red]2K[/bold red][/bold yellow]"
            )
            консоль.print(
                "[bold yellow][bold white](08)[/bold white]: Удалить Аккаунт                 [bold red]Бесплатно[/bold red][/bold yellow]"
            )
            консоль.print(
                "[bold yellow][bold white](09)[/bold white]: Зарегистрировать Аккаунт               [bold red]Бесплатно[/bold red][/bold yellow]"
            )
            консоль.print(
                "[bold yellow][bold white](10)[/bold white]: Удалить Друзей                 [bold red]500[/bold red][/bold yellow]"
            )
            консоль.print(
                "[bold yellow][bold white](11)[/bold white]: Разблокировать Lamborghini (только ios) [bold red]5K[/bold red][/bold yellow]"
            )
            консоль.print(
                "[bold yellow][bold white](12)[/bold white]: Разблокировать Все Машины                [bold red]6K[/bold red][/bold yellow]"
            )
            консоль.print(
                "[bold yellow][bold white](13)[/bold white]: Разблокировать Все Машины с Сиреной          [bold red]3.5K[/bold red][/bold yellow]"
            )
            консоль.print(
                "[bold yellow][bold white](14)[/bold white]: Разблокировать Двигатель W16              [bold red]4K[/bold red][/bold yellow]"
            )
            консоль.print(
                "[bold yellow][bold white](15)[/bold white]: Разблокировать Все Гудки               [bold red]3K[/bold red][/bold yellow]"
            )
            консоль.print(
                "[bold yellow][bold white](16)[/bold white]: Разблокировать Отключение Урона          [bold red]3K[/bold red][/bold yellow]"
            )
            консоль.print(
                "[bold yellow][bold white](17)[/bold white]: Разблокировать Безлимитное Топливо          [bold red]3K[/bold red][/bold yellow]"
            )
            консоль.print(
                "[bold yellow][bold white](18)[/bold white]: Разблокировать Дом 3                  [bold red]4K[/bold red][/bold yellow]"
            )
            консоль.print(
                "[bold yellow][bold white](19)[/bold white]: Разблокировать Дым                   [bold red]4K[/bold red][/bold yellow]"
            )
            консоль.print(
                "[bold yellow][bold white](20)[/bold white]: Разблокировать Колёса                  [bold red]4K[/bold red][/bold yellow]"
            )
            консоль.print(
                "[bold yellow][bold white](21)[/bold white]: Разблокировать Экипировку М           [bold red]3K[/bold red][/bold yellow]"
            )
            консоль.print(
                "[bold yellow][bold white](22)[/bold white]: Разблокировать Экипировку Ж           [bold red]3K[/bold red][/bold yellow]"
            )
            консоль.print(
                "[bold yellow][bold white](23)[/bold white]: Изменить Победы в Гонках               [bold red]1K[/bold red][/bold yellow]"
            )
            консоль.print(
                "[bold yellow][bold white](24)[/bold white]: Изменить Поражения в Гонках              [bold red]1K[/bold red][/bold yellow]"
            )
            консоль.print(
                "[bold yellow][bold white](25)[/bold white]: Клонировать Аккаунт                  [bold red]7K[/bold red][/bold yellow]"
            )
            консоль.print(
                "[bold yellow][bold white](26)[/bold white]: Настроить Л.С.                      [bold red]2.5K[/bold red][/bold yellow]"
            )
            консоль.print(
                "[bold yellow][bold white](0) [/bold white]: Выйти из Инструмента [/bold yellow]"
            )

            консоль.print(
                "[bold red]===============[bold white][ CPM DarkTool ][/bold white]===============[/bold red]"
            )

            сервис = IntPrompt.ask(
                f"[bold][?] Выберите сервис [red][1-{варианты[-1]} или 0][/red][/bold]",
                choices=варианты,
                show_choices=False,
            )

            консоль.print(
                "[bold red]===============[bold white][ CPM DarkTool ][/bold white]===============[/bold red]"
            )

            if сервис == 0:  # Выход
                консоль.print("[bold white] Спасибо за использование моего инструмента[/bold white]")
            elif сервис == 1:  # Увеличить Деньги
                консоль.print(
                    "[bold yellow][bold white][?][/bold white] Введите сколько денег вы хотите[/bold yellow]"
                )
                количество = IntPrompt.ask("[?] Количество")
                консоль.print("[%] Сохранение ваших данных: ", end=None)
                if количество > 0 and количество <= 500000000:
                    if cpm.set_player_money(количество):
                        консоль.print("[bold green]УСПЕШНО (✔)[/bold green]")
                        консоль.print(
                            "[bold green]======================================[/bold green]"
                        )
                        ответ = Prompt.ask(
                            "[?] Вы хотите выйти?", choices=["y", "n"], default="n"
                        )
                        if ответ == "y":
                            консоль.print(
                                "[bold white] Спасибо за использование моего инструмента[/bold white]"
                            )
                        else:
                            continue
                    else:
                        консоль.print("[bold red]ОШИБКА (✘)[/bold red]")
                        консоль.print(
                            "[bold red]пожалуйста, попробуйте позже! (✘)[/bold red]"
                        )
                        sleep(2)
                        continue
                else:
                    консоль.print("[bold red]ОШИБКА (✘)[/bold red]")
                    консоль.print("[bold red]пожалуйста, используйте корректные значения! (✘)[/bold red]")
                    sleep(2)
                    continue
            elif сервис == 2:  # Увеличить Монеты
                консоль.print(
                    "[bold yellow][bold white][?][/bold white] Введите сколько монет вы хотите[/bold yellow]"
                )
                количество = IntPrompt.ask("[?] Количество")
                print("[ % ] Сохранение ваших данных: ", end="")
                if количество > 0 and количество <= 500000:
                    if cpm.set_player_coins(количество):
                        консоль.print("[bold green]УСПЕШНО (✔)[/bold green]")
                        консоль.print(
                            "[bold green]======================================[/bold green]"
                        )
                        ответ = Prompt.ask(
                            "[?] Вы хотите выйти?", choices=["y", "n"], default="n"
                        )
                        if ответ == "y":
                            консоль.print(
                                "[bold white] Спасибо за использование моего инструмента[/bold white]"
                            )
                        else:
                            continue
                    else:
                        консоль.print("[bold red]ОШИБКА[/bold red]")
                        консоль.print("[bold red]Попробуйте снова[/bold red]")
                        sleep(2)
                        continue
                else:
                    консоль.print("[bold red]ОШИБКА[/bold red]")
                    консоль.print(
                        "[bold yellow] 'Пожалуйста, используйте корректные значения[/bold yellow]"
                    )
                    sleep(2)
                    continue
            elif сервис == 3:  # Ранг Короля
                консоль.print(
                    "[bold red][!] Примечание:[/bold red]: если ранг короля не появляется в игре, закройте и откройте её несколько раз.",
                    end=None,
                )
                консоль.print(
                    "[bold red][!] Примечание:[/bold red]: пожалуйста, не делайте ранг короля на одном аккаунте дважды.",
                    end=None,
                )
                sleep(2)
                консоль.print("[%] Присвоение вам ранга Короля: ", end=None)
                if cpm.set_player_rank():
                    консоль.print("[bold yellow] 'УСПЕШНО[/bold yellow]")
                    консоль.print(
                        "[bold yellow] '======================================[/bold yellow]"
                    )
                    ответ = Prompt.ask(
                        "[?] Вы хотите выйти?", choices=["y", "n"], default="n"
                    )
                    if ответ == "y":
                        консоль.print(
                            "[bold white] Спасибо за использование моего инструмента[/bold white]"
                        )
                    else:
                        continue
                else:
                    консоль.print("[bold red]ОШИБКА[/bold red]")
                    консоль.print("[bold red]Попробуйте снова[/bold red]")
                    sleep(2)
                    continue
            elif сервис == 4:  # Изменить ID
                консоль.print("[bold yellow] '[?] Введите ваш новый ID[/bold yellow]")
                новый_id = Prompt.ask("[?] ID")
                консоль.print("[%] Сохранение ваших данных: ", end=None)
                    len(новый_id) >= 8
                    and len(новый_id)
                    <= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999

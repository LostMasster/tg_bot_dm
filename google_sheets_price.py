import asyncio
from gspread import Client, Spreadsheet, Worksheet, service_account
import json
from igbore_git import table_id, table_link, client_init


def client_init_json() -> Client:
    """Создание клиента для работы с Google Sheets."""
    return service_account(filename=f'{client_init}')


def get_table_by_url(client: Client, table_url):
    """Получение таблицы из Google Sheets по ссылке."""
    return client.open_by_url(table_url)


def get_table_by_id(client: Client, table_url):
    """Получение таблицы из Google Sheets по ID таблицы."""
    return client.open_by_key(table_url)

def test_get_table(table_url: str, table_key: str):
    """Тестирование получения таблицы из Google Sheets."""
    client = client_init_json()
    table = get_table_by_url(client, table_url)
    print('Инфо по таблице по ссылке: ', table)
    table = get_table_by_id(client, table_key)
    print('Инфо по таблице по id: ', table)


def get_worksheet_info(table: Spreadsheet) -> dict:
    """Возвращает количество листов в таблице и их названия."""
    worksheets = table.worksheets()
    worksheet_info = {
        "count": len(worksheets),
        "names": [worksheet.title for worksheet in worksheets]
    }
    return worksheet_info


async def test_get_worksheet_info():
    # Создаем клиента и открываем таблицу
    client = client_init_json()
    table = get_table_by_id(client, table_id)

    # Получаем информацию о листах
    info = get_worksheet_info(table)
    print(f"Количество листов: {info['count']}")
    print("Названия листов:")
    for name in info['names']:
        print(name)
    with open("json_files_dm_sheet/json_name_worksheet.json", "w") as file:
        json.dump([i for i in info["names"]], file)
        print("Файл json_name_worksheet.json удачно записан")


# with open("json_name_worksheet.json", "r") as file:
#     name_worksheet = json.load(file)
#     print(name_worksheet)


def extract_data_from_sheet(table: Spreadsheet, sheet_name: str) -> list[dict]:
    """
    Извлекает данные из указанного листа таблицы Google Sheets и возвращает список словарей.

    :param table: Объект таблицы Google Sheets (Spreadsheet).
    :param sheet_name: Название листа в таблице.
    :return: Список словарей, представляющих данные из таблицы.
    """
    worksheet = table.worksheet(sheet_name)
    rows = worksheet.get_all_records()
    return rows


def test_get_data():
    """Тестирование извлечения данных из таблицы Google Sheets."""
    client = client_init_json()
    table = get_table_by_id(client, table_id)
    data = extract_data_from_sheet(table, ' iPhone 2025')
    # for i in data:
    #     print(i)
    with open("json_price_list_DM.json", "w") as file:
        json.dump(data, file)
    print("Файл json_price_list_DM.json удачно записан")


async def get_all_data():
    """Считываем все таблици из Google Sheets и сохраняем в json файлы"""
    client = client_init_json()
    table = get_table_by_id(client, table_id)
    with open("json_files_dm_sheet/json_name_worksheet.json", "r", encoding="utf-8") as file:
        info = json.load(file)
        for i in info:
            data = extract_data_from_sheet(table, i)
            with open(f"json_files_dm_sheet/{i}.json",
                      "w", encoding="utf-8") as f:
                json.dump(data, f)
        print("Данные с таблици сохранены")


# get_all_data()


# iPhone_2025 = test_get_data()
# # print(iPhone_2025)
# price_iphone = next((price["Wymiana szybki wyświetlacza \nGwarancja 90 dni"]
#                      for price in iPhone_2025 if price["Столбец 1"] == "iPhone XS"), None)
# print(price_iphone)
#
# price, material, time_of_rep = price_iphone.split('\n')
# print(f"Замена стекла дисплея будет стоить {price}. {time_of_rep}")


# model_numer = 14, model = Pro, service = repair-glas-lcd
async def get_iPhone_price(model_numer, model, service, language):
    lang_list = ["pl", "ua", "en", "ru"]
    if language not in lang_list:
        language = "pl"
    def is_no_text_in_sheet(language):
        if language == "pl":
            return (
                f"🤷 Cenę dla modelu iPhone {model_numer} {model} należy ustalać z konsultantem, "
                f"ponieważ koszt i dostępność części może zmieniać się w zależności od konkretnej sytuacji."
            )
        elif language == "ru":
            return (
                f"🤷 Стоимость для модели iPhone {model_numer} {model} необходимо уточнять у консультанта, "
                f"поскольку цена и доступность деталей могут меняться в зависимости от конкретной ситуации."
            )
        elif language == "ua":
            return (
                f"🤷 Ціну для моделі iPhone {model_numer} {model} слід узгоджувати з консультантом, "
                f"оскільки вартість і доступність деталей можуть змінюватися залежно від конкретної ситуації."
            )
        elif language == "en":
            return (
                f"🤷 The price for iPhone model {model_numer} {model} should be confirmed with a consultant, "
                f"as the cost and availability of parts may vary depending on the specific situation."
            )
    if service == "repair-glas-lcd":
        with open("json_files_dm_sheet/iPhone 2025.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            # print(data)
            price_iphone = next((price["Wymiana szybki wyświetlacza\nGwarancja 90 dni"]
                                 for price in data if price["Device_name"] == f"iPhone {model_numer}" +
                                 (f" {model}" if model else "")), None)
            print(price_iphone)
            if price_iphone == "-":
                return is_no_text_in_sheet(language)

            price, guarantee, time_of_rep = price_iphone.split('\n')

            if language == "pl":
                return (
                    f"Oto odpowiedź na Państwa zapytanie!\n"
                    f"✔️ Koszt wymiany szkła wyświetlacza w Państwa modelu iPhone {model_numer} {model} to"
                    f" {price}.\n⏱️ Średni czas naprawy {time_of_rep} godzin/ny (jeśli część jest na stanie!)\n"
                    f"🤝 Gwarancja: {guarantee} dni\n"
                )
            elif language == "ru":
                return (
                    f"Вот ответ на Ваш запрос!\n"
                    f"✔️ Стоимость замены стекла дисплея в модели iPhone {model_numer} {model} составляет {price}.\n"
                    f"⏱️ Среднее время ремонта {time_of_rep} часа/ов"
                    f"(если деталь в наличии!)\n"
                    f"🤝 Гарантия: {guarantee} дней\n"
                )
            elif language == "ua":
                return (
                    f"Ось відповідь на Ваш запит!\n"
                    f"✔️ Вартість заміни скла дисплея у моделі iPhone {model_numer} {model} становить {price}.\n"
                    f"⏱️ Середній час ремонту: {time_of_rep} годин/и"
                    f"(якщо деталь є в наявності!)\n"
                    f"🤝 Гарантія: {guarantee} днів\n"
                )
            elif language == "en":
                return (
                    f"Here is the answer to your inquiry!\n"
                    f"✔️ The cost of replacing the display glass for iPhone model {model_numer} {model} is {price}.\n"
                    f"⏱️ Average repair time: {time_of_rep} hour/s"
                    f"(if the part is in stock!)\n"
                    f"🤝 Warranty: {guarantee} days\n"
                )

    elif service == "display-replacement":
        with open("json_files_dm_sheet/iPhone 2025.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            price_iphone_orig = next((price["Wymiana LCD ORG\nGwarancja 180 dni"]
                                      for price in data if price["Device_name"] == f"iPhone {model_numer}" +
                                      (f" {model}" if model else "")), None)

            price_iphone_copy = next((price["Wymiana LCD Copy\nGwarancja 90 dni"]
                                      for price in data if price["Device_name"] == f"iPhone {model_numer}" +
                                      (f" {model}" if model else "")), None)
            print(price_iphone_orig)
            if price_iphone_orig == price_iphone_copy == "-":
                return is_no_text_in_sheet(language)

            if price_iphone_orig != "-":
                price, guarantee_orig, time_of_rep = price_iphone_orig.split("\n")
            if price_iphone_copy != "-":
                price_copy, guarantee_copy, time_of_rep_copy = price_iphone_copy.split("\n")

            if language == "pl":
                return (
                        f"Oto odpowiedź na Państwa zapytanie!\n"
                        + (f"✔️ Koszt wymiany wyświetlacza na oryginał w Państwa modelu iPhone {model_numer} {model} to"
                           f" {price}.\n" if price_iphone_orig != "-" else "")
                        + (f"✔️ Koszt wymiany wyświetlacza na zamiennik to {price_copy}.\n" if price_iphone_copy != "-" else "")
                        + f"⏱️ Średni czas naprawy {time_of_rep if price_iphone_orig != "-" else time_of_rep_copy} godzin/ny (jeśli część jest na stanie!)\n"
                          f"🤝 Gwarancja:\n"
                        + (f"Oryginał: {guarantee_orig} dni\n" if price_iphone_orig != "-" else "")
                        + (f"Zamiennik: {guarantee_copy} dni\n" if price_iphone_copy != "-" else "")
                        + (f"\n\n ⚠️ Ważna informacja:\n"
                         f"Po wymianie wyświetlacza w tych modelach iPhone, niezależnie od tego, czy jest to część oryginalna, "
                         f"czy zamiennik, w ustawieniach telefonu pojawi się komunikat o wymianie.)\n"
                         f"Wynika to z faktu, że iPhone rozpoznaje, iż nowy wyświetlacz nie jest tym, który został zainstalowany"
                         f" fabrycznie/początkowo.\nTen komunikat w żaden sposób nie wpływa na działanie urządzenia i wyświetla się"
                         f" wyłącznie w ustawieniach. 😊"
                           )
                        )
            elif language == "ru":
                return (
                        f"Вот ответ на Ваш запрос!\n"
                        + (f"✔️ Стоимость замены дисплея на оригинальный в модели iPhone {model_numer} {model} составляет {price}.\n"
                           if price_iphone_orig != "-" else "")
                        + (f"✔️ Стоимость замены дисплея на аналог составляет {price_copy}.\n"
                           if price_iphone_copy != "-" else "")
                        + f"⏱️ Среднее время ремонта {time_of_rep if price_iphone_orig != '-' else time_of_rep_copy} часа/ов (если деталь в наличии!)\n"
                          f"🤝 Гарантия:\n"
                        + (f"Оригинал: {guarantee_orig} дней\n" if price_iphone_orig != "-" else "")
                        + (f"Аналог: {guarantee_copy} дней\n" if price_iphone_copy != "-" else "")
                        + (
                            f"\n\n ⚠️ Важная информация:\n"
                            f"После замены дисплея в этих моделях iPhone, независимо от того, оригинальная ли это деталь или аналог, "
                            f"в настройках телефона появится уведомление о замене.\n"
                            f"Это связано с тем, что iPhone распознаёт, что новый дисплей отличается от заводского.\n"
                            f"Это уведомление никак не влияет на работу устройства и отображается только в настройках. 😊"
                        )
                )

            elif language == "ua":
                return (
                        f"Ось відповідь на Ваш запит!\n"
                        + (f"✔️ Вартість заміни дисплея на оригінальний у моделі iPhone {model_numer} {model} становить {price}.\n"
                           if price_iphone_orig != "-" else "")
                        + (f"✔️ Вартість заміни дисплея на замінник становить {price_copy}.\n"
                           if price_iphone_copy != "-" else "")
                        + f"⏱️ Середній час ремонту: {time_of_rep if price_iphone_orig != '-' else time_of_rep_copy}"
                          f" годин/и (якщо деталь є в наявності!)\n"
                          f"🤝 Гарантія:\n"
                        + (f"Оригінал: {guarantee_orig}\n днів" if price_iphone_orig != "-" else "")
                        + (f"Замінник: {guarantee_copy}\n днів" if price_iphone_copy != "-" else "")
                        + (
                            f"\n\n ⚠️ Важлива інформація:\n"
                            f"Після заміни дисплея в цих моделях iPhone, незалежно від того, чи це оригінальна деталь чи замінник, "
                            f"у налаштуваннях телефону з’явиться повідомлення про заміну.\n"
                            f"Це пов’язано з тим, що iPhone розпізнає, що новий дисплей відрізняється від заводського.\n"
                            f"Це повідомлення жодним чином не впливає на роботу пристрою і відображається лише в налаштуваннях. 😊"
                        )
                )

            elif language == "en":
                return (
                        f"Here is the answer to your inquiry!\n"
                        + (f"✔️ The cost of replacing the display with an original one for iPhone model {model_numer} {model} is {price}.\n"
                           if price_iphone_orig != "-" else "")
                        + (f"✔️ The cost of replacing the display with a copy is {price_copy}.\n"
                           if price_iphone_copy != "-" else "")
                        + f"⏱️ Average repair time: {time_of_rep if price_iphone_orig != '-' else time_of_rep_copy} "
                          f"hour/s (if the part is in stock!)\n"
                          f"🤝 Warranty:\n"
                        + (f"Original: {guarantee_orig} days\n" if price_iphone_orig != "-" else "")
                        + (f"Copy: {guarantee_copy} days\n" if price_iphone_copy != "-" else "")
                        + (
                            f"\n\n ⚠️ Important information:\n"
                            f"After replacing the display in these iPhone models, regardless of whether it's an original or a copy, "
                            f"a message about the replacement will appear in the phone settings.\n"
                            f"This is because the iPhone detects that the new display is not the one originally installed.\n"
                            f"This message does not affect the device's functionality and appears only in the settings. 😊"
                        )
                )

    elif service == "back-cover":
        with open("json_files_dm_sheet/iPhone 2025.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            price_iphone = next((price["Wymiana tylnej klapki\nGwarancja 90 dni"]
                                 for price in data if price["Device_name"] == f"iPhone {model_numer}" +
                                 (f" {model}" if model else "")), None)
            print(price_iphone)
            if price_iphone == "-":
                return is_no_text_in_sheet(language)

            price, guarantee, time_of_rep = price_iphone.split("\n")
            if language == "pl":
                return (
                    f"Oto odpowiedź na Państwa zapytanie!\n"
                    f"✔️ Koszt wymiany tylnej obudowy w Państwa modelu iPhone {model_numer} {model} to"
                    f" {price}.\n⏱️ Średni czas naprawy {time_of_rep} godzin/ny (jeśli część jest na stanie!)\n"
                    f"🤝 Gwarancja: {guarantee} dni\n"
                )
            elif language == "ru":
                return (
                    f"Вот ответ на Ваш запрос!\n"
                    f"✔️ Стоимость замены задней крышки в модели iPhone {model_numer} {model} составляет {price}.\n"
                    f"⏱️ Среднее время ремонта {time_of_rep} часа/ов (если деталь в наличии!)\n"
                    f"🤝 Гарантия: {guarantee} дней\n"
                )
            elif language == "ua":
                return (
                    f"Ось відповідь на Ваш запит!\n"
                    f"✔️ Вартість заміни задньої кришки у моделі iPhone {model_numer} {model} становить {price}.\n"
                    f"⏱️ Середній час ремонту: {time_of_rep} годин/и (якщо деталь є в наявності!)\n"
                    f"🤝 Гарантія: {guarantee} днів\n"
                )
            elif language == "en":
                return (
                    f"Here is the answer to your inquiry!\n"
                    f"✔️ The cost of replacing the back cover for iPhone model {model_numer} {model} is {price}.\n"
                    f"⏱️ Average repair time: {time_of_rep} hour/s (if the part is in stock!)\n"
                    f"🤝 Warranty: {guarantee} days\n"
                )

    elif service == "replacement-case":
        with open("json_files_dm_sheet/iPhone 2025.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            price_iphone = next((price["Wymiana korpusu Copy\nGwarancja 90 dni"]
                                 for price in data if price["Device_name"] == f"iPhone {model_numer}" +
                                 (f" {model}" if model else "")), None)
            print(price_iphone)
            if price_iphone == "-":
                return is_no_text_in_sheet(language)

            price, guarantee, time_of_rep = price_iphone.split("\n")
            if language == "pl":
                return (
                    f"Oto odpowiedź na Państwa zapytanie!\n"
                    f"✔️ Koszt wymiany obudowy na zamiennik w Państwa modelu iPhone {model_numer} {model} to"
                    f" {price}.\n⏱️ Średni czas naprawy {time_of_rep} godzin/ny (jeśli część jest na stanie!)\n"
                    f"🤝 Gwarancja: {guarantee} dni\n"
                )
            elif language == "ru":
                return (
                    f"Вот ответ на Ваш запрос!\n"
                    f"✔️ Стоимость замены корпуса на аналог в модели iPhone {model_numer} {model} составляет {price}.\n"
                    f"⏱️ Среднее время ремонта {time_of_rep} часа/ов (если деталь в наличии!)\n"
                    f"🤝 Гарантия: {guarantee} дней\n"
                )
            elif language == "ua":
                return (
                    f"Ось відповідь на Ваш запит!\n"
                    f"✔️ Вартість заміни корпусу на замінник у моделі iPhone {model_numer} {model} становить {price}.\n"
                    f"⏱️ Середній час ремонту: {time_of_rep} годин/и (якщо деталь є в наявності!)\n"
                    f"🤝 Гарантія: {guarantee} днів\n"
                )
            elif language == "en":
                return (
                    f"Here is the answer to your inquiry!\n"
                    f"✔️ The cost of replacing the housing with a copy for iPhone model {model_numer} {model} is {price}.\n"
                    f"⏱️ Average repair time: {time_of_rep} hour/s (if the part is in stock!)\n"
                    f"🤝 Warranty: {guarantee} days\n"
                )

    elif service == "battery-replacement":
        with open("json_files_dm_sheet/iPhone 2025.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            price_iphone_orig = next((price["Wymiana Baterii\nORG Jakość\nGwarancja 180 dni"]
                                 for price in data if price["Device_name"] == f"iPhone {model_numer}" +
                                 (f" {model}" if model else "")), None)

            price_iphone_copy = next((price["Wymiana Baterii\nCopy\nGwarancja 90 dni"]
                                      for price in data if price["Device_name"] == f"iPhone {model_numer}" +
                                      (f" {model}" if model else "")), None)
            print(price_iphone_orig)
            if price_iphone_orig == price_iphone_copy == "-":
                return is_no_text_in_sheet(language)

            if price_iphone_orig != "-":
                price_orig, guarantee_orig, time_of_rep_orig = price_iphone_orig.split("\n")
            if price_iphone_copy != "-":
                price_copy, guarantee_copy, time_of_rep_copy = price_iphone_copy.split("\n")
            if language == "pl":
                return (
                        f"Oto odpowiedź na Państwa zapytanie!\n"
                        + (f"✔️ Koszt wymiany baterii na oryginał w Państwa modelu iPhone {model_numer} {model} to"
                           f" {price_orig}.\n" if price_iphone_orig != "-" else "")
                        + (f"✔️ Koszt wymiany baterii na zamiennik to {price_copy}.\n" if price_iphone_copy != "-" else "")
                        + f"⏱️ Średni czas naprawy {time_of_rep_orig if price_iphone_orig != "-" else time_of_rep_copy} godzin/ny (jeśli część jest na stanie!)\n"
                          f"🤝 Gwarancja:\n"
                        + (f"Oryginał: {guarantee_orig} dni\n" if price_iphone_orig != "-" else "")
                        + (f"Zamiennik: {guarantee_copy} dni\n" if price_iphone_copy != "-" else "")
                        + (f"\n⚠️ Ważna informacja:\n\n"
                           f"Podczas wymiany baterii, niezależnie od tego, czy jest to bateria w jakości oryginalnej,"
                           f"czy kopia, w ustawieniach telefonu pojawi się komunikat o wymianie."
                           f"Jest to związane z tym, że iPhone rozpoznaje nową baterię jako inną niż ta, która była"
                           f"oryginalnie zainstalowana.\n"
                           f"Na urządzeniach z iOS 18.1.1 i wyżej: Poziom pojemności baterii będzie wyświetlany prawidłowo."
                           f"\n\nNa urządzeniach ze starszą wersją iOS:"
                           f"Komunikat o wymianie również się pojawi, ale poziom pojemności baterii będzie"
                           f"wyświetlany jako „-”.\n\n"
                           f"💡 Jak sprawdzić rzeczywistą pojemność baterii w takim przypadku?\n"
                           f"Polecamy skorzystać z aplikacji 3uTools.\n\n"
                           f"✅ Ważne: Te zmiany nie wpływają na funkcjonalność urządzenia 😊"
                           )
                )
            elif language == "ru":
                return (
                        f"Вот ответ на Ваш запрос!\n"
                        + (f"✔️ Стоимость замены батареи на оригинальную в модели iPhone {model_numer} {model} составляет {price_orig}.\n"
                           if price_iphone_orig != "-" else "")
                        + (f"✔️ Стоимость замены батареи на аналог составляет {price_copy}.\n"
                           if price_iphone_copy != "-" else "")
                        + f"⏱️ Среднее время ремонта: {time_of_rep_orig if price_iphone_orig != '-' else time_of_rep_copy} часа/в (если деталь в наличии!)\n"
                          f"🤝 Гарантия:\n"
                        + (f"Оригинал: {guarantee_orig} дней\n" if price_iphone_orig != "-" else "")
                        + (f"Аналог: {guarantee_copy} дней\n" if price_iphone_copy != "-" else "")
                        + (
                            f"\n⚠️ Важная информация:\n\n"
                            f"При замене батареи, независимо от того, оригинальная она или аналог, в настройках телефона появится сообщение о замене.\n"
                            f"Это связано с тем, что iPhone распознаёт новую батарею как отличающуюся от заводской.\n"
                            f"На устройствах с iOS 18.1.1 и выше: уровень ёмкости батареи будет отображаться корректно.\n\n"
                            f"На устройствах со старой версией iOS: сообщение о замене также появится, но уровень ёмкости будет отображаться как «-».\n\n"
                            f"💡 Как проверить реальную ёмкость батареи в таком случае?\n"
                            f"Рекомендуем использовать приложение 3uTools.\n\n"
                            f"✅ Важно: Эти изменения не влияют на работу устройства 😊"
                        )
                )
            elif language == "ua":
                return (
                        f"Ось відповідь на Ваш запит!\n"
                        + (f"✔️ Вартість заміни батареї на оригінальну у моделі iPhone {model_numer} {model} становить {price_orig}.\n"
                           if price_iphone_orig != "-" else "")
                        + (f"✔️ Вартість заміни батареї на замінник становить {price_copy}.\n"
                           if price_iphone_copy != "-" else "")
                        + f"⏱️ Середній час ремонту: {time_of_rep_orig if price_iphone_orig != '-' else time_of_rep_copy} годин/и (якщо деталь є в наявності!)\n"
                          f"🤝 Гарантія:\n"
                        + (f"Оригінал: {guarantee_orig} днів\n" if price_iphone_orig != "-" else "")
                        + (f"Замінник: {guarantee_copy} днів\n" if price_iphone_copy != "-" else "")
                        + (
                            f"\n⚠️ Важлива інформація:\n\n"
                            f"Під час заміни батареї, незалежно від того, чи це оригінал чи копія, у налаштуваннях телефону з’явиться повідомлення про заміну.\n"
                            f"Це пов’язано з тим, що iPhone розпізнає нову батарею як іншу, ніж встановлену на заводі.\n"
                            f"На пристроях з iOS 18.1.1 і вище: рівень ємності батареї буде відображатися коректно.\n\n"
                            f"На пристроях зі старішою версією iOS: повідомлення також з’явиться, але рівень ємності буде показано як «-».\n\n"
                            f"💡 Як перевірити реальну ємність батареї в такому випадку?\n"
                            f"Рекомендуємо скористатися додатком 3uTools.\n\n"
                            f"✅ Важливо: Ці зміни не впливають на функціональність пристрою 😊"
                        )
                )
            elif language == "en":
                return (
                        f"Here is the answer to your inquiry!\n"
                        + (f"✔️ The cost of replacing the battery with an original one for iPhone model {model_numer} {model} is {price_orig}.\n"
                           if price_iphone_orig != "-" else "")
                        + (f"✔️ The cost of replacing the battery with a copy is {price_copy}.\n"
                           if price_iphone_copy != "-" else "")
                        + f"⏱️ Average repair time: {time_of_rep_orig if price_iphone_orig != '-' else time_of_rep_copy} hour/s (if the part is in stock!)\n"
                          f"🤝 Warranty:\n"
                        + (f"Original: {guarantee_orig} days\n" if price_iphone_orig != "-" else "")
                        + (f"Copy: {guarantee_copy} days\n" if price_iphone_copy != "-" else "")
                        + (
                            f"\n⚠️ Important information:\n\n"
                            f"When replacing the battery, whether it's original or a copy, a replacement message will appear in the phone settings.\n"
                            f"This is because the iPhone detects the new battery as different from the one originally installed.\n"
                            f"On devices with iOS 18.1.1 and above: battery capacity level will be displayed correctly.\n\n"
                            f"On devices with older iOS versions: the replacement message will also appear, but the battery capacity level will show as “-”.\n\n"
                            f"💡 How to check the actual battery capacity in this case?\n"
                            f"We recommend using the 3uTools application.\n\n"
                            f"✅ Important: These changes do not affect the functionality of the device 😊"
                        )
                )
    elif service == "charg-conn":
        with open("json_files_dm_sheet/iPhone 2025.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            price_iphone = next((price["Wymiana gniazda ladowania/\ndolna tasma z mikrofonem\nGwarancja 90 dni"]
                                 for price in data if price["Device_name"] == f"iPhone {model_numer}" +
                                 (f" {model}" if model else "")), None)
            print(price_iphone)
            if price_iphone == "-":
                return is_no_text_in_sheet(language)

            price, guarantee, time_of_rep = price_iphone.split("\n")
            if language == "pl":
                return (
                    f"Oto odpowiedź na Państwa zapytanie!\n"
                    f"✔️ Koszt wymiany gniazda ładowania w Państwa modelu iPhone {model_numer} {model} to"
                    f" {price}.\n⏱️ Średni czas naprawy {time_of_rep} godzin/ny (jeśli część jest na stanie!)\n"
                    f"🤝 Gwarancja: {guarantee} dni\n"
                )
            elif language == "ru":
                return (
                    f"Вот ответ на Ваш запрос!\n"
                    f"✔️ Стоимость замены разъема зарядки в модели iPhone {model_numer} {model} составляет {price}.\n"
                    f"⏱️ Среднее время ремонта {time_of_rep} часа/ов (если деталь в наличии!)\n"
                    f"🤝 Гарантия: {guarantee} дней\n"
                )
            elif language == "ua":
                return (
                    f"Ось відповідь на Ваш запит!\n"
                    f"✔️ Вартість заміни роз'єму зарядки у моделі iPhone {model_numer} {model} становить {price}.\n"
                    f"⏱️ Середній час ремонту: {time_of_rep} годин/и (якщо деталь є в наявності!)\n"
                    f"🤝 Гарантія: {guarantee} днів\n"
                )
            elif language == "en":
                return (
                    f"Here is the answer to your inquiry!\n"
                    f"✔️ The cost of replacing the charging port for iPhone model {model_numer} {model} is {price}.\n"
                    f"⏱️ Average repair time: {time_of_rep} hour/s (if the part is in stock!)\n"
                    f"🤝 Warranty: {guarantee} days\n"
                )

    elif service == "repl-speaker":
        with open("json_files_dm_sheet/iPhone 2025.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            price_iphone = next((price["Wymiana glosnika\nGóra\nGwarancja 90 dni"]
                                 for price in data if price["Device_name"] == f"iPhone {model_numer}" +
                                 (f" {model}" if model else "")), None)
            print(price_iphone)
            if price_iphone == "-":
                return is_no_text_in_sheet(language)

            price, guarantee, time_of_rep = price_iphone.split("\n")
            if language == "pl":
                return (
                    f"Oto odpowiedź na Państwa zapytanie!\n"
                    f"✔️ Koszt wymiany głośnika w Państwa modelu iPhone {model_numer} {model} to"
                    f" {price}.\n⏱️ Średni czas naprawy {time_of_rep} godzin/ny (jeśli część jest na stanie!)\n"
                    f"🤝 Gwarancja: {guarantee} dni\n"
                )
            elif language == "ru":
                return (
                    f"Вот ответ на Ваш запрос!\n"
                    f"✔️ Стоимость замены динамика в модели iPhone {model_numer} {model} составляет {price}.\n"
                    f"⏱️ Среднее время ремонта {time_of_rep} часа/ов (если деталь в наличии!)\n"
                    f"🤝 Гарантия: {guarantee} дней\n"
                )
            elif language == "ua":
                return (
                    f"Ось відповідь на Ваш запит!\n"
                    f"✔️ Вартість заміни динаміка у моделі iPhone {model_numer} {model} становить {price}.\n"
                    f"⏱️ Середній час ремонту: {time_of_rep} годин/и (якщо деталь є в наявності!)\n"
                    f"🤝 Гарантія: {guarantee} днів\n"
                )
            elif language == "en":
                return (
                    f"Here is the answer to your inquiry!\n"
                    f"✔️ The cost of replacing the speaker for iPhone model {model_numer} {model} is {price}.\n"
                    f"⏱️ Average repair time: {time_of_rep} hour/s (if the part is in stock!)\n"
                    f"🤝 Warranty: {guarantee} days\n"
                )




    elif service == "does-not-turn-on":
        with open("json_files_dm_sheet/iPhone 2025.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            price_iphone = next((price["Nie włęcza śie\nGwarancja 90 dni"]
                                 for price in data if price["Device_name"] == f"iPhone {model_numer}" +
                                 (f" {model}" if model else "")), None)
            print(price_iphone)
            if price_iphone == "-":
                return is_no_text_in_sheet(language)

            price, guarantee, time_of_rep = price_iphone.split("\n")
            if language == "pl":
                return (
                    f"Oto odpowiedź na Państwa zapytanie!\n"
                    f"✔️ Koszt naprawy w Państwa modelu iPhone {model_numer} {model} to"
                    f" {price}.\n⏱️ Średni czas naprawy {time_of_rep} godzin/ny (jeśli część jest na stanie!)\n"
                    f"🤝 Gwarancja: {guarantee} dni\n"
                )
            elif language == "ru":
                return (
                    f"Вот ответ на Ваш запрос!\n"
                    f"✔️ Стоимость ремонта модели iPhone {model_numer} {model} составляет {price}.\n"
                    f"⏱️ Среднее время ремонта {time_of_rep} часа/ов (если деталь в наличии!)\n"
                    f"🤝 Гарантия: {guarantee} дней\n"
                )
            elif language == "ua":
                return (
                    f"Ось відповідь на Ваш запит!\n"
                    f"✔️ Вартість ремонту моделі iPhone {model_numer} {model} становить {price}.\n"
                    f"⏱️ Середній час ремонту: {time_of_rep} годин/и (якщо деталь є в наявності!)\n"
                    f"🤝 Гарантія: {guarantee} днів\n"
                )
            elif language == "en":
                return (
                    f"Here is the answer to your inquiry!\n"
                    f"✔️ The cost of repair for iPhone model {model_numer} {model} is {price}.\n"
                    f"⏱️ Average repair time: {time_of_rep} hour/s (if the part is in stock!)\n"
                    f"🤝 Warranty: {guarantee} days\n"
                )

    elif service == "probl-after-water":
        with open("json_files_dm_sheet/iPhone 2025.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            price_iphone = next((price["Czyszczenie po zalaniu\n1 - 5 dni\nGwarancja 30 - 90 dni"]
                                 for price in data if price["Device_name"] == f"iPhone {model_numer}" +
                                 (f" {model}" if model else "")), None)
            print(price_iphone)
            if price_iphone == "-":
                return is_no_text_in_sheet(language)

            price, guarantee, time_of_rep = price_iphone.split("\n")
            if language == "pl":
                return (
                    f"Oto odpowiedź na Państwa zapytanie!\n"
                    f"✔️ Koszt Czyszczenia po zalaniu w Państwa modelu iPhone {model_numer} {model} to"
                    f" {price}.\n⏱️ Średni czas naprawy {time_of_rep} godzin/ny (jeśli część jest na stanie!)\n"
                    f"🤝 Gwarancja: {guarantee} dni\n"
                )
            elif language == "ru":
                return (
                    f"Вот ответ на Ваш запрос!\n"
                    f"✔️ Стоимость чистки после попадания жидкости в модели iPhone {model_numer} {model} составляет {price}.\n"
                    f"⏱️ Среднее время ремонта {time_of_rep} часа/ов (если деталь в наличии!)\n"
                    f"🤝 Гарантия: {guarantee} дней\n"
                )
            elif language == "ua":
                return (
                    f"Ось відповідь на Ваш запит!\n"
                    f"✔️ Вартість очищення після потрапляння рідини у моделі iPhone {model_numer} {model} становить {price}.\n"
                    f"⏱️ Середній час ремонту: {time_of_rep} годин/и (якщо деталь є в наявності!)\n"
                    f"🤝 Гарантія: {guarantee} днів\n"
                )
            elif language == "en":
                return (
                    f"Here is the answer to your inquiry!\n"
                    f"✔️ The cost of cleaning after liquid damage for iPhone model {model_numer} {model} is {price}.\n"
                    f"⏱️ Average repair time: {time_of_rep} hour/s (if the part is in stock!)\n"
                    f"🤝 Warranty: {guarantee} days\n"
                )

    elif service == "display-polishing":
        with open("json_files_dm_sheet/iPhone 2025.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            price_iphone_lcd = next((price["Polerowanie Ekran"] for price in data if price["Device_name"] ==
                                     f"iPhone {model_numer}" + (f" {model}" if model else "")), None)
            price_iphone_bottom = next((price["Polerowanie Tyl"] for price in data if price["Device_name"] ==
                                        f"iPhone {model_numer}" + (f" {model}" if model else "")), None)
            price_iphone_lcd_plus_bottom = next((price["Polerowanie Ekran + Tyl"] for price in data if price["Device_name"] ==
                                                f"iPhone {model_numer}" + (f" {model}" if model else "")), None)
            if price_iphone_lcd == price_iphone_bottom == price_iphone_lcd_plus_bottom == "-":
                return is_no_text_in_sheet(language)

            if price_iphone_lcd != "-":
                price_lcd, time_of_rep_lcd, dell_lcd = price_iphone_lcd.split("\n")

            if price_iphone_bottom != "-":
                price_bottom, time_of_rep_bottom, dell_bottom = price_iphone_bottom.split("\n")

            if price_iphone_lcd_plus_bottom != "-":
                price_lcd_plus_bottom, time_of_rep_lcd_plus_bottom, dell_lcd_plus_bottom = price_iphone_lcd_plus_bottom.split("\n")

            if language == "pl":
                return (f"Oto odpowiedź na Państwa zapytanie!\n"
                        + ((f"✔️ Koszt Polerowania Ekranu w Państwa modelu iPhone {model_numer} {model} to {price_lcd}.\n"
                            + f"⏱️ Średni czas naprawy {time_of_rep_lcd} godzin/ny\n"
                            )
                           if price_iphone_lcd != "-" else ""
                           )
                        + ((f"✔️ Koszt Polerowania Tylu w Państwa modelu iPhone {model_numer} {model} to {price_bottom}.\n"
                            + f"⏱️ Średni czas naprawy {time_of_rep_bottom} godzin/ny\n"
                            )
                           if price_iphone_bottom != "-" else ""
                           )
                        + ((f"✔️ Koszt Polerowania Ekran + Tyl w Państwa modelu iPhone {model_numer} {model} to {price_lcd_plus_bottom}.\n"
                            + f"⏱️ Średni czas naprawy {time_of_rep_lcd_plus_bottom} godzin/ny\n"
                            )
                           if price_iphone_lcd_plus_bottom != "-" else ""
                           )
                        )
            elif language == "ru":
                return (
                        f"Вот ответ на Ваш запрос!\n"
                        + (
                            f"✔️ Стоимость полировки экрана в модели iPhone {model_numer} {model} составляет {price_lcd}.\n"
                            f"⏱️ Среднее время ремонта {time_of_rep_lcd} часа/ов\n"
                            if price_iphone_lcd != "-" else ""
                        )
                        + (
                            f"✔️ Стоимость полировки задней части в модели iPhone {model_numer} {model} составляет {price_bottom}.\n"
                            f"⏱️ Среднее время ремонта {time_of_rep_bottom} часа/ов\n"
                            if price_iphone_bottom != "-" else ""
                        )
                        + (
                            f"✔️ Стоимость полировки экрана и задней части в модели iPhone {model_numer} {model} составляет {price_lcd_plus_bottom}.\n"
                            f"⏱️ Среднее время ремонта {time_of_rep_lcd_plus_bottom} часа/ов\n"
                            if price_iphone_lcd_plus_bottom != "-" else ""
                        )
                )
            elif language == "ua":
                return (
                        f"Ось відповідь на Ваш запит!\n"
                        + (
                            f"✔️ Вартість полірування екрана у моделі iPhone {model_numer} {model} становить {price_lcd}.\n"
                            f"⏱️ Середній час ремонту: {time_of_rep_lcd} годин/и\n"
                            if price_iphone_lcd != "-" else ""
                        )
                        + (
                            f"✔️ Вартість полірування задньої частини у моделі iPhone {model_numer} {model} становить {price_bottom}.\n"
                            f"⏱️ Середній час ремонту: {time_of_rep_bottom} годин/и\n"
                            if price_iphone_bottom != "-" else ""
                        )
                        + (
                            f"✔️ Вартість полірування екрана та задньої частини у моделі iPhone {model_numer} {model} становить {price_lcd_plus_bottom}.\n"
                            f"⏱️ Середній час ремонту: {time_of_rep_lcd_plus_bottom} годин/и\n"
                            if price_iphone_lcd_plus_bottom != "-" else ""
                        )
                )
            elif language == "en":
                return (
                        f"Here is the answer to your inquiry!\n"
                        + (
                            f"✔️ The cost of polishing the screen for iPhone model {model_numer} {model} is {price_lcd}.\n"
                            f"⏱️ Average repair time: {time_of_rep_lcd} hour/s\n"
                            if price_iphone_lcd != "-" else ""
                        )
                        + (
                            f"✔️ The cost of polishing the back for iPhone model {model_numer} {model} is {price_bottom}.\n"
                            f"⏱️ Average repair time: {time_of_rep_bottom} hour/s\n"
                            if price_iphone_bottom != "-" else ""
                        )
                        + (
                            f"✔️ The cost of polishing both screen and back for iPhone model {model_numer} {model} is {price_lcd_plus_bottom}.\n"
                            f"⏱️ Average repair time: {time_of_rep_lcd_plus_bottom} hour/s\n"
                            if price_iphone_lcd_plus_bottom != "-" else ""
                        )
                )





# model_numer = "16"
# model = "Plus"
# service = "repair-glas-lcd"
# asyncio.run(get_iPhone_price(model_numer, model, service))




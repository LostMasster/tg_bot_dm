import requests
from igbore_git import api_key_rm


# Создание квитанции
async def new_order(asset_id, client_id, malfunction, engineer, manager_notes, language,
                    equipment, brand, model, manager=233517, ):
    file = open('token_rm.txt', 'r')
    token_rm = file.readline()
    url = f"https://api.remonline.app/order/?asset_uid[]=5878093&token={token_rm}"

    payload = {
        "asset_id": asset_id,  #айди устройства
        "branch_id": 151846,
        "order_type": 247262,
        "client_id": client_id,
        "malfunction": malfunction,  # Uszkodzenie
        "manager": manager,
        "engineer": engineer,
        "manager_notes": manager_notes,
        "custom_fields": {"f8001779": language,
                          "7051493": equipment,  #Комплектация
                          "f8001721": "7545378",
                          "brand": brand,
                          "model": model,
                          "serial": "telegram_",
                          "kindof_good": "",
                          "group": "Laptop",
                          "f859313": "-",
                          "8001721": "Obtarcia i zadrapania, Brak możliwości sprawdzenia"
                                     " podzespołów"  #Stan urządzenia i opis awarii:
                          },
        "ad_campaign_id": 463958
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)
import json
barometer = {}
Hydra = {}
Test_S = {}
pascal = {}
POCA = {}
Test_A = {}
for i in range(4, 18):
    print(i)
    file_name = "log-" + str(i) + ".txt"
    with open(file_name, encoding='utf-8') as json_file:
        dict = json.load(json_file)
    for key in dict:
        if(dict[key]["uName"] == 'Опорный барометр'):
            barometer[dict[key]['Date']] = {
            "temp": float(dict[key]['data']['weather_temp']),
            "pressure": float(dict[key]['data']['weather_pressure'])}
        if(dict[key]["uName"] == 'Hydra-L' or dict[key]["uName"] == 'Hydra-L1'):
            Hydra[dict[key]['Date']] = {
            "temp": float(dict[key]['data']['BME280_temp']),
            "pressure": float(dict[key]['data']['BME280_pressure']),
            "humidity": float(dict[key]['data']['BME280_humidity']),
            "ef_temp": float(dict[key]['data']['BME280_temp']) - 0.4*(float(dict[key]['data']['BME280_temp'])-10)*(1-float(dict[key]['data']['BME280_humidity'])/100)}#ЭТ=t−0.4∗( t−10)∗(1−h/100)
        if (dict[key]["uName"] == 'Тест Студии'):
            Test_S[dict[key]['Date']] = {
            "temp": (float(dict[key]['data']["BMP280_temp"]) + float(dict[key]['data']["BME280_temp"]) + float(dict[key]['data']["DS18B20_temp"]) + float(dict[key]['data']["AM2321_temp"]))/4,
            "pressure": (float(dict[key]['data']["BMP280_pressure"]) + float(dict[key]['data']["BME280_pressure"]))/2,
            "humidity": (float(dict[key]['data']["BME280_humidity"]) + float(dict[key]['data']["AM2321_humidity"]))/2,
            "ef_temp": float(dict[key]['data']["BMP280_temp"]) - 0.4 * (float(dict[key]['data']["BMP280_temp"]) - 10) * (1 - float(dict[key]['data']["BME280_humidity"]) / 100)}
        if(dict[key]["uName"] == 'Паскаль'):
            pascal[dict[key]['Date']] = {
            "temp": float(dict[key]['data']['weather_temp']),
            "pressure": float(dict[key]['data']['weather_pressure'])}
        if(dict[key]["uName"] == 'РОСА К-2'):
            POCA[dict[key]['Date']] = {
            "temp": float(dict[key]['data']['weather_temp']),
            "pressure": float(dict[key]['data']['weather_pressure']),
            "humidity": float(dict[key]['data']['weather_humidity']),
            "ef_temp": float(dict[key]['data']['weather_temp']) - 0.4 * (float(dict[key]['data']['weather_temp']) - 10) * (1 - float(dict[key]['data']['weather_humidity']) / 100)}
        if(dict[key]["uName"] == 'Тест воздуха'):
            Test_A[dict[key]['Date']] = {
            "temp": float(dict[key]['data']['BME280_temp']),
            "pressure": float(dict[key]['data']['BME280_pressure']),
            "humidity": float(dict[key]['data']['BME280_humidity']),
            "ef_temp": float(dict[key]['data']['BME280_temp']) - 0.4 * (float(dict[key]['data']['BME280_temp']) - 10) * (1 - float(dict[key]['data']['BME280_humidity']) / 100)}
with open("Опорный барометр.json", 'w', encoding='utf-8') as f:
    json.dump(barometer, f)
with open("Hydra-L.json", 'w', encoding='utf-8') as f:
    json.dump(Hydra, f)
with open("Тест Студии.json", 'w', encoding='utf-8') as f:
    json.dump(Test_S, f)
with open("Паскаль.json", 'w', encoding='utf-8') as f:
    json.dump(pascal, f)
with open("РОСА К-2.json", 'w', encoding='utf-8') as f:
    json.dump(POCA, f)
with open("Тест воздуха.json", 'w', encoding='utf-8') as f:
    json.dump(Test_A, f)

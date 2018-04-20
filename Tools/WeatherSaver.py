from Model.DataModel import Weather
from Utils.save_to_MySql import MySqlSaver
from Utils.utils import get_json_file, parse_id_version, get_each_json_list, parse_year_time_hour
import logging, xlrd

logging.basicConfig(filename='weather_log', format='[%(asctime)s]   %(message)s', datefmt='%Y-%m-%d %H:%M:%S %p',
                    level=logging.DEBUG, filemode='a')
mysql = MySqlSaver('hobot_data_test')

saved_set = set()


def collect(root_path):
    g = get_json_file(root_path)
    while True:
        try:
            file_path = next(g)
            data_id, version = parse_id_version(file_path)
            json_list = get_each_json_list(file_path)
            for js in json_list:
                collect_weather_data(js, data_id)
        except StopIteration:
            break


def update():
    workbook = xlrd.open_workbook(r"D:\数据分布\天气道路时间表.xlsx")
    sheet = workbook.sheet_by_index(0)
    n = sheet.nrows
    for i in range(1, n):
        key = sheet.cell(i, 0).value
        weather = sheet.cell(i, 4).value
        road = sheet.cell(i, 5).value
        daynight = sheet.cell(i, 6).value
        update_weather(key, weather=weather, road=road, daynight=daynight)


def collect_weather_data(js, data_id):
    image_key = js['image_key']
    year, time, hour = parse_year_time_hour(image_key)
    if not year is None:
        key = data_id + "_" + year + "_" + str(int(hour))
        wea = Weather(data_id=data_id, key=key, year=year, hour=hour)
        global saved_set
        if key in saved_set:
            return
        else:
            saved_set.add(key)
            print('collect_weather_data', key)
            mysql.save(wea)
            mysql.commit()


def update_weather(key, weather, road, daynight):
    print('update_weather')
    d = {Weather.weather: weather,
         Weather.road: road,
         Weather.daynight: daynight}
    mysql.update(Weather, Weather.key == key, d)
    mysql.commit()


if __name__ == '__main__':
    # l = [r'D:\数据分布\行人\zyy_pedestrian\test_data',
    #      r'D:\数据分布\行人\zyy_pedestrian\train_data',
    #      r'D:\项目汇总\ADAS\车头车尾\TestingSet\ADAS车辆-测试集JSON',
    #      r'D:\数据分布\车辆\train_data_merge_json_2018_0409',
    #      r'D:\数据分布\交通标志牌\test_data']
    # for _ in l:
    #     collect(_)
    collect(r'D:\项目汇总\ADAS\车头车尾\TestingSet\ADAS车辆-测试集JSON')
    # update()

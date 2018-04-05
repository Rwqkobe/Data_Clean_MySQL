from save_to_MySql import MySqlSaver
from DataModel import DataModel, Head, Person
import math
from utils import *
from config import data_dict

DATA_TYPE = 'test'
TYPE = 'Vehicle'
mysql = MySqlSaver('hobot_data_test')


# # id = 1
#
#
# def main(root_path):
#     g = get_json_file(root_path)
#     m = MySqlSaver('adas_data_test')
#     while True:
#         try:
#             file_path = next(g)
#             data_id, version = parse_id_version(file_path)
#             l = get_each_json_list(file_path)
#             save_pedestrian(l, data_id, version, m)
#         except StopIteration:
#             break
#
#
# def save_pedestrian(l, data_id, version, m):
#     global id
#     for j in l:
#         d = parse_pedestrian_json(id, j, data_id, version)
#         if d is None:
#             continue
#         print('id=%d,dict=%s' % (id, str(d)))
#         p = Pedestrian(id=id, image_key=d['image_key'], year=d['year'], time=d['time'], hour=d['hour'],
#                        rect_num=d['rect_num'], version=version, data_id=data_id)
#         m.save(p)
#         id += 1
#         try:
#             persons = j['person']
#             # 如果有人，就把人存储到mysql的表中
#             for person in persons:
#                 save_person(person, m, d)
#         except:
#             continue
#
#
# def save_person(person, m, pic_dict):
#     try:
#         height = abs(round(float(person['data'][3]) - float(person['data'][1]), 1))
#         width = abs(round(float(person['data'][2]) - float(person['data'][0]), 1))
#         area = int(height * width)
#         diagonal = round(math.sqrt((height ** 2 + width ** 2)), 1)
#         h_div_w = round(height / width, 1)
#         hard = person['attrs'].get('hard', None)
#         occlusion = person['attrs'].get('occlusion', None)
#         humanCheck = person['attrs'].get('humanCheck', None)
#         ignore = person['attrs'].get('ignore', None)
#         part = person['attrs'].get('part', None)
#         blur = person['attrs'].get('blur', None)
#         type = person['attrs'].get('type', None)
#         score = person['attrs'].get('score', None)
#         pose = person['attrs'].get('pose', None)
#         pr = PersonRect(image_id=pic_dict['id'], height=height, width=width, area=area, diagonal=diagonal,
#                         h_div_w=h_div_w, hard=hard, occlusion=occlusion, pose=pose, ignore=ignore, score=score,
#                         blur=blur, humanCheck=humanCheck, type=type, part=part)
#         m.save(pr)
#     except:
#         raise
#
#
# if __name__ == '__main__':
#     main(r'D:\数据分布\行人\zyy_pedestrian\test_data')

def main(root_path):
    g = get_json_file(root_path)
    while True:
        try:
            file_path = next(g)
            data_id, version = parse_id_version(file_path)
            json_list = get_each_json_list(file_path)
            for js in json_list:
                save_body_data(js, data_id, version)
        except StopIteration:
            break


def save_body_data(js, data_id, version):
    image_key = js['image_key']
    key = data_id + "_" + str(version) + '_' + image_key
    video_name = get_json(js, 'video_name')
    video_index = get_json(js, 'video_index')
    width = js['width']
    height = js['height']
    rects = get_json(js, data_dict[TYPE])
    if TYPE == 'DMS':
        year, time, hour = None, None, None
    else:
        year, time, hour = parse_year_time_hour(image_key)

    if rects:
        rect_num = len(rects)
    else:
        rect_num = 0

    body = DataModel(key=key, data_type=DATA_TYPE, type=TYPE, data_id=data_id, version=version,
                     image_key=image_key, video_name=video_name, video_index=video_index,
                     width=width, height=height, year=year, hour=hour, time=time, rect_num=rect_num)
    mysql.save(body)
    if rects:
        if data_dict[TYPE] == 'person':
            save_person(rects, key=key)
        elif data_dict[TYPE] == 'vehicle':
            pass
        elif data_dict[TYPE] == 'head':
            pass


def save_person(persons, key):
    for person in persons:
        try:
            height = abs(round(float(person['data'][3]) - float(person['data'][1]), 1))
            width = abs(round(float(person['data'][2]) - float(person['data'][0]), 1))
            area = int(height * width)
            diagonal = round(math.sqrt((height ** 2 + width ** 2)), 1)
            h_div_w = round(height / width, 1)
            hard = person['attrs'].get('hard', None)
            occlusion = person['attrs'].get('occlusion', None)
            ignore = person['attrs'].get('ignore', None)
            blur = person['attrs'].get('blur', None)
            type = person['attrs'].get('type', None)
            pose = person['attrs'].get('pose', None)
            pr = Person(key=key, height=height, width=width, area=area, diagonal=diagonal, h_div_w=h_div_w,
                        pose=pose, type=type, ignore=ignore, blur=blur, occlusion=occlusion, hard=hard)
            mysql.save(pr)
        except:
            raise


main(r'D:\数据分布\车辆\test_data')

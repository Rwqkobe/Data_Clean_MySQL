import os, json


def parse_pedestrian_json(id, j, data_id, version):
    d = dict()
    try:
        d['id'] = id
        d['image_key'] = j['image_key']
        d['data_id'] = data_id
        d['version'] = version
        try:
            d['year'], d['time'], d['hour'] = parse_year_time_hour(d['image_key'])
        except:
            return None
        try:
            d['rect_num'] = len(j['person'])
        except:
            d['rect_num'] = 0
        d['weather'] = None
        d['road'] = None
        d['daynight'] = None
    except:
        print('parse_pedestrian_json error, json is ', j)
    return d


def parse_year_time_hour(image_key):
    image_name = os.path.splitext(image_key)[0]
    if image_name.find('Michigan') != -1:
        return None
    if image_name.find('ADAS') != -1:
        image_key = image_name.split('_')[1].replace('-', '_')
    elif image_name.find('Michigan') != -1:
        raise KeyError
    else:
        image_key = image_name
    time_list = image_key.split('_')
    year = time_list[0]
    time = time_list[1]
    hour = int(time[:2])
    return year, time, hour


# 每次返回一个json的文件路径
def get_json_file(path):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if not os.path.isdir(file_path):
            yield file_path


def parse_id_version(file_path):
    data_id = file_path.split('\\')[-1].split('_')[0]
    try:
        if not file_path.split('\\')[-1] == -1:
            version = int(file_path.split('\\')[-1].split('_')[1].split('.')[0].replace('v',''))
        else:
            version = None
    except:
        print('version error,file_path is ', file_path)
        raise
    return data_id, version


# return each json in this file as a list
def get_each_json_list(file_path):
    l = list()
    with open(file_path, 'r')as f:
        for line in f.readlines():
            l.append(json.loads(line))
    return l


def get_json(js, key):
    try:
        return js[key]
    except KeyError:
        return None

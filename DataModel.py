from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from save_to_MySql import Base


class DataModel(Base):
    __tablename__ = 'image_data'
    data_type = Column(String(20))  # data_type = train or test
    type = Column(String(20))  # type = vehicle or pedestrian or dms ...
    id = Column(Integer, primary_key=True, autoincrement=True)
    data_id = Column(String(20))
    version = Column(Integer)

    key = Column(String(100), unique=True)
    image_key = Column(String(100))
    video_name = Column(String(100))
    video_index = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)

    # time
    year = Column(String(20))
    hour = Column(Integer)
    time = Column(String(20))
    # calculate
    rect_num = Column(Integer)
    # fill by us
    weather = Column(String(20))
    road = Column(String(20))
    daynight = Column(String(20))

    # relationships
    # lane = relationship()  # 车道线
    # vehicle = relationship()  #
    person = relationship('Person')
    head = relationship('Head')
    # hand = relationship()
    # face_keypoint_8 = relationship()
    # face_keypoint_72 = relationship()
    # shoulder_foot_keypoint_4 = relationship()
    # plate_box = relationship()
    # plate_point = relationship()
    # parsing = relationship()
    # recognition = relationship()
    # voice = relationship()
    # classify = relationship()
    # belong_to = relationship()


class Person(Base):
    __tablename__ = 'person'
    # identity
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(100), ForeignKey('image_data.key'))
    # rect
    height = Column(Float(precision=1))
    width = Column(Float(precision=1))
    area = Column(Integer)
    diagonal = Column(Float(precision=1))
    h_div_w = Column(Float(precision=1))
    # attrs
    pose = Column(String(20))
    type = Column(String(20))
    # others
    ignore = Column(String(20))
    blur = Column(String(20))
    occlusion = Column(String(20))
    hard = Column(String(20))


class Head(Base):
    __tablename__ = 'head'
    # identity
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(100), ForeignKey('image_data.key'))
    # rect
    height = Column(Float(precision=1))
    width = Column(Float(precision=1))
    area = Column(Integer)
    diagonal = Column(Float(precision=1))
    h_div_w = Column(Float(precision=1))
    # attrs
    gender = Column(String(20))
    has_glasses = Column(String(20))
    hair = Column(String(20))
    age = Column(String(20))
    new_age = Column(String(20))
    has_hat = Column(String(20))
    look = Column(String(20))
    # others
    left_eye = Column(String(20))
    right_eye = Column(String(20))
    orientation = Column(String(20))
    occlusion = Column(String(20))
    ignore = Column(String(20))
    hard = Column(String(20))

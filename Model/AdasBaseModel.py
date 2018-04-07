# from sqlalchemy import Column, String, Integer, Float, ForeignKey
# from sqlalchemy.orm import relationship
# from save_to_MySql import Base
#
# pedestrian_tablename = 'pedestrian_test'
# person_rect_tablename = 'person_rect_test'
#
#
# class Pedestrian(Base):
#     __tablename__ = pedestrian_tablename
#     id = Column(Integer, primary_key=True)
#     image_key = Column(String(100))
#     year = Column(String(20))
#     hour = Column(Integer)
#     time = Column(String(20))
#     rect_num = Column(Integer)
#     weather = Column(String(20))
#     version = Column(Integer)
#     road = Column(String(20))
#     daynight = Column(String(20))
#     data_id = Column(String(20))
#     persons = relationship('PersonRect')
#
#
# class Person(Base):
#     __tablename__ = person_rect_tablename
#     # identity
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     image_id = Column(Integer, ForeignKey('pedestrian_test.id'))
#     # rect
#     height = Column(Float(precision=1))
#     width = Column(Float(precision=1))
#     area = Column(Integer)
#     diagonal = Column(Float(precision=1))
#     h_div_w = Column(Float(precision=1))
#     # attrs
#     pose = Column(String(20))
#     type = Column(String(20))
#     # others
#     ignore = Column(String(20))
#     blur = Column(String(20))
#     occlusion = Column(String(20))
#     hard = Column(String(20))
#
#
# class DMS(Base):
#     __tablename__ = 'dms_test'

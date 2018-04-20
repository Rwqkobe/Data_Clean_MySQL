from sqlalchemy.exc import IntegrityError,InvalidRequestError

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import logging

Base = declarative_base()

DB_CONNECT_STRING = 'mysql+mysqldb://root:123456@localhost/'


class MySqlSaver(object):
    def __init__(self, db_name):
        print('init MySqlSaver')
        engine = create_engine(DB_CONNECT_STRING + db_name+'?charset=utf8', echo=True)
        Base.metadata.create_all(engine)
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def save(self, data_object):
        try:
            self.session.add(data_object)
        except IntegrityError as e:
            self.session.rollback()
            if str(e.args).find('Duplicate entry') == -1:
                raise
            else:
                print('---------save-------IntegrityError,Duplicate entry-------------')
                return
        except InvalidRequestError as e:
            if str(e.args).find('Duplicate entry') == -1:
                raise
            else:
                print('---------save-------InvalidRequestError,Duplicate entry-------------')
                return
        # finally:
        #     self.session.close()

    def commit(self):
        try:
            self.session.commit()
            self.session.close()
        except IntegrityError as e:
            if str(e.args).find('Duplicate entry') == -1:
                raise
            else:
                # raise
                print('--------commit--------IntegrityError,Duplicate entry-------------')
                return
        except InvalidRequestError as e:
            if str(e.args).find('Duplicate entry') == -1:
                raise
            else:
                print('----------commit------InvalidRequestError,Duplicate entry-------------')
                return

    def query(self, *entities, **kwargs):
        return self.session.query(*entities, **kwargs)

    def update(self, entity, criterion, kwargs):
        self.session.query(entity).filter(criterion).update(kwargs)

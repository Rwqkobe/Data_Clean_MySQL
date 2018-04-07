from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

DB_CONNECT_STRING = 'mysql+mysqldb://root:123456@localhost/'


class MySqlSaver(object):
    def __init__(self, db_name):
        print('init MySqlSaver')
        engine = create_engine(DB_CONNECT_STRING + db_name, echo=True)
        Base.metadata.create_all(engine)
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def save(self, data_object):
        try:
            self.session.add(data_object)
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def query(self, *entities, **kwargs):
        return self.session.query(*entities, **kwargs)

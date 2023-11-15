'''import dependencies'''
from sqlalchemy import Column, Integer, String
from .db import Base


class CompanyModel(Base):
    '''company website database'''
    __tablename__ = "web_scrapper"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    tag = Column(String)
    text = Column(String)

    def as_dict(self):
        '''Convert CompanyModel object to a dictionary'''
        return {column.id: getattr(self, column.id)
                for column in self.__table__.columns}

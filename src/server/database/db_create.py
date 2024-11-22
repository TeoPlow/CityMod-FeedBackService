from sqlalchemy import Column, Integer, Text, BigInteger, ForeignKey, TIMESTAMP, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from server.database.db_connection import engine
from config import logger_config
from datetime import datetime
import logging
import logging.config

from werkzeug.security import generate_password_hash, check_password_hash


logger = logging.getLogger('server')
logging.config.dictConfig(logger_config)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    password_hash = Column(String(128), nullable=False)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)

    reviews = relationship('Review', back_populates='user')
    bug_reports = relationship('BugReport', back_populates='user')
    offers = relationship('Offer', back_populates='user')


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    review = Column(Text, nullable=False)
    time = Column(TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)

    user = relationship('User', back_populates='reviews')


class BugReport(Base):
    __tablename__ = 'bug_reports'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    message = Column(Text, nullable=False)
    files_id = Column(BigInteger, ForeignKey('files.id'), nullable=True)
    time = Column(TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)

    user = relationship('User', back_populates='bug_reports')
    file = relationship('File', back_populates='bug_reports')


class Offer(Base):
    __tablename__ = 'offers'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    offer = Column(Text, nullable=False)
    files_id = Column(BigInteger, ForeignKey('files.id'), nullable=True)
    time = Column(TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)

    user = relationship('User', back_populates='offers')
    file = relationship('File', back_populates='offers')


class File(Base):
    __tablename__ = 'files'

    id = Column(BigInteger, primary_key=True)
    type = Column(Text, nullable=False)
    file_name = Column(Text, nullable=False)
    file_info = Column(Text, nullable=True)
    file_path = Column(Text, nullable=False)
    time = Column(TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)

    bug_reports = relationship('BugReport', back_populates='file')
    offers = relationship('Offer', back_populates='file')
    mods = relationship('Mod', back_populates='file')
    maps = relationship('Map', back_populates='file')
    other_contents = relationship('OtherContent', back_populates='file')


class Mod(Base):
    __tablename__ = 'mods'

    id = Column(BigInteger, primary_key=True)
    name = Column(Text, nullable=False)
    release_channel = Column(Text, nullable=False)
    version = Column(Text, nullable=False)
    game_versions = Column(Text, nullable=False)
    changelog = Column(Text, nullable=False)
    files_id = Column(BigInteger, ForeignKey('files.id'), nullable=False)
    time = Column(TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)

    file = relationship('File', back_populates='mods')


class Map(Base):
    __tablename__ = 'maps'

    id = Column(BigInteger, primary_key=True)
    name = Column(Text, nullable=False)
    changelog = Column(Text, nullable=False)
    files_id = Column(BigInteger, ForeignKey('files.id'), nullable=False)
    time = Column(TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)

    file = relationship('File', back_populates='maps')


class OtherContent(Base):
    __tablename__ = 'other_content'

    id = Column(BigInteger, primary_key=True)
    name = Column(Text, nullable=False)
    info = Column(Text, nullable=False)
    files_id = Column(BigInteger, ForeignKey('files.id'), nullable=False)
    time = Column(TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)

    file = relationship('File', back_populates='other_contents')

def update_database():
    logger.info(f"Обновляю таблицы в базе данных")
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    update_database()
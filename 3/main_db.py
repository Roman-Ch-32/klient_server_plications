from datetime import datetime

import ipaddress as ipaddress
from sqlalchemy import Column, Integer, String, create_engine, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker


class Database:
    Base = declarative_base()

    def __init__(self):
        self.engine = create_engine('sqlite:///declarative_style_base.db3', echo=True)
        self.Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.session.query(self.ActiveUsers).delete()
        self.session.commit()


    class AllUser(Base):
        __tablename__ = 'all_users'
        id = Column(Integer, primary_key=True)
        login = Column(String, ForeignKey('all_users.id'), unique=True)
        name = Column(String, unique=True)
        password = Column(String)
        last_connection = Column(DateTime)

        def __init__(self, user, login, name, password):
            self.user = user
            self.name = name
            self.loign = login
            self.password = password
            self.last_connection = datetime.now()


    class HistoryUsers(Base):
        __tablename__ = 'history_users'
        id = Column(Integer, primary_key=True)
        name = Column(String, unique=True)
        login = Column(String, ForeignKey('all_users.id'), unique=True)
        connections = Column(DateTime)
        ipaddr = Column(Integer)
        port = Column(Integer)

        def __init__(self, user, name, login, port, ip):
            self.user = user
            self.name = name
            self.login = login
            self.connections = datetime.now()
            self.ip = ip
            self.port = port

    class ActiveUsers(Base):
        __tablename__ = 'active_users'
        id = Column(Integer, primary_key=True)
        name = Column(String, unique=True)
        login = Column(String, ForeignKey('all_users.id'), unique=True)
        connections = Column(DateTime)
        ip = Column(Integer)
        port = Column(Integer)

        def __init__(self, user, name, login, port, ip):
            self.user = user
            self.name = name
            self.login = login
            self.connections = datetime.now()
            self.ip = ip
            self.port = port

    def user_login(self, ip, port, login, name, password):
        rez = self.session.query(self.AllUser).filter_by(login=login)

        if rez.count():
            user = rez.first()
            user.last_connection = datetime.now()
        else:
            user = self.AllUser(ip, login, name, password)
            user.last_connection = datetime.now()
            self.session.add(user)
            self.session.commit()

        new_active_user = self.ActiveUsers(user.id, ip, port, name, datetime.now())
        self.session.add(new_active_user)

        history = self.HistoryUsers(user.id, ip, port, name, datetime.now())
        self.session.add(history)

        self.session.commit()

    def user_logout(self, login):

        rez = self.session.query(self.ActiveUsers).filter_by(login=login)

        if rez.count():
            user = rez.first()
            self.session.query(self.ActiveUsers).delete(user)
            self.session.commit()

    def users_list(self):
        query = self.session.query(
            self.AllUser.login,
            self.AllUser.last_connection,
        )
        # Возвращаем список тюплов
        return query.all()

    # Функция возвращает список активных пользователей
    def active_users_list(self):
        # Запрашиваем соединение таблиц и собираем тюплы имя, адрес, порт, время.
        query = self.session.query(
            self.AllUser.login,
            self.ActiveUsers.ip,
            self.ActiveUsers.port,
            self.ActiveUsers.connections
        ).join(self.AllUser)
        # Возвращаем список тюплов
        return query.all()

    # Функция возвращает историю входов по пользователю или по всем пользователям
    def login_history(self, username=None):
        # Запрашиваем историю входа
        query = self.session.query(self.AllUser.login,
                                   self.HistoryUsers.connections,
                                   self.HistoryUsers.ip,
                                   self.HistoryUsers.port
                                   ).join(self.AllUser)
        # Если было указано имя пользователя, то фильтруем по нему
        if username:
            query = query.filter(self.AllUser.login == username)
        return query.all()


if __name__ == '__main__':
    db = Database()
    db.user_login('192.168.1.4', 8888, 'client_1', 'client_11', 'passw',)
    db.user_login('192.168.1.5', 7777, 'client_2', 'client_22', 'passw')
    # выводим список кортежей - активных пользователей
    print(db.active_users_list())
    # выполянем 'отключение' пользователя
    db.user_logout('client_1')
    print(db.users_list())
    # выводим список активных пользователей
    print(db.active_users_list())
    db.user_logout('client_2')
    print(db.users_list())
    print(db.active_users_list())

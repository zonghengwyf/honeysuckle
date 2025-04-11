import uuid
import os.path
from datetime import datetime
from typing import Type, List, Dict
from sqlalchemy import create_engine, Column, Integer, DateTime, String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session

from config import DbConfig
from app.utils.util import current_strftime

# 创建数据库引擎
engine = create_engine(DbConfig.DB_APT_URI, pool_pre_ping=True)

# 创建基本模型
Base = declarative_base()

class ModelBase(Base):
    __abstract__ = True
    __table_args__ = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(String(36), primary_key=True, nullable=False, default=lambda: str(uuid.uuid4()))
    create_time = Column('create_time', DateTime, default=current_strftime, comment="创建时间", index=True)
    update_time = Column('update_time', DateTime, default=current_strftime, onupdate=current_strftime, comment="更新时间")

    def as_dict(self):
        """将模型实例转换为字典，方便序列化"""
        object_dict = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                object_dict[column.name] = value.strftime("%Y-%m-%d %H:%M:%S")
            else:
                object_dict[column.name] = value
        return object_dict


class DbBase:
    def __init__(self, autocommit=False, autoflush=False, expire_on_commit=False, **kwargs):
        _session = sessionmaker(bind=engine, autocommit=autocommit, autoflush=autoflush,
                                       expire_on_commit=expire_on_commit, **kwargs)
        self.session = scoped_session(_session)

    def close(self):
        """关闭数据库会话"""
        self.session.close()

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """处理上下文管理器的退出逻辑"""
        try:
            if exc_val is None:
                self.session.flush()
                self.session.commit()
            else:
                self.session.rollback()
        except SQLAlchemyError:
            self.session.rollback()
        finally:
            self.close()

    def get_all(self, model: Type[Base]):
        """获取模型的所有实例"""
        return self.session.query(model).all()

    def add(self, model: Type[Base], data: dict, commit: bool = True, flush: bool = True):
        """添加实例到数据库

        :param model: 模型类
        :param data: 字典，包含模型字段及其值
        :param commit: 是否提交会话
        :param flush: 是否刷新会话
        """
        db_obj = model(**data)
        self.session.add(db_obj)
        try:
            if commit:
                self.session.commit()
            if flush:
                self.session.flush()
            return db_obj
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def bulk_add(self, model: Type[Base], data_list: List[Dict], batch_size: int = 100, commit: bool = True):
        """批量添加实例到数据库

        :param model: 模型类
        :param data_list: 包含多个字典的列表，每个字典代表一个实例
        :param batch_size: 每次插入的批量大小
        :param commit: 是否提交会话
        """
        total_records = len(data_list)
        for i in range(0, total_records, batch_size):
            batch = data_list[i:i + batch_size]
            db_objs = [model(**data) for data in batch]
            self.session.add_all(db_objs)
            try:
                if commit:
                    self.session.commit()
            except SQLAlchemyError as e:
                self.session.rollback()
                raise e

        # 最后刷新会话
        if commit:
            self.session.flush()

    def get(self, model: Type[Base], data_id: int):
        """根据 ID 获取实例

        :param model: 模型类
        :param data_id: 要获取的实例 ID
        :return: 实例或 None
        """
        return self.session.query(model).filter(model.id == data_id).first()

    def update(self, model: Type[Base], commit: bool = True, flush: bool = False):
        """更新数据库中的实例

        :param model: 要更新的模型实例
        :param commit: 是否提交会话
        :param flush: 是否刷新会话
        """
        try:
            updated_obj = self.session.merge(model)
            if commit:
                self.session.commit()
            if flush:
                self.session.flush()
            return updated_obj
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def delete(self, model: Type[Base], data_id: int, commit: bool = True, flush: bool = False):
        """根据 ID 删除实例

        :param model: 模型类
        :param data_id: 要删除的实例 ID
        :param commit: 是否提交会话
        :param flush: 是否刷新会话
        """
        instance = self.get(model, data_id)
        if instance:
            try:
                self.session.delete(instance)
                if commit:
                    self.session.commit()
                if flush:
                    self.session.flush()
            except SQLAlchemyError as e:
                self.session.rollback()
                raise e

async def get_db():
    db = DbBase()
    try:
        yield db
    finally:
        db.close()


# 创建数据库表
def init_db(init_sql_file=None):
    """初始化数据库，创建所有表"""
    Base.metadata.create_all(bind=engine)
    if init_sql_file and os.path.exists(init_sql_file):
        with engine.connect() as connection:
            with open(init_sql_file, 'r') as file:
                sql_script = file.read()
                connection.execute(sql_script)
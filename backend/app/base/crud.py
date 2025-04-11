from sqlalchemy.orm import Session
from typing import TypeVar, Generic, List, Optional
from pydantic import BaseModel
from sqlalchemy.ext.declarative import as_declarative, declared_attr

# 泛型类型
ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)

@as_declarative()
class Base:
    id: int
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'

class CRUDBase(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: ModelType):
        self.model = model

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        """创建新记录"""
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Optional[ModelType]:
        """根据ID获取记录"""
        return db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 10) -> List[ModelType]:
        """获取所有记录，支持分页"""
        return db.query(self.model).offset(skip).limit(limit).all()

    def update(self, db: Session, id: int, obj_in: CreateSchemaType) -> Optional[ModelType]:
        """更新记录"""
        db_obj = self.get(db, id)
        if db_obj:
            for key, value in obj_in.dict(exclude_unset=True).items():
                setattr(db_obj, key, value)
            db.commit()
            db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int) -> Optional[ModelType]:
        """删除记录"""
        db_obj = self.get(db, id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj
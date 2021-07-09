from typing import Generic, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..database import Base


ModelType = TypeVar('ModelType', bound=Base)
SchemaType = TypeVar('SchemaType', bound=BaseModel)


class PostCRUDBase(Generic[ModelType, SchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_list(
        self, db: Session, skip: int, limit: int, post_id: Optional[int] = None
    ):
        if post_id:
            return db.query(self.model).filter(
                self.model.post_id == post_id).offset(skip).limit(limit).all()
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_singl(self, db: Session, id: int, post_id: Optional[int] = None):
        if post_id:
            return db.query(self.model).filter(
                self.model.id == id, self.model.post_id == post_id).first()
        return db.query(self.model).filter(self.model.id == id).first()

    def create(
        self, db: Session, obj: SchemaType,
        author_id: int, post_id: Optional[int] = None
    ):
        if post_id:
            db_obj = self.model(
                **obj.dict(), author_id=author_id, post_id=post_id
            )
        else:
            db_obj = self.model(**obj.dict(), author_id=author_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, db_obj: ModelType, obj_update: SchemaType
    ):
        obj_data = jsonable_encoder(db_obj)
        updated_data = obj_update.dict()
        for field in obj_data:
            if field in updated_data:
                setattr(db_obj, field, updated_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, obj: ModelType):
        db.delete(obj)
        db.commit()
        return obj

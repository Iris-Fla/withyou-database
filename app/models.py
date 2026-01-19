from sqlalchemy import Column, Integer, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base

class Place(Base):
    __tablename__ = "places"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    lat = Column(Float)
    lng = Column(Float)
    title = Column(Text)
    description = Column(Text)
    # 子要素(写真)との紐付け
    photos = relationship("Photo", back_populates="place")

class Photo(Base):
    __tablename__ = "photos"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    place_id = Column(Integer, ForeignKey("places.id")) # 外部キー
    path = Column(Text) # 画像ファイルの保存パス
    # 親要素(場所)との紐付け
    place = relationship("Place", back_populates="photos")
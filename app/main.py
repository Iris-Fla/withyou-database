import os
import shutil
from uuid import uuid4
from fastapi import FastAPI, Depends, UploadFile, File
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import models, schemas
from database import engine, get_db, wait_for_db

wait_for_db()
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="WithYou Database API", description="場所と写真を管理するAPI")

# ルートエンドポイント：Swagger UIにリダイレクト
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

# 「static」フォルダを "/static" というURLで公開する
UPLOAD_DIR = "static"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

@app.post("/places/", response_model=schemas.PlaceResponse)
def create_place(place: schemas.PlaceCreate, db: Session = Depends(get_db)):
    db_place = models.Place(**place.dict())
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place

@app.get("/places/", response_model=list[schemas.PlaceResponse])
def read_places(db: Session = Depends(get_db)):
    return db.query(models.Place).all()

@app.get("/places/{place_id}", response_model=schemas.PlaceResponse)
def read_place(place_id: int, db: Session = Depends(get_db)):
    return db.query(models.Place).filter(models.Place.id == place_id).first()

@app.put("/places/{place_id}", response_model=schemas.PlaceResponse)
def update_place(place_id: int, place: schemas.PlaceUpdate, db: Session = Depends(get_db)):
    db_place = db.query(models.Place).filter(models.Place.id == place_id).first()
    if not db_place:
        return {"エラー": "場所が見つかりません"}
    
    # 更新対象のフィールドのみ更新
    update_data = place.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_place, key, value)
    
    db.commit()
    db.refresh(db_place)
    return db_place

@app.delete("/places/{place_id}")
def delete_place(place_id: int, db: Session = Depends(get_db)):
    db_place = db.query(models.Place).filter(models.Place.id == place_id).first()
    if not db_place:
        return {"error": "Place not found"}
    
    # 写真も一緒に削除
    photos = db.query(models.Photo).filter(models.Photo.place_id == place_id).all()
    for photo in photos:
        file_path = photo.path.replace("/static/", UPLOAD_DIR + "/")
        if os.path.exists(file_path):
            os.remove(file_path)
        db.delete(photo)
    
    db.delete(db_place)
    db.commit()
    return {"メッセージ": "場所が正常に削除されました"}

# 写真のアップロードエンドポイント
@app.post("/places/{place_id}/photos/")
async def upload_photo(place_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # ユニークなファイル名を生成
    file_extension = file.filename.split(".")[-1]
    file_name = f"{uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, file_name)

    # サーバーにファイルを保存
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # DBにパスを保存（URL形式で保存しておくと便利）
    db_photo = models.Photo(place_id=place_id, path=f"/static/{file_name}")
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo

@app.get("/photos/", response_model=list[schemas.PhotoResponse])
def read_photos(db: Session = Depends(get_db)):
    return db.query(models.Photo).all()

@app.get("/photos/{photo_id}", response_model=schemas.PhotoResponse)
def read_photo(photo_id: int, db: Session = Depends(get_db)):
    return db.query(models.Photo).filter(models.Photo.id == photo_id).first()

@app.delete("/photos/{photo_id}")
def delete_photo(photo_id: int, db: Session = Depends(get_db)):
    db_photo = db.query(models.Photo).filter(models.Photo.id == photo_id).first()
    if not db_photo:
        return {"エラー": "写真が見つかりません"}
    
    # ファイルを削除
    file_path = db_photo.path.replace("/static/", UPLOAD_DIR + "/")
    if os.path.exists(file_path):
        os.remove(file_path)
    
    db.delete(db_photo)
    db.commit()
    return {"メッセージ": "写真が正常に削除されました"}
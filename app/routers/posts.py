from fastapi import Body, FastAPI, HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
from typing import List

router = APIRouter(
    prefix = '/posts'
)

@router.get('/', response_model = List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return posts


@router.get('/{id}', response_model = schemas.Post)
def get_post_by_id(id:int, db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'O post de id {id} nao foi encontrado')
    
    if post.owner_id!= current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Not authorized to perform requested action')

    return post


@router.post('/', status_code = status.HTTP_201_CREATED, response_model= schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(**post.model_dump())
    new_post.owner_id = current_user.id 
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.delete('/{id}', status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id)
    post_in_db= post.first()
    
    if post_in_db == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} does not exist')
    
    post.delete()
    db.commit()
    return {"message": "succefull"}

@router.put("/{id}")
def update_post(id: int, updated_post: schemas.PostBase, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_in_db = post_query.first()

    if post_in_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} does not exist')

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}



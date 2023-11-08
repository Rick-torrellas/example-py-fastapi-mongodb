from fastapi import APIRouter, Response , status
from config.mongodb import conection
from schemas.user import userEntity,usersEntity
from models.user import User
from passlib.hash import sha256_crypt
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT,HTTP_201_CREATED,HTTP_200_OK

database = conection.local.user
user = APIRouter()
@user.get('/users', response_model=list[User], response_description="Agarra a todos los usuarios",description="Agarra a todos los usuarios",status_code=HTTP_200_OK)
async def find_all_users():
    return usersEntity(database.find())

@user.post('/users', response_model=User)
async def create_user(user: User):
    new_user = dict(user)
    new_user["password"] = sha256_crypt.encrypt(new_user["password"])
    del new_user["id"]
    id = database.insert_one(new_user).inserted_id
    user = database.find_one({"_id": id})
    return userEntity(user)

@user.get('/users/{id}')
async def find_user(id: str):
        return userEntity(database.find_one({"_id": ObjectId(id)}))

@user.put("/users/{id}")
async def update_user(id: str, user: User):
    print(id)
    print(user)
    update_user = dict(user)
    del update_user["id"]
    database.find_one_and_update({
        "_id": ObjectId(id)
    }, {
        "$set": update_user
    })
    return userEntity(database.find_one({"_id": ObjectId(id)}))

@user.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
async def delete_user(id: str):
     database.find_one_and_delete({"_id": ObjectId(id)})
     return Response(status_code=HTTP_204_NO_CONTENT)

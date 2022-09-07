from typing import List, Union

from fastapi import FastAPI
from models import Pet, PetTransformer
from serializers import PetIsAdopted, PetSerializer, PetUpdateSerializer
from tortoise import Tortoise


app = FastAPI()


async def db_init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()

@app.on_event("startup")
async def startup():
    await db_init()

@app.get("/api/pets/", response_model=List[PetSerializer])
async def read_root(search_terms: Union[str, None] = None):
    if search_terms is None:
        return await PetTransformer.from_queryset(Pet.all())
    return await PetTransformer.from_queryset(Pet.filter(specie__in=search_terms.split(',')))


@app.get("/api/pets/{pet_id}/", response_model=PetSerializer)
async def read_pet(pet_id: int):
    return await PetTransformer.from_queryset_single(Pet.filter(id=pet_id).first())


@app.put("/api/pets/{pet_id}/")
async def update_item(pet_id: int, pet: PetUpdateSerializer):
    await Pet.filter(id=pet_id).update(**pet.dict())
    return pet


@app.post("/api/pets/", status_code=201, response_model=PetSerializer)
async def create_pet(pet: PetSerializer):
    await Pet.create(**pet.dict())
    return pet


@app.delete("/api/pets/{id}", status_code=204)
async def delete_pet(id: int):
    await Pet.filter(id=id).delete()
    return {}

@app.get("/api/pets/{id}/is_adopted", response_model=PetIsAdopted)
async def is_adopted(id: int):
    return await PetTransformer.from_queryset_single(Pet.filter(id=id).first())

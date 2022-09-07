from pydantic import BaseModel

class PetIsAdopted(BaseModel):
    is_adopted: bool

class PetSpecieOnly(BaseModel):
    specie: str

class PetSerializer(BaseModel):
    id: int
    specie: str
    is_adopted: bool

class PetUpdateSerializer(BaseModel):
    specie: str
    is_adopted: bool

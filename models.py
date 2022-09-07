from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

class Pet(Model):
    # Defining `id` field is optional, it will be defined automatically
    # if you haven't done it yourself
    id = fields.IntField(pk=True)
    specie = fields.CharField(max_length=255)
    is_adopted = fields.BooleanField(default=False)

    # Defining ``__str__`` is also optional, but gives you pretty
    # represent of model in debugger and interpreter
    def __str__(self):
        return self.specie

PetTransformer = pydantic_model_creator(Pet, name="Pet")

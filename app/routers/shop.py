from fastapi import APIRouter, HTTPException, status

from app.models import Shop, ShopIn_Pydantic
from app.models import Users, User_Pydantic  # why do you need this?
from pydantic import BaseModel

router = APIRouter(
    tags=["Shop"],
    prefix="/shop"
)


class Status(BaseModel):  # Status msg for errors
    message: str


# Get all items from shop
@router.get("/")
async def get_items():
    return await User_Pydantic.from_queryset(Shop.all())


# Get item by id
@router.get("/{item_id}")
async def get_item_by_id(item_id: int):
    return await User_Pydantic.from_queryset_single(Shop.get(id=item_id))


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User_Pydantic)  # Not copy-paste Create shop
async def create_product(product: ShopIn_Pydantic):
    product_obj = await Shop.create(**product.dict())  # чтобы добавить брать входные данные и добавлять в бд
    return await User_Pydantic.from_tortoise_orm(product_obj)  # вернуть введенные данные


@router.delete("/{product_id}", status_code=status.HTTP_410_GONE, response_model=Status)  # Delete product
async def delete_product(product_id: int):
    deleted_count = await Shop.filter(id=product_id).delete()
    if not deleted_count:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Product not found")
    return Status(message=f"Deleted product {product_id}")

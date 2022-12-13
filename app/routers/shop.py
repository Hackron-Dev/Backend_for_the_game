from fastapi import APIRouter, HTTPException, Depends, status

from app import oauth2, schemas
from app.oauth2 import get_current_user
from app.models import Shop, Shop_Pydantic, ShopIn_Pydantic

router = APIRouter(
    tags=["Shop"],
    prefix="/shop",
    dependencies=[Depends(oauth2.JWTBearer())]
)


# Get all items from shop
@router.get("")
async def get_items():
    return await Shop_Pydantic.from_queryset(Shop.all())


# Get item by id
@router.get("/{product_id}")
async def get_item_by_id(product_id: int, user_id: int = Depends(get_current_user)):
    try:
        shop_obj = await Shop_Pydantic.from_queryset_single(Shop.get(id=product_id, user=user_id))
    except:
        raise HTTPException(404, detail="NOT FOUND")
    return await shop_obj


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Shop_Pydantic)  # Not copy-paste Create shop
async def create_product(product: ShopIn_Pydantic, user_id: int = Depends(get_current_user)):
    product_obj = await Shop.create(user=user_id,
                                    **product.dict())  # чтобы добавить брать входные данные и добавлять в бд
    return await Shop_Pydantic.from_tortoise_orm(product_obj)  # вернуть введенные данные


@router.delete("/{product_id}", status_code=status.HTTP_410_GONE, response_model=schemas.Status)  # Delete product
async def delete_product(product_id: int):
    deleted_count = await Shop.filter(id=product_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return schemas.Status(message=f"Deleted product {product_id}")

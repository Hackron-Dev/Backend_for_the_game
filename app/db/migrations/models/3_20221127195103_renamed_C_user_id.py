from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "shop" DROP CONSTRAINT "fk_shop_users_8e5addcb";
        ALTER TABLE "shop" RENAME COLUMN "user_id_id" TO "user_id";
        ALTER TABLE "shop" ADD CONSTRAINT "fk_shop_users_198e0625" FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "shop" DROP CONSTRAINT "fk_shop_users_198e0625";
        ALTER TABLE "shop" RENAME COLUMN "user_id" TO "user_id_id";
        ALTER TABLE "shop" ADD CONSTRAINT "fk_shop_users_8e5addcb" FOREIGN KEY ("user_id_id") REFERENCES "users" ("id") ON DELETE CASCADE;"""

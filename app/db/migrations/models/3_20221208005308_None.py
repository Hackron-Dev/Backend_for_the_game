from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "login" VARCHAR(50) NOT NULL UNIQUE,
    "password" VARCHAR(128) NOT NULL,
    "balance" INT NOT NULL  DEFAULT 0,
    "is_admin" BOOL NOT NULL  DEFAULT False
);
COMMENT ON TABLE "users" IS 'The User model';
CREATE TABLE IF NOT EXISTS "shop" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL,
    "description" VARCHAR(200),
    "price" INT NOT NULL,
    "image" VARCHAR(200),
    "quantity" INT,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "shop" IS 'Shops Model';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """

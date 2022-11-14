from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "zip_codes" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "code" VARCHAR(5) NOT NULL UNIQUE
);;
        DROP TABLE IF EXISTS "testmodel";
        CREATE TABLE "zip_code_favourite" (
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "zip_codes_id" INT NOT NULL REFERENCES "zip_codes" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "zip_code_favourite";
        DROP TABLE IF EXISTS "zip_codes";"""

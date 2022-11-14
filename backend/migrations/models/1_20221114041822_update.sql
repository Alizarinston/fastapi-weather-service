-- upgrade --
CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(20) NOT NULL UNIQUE,
    "password_hash" VARCHAR(128)
);
-- downgrade --
DROP TABLE IF EXISTS "users";

-- upgrade --
CREATE TABLE IF NOT EXISTS "testmodel" (
    "id" VARCHAR(22) NOT NULL  PRIMARY KEY,
    "title" VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);

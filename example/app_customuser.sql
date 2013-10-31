BEGIN TRANSACTION;
DROP TABLE IF EXISTS "app_customuser";
CREATE TABLE "app_customuser" (
    "id" integer NOT NULL PRIMARY KEY,
    "username" varchar(128) NOT NULL,
    "last_login" datetime
);
COMMIT;

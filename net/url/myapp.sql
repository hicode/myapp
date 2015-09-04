BEGIN;
CREATE TABLE "myapp_market" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" varchar(8) NOT NULL,
    "currency" varchar(3) NOT NULL
)
;
CREATE TABLE "myapp_product" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "code" varchar(8) NOT NULL,
    "market" varchar(8) NOT NULL,
    "companyName" varchar(32) NOT NULL
)
;
CREATE TABLE "myapp_watchlist" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "code" varchar(8) NOT NULL,
    "market" varchar(8) NOT NULL,
    "watchReason" varchar(256) NOT NULL
)
;
CREATE TABLE "myapp_kdaily" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "code" varchar(8) NOT NULL,
    "market" varchar(8) NOT NULL,
    "p" decimal NOT NULL,
    "o" decimal NOT NULL,
    "h" decimal NOT NULL,
    "l" decimal NOT NULL,
    "c" decimal NOT NULL,
    "amt" decimal NOT NULL,
    "vol" decimal NOT NULL,
    "date" date NOT NULL
)
;
CREATE TABLE "myapp_kmin" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "code" varchar(8) NOT NULL,
    "market" varchar(8) NOT NULL,
    "p" decimal NOT NULL,
    "o" decimal NOT NULL,
    "h" decimal NOT NULL,
    "l" decimal NOT NULL,
    "c" decimal NOT NULL,
    "amt" decimal NOT NULL,
    "vol" decimal NOT NULL,
    "date" date NOT NULL,
    "time" time NOT NULL
)
;

COMMIT;

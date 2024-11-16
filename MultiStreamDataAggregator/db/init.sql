
CREATE TABLE "streamBTCUSDT" (
    "id" serial PRIMARY KEY,
    "UNIXTIME" bigint NOT NULL,
    "side" VARCHAR,
    "size" NUMERIC,
    "price" NUMERIC,
    "priceChange" VARCHAR,
    "tradeID" VARCHAR,
    "blockTrade" BOOLEAN
);

CREATE TABLE "streamETHUSDT" (
    "id" serial PRIMARY KEY,
    "UNIXTIME" bigint NOT NULL,
    "side" VARCHAR,
    "size" NUMERIC,
    "price" NUMERIC,
    "priceChange" VARCHAR,
    "tradeID" VARCHAR,
    "blockTrade" BOOLEAN
);

CREATE TABLE "streamXRPUSDT" (
    "id" serial PRIMARY KEY,
    "UNIXTIME" bigint NOT NULL,
    "side" VARCHAR,
    "size" NUMERIC,
    "price" NUMERIC,
    "priceChange" VARCHAR,
    "tradeID" VARCHAR,
    "blockTrade" BOOLEAN
);

CREATE TABLE "streamSOLUSDT" (
    "id" serial PRIMARY KEY,
    "UNIXTIME" bigint NOT NULL,
    "side" VARCHAR,
    "size" NUMERIC,
    "price" NUMERIC,
    "priceChange" VARCHAR,
    "tradeID" VARCHAR,
    "blockTrade" BOOLEAN
);
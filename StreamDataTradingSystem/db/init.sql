
CREATE TABLE stream (
    id serial PRIMARY KEY,
    UNIXTIME bigint NOT NULL,
    side VARCHAR,
    size NUMERIC,
    price NUMERIC,
    priceChange VARCHAR,
    tradeID VARCHAR,
    blockTrade BOOLEAN
);
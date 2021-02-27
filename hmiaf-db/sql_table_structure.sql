CREATE DATABASE hmiaf;

CREATE TABLE hmiaf.items(
    item_id int(16) NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
    store_name VARCHAR(64) NOT NULL,
    item_link varchar(256) NOT NULL UNIQUE,
    is_multipack BOOLEAN,
    multipack_quantity int(16)
);

CREATE TABLE hmiaf.prices(
    price_id int(16) NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
    item_id int(16) NOT NULL,
    grabbed_time DATETIME NOT NULL,
    price FLOAT NOT NULL,
    CONSTRAINT `prices.item_id`
        FOREIGN KEY (item_id) REFERENCES items (item_id) 
        ON DELETE CASCADE 
        ON UPDATE RESTRICT
);


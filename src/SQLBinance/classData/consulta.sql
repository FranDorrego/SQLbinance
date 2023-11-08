-- Creo la tabla de comprobantes
Drop table IF EXISTS comprobante;
CREATE TABLE comprobante (
    id INTEGER PRIMARY KEY,
    path TEXT,
    nombre_envia TEXT,
    CUIT_envia TEXT,
    nombre_recibe TEXT,
    CUIT_recibe TEXT,
    Cantidad REAL,
    Banco_envia TEXT,
    Banco_recibe TEXT
);

-- Creo el membrete de la operacion
DROP TABLE IF EXISTS Informe;
CREATE TABLE Informe (
    id INTEGER PRIMARY KEY,
    fecha DATE DEFAULT CURRENT_DATE, 
    punto_equilibrio REAL DEFAULT 0, 
    total_compra_fiat REAL DEFAULT 0, 
    total_venta_fiat REAL DEFAULT 0, 
    tipo_fiat TEXT DEFAULT '', 
    total_compra_cripto REAL DEFAULT 0, 
    total_venta_cripto REAL DEFAULT 0, 
    tipo_cripto TEXT DEFAULT '' 
);

-- Creo la tabla principal
Drop table IF EXISTS transacciones;
CREATE TABLE Transacciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    orderNumber TEXT,
    advNo TEXT,
    tradeType TEXT,
    asset TEXT,
    fiat TEXT,
    fiatSymbol TEXT,
    amount REAL,
    totalPrice REAL,
    unitPrice REAL,
    orderStatus TEXT,
    createTime INTEGER,
    commission REAL,
    counterPartNickName TEXT,
    advertisementRole TEXT,
    id_comprobante INTEGER DEFAULT(NULL),
    id_informe INTEGER DEFAULT(NULL),

    FOREIGN KEY (id_comprobante)
        REFERENCES Comprobante(id),
    FOREIGN KEY (id_informe)
        REFERENCES Informe(id)
);

-- ID COMPROBANTE
Drop TRIGGER IF EXISTS crea_comprobante;
CREATE TRIGGER crea_comprobante
AFTER INSERT ON Transacciones
BEGIN
    -- Inserta un registro en la tabla Comprobante
    INSERT INTO Comprobante (path) VALUES ('');

    -- Actualiza la columna id_comprobante en la tabla Transacciones
    UPDATE Transacciones
    SET id_comprobante = (SELECT last_insert_rowid() FROM Comprobante)
    WHERE id = new.id;
END;


INSERT INTO Transacciones (orderNumber, advNo, tradeType, asset, fiat, fiatSymbol, amount, totalPrice, unitPrice, orderStatus, createTime, commission, counterPartNickName, advertisementRole) VALUES (
    '20219644646554779648',
    '11218246497340923904',
    'BULL',
    'BUSD',
    'CNY',
    '￥',
    5000.00000000,
    33400.00000000,
    6.68,
    'COMPLETED',
    1619361369000,
    0,
    'ab***',
    'TAKER'
);

UPDATE Transacciones
SET id_informe = 1;

SELECT 
    tradeType,
    SUM(totalPrice) AS total_fiat,
    SUM(amount) AS total_cripto
FROM Transacciones 
WHERE id_informe = 1
GROUP BY tradeType; 


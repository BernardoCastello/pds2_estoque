CREATE SEQUENCE id_seq START 1 INCREMENT 1;
CREATE SEQUENCE venda_seq START 1 INCREMENT 1;

CREATE TABLE produtos (
    id INTEGER DEFAULT nextval('id_seq') PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cod_barras INTEGER NOT NULL,
    lote INTEGER NOT NULL,
    fabricante VARCHAR(255) NOT NULL,
    dt_fabricacao DATE,
    dt_validade DATE,
    preco DECIMAL(10, 2) NOT NULL,
    quantidade INTEGER NOT NULL,
    obs VARCHAR(255) NOT NULL
);

CREATE TABLE vendas_historico (
    venda_id INTEGER DEFAULT nextval('venda_seq') PRIMARY KEY,
    produto_id INTEGER REFERENCES produtos(id),
    data_venda DATE NOT NULL,
    quantidade INTEGER NOT NULL,
    preco_unitario DECIMAL(10, 2) NOT NULL,
    valor_total DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);


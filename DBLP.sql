CREATE SCHEMA library;

CREATE TABLE library.customers
(
    id_customer INT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,

);


CREATE TABLE library.books
(
    id_book INT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    id_genre INT NULL,
);

ALTER TABLE library.books
ADD CONSTRAINT fk_genre
FOREIGN KEY (id_genre) REFERENCES library.genders(id_gender);


CREATE TABLE library.authors
(
    id_author INT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    nationality VARCHAR(100) NULL,
);

CREATE table library.genders
(
    id_gender INT PRIMARY KEY,
    name_gender VARCHAR(100) NOT NULL,
    [description] VARCHAR(500) NULL
);



CREATE TABLE library.loans
(
    id_loan INT PRIMARY KEY,
    id_customer INT NOT NULL,
    id_book INT NOT NULL,
    loan_date DATE NOT NULL,
    return_date DATE NULL,
    loan_status BIT DEFAULT 1 NOT NULL
);

ALTER TABLE library.loans
ADD CONSTRAINT fk_customer
FOREIGN KEY (id_customer) REFERENCES library.customers(id_customer);

ALTER TABLE library.loans
ADD CONSTRAINT fk_book
FOREIGN KEY (id_book) REFERENCES library.books(id_book);



CREATE TABLE library.book_authors
(
    id_book INT NOT NULL,
    id_author INT NOT NULL,
    date_published DATE NULL,
);

ALTER TABLE library.book_authors
ADD CONSTRAINT pk_book_authors
PRIMARY KEY (id_book, id_author);

ALTER TABLE library.book_authors
ADD CONSTRAINT fk_book_ba
FOREIGN KEY (id_book) REFERENCES library.books(id_book);

ALTER TABLE library.book_authors
ADD CONSTRAINT fk_author_ba
FOREIGN KEY (id_author) REFERENCES library.authors(id_author);

SELECT * FROM library.customers;
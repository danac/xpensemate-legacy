BEGIN TRANSACTION;
CREATE TABLE balance (
	id INTEGER NOT NULL, 
	year INTEGER, 
	month INTEGER, 
	day INTEGER, 
	PRIMARY KEY (id)
);
CREATE TABLE balance_person (
	balance_id INTEGER NOT NULL, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (balance_id, person_id), 
	FOREIGN KEY(balance_id) REFERENCES balance (id), 
	FOREIGN KEY(person_id) REFERENCES person (id)
);
CREATE TABLE expense (
	id INTEGER NOT NULL, 
	year INTEGER NOT NULL, 
	month INTEGER NOT NULL, 
	day INTEGER NOT NULL, 
	description TEXT NOT NULL, 
	amount FLOAT NOT NULL, 
	person_id INTEGER NOT NULL, 
	balance_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(person_id) REFERENCES person (id), 
	FOREIGN KEY(balance_id) REFERENCES balance (id)
);
CREATE TABLE person (
	id INTEGER NOT NULL, 
	name VARCHAR(50), 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
COMMIT;

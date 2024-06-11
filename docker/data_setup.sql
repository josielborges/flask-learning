CREATE TABLE game
(
    id       SERIAL PRIMARY KEY,
    name     VARCHAR(50) NOT NULL,
    category VARCHAR(40) NOT NULL,
    console  VARCHAR(20) NOT NULL
);

CREATE TABLE appuser
(
    username VARCHAR(10) PRIMARY KEY,
    name     VARCHAR(50)  NOT NULL,
    password VARCHAR(100) NOT NULL
);

INSERT INTO appuser (name, username, password)
VALUES ('Josiel', 'josiel', '1234');
INSERT INTO appuser (name, username, password)
VALUES ('Jussara', 'jussara', '5678');
INSERT INTO appuser (name, username, password)
VALUES ('Pedro', 'pedro', '4321');

INSERT INTO game (name, category, console)
VALUES ('Tetris', 'Puzzle', 'Atari');
INSERT INTO game (name, category, console)
VALUES ('God of War', 'Hack and Slash', 'PS2');
INSERT INTO game (name, category, console)
VALUES ('Mortal Kombat I', 'Luta', 'PS2');
INSERT INTO game (name, category, console)
VALUES ('Need for Speed', 'Corrida', 'PC');
CREATE SCHEMA products
  DEFAULT CHARACTER SET utf8
  DEFAULT COLLATE utf8_general_ci;

USE products;

-- auto-generated definition
CREATE TABLE ngram
(
  id     INT AUTO_INCREMENT
    PRIMARY KEY,
  gram   VARCHAR(255) NOT NULL,
  length TINYINT(3)   NOT NULL,
  CONSTRAINT ngram_gram_uindex
  UNIQUE (gram)
)
  DEFAULT CHARACTER SET utf8
  DEFAULT COLLATE utf8_general_ci
  ENGINE = InnoDB;

ALTER TABLE ngram ADD KEY(`gram`);
-- CREATE INDEX ngram_ngram_index
--   ON ngram (gram);

CREATE INDEX ngram_length_index
  ON ngram (length);

-- auto-generated definition
CREATE TABLE word
(
  id     INT AUTO_INCREMENT
    PRIMARY KEY,
  word   VARCHAR(255) NOT NULL,
  length TINYINT(3)   NOT NULL,
  CONSTRAINT word_word_uindex
  UNIQUE (word)
)
  DEFAULT CHARACTER SET utf8
  DEFAULT COLLATE utf8_general_ci
  ENGINE = InnoDB;

CREATE INDEX word_length_index
  ON word (length);

-- auto-generated definition
CREATE TABLE word_to_ngram
(
  word_id  INT NOT NULL,
  ngram_id INT NOT NULL,
  PRIMARY KEY (word_id, ngram_id)
)
  DEFAULT CHARACTER SET utf8
  DEFAULT COLLATE utf8_general_ci
  ENGINE = InnoDB;

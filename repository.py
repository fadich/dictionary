import sql


def insert(word, length):
    """ Insert new word with N-grams """

    # TODO: check the word existence!
    # ...
    grams = parse_ngrams(word)

    q_word = "INSERT INTO `dictionary`.`word` ('word', 'length') VALUES ('" + word + "', " + str(length) + ");"
    # Execute and get word ID
    word_id = 0

    for gram in grams:
        # TODO: check the ngram existence and get it's ID!
        # else:
        # q_gram = "SELECT id FROM `ngram` WHERE `gram` = '%s'" % gram
        # gram_id = execute
        gram_id = 0

        if not gram_id:
            q_gram = "INSERT INTO `ngram` ('gram', 'length') VALUE ('%s', %d);" % (gram, len(gram))
            # Execute and get n-gram ID
            gram_id = 0

        q_ref = "INSERT INTO `word_to_ngram` ('word_id', 'ngram_id') VALUE ('%d', %d);" % (word_id, gram_id)


def parse_ngrams(word):
    """ Get words' N-grams"""

    grams = []
    length = len(word)
    for size in range(1, length + 1):
        for current in range(length):
            if size + current <= length:
                grams.append(word[current:(size + current)])

    return grams

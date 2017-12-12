import MySQLdb


try:
    db = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="toor",
        db="dictionary")
except MySQLdb.Error as err:
    print("Connection error: {}".format(err))


def insert(word, length):
    """ Insert new word with N-grams """

    # TODO: check the word existence!
    # ...
    grams = parse_ngrams(word)

    q_word = """INSERT INTO `dictionary`.`word` (`word`, `length`) VALUES ('%s', %d);""" % (word, length)

    try:
        cur = db.cursor(MySQLdb.cursors.DictCursor)
        # cur.execute(q_word)
        word_id = cur.lastrowid
        db.commit()
    except MySQLdb.Error as err:
        print("Query error: {}".format(err))
        return

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

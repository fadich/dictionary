import MySQLdb


try:
    db = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="toor",
        db="dictionary")
except MySQLdb.Error as err:
    print("Connection error: {}".format(err))


def insert(word):
    """ Insert new word with N-grams """
    db.rollback()

    try:
        cur = db.cursor(MySQLdb.cursors.DictCursor)
    except MySQLdb.Error as error:
        print("Query error: {}".format(error))
        return

    # TODO: check the word existence!
    # ...

    q_word = """INSERT INTO `word` (`word`, `length`) VALUES (%s, %s);"""

    try:
        cur.execute(q_word, (word.lower(), len(word)))
        word_id = cur.lastrowid
    except MySQLdb.Error as error:
        db.rollback()
        print("Word // Query error: {}".format(error))
        return

    if not word_id:
        db.rollback()
        return

    grams = set([s.lower() for s in parse_ngrams(word)])
    for gram in grams:

        q_gram = """SELECT id FROM `ngram` WHERE `gram` = %s;"""

        try:
            cur.execute(q_gram.lower(), (gram,))
            gram_inf = cur.fetchone()
        except MySQLdb.Error as error:
            db.rollback()
            print("N-Gram select " + gram + "// Query error: {}".format(error))
            return

        if not gram_inf:
            q_gram = """INSERT INTO `ngram` (`gram`, `length`) VALUE (%s, %s);"""

            try:
                cur.execute(q_gram, (gram.lower(), len(gram)))
                gram_id = cur.lastrowid
            except MySQLdb.Error as error:
                db.rollback()
                print("N-Gram insert " + gram + "// Query error: {}".format(error))
                return
        else:
            gram_id = gram_inf.get('id')

        q_ref = """INSERT INTO `word_to_ngram` (`word_id`, `ngram_id`) VALUE (%s, %s);"""
        try:
            cur.execute(q_ref, (word_id, gram_id))
        except MySQLdb.Error as error:
            db.rollback()
            print("Relation insert for " + gram + " // Query error: {}".format(error))
            return

    db.commit()


def parse_ngrams(word):
    """ Get words' N-grams"""

    grams = []
    length = len(word)
    for size in range(1, length + 1):
        for current in range(length):
            if size + current <= length:
                grams.append(word[current:(size + current)])

    return grams

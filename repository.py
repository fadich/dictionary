import MySQLdb
import sys
import re


reload(sys)
sys.setdefaultencoding('utf-8')

try:
    db = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="toor",
        db="products_2",
        charset='utf8')
except MySQLdb.Error as err:
    print("Connection error: {}".format(err))

try:
    cur = db.cursor(MySQLdb.cursors.DictCursor)
except MySQLdb.Error as error:
    print("Query error: {}".format(error))


def insert(word):
    """ Insert new word with N-grams """
    db.rollback()

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

    grams = parse_ngrams(word)
    for gram in grams:
        if not len(gram):
            continue

        q_gram = """SELECT id FROM `ngram` WHERE `gram` = %s;"""

        try:
            cur.execute(q_gram, (gram,))
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
            # db.rollback()
            # print("Relation insert for " + gram + " // Query error: {}".format(error))
            ''
            # return

    db.commit()


def parse_ngrams(word, unique=True, lower=True, min=2, max=2):
    """ Get words' N-grams"""

    word = re.sub(u"[\s\.\\\/\!\@\#\$\%\^\&\*\(\)\_\-\+\~\`\,\'\"\]\[\{\}\=]+", '', word)

    if min >= len(word):
        min = len(word) - 2
    if max >= len(word):
        max = len(word)

    grams = []
    length = len(word)
    for size in range(min, max + 1):
        for current in range(length):
            if size + current <= length:
                grams.append(word[current:(size + current)])

    if lower:
        grams = [gram.lower() for gram in grams]
    if unique:
        grams = set(grams)

    return grams


def search(query, order='DESC'):
    """ Searching word by query """

    query = re.sub(u"[\s\.\\\/\!\@\#\$\%\^\&\*\(\)\_\-\+\~\`]+", '', query)

    if not query:
        return None

    if len(query) <= 3:
        q_search = """
            SELECT
              w.word       AS `Word`,
              w.length     AS `Length`,
              1 / w.length AS `Score`
            FROM word w
            WHERE %s
            ORDER BY `Score` %s, w.length %s
                """
        conditions = 'w.word LIKE(\'%' + query + '%\')'
    else:
        grams = parse_ngrams(query)
        q_search = """
            SELECT
              w.word        AS `Word`,
              MAX(n.length) AS `Length`,
              -- GROUP_CONCAT(n.gram) AS `N-grams`,
              SUM(n.length) AS `Score`
            FROM ngram n
            INNER JOIN word_to_ngram wn ON wn.ngram_id = n.id
            INNER JOIN word          w  ON wn.word_id = w.id
            WHERE %s
            GROUP BY w.id
            ORDER BY `Score` %s, w.length %s
        """
        conditions = 'n.gram IN(' + ','.join(["'%s'" % gram for gram in grams]) + ')'

    sec_order = "ASC" if order == "DESC" else "DESC"

    try:
        cur.execute(q_search % (conditions, order, sec_order))
        res = cur.fetchall()
    except MySQLdb.Error as error:
        db.rollback()
        print("Search words // Query error: {}".format(error))
        return

    return res

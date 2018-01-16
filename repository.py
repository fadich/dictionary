import MySQLdb
import sys
import re


reload(sys)
sys.setdefaultencoding('utf-8')

words = list()

try:
    db = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="toor",
        db="words",
        charset='utf8')
except MySQLdb.Error as err:
    print("Connection error: {}".format(err))

try:
    cur = db.cursor(MySQLdb.cursors.DictCursor)
except MySQLdb.Error as error:
    print("Query error: {}".format(error))

try:
    q_init = """
        SELECT
          w.word       AS `word`
        FROM word w
    """

    cur.execute(q_init)
    res = cur.fetchall()
    if res:
        for word in res:
            word['_word'] = re.sub(u"[\s\.\\\/\!\@\#\$\%\^\&\*\(\)\_\-\+\~\`\,\'\"\]\[\{\}\=]+", '', word.get('word')).lower()
            words.append(word)
except MySQLdb.Error as error:
    print("Query error: {}".format(error))


def insert(word):
    """Insert new word"""
    db.rollback()

    q_word = """INSERT INTO `word` (`word`, `length`) VALUES (%s, %s);"""

    try:
        cur.execute(q_word, (word, len(word)))
    except MySQLdb.Error as error:
        db.rollback()
        print("Word // Query error: {}".format(error))
        return

    words.append(word)

    db.commit()


def parse_ngrams(word, unique=True, lower=True, min=2, max=3):
    """ Get words' N-grams"""

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


def search(query):
    res = []
    query = re.sub(u"[\s\.\\\/\!\@\#\$\%\^\&\*\(\)\_\-\+\~\`\,\'\"\]\[\{\}\=]+", '', query)
    opt_len = 2 if len(query) < 6 else int(len(query) / 2)
    grams = parse_ngrams(query, min=opt_len, max=opt_len)

    for word in words:
        score = 0.0
        for gram in grams:
            length = len(gram)
            score += word.get('_word').count(gram) * length
        if score:
            word['_score'] = score
            res.append(word)

    # Sorting results...
    for i in range(len(res) - 1):
        k = i + 1
        while k:
            if res[k].get('_score') < res[k - 1].get('_score'):
                res[k - 1], res[k] = res[k], res[k - 1]
                k -= 1
                continue

            break

    return res

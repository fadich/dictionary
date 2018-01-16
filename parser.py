import repository
import sys


reload(sys)
sys.setdefaultencoding('utf-8')

resource = open('source/words.txt', 'r')

i = 1
word = resource.readline().strip()
while word:
    print("%s" % word)

    repository.insert(word.decode('utf-8'))

    i += 1
    word = resource.readline().strip()

resource.close()


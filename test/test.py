from snownlp import SnowNLP
import jieba


if __name__ == '__main__':
    s = '刚拿到,很新,因为主板没到所以没有装机后续跟进'
    # jieba.add_word("不高兴")
    k = SnowNLP(s).sentiments
    print(k)
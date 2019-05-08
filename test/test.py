from snownlp import SnowNLP

ci_path = r"./static/data/analysis.txt"
with open(ci_path, 'r', encoding='utf-8') as f:
    while True:
        try:
            s = f.readline()
            p = SnowNLP(s).sentiments
            print(s.strip('\n') + "|||||||||" + str(p))
        except IOError as e:
            print(e)

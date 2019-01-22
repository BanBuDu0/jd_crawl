from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import time

str = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
def generateByfrequent(ci):
    # ci = test.hotcomments()
    font = r'./simhei.ttf'
    wordcloud = WordCloud(background_color="white", width=1000, height=860, font_path=font).generate_from_frequencies(
        ci)
    path = "./static/{}hotcomments.jpg".format(str)
    wordcloud.to_file(path)
    return path
    '''
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    '''

def generateByText(ci):
    font = r'./simhei.ttf'
    stopwords = STOPWORDS.copy()
    stopwords.add('此用户未填写评价内容')
    # str = ['此用户未填写评价内容']
    wordcloud = WordCloud(background_color="white", width=1000, height=860, font_path=font, stopwords=stopwords).generate(ci)
    path = "./static/{}pcomments.jpg".format(str)
    wordcloud.to_file(path)
    return path
    '''
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    '''



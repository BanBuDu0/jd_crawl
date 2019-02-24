from multiprocessing import Pool
import requests


def get_page(url):
    ret = requests.get(url).text
    return {'url': url, 'ret': ret}


def parse_page(ret):
    with open('ab.txt', 'a') as f:
        f.write('%s - %s\n' % (ret['url'], len(ret['ret'])))


if __name__ == '__main__':
    urls = [
    'https://www.baidu.com',
    'http://www.sina.com.cn/'
    ]
    p = Pool()
    for url in urls:
        p.apply_async(get_page, args=(url,), callback=parse_page)
    p.close()
    p.join()
    print('主')
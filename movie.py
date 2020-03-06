from urllib.request import urlopen
import re
import json

# +++++++++++++++++++++++++++++++++++++++#
# https://www.jianshu.com/p/9ebf6924f613
# +++++++++++++++++++++++++++++++++++++++#
def get_dytt_url(homepage):
    index_content = urlopen(homepage).read().decode('gbk', 'ignore')  # 获取电影天堂主页源代码
    index_obj = re.compile(r"最新电影下载</a>]<a href='(?P<film_url>.*?)'>", re.S)  # 2019新片精品链接
    return index_obj.finditer(index_content)  # 创建一个迭代器


def get_dytt_info(film_url_ite):
    for k, fil_url in enumerate(film_url_ite, 1):  # 遍历电影每个url
        print(k, homepage + fil_url.group("film_url"))
        film_content = urlopen(homepage + fil_url.group("film_url")).read().decode('gbk', 'ignore')  # 获取2019新片精品源代码
        film_obj = re.compile(r'◎译　　名(?P<trans_name>.*?)<br />.*?◎片　　名(?P<film_name>.*?)<br />.*?'
                              r'◎主　　演(?P<film_actor>.*?)<br /><br />.*?<td style="WORD-WRAP: break-word" '
                              r'bgcolor="#fdfddf"><a href="(?P<down_url>.*?)">', re.S)
        yield film_obj.finditer(film_content)  # 生成器函数


def record_dytt_info(film_ite, json_file, i):
    for film in film_ite:  # 遍历每部电影
        film_dict = {}
        film_dic = {}
        film_dic['trans_name'] = film.group("trans_name").strip().replace('&middot;', '·')  # 电影译名放入字典
        film_dic['film_name'] = film.group("film_name").strip().replace('&middot;', '·')  # 电影名放入字典
        farts_lst = film.group("film_actor").strip().split('<br />')  # 主演列表
        farts = []
        for art in farts_lst:  # 遍历主演
            farts.append(art.strip().replace('&middot;', '·'))  # 字符串替换
        film_dic['film_actor'] = farts  # 主演放入字典
        film_dic['down_url'] = film.group("down_url").strip()  # 下载url放入字典
        film_dict[i] = film_dic  # 将字典放入电影数数字典
        mode_type = "w" if i == 1 else "a"  # 当i=1时,清空json文件,否则追加写入
        with open(json_file, mode=mode_type, encoding="utf-8") as f:
            f.write(json.dumps(film_dict, ensure_ascii=False, indent=2) + ",\n")


if __name__ == "__main__":
    homepage = "https://www.dytt8.net"  # 电影天堂主页
    film_url_ite = get_dytt_url(homepage)  # 电影url迭代器
    for i, film_info_ite in enumerate(get_dytt_info(film_url_ite), 1):  # 遍历迭代器函数
        record_dytt_info(film_info_ite, "film_info.json", i)  # 获取电影的主演/名字/下载链接

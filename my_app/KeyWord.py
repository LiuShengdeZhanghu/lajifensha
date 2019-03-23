#coding=gbk
import jieba
import os
import re
import jieba.analyse
import csv
from numpy.linalg import svd
import math
import numpy

class KeyWord:
    def __init__(self):
        self.source_path = os.path.abspath('.')+"\\static\\"
        self.pattern = re.compile(r"^[A-Za-z0-9\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+$")
        self.stop_words_list_path = self.source_path + 'stopWord_1.txt'
        self.read_data_path = self.source_path + 'demo100-2.csv'
        self.keyword_list =['垃圾','项目','生活','建设','环保','城市','烟气','排放','发展','发电厂','设施','运营','工程','填埋','能力',
                '国家','系统','分类','居民','社会','规模','亿元','公众','控制','焚烧炉','飞灰','信息','工艺','填埋场','情况',
                '全国','提高','焚烧厂','炉排','资源化','循环','监测','周边','固废','资源','推进','净化','实施','市场','浓度',
                '水平','回收','解决','监管']
        self.wordNum_list = ['垃圾', '焚烧', '项目', '生活', '发电', '建设', '环保', '环境', '技术',
                    '城市', '烟气', '排放', '企业', '发展', '发电厂', '标准', '投资', '行业','公司', '政府',
                    '采用', '设施', '运行', '无害化', '运营', '工程', '污染', '填埋', '工作','能力', '设备',
                    '国家', '系统', '分类', '管理', '规划', '污染物', '居民', '社会', '规模','亿元', '过程',
                    '公众', '控制', '处置', '经济', '焚烧炉', '设计', '飞灰', '影响', '信息', '工艺', '填埋场',
                    '产业', '报告', '滤液', '情况', '公开', '全国', '国际','能源', '提高', '焚烧厂', '建成',
                    '分析', '炉排', '资源化', '循环', '监测', '光大', '周边','固废', '资源', '推进', '净化',
                    '实施', '邻避', '成本', '锅炉', '市场', '浓度', '水平', '生产', '数据', '研究', '政策',
                    '发布', '处理厂', '群众', '措施', '回收', '选址', '生态','提供', '解决', '先进','监管',
                    '部门', '减少','投入']
        self.num_list = [0, 2, 3, 5, 6, 9, 10, 11, 13, 14, 21, 24, 25, 27, 29, 31, 32, 33, 37, 38, 39,
                         40, 42, 43, 46, 48, 50, 51, 52, 56, 58, 61, 62, 65, 66, 67, 68, 70, 71, 72, 73,
                         74, 75, 79, 80, 81, 90, 94, 96]
        self.stop_words_list = []
        self.stop_words_list_ge = (
            line.strip()
            for line in open(self.stop_words_list_path, 'r',
                             encoding='UTF-8').readlines())
        for wd in self.stop_words_list_ge:
            self.stop_words_list.append(wd)

    def TF_IDFKeyWord(self,content):
        keyWord = jieba.analyse.extract_tags(content,topK=15,withWeight=True,allowPOS=( 'n', 'vn', 'v'))
        rt_list = []
        for item in keyWord:
            rt_list.append({item[0]:item[1]})
        return rt_list

    def word_judge(self, seg):
        if len(seg) < 2:
            return False
        match = self.pattern.match(seg)
        if match:
            return False
        if seg in self.stop_words_list:
            return False
        return True

    def data_prepare(self,content):
        word_list1 = jieba.cut(content)
        word_list2 = []
        for item in word_list1:
            if self.word_judge(item):
                word_list2.append(item)
        time_list = []
        for word1 in self.wordNum_list:
            time = 0
            for word2 in word_list2:
                if word1 == word2:
                    time += 1
            time_list.append(time)
        csv_file = csv.reader(open(self.read_data_path, 'r'))
        matrix_word = numpy.array([word for word in csv_file])
        new_matrix_word = numpy.delete(matrix_word, 0, axis=0)
        #把案例的词频填入
        new_matrix_word = numpy.vstack((numpy.array([time_list]),new_matrix_word))
        new_matrix_word = numpy.array(new_matrix_word, dtype=float)
        u, s, v = svd(new_matrix_word)
        list2 = []
        #求出当前案例的关键词到文本的语义距离
        for i in range(1):
            for j in range(100):
                list1 = []
                for k in range(10):
                    s = u[i][k] - v[k][j]
                    list1.append(s)
                num = math.sqrt(sum([pow(s, 2) for s in list1]))
                list2.append(num)
        word_to_text = []
        for i in self.num_list:
            word_to_text.append(list2[i])
        return word_to_text

    #一个测试方法，找出聚类后的关键词在矩阵中的位置
    def test(self):
        list = []
        for i in range(len(self.wordNum_list)):
            if self.wordNum_list[i] in self.keyword_list:
                list.append(i)
        print(list)


# self.keyword_list =['垃圾','项目','生活','建设','环保','城市','烟气','排放','发展','发电厂','设施','运营','工程','填埋','能力',
#                 '国家','系统','分类','居民','社会','规模','亿元','公众','控制','焚烧炉','飞灰','信息','工艺','填埋场','情况',
#                 '全国','提高','焚烧厂','炉排','资源化','循环','监测','周边','固废','资源','推进','净化','实施','市场','浓度',
#                 '水平','回收','解决','监管']
# kk = KeyWord()
# str = """2016年6月25日，湖北省仙桃市居民为抗议垃圾焚烧发电厂建设，走上街头。仙桃官方试图说服市民，建垃圾焚烧发电厂对仙桃市具有显著的经济效益、社会效益和环境效益。仙桃市生活垃圾焚烧发电厂（下称垃圾焚烧发电厂），其主要功能是消纳仙桃市区和周边乡镇的生活垃圾。项目位于仙桃市干河办事处郑仁口村。
#         抗议民众认为，仙桃市政府刻意隐瞒垃圾焚烧发电厂建设，从选址到招标和建设已超过两年，除官方在网上公示，更多居民无从知情。该垃圾焚烧发电厂在建设施工中也未打标语，其用途附近居民甚至都不知晓。仙桃市长周文霞曾亲自走到街头与抗议居民对话。然而最终，仙桃市人民政府新闻办公室不得不透过官方微博发布通告。
#         此前，这一项目被仙桃市政府全力推进。仙桃市人民政府披露的消息显示，这一垃圾焚烧项目已经开工建设两年，原本预计于2016年年底点火试烧。可以在仙桃市政府官网看到，仙桃市人民政府新闻办公室26日下午发布的最新通告为《关于停止“生活垃圾焚烧发电项目”的通告》。该通告称，26日12时，经市委市政府研究，决定停止“生活垃圾焚烧发电项目”。希望广大市民不信谣、不传谣、不围观、不采取过激行为，遵纪守法，共同维护仙桃大局稳定。据此前报道，26日上午，仙桃市人民政府官网先后发布两条消息称，仙桃市生活垃圾焚烧发电项目旨在解决市民的生活垃圾处置问题。部分群众对生活垃圾焚烧发电项目存在疑虑，为了消除疑虑、维护稳定，经项目工程建设指挥部研究并报市政府批准，该项目暂缓建设，待进一步评估论证、征求广大市民意见后再行决定。据了解，民众不满的主要是选择距离居住区太近，以及担心没有有效的机制可以监督焚烧厂按照规范运作。有人认为这是盲目的“邻避效应”在起作用，担心民众这样的抗议会导致几年后仙桃垃圾围城。这恐怕也是因为地方政府在这类化工项目的监管上总出问题，才令大家如此不放心，宁愿不要也不愿承担风险。实际上，将板子都打在“邻避问题”也根本无助于解决这类在中国已经越来越频出的冲突，强力的监管与对民众有效畅通投诉惩罚机制，才是破解难题的钥匙。否则，事情的结果，永远只会是双输。
#         据仙桃官方报道，引发这次事件的这一生活垃圾焚烧发电项目由香港绿色东方投资控股有限公司以BOT模式与仙桃市政府合作兴建，2013年8月获省发改委正式立项核准。2014年6月24日奠基。生活垃圾焚烧发电项目一期规模为一炉一机。即一条日处理500吨生活垃圾焚烧线；一台9MW汽轮发电机组。采用具有国际先进水平的机械炉排炉，配有设备完善的尾气处理工艺，保证尾气各项污染排放指标优于国家标准，其中二噁英排放指标达到欧盟Ⅱ标准。预计于2015年2月安装完工，5月正式投产运营发电。投产使用后，将推进城乡生活垃圾处理无害化，减量化和资源再利用，将有力保护城市环境，节约土地资源，促进仙桃经济社会可持续发展。
#         可是，就是这么一个“利国利民”的好事，老百姓却不买账！
#         就其原因，无非是即使技术过关，老百姓也根本不相信企业会真正在环保上花这个代价，也不相信相关部门会真正监管到位，食品安全该是不存在技术问题吧，为什么企业还是用地沟油、苏丹红、三聚氰胺？利益驱使；企业为什么敢这样？某些部门监管不到位！
#         有知名仙桃籍法学者说，每次回老家，一进仙桃城区范围的高速路段，一股恶臭扑鼻而来。刚开始以为是谁在车里放屁了，后来发现是仙桃化工区飘来的。他很感概，“谁在我的家乡放了一个臭屁，然后走了！”
#         这次仙桃事件，可能发端于垃圾焚烧发电项目，但发源于爱家园，故土情深，对这种群众性自发的邻避运动，既然垃圾处理技术过关，就应该要进行科普，让老百姓知情，重在沟通和协商，采取强硬手段似为不妥。
#         正如另一知名仙桃籍法学学者所言：垃圾焚烧厂之规划兹事体大，若有差池，受害者并非仅为普通群众、普通公务员，警察、当地领导也可能被殃及。硬性维稳，事件或暂时获得平息，但政府的公信力一定加倍流失。诚哉斯言。
#         湖北省纪委就此发布问责通报，因在事件中领导不力、工作失职，造成恶劣影响，湖北省委决定，免去仙桃市委书记冯云乔（副厅级）职务，终止其提拔任用程序。与此同时湖北省已问责干部300人，处分206人。为推进问责工作，湖北省研究制定了《党风廉政建设主体责任和监督责任追究暂行办法》和《行政问责办法》，目前正抓紧制定《中国共产党问责条例》实施办法。          """
# kk.data_prepare(str)
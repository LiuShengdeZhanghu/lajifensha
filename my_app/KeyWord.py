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
        self.pattern = re.compile(r"^[A-Za-z0-9\s+\.\!\/_,$%^*(+\"\']+|[+��������������~@#��%����&*����]+$")
        self.stop_words_list_path = self.source_path + 'stopWord_1.txt'
        self.read_data_path = self.source_path + 'demo100-2.csv'
        self.keyword_list =['����','��Ŀ','����','����','����','����','����','�ŷ�','��չ','���糧','��ʩ','��Ӫ','����','����','����',
                '����','ϵͳ','����','����','���','��ģ','��Ԫ','����','����','����¯','�ɻ�','��Ϣ','����','����','���',
                'ȫ��','���','���ճ�','¯��','��Դ��','ѭ��','���','�ܱ�','�̷�','��Դ','�ƽ�','����','ʵʩ','�г�','Ũ��',
                'ˮƽ','����','���','���']
        self.wordNum_list = ['����', '����', '��Ŀ', '����', '����', '����', '����', '����', '����',
                    '����', '����', '�ŷ�', '��ҵ', '��չ', '���糧', '��׼', 'Ͷ��', '��ҵ','��˾', '����',
                    '����', '��ʩ', '����', '�޺���', '��Ӫ', '����', '��Ⱦ', '����', '����','����', '�豸',
                    '����', 'ϵͳ', '����', '����', '�滮', '��Ⱦ��', '����', '���', '��ģ','��Ԫ', '����',
                    '����', '����', '����', '����', '����¯', '���', '�ɻ�', 'Ӱ��', '��Ϣ', '����', '����',
                    '��ҵ', '����', '��Һ', '���', '����', 'ȫ��', '����','��Դ', '���', '���ճ�', '����',
                    '����', '¯��', '��Դ��', 'ѭ��', '���', '���', '�ܱ�','�̷�', '��Դ', '�ƽ�', '����',
                    'ʵʩ', '�ڱ�', '�ɱ�', '��¯', '�г�', 'Ũ��', 'ˮƽ', '����', '����', '�о�', '����',
                    '����', '������', 'Ⱥ��', '��ʩ', '����', 'ѡַ', '��̬','�ṩ', '���', '�Ƚ�','���',
                    '����', '����','Ͷ��']
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
        #�Ѱ����Ĵ�Ƶ����
        new_matrix_word = numpy.vstack((numpy.array([time_list]),new_matrix_word))
        new_matrix_word = numpy.array(new_matrix_word, dtype=float)
        u, s, v = svd(new_matrix_word)
        list2 = []
        #�����ǰ�����Ĺؼ��ʵ��ı����������
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

    #һ�����Է������ҳ������Ĺؼ����ھ����е�λ��
    def test(self):
        list = []
        for i in range(len(self.wordNum_list)):
            if self.wordNum_list[i] in self.keyword_list:
                list.append(i)
        print(list)


# self.keyword_list =['����','��Ŀ','����','����','����','����','����','�ŷ�','��չ','���糧','��ʩ','��Ӫ','����','����','����',
#                 '����','ϵͳ','����','����','���','��ģ','��Ԫ','����','����','����¯','�ɻ�','��Ϣ','����','����','���',
#                 'ȫ��','���','���ճ�','¯��','��Դ��','ѭ��','���','�ܱ�','�̷�','��Դ','�ƽ�','����','ʵʩ','�г�','Ũ��',
#                 'ˮƽ','����','���','���']
# kk = KeyWord()
# str = """2016��6��25�գ�����ʡ�����о���Ϊ�����������շ��糧���裬���Ͻ�ͷ�����ҹٷ���ͼ˵�����񣬽��������շ��糧�������о��������ľ���Ч�桢���Ч��ͻ���Ч�档�����������������շ��糧���³��������շ��糧��������Ҫ���������������������ܱ������������������Ŀλ�������иɺӰ��´�֣�ʿڴ塣
#         ����������Ϊ���������������������������շ��糧���裬��ѡַ���б�ͽ����ѳ������꣬���ٷ������Ϲ�ʾ����������޴�֪�顣���������շ��糧�ڽ���ʩ����Ҳδ��������;����������������֪���������г�����ϼ�������ߵ���ͷ�뿹�����Ի���Ȼ�����գ������������������Ű칫�Ҳ��ò�͸���ٷ�΢������ͨ�档
#         ��ǰ����һ��Ŀ������������ȫ���ƽ�������������������¶����Ϣ��ʾ����һ����������Ŀ�Ѿ������������꣬ԭ��Ԥ����2016����׵�����ա��������������������������������������������Ű칫��26�����緢��������ͨ��Ϊ������ֹͣ�������������շ�����Ŀ����ͨ�桷����ͨ��ƣ�26��12ʱ������ί�������о�������ֹͣ�������������շ�����Ŀ����ϣ�����������ҥ������ҥ����Χ�ۡ�����ȡ������Ϊ������ط�����ͬά�����Ҵ���ȶ����ݴ�ǰ������26�����磬�������������������Ⱥ󷢲�������Ϣ�ƣ������������������շ�����Ŀּ�ڽ����������������������⡣����Ⱥ�ڶ������������շ�����Ŀ�������ǣ�Ϊ���������ǡ�ά���ȶ�������Ŀ���̽���ָ�Ӳ��о�������������׼������Ŀ�ݻ����裬����һ��������֤��������������������о��������˽⣬���ڲ�������Ҫ��ѡ������ס��̫�����Լ�����û����Ч�Ļ��ƿ��Լල���ճ����չ淶������������Ϊ����äĿ�ġ��ڱ�ЧӦ���������ã��������������Ŀ���ᵼ�¼������������Χ�ǡ������Ҳ����Ϊ�ط����������໯����Ŀ�ļ�����ܳ����⣬��������˲����ģ���Ը��ҪҲ��Ը�е����ա�ʵ���ϣ������Ӷ����ڡ��ڱ����⡱Ҳ���������ڽ���������й��Ѿ�Խ��ԽƵ���ĳ�ͻ��ǿ���ļ�����������Ч��ͨͶ�߳ͷ����ƣ������ƽ������Կ�ס���������Ľ������Զֻ����˫�䡣
#         �����ҹٷ���������������¼�����һ�����������շ�����Ŀ�������ɫ����Ͷ�ʿع����޹�˾��BOTģʽ�����������������˽���2013��8�»�ʡ����ί��ʽ�����׼��2014��6��24�յ���������������շ�����Ŀһ�ڹ�ģΪһ¯һ������һ���մ���500���������������ߣ�һ̨9MW���ַ�����顣���þ��й����Ƚ�ˮƽ�Ļ�е¯��¯�������豸���Ƶ�β���������գ���֤β��������Ⱦ�ŷ�ָ�����ڹ��ұ�׼�����ж��fӢ�ŷ�ָ��ﵽŷ�ˢ��׼��Ԥ����2015��2�°�װ�깤��5����ʽͶ����Ӫ���硣Ͷ��ʹ�ú󣬽��ƽ������������������޺���������������Դ�����ã��������������л�������Լ������Դ���ٽ����Ҿ������ɳ�����չ��
#         ���ǣ�������ôһ�����������񡱵ĺ��£��ϰ���ȴ�����ˣ�
#         ����ԭ���޷��Ǽ�ʹ�������أ��ϰ���Ҳ������������ҵ�������ڻ����ϻ�������ۣ�Ҳ��������ز��Ż�������ܵ�λ��ʳƷ��ȫ���ǲ����ڼ�������ɣ�Ϊʲô��ҵ�����õع��͡��յ��졢�����谷��������ʹ����ҵΪʲô��������ĳЩ���ż�ܲ���λ��
#         ��֪�����Ҽ���ѧ��˵��ÿ�λ��ϼң�һ�����ҳ�����Χ�ĸ���·�Σ�һ�ɶ���˱Ƕ������տ�ʼ��Ϊ��˭�ڳ����ƨ�ˣ��������������һ�����Ʈ���ġ����ܸиţ���˭���ҵļ������һ����ƨ��Ȼ�����ˣ���
#         ��������¼������ܷ������������շ�����Ŀ������Դ�ڰ���԰���������������Ⱥ�����Է����ڱ��˶�����Ȼ���������������أ���Ӧ��Ҫ���п��գ����ϰ���֪�飬���ڹ�ͨ��Э�̣���ȡǿӲ�ֶ���Ϊ���ס�
#         ������һ֪�����Ҽ���ѧѧ�����ԣ��������ճ�֮�滮����������в�أ��ܺ��߲��ǽ�Ϊ��ͨȺ�ڡ���ͨ����Ա�����졢�����쵼Ҳ���ܱ��꼰��Ӳ��ά�ȣ��¼�����ʱ���ƽϢ���������Ĺ�����һ���ӱ���ʧ������˹�ԡ�
#         ����ʡ��ί�ʹ˷�������ͨ���������¼����쵼����������ʧְ����ɶ���Ӱ�죬����ʡί��������ȥ������ί��Ƿ����ǣ���������ְ����ֹ��������ó������ͬʱ����ʡ������ɲ�300�ˣ�����206�ˡ�Ϊ�ƽ�������������ʡ�о��ƶ��ˡ��������������������κͼල����׷�����а취���͡���������취����Ŀǰ��ץ���ƶ����й�����������������ʵʩ�취��          """
# kk.data_prepare(str)
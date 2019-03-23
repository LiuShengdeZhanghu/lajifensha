import xlrd
# import numpy
import math
import os

# import os

class sim_calByCenter:
    def __init__(self):
        self.source_path = os.path.abspath('.') + "\\static\\"
        self.read_data_path = self.source_path+"cluster_center_data.xlsx"

    def read_data(self,clusterCenter_file):
        '''
        从聚类产生的excel表中读取数据，用于相似度的计算
        '''
        # 读取excel数据
        workbook = xlrd.open_workbook(clusterCenter_file)
        # 定位工作表
        sheet = workbook.sheet_by_index(0)
        # print(sheet.nrows,sheet.ncols)

        # 行数
        row_num = sheet.nrows
        # 列数
        col_num = sheet.ncols

        # 存储读取到的数据
        clusterCenter_list = []

        row_index = 0
        while (row_index < row_num):
            list = []
            col_index = 0
            while (col_index < col_num):
                # print(sheet.cell_value(row_index,col_index))
                list.append(sheet.cell_value(row_index, col_index))
                col_index = col_index + 1
            row_index = row_index + 1
            clusterCenter_list.append(list)
        return clusterCenter_list


    def cosine_dis(self,current_data):
        '''
        余弦相似度算法
        '''
        # 存储相似度计算结果
        # result = {}
        clusterCenter_list = self.read_data(self.read_data_path)
        result = []
        for data in clusterCenter_list:
            sum_xx = 0
            sum_yy = 0
            sum_xy = 0
            index = 0
            while (index < len(data)):
                sum_xy += float(current_data[index]) * float(data[index])
                sum_xx += math.pow(float(current_data[index]), 2)
                sum_yy += math.pow(float(data[index]), 2)
                index += 1
            # print(sum_xy)
            # print(sum_xx)
            # print(sum_yy)
            sim_value = sum_xy / (math.sqrt(sum_xx) * math.sqrt(sum_yy))
            # result[data[len(data) - 1]] = sim_value
            result.append(sim_value)
        print(result)
        max_simValue = max(result)
        print(max_simValue)
        if result.index(max_simValue) == 0:
            result.append("A")
            return result
        elif result.index(max_simValue) == 1:
            result.append("B")
            return result
        elif result.index(max_simValue) == 2:
            result.append("C")
            return result
        elif result.index(max_simValue) == 3:
            result.append("D")
            return result
        return ""


# os.rename(r'Cluster/cluster_center.xls', r'Cluster/cluster_center.xml')
# if __name__ == "__main__":
#     list = read_data('E:\\Not In My Back Yard\\Data\\cluster_center_data.xlsx')
#     data = [
#         0.943718136, 0.919436529, 0.937990941, 0.423595613, 0.431268235,
#         0.429434191, 0.815572656, 0.660243087, 0.402787722, 0.202231073,
#         0.271171516, 0.261828741, 0.116180903, 0.149708845, 0.163671045,
#         0.122716341, 0.188907699, 0.224021695, 0.19497443, 0.110780618,
#         0.109060548, 0.155033262, 0.212313683, 0.194892829, 0.152332155,
#         0.627581767, 0.538738258, 0.246325116, 0.136978826, 0.109899059,
#         0.125003946, 0.095600044, 0.145152643, 0.121435541, 0.096014121,
#         0.063053562, 0.255838449, 0.095810199, 0.100654743, 0.077362504,
#         0.114760231, 0.273202773, 0.055942315, 0.144644741, 0.179278974,
#         0.067522918, 0.082314457, 0.054442222, 0.093770724
#     ]
#     data = [0.9675124644932765, 0.8778859870882605, 0.9004404409550543, 0.4066772689425977, 0.4397673067057653, 0.40919565243060535, 0.8263369239949842, 0.665511216556702, 0.3878955831887085, 0.21775006766765248, 0.2596231721113967, 0.2717737194673904, 0.12579684756305587, 0.168659171161496, 0.16585041047472834, 0.13482346655512856, 0.2027442359672828, 0.2564735907194379, 0.20524783663882742, 0.11262304658788383, 0.10694213371149258, 0.17262333853385442, 0.20806397766229348, 0.21417959231348238, 0.18475592594274154, 0.6485639967213926, 0.5420752847444931, 0.262789390422656, 0.15598632492854347, 0.12995389935367146, 0.13434457708225245, 0.11753626839471303, 0.1691937412189411, 0.16267086777348802, 0.1222335560354719, 0.09728880715328002, 0.26479467368164483, 0.09588462226174817, 0.10843311731419364, 0.10677487060875986, 0.09571089348968465, 0.28106406842407594, 0.06823635680560126, 0.16288927325025662, 0.19242556555878862, 0.08067844938364874, 0.1239411102593126, 0.07678353096278556, 0.11552318838035665]
#     print(cosine_dis(data, list))
    # print(list)
    # [1.0, 0.1593941782225661, 0.3139867639512756, 0.4365189345544196]
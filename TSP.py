import json
import random
import os


class TSP:
    def __init__(self):
        self.mat = None
        self.v_num = None

    def randMat(self, n):
        self.v_num = n
        self.mat = []
        for i in range(n):
            self.mat.append([round(random.random(), 6) for _ in range(n)])
            self.mat[i][i] = 0

    def save(self, filepath):
        with open(filepath, 'w') as fp:
            json.dump({
                'v_num': self.v_num,
                'mat': self.mat
            }, fp)

    def load(self, filepath):
        with open(filepath, 'r') as fp:
            tsp_json = json.load(fp)
            self.v_num = tsp_json.get('v_num')
            self.mat = tsp_json.get('mat')

    def cost(self, ans):
        if len(ans) != self.v_num:
            return None

        cost = 0
        for i in range(self.v_num):
            cost += self.mat[ans[i]][ans[(i+1) % self.v_num]]

        return cost

    def makeDataSet(self, num, v_num, datapath):
        dir_path = datapath+'/'+'tsp_'+str(v_num)
        try:
            os.makedirs(dir_path)
        except FileExistsError:
            pass

        for i in range(num):
            self.randMat(v_num)
            file_path = dir_path+'/'+'tsp{}.json'.format(i)
            self.save(file_path)

        return True


if __name__ == '__main__':
    tspTest = TSP()
    min_num = 12
    max_num = 16
    num = 100
    datapath = 'tspDataSet'
    print('生成TSP数据集中...')
    for i in range(min_num, max_num+1):
        tspTest.makeDataSet(num, i, datapath)
    print('数据集生成成功...')
    print('数据集大小为{0}'.format(num))
    print('TSP大小为{0}~{1}'.format(min_num, max_num))
    print('数据集路径为{0}'.format(os.sep.join([os.getcwd(), datapath])))

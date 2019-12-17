import math
import random
import time
from queue import PriorityQueue

from TSP import TSP


class Path:
    def __init__(self, pre, current, length, cost, left):
        self.pre = pre
        self.current = current
        self.length = length
        self.cost = cost
        self.left = left

    def __lt__(self, other):
        return self.cost + self.left < other.cost + other.left


def _upBound(tsp: TSP):
    cost = 0
    v = 0
    sSet = [0]
    dSet = list(range(1, tsp.v_num))

    while dSet:
        min_path = min([(tsp.mat[v][i], i) for i in dSet])
        cost += min_path[0]
        v = min_path[1]
        sSet.append(v)
        dSet.remove(v)
    cost += tsp.mat[v][0]

    return cost+1e-6


def aStar(tsp: TSP):
    # 记录起始时间
    print('aStar begin...')
    start_time = time.time()
    mat = tsp.mat
    v_num = tsp.v_num
    up_cost = _upBound(tsp)
    # print(up_cost)

    paths = PriorityQueue()
    path = Path(None, 0, 1, 0, 2*min(mat[0]))
    paths.put(path)

    while not paths.empty():
        path = paths.get()  # type: Path
        if path.length == v_num:
            # 找到解
            break
        for i in range(v_num):
            find = False
            tmp = path
            while tmp != None:
                if i == tmp.current:
                    find = True
                    break
                tmp = tmp.pre
            if find:
                continue

            next_path = Path(path, i, path.length+1,
                             path.cost + mat[path.current][i],
                             min(mat[i]) + min(mat[0]))
            if next_path.length == v_num:
                next_path.cost += mat[i][0]
                next_path.left = 0

            if path.cost+path.left < up_cost:
                paths.put(next_path)

    cost = round(path.cost, 6)
    ans = []
    while path != None:
        ans.insert(0, path.current)
        path = path.pre
    total_time = round(time.time()-start_time, 3)
    print('aStar end...')
    print('total time:', total_time, 's')
    return (cost, total_time, ans)


def SA(tsp: TSP, Tmax=35, Tmin=10, times=1, kB=0.001):
    '''Tmax: 起始温度
    Tmin: 终止温度
    times: 退火次数
    kB: 转移概率系数

    Tmax/Tmin决定退火时间, kB越小接受差解概率越低
    '''
    # 记录起始时间
    start_time = time.time()
    print('SA begin...')
    best_ans = []
    best_cost = 1e100
    v_num = tsp.v_num  # 顶点数

    for _ in range(times):  # 多烧几次
        T = Tmax  # 初始温度
        t = 0  # 外循环次数
        ans = list(range(v_num))
        random.shuffle(ans)  # 初始解
        cost = tsp.cost(ans)  # 初始费用

        while T > Tmin:  # 外循环
            std_T = (T-Tmin)/(Tmax-Tmin)*100  # (Tmin, Tmax) ~ (0, 100)
            number = (T-Tmin)/(Tmax-Tmin)*v_num  # (Tmin, Tmax) ~ (1, v_num)

            for _ in range(int(1100-10*std_T)):  # 内循环达到指定次数之后退出
                new_ans = ans.copy()
                # 产生随机解
                change_num = random.randint(0, 2)+int(number+0.5)

                for _ in range(change_num):
                    now_pos = random.randint(0, v_num-1)
                    bias = random.randint(1, v_num)  # 随机获得偏移量
                    next_pos = (now_pos + bias) % v_num  # 偏移后的位置
                    # 交换
                    new_ans[now_pos], new_ans[next_pos] = new_ans[next_pos], new_ans[now_pos]

                new_cost = tsp.cost(new_ans)  # 计算新的费用
                # 计算转移概率, 与kB有关
                p = math.exp((cost-new_cost)/(kB*std_T*v_num))
                if random.random() < p:
                    cost = new_cost
                    ans = new_ans.copy()
            t += 1
            T = Tmax/math.log10(10+t)

        if cost < best_cost:
            best_cost = cost
            best_ans = ans.copy()

    best_cost = round(best_cost, 6)
    total_time = round(time.time()-start_time, 3)
    print('SA end...')
    print('total time:', total_time, 's')
    return (best_cost, total_time, best_ans)

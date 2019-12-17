from TSP import TSP
from search import aStar, SA
import os


def test(begin, end):
    end += 1
    result_path = 'testResult'

    try:
        os.makedirs(result_path)
    except FileExistsError:
        pass

    tsp = TSP()
    dataset_path = 'tspDataSet/tsp_{}'

    for i in range(begin, end):
        dataset = os.listdir(dataset_path.format(i))

        with open(result_path+'/result_{}.txt'.format(i), 'w') as f:
            for data in dataset:
                datapath = dataset_path.format(i)+'/'+data
                tsp.load(datapath)

                sa_ans = SA(tsp, 300, 100, kB=0.001)
                print(sa_ans)
                aStar_ans = aStar(tsp)
                print(aStar_ans)
                print()

                f.write('SA:{}:{}:{}\n'.format(*sa_ans))
                f.write('aStar:{}:{}:{}\n'.format(*aStar_ans))


def analyse(begin, end):
    end += 1
    result_path = 'testResult'

    sa_min_time = []
    sa_max_time = []

    aStar_min_time = []
    aStar_max_time = []

    sa_avg_time = []
    aStar_avg_time = []

    avg_delta_cost = []

    best_rate = []

    for N in range(begin, end):
        result_costs = {
            'SA': [],
            'aStar': [],
        }

        result_times = {
            'SA': [],
            'aStar': [],
        }

        with open(result_path+'/'+'result_{}.txt'.format(N)) as f:
            result = f.readline()
            while result:
                result = result.split(':')
                result_costs[result[0]].append(float(result[1]))
                result_times[result[0]].append(float(result[2]))
                result = f.readline()

        sa_min_time.append(min(result_times['SA']))
        sa_max_time.append(max(result_times['SA']))

        aStar_min_time.append(min(result_times['aStar']))
        aStar_max_time.append(max(result_times['aStar']))

        sa_avg_time.append(sum(result_times['SA'])/len(result_times['SA']))
        aStar_avg_time.append(
            sum(result_times['aStar'])/len(result_times['aStar']))

        delta_cost = [i-j for i, j
                      in zip(result_costs['SA'], result_costs['aStar'])]

        avg_delta_cost.append(sum(delta_cost)/len(delta_cost))

        best_count = len([x for x in delta_cost if x < 1e-6])
        best_rate.append(best_count/len(delta_cost))

    with open('analyse_result.txt', 'w') as f:
        f.write('N             ')
        for i in range(begin, end):
            f.write('\t{:10d}'.format(i))
        f.write('\n')

        f.write('SA_min_time   ')
        for i in range(end-begin):
            f.write('\t{:10.3f}s'.format(sa_min_time[i]))
        f.write('\n')

        f.write('SA_max_time   ')
        for i in range(end-begin):
            f.write('\t{:10.3f}s'.format(sa_max_time[i]))
        f.write('\n')

        f.write('aStar_min_time')
        for i in range(end-begin):
            f.write('\t{:10.3f}s'.format(aStar_min_time[i]))
        f.write('\n')

        f.write('aStar_max_time')
        for i in range(end-begin):
            f.write('\t{:10.3f}s'.format(aStar_max_time[i]))
        f.write('\n')

        f.write('SA_avg_time   ')
        for i in range(end-begin):
            f.write('\t{:10.3f}s'.format(sa_avg_time[i]))
        f.write('\n')

        f.write('aStar_avg_time')
        for i in range(end-begin):
            f.write('\t{:10.3f}s'.format(aStar_avg_time[i]))
        f.write('\n')

        f.write('avg_delta_cost')
        for i in range(end-begin):
            f.write('\t{:10.3f}c'.format(avg_delta_cost[i]))
        f.write('\n')

        f.write('best_rate    ')
        for i in range(end-begin):
            f.write('\t{:10.3f}%'.format(best_rate[i]*100))
        f.write('\n')


if __name__ == "__main__":
    pass
    # test(12, 16) # 跑数据集，时间较长
    analyse(12, 16) # 对结果进行分析

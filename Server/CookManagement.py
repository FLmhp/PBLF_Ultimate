import heapq
import csv

def read_cook_counts(file_path):
    high_cooks = mid_cooks = low_cooks = 0
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['级别'] == '高级':
                high_cooks = int(row['数量'])
            elif row['级别'] == '中级':
                mid_cooks = int(row['数量'])
            elif row['级别'] == '低级':
                low_cooks = int(row['数量'])
    return high_cooks, mid_cooks, low_cooks
def cook_dishes(cook_times):
    high_cooks, mid_cooks, low_cooks = read_cook_counts('Cooks.csv')
    # 用来保存每位厨师的空闲时间和编号
    free_times = []
    # 初始化厨师的空闲时间为0，编号从0开始
    chefs = {}
    
    for chef_id in range(high_cooks):
        free_times.append((0, 'high', chef_id))  # (空闲时间, 厨师类型, 厨师编号)
        chefs[f'High Chef {chef_id}'] = {'dishes': [], 'total_time': 0}
        
    for chef_id in range(mid_cooks):
        free_times.append((0, 'mid', chef_id))  
        chefs[f'Mid Chef {chef_id}'] = {'dishes': [], 'total_time': 0}
        
    for chef_id in range(low_cooks):
        free_times.append((0, 'low', chef_id))  
        chefs[f'Low Chef {chef_id}'] = {'dishes': [], 'total_time': 0}

    heapq.heapify(free_times)  # 创建一个最小堆

    for i in range(len(cook_times)):
        cook_time = cook_times[i]

        # 获取最早空闲的厨师
        free_time, cook_type, chef_id = heapq.heappop(free_times)

        # 根据厨师类型确定实际制作时长
        if cook_type == 'high':
            actual_time = cook_time * 0.5
        elif cook_type == 'mid':
            actual_time = cook_time * 0.7
        else:  # 'low'
            actual_time = cook_time

        # 更新厨师的空闲时间
        new_free_time = free_time + actual_time

        # 将厨师的空闲时间和类型重新放回堆中
        heapq.heappush(free_times, (new_free_time, cook_type, chef_id))

        # 记录每位厨师的制作情况
        chef_key = f"{cook_type.capitalize()} Chef {chef_id}"
        chefs[chef_key]['dishes'].append(i)
        chefs[chef_key]['total_time'] += actual_time

    # return chefs
    return round(max([i['total_time'] for  i in list(chefs.values())]), 2)  # 取最长制作时间的厨师

# 示例用法
# cook_times = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]  # 制作时长

# result = cook_dishes(cook_times)
# for chef, details in result.items():
#     print(f"{chef}: Dishes {details['dishes']} - Total time {details['total_time']:.2f}")

import numpy as np

file_path="E:/code/python code/PhysioInsight/data/download/resp_125hz_60s_bidmc.txt"

# 使用 np.genfromtxt 加载数据并指定要读取的列范围 (跳过前两行，使用第 2列到全部)
data = np.genfromtxt(file_path, skip_header=2, usecols=(1,))

file_name = "../data/unknownSignal/resp_125hz_60s_bidmc.txt"
np.savetxt(file_name,data)


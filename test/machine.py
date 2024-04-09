import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# 1. 读取数据
filename = '../data/info_data.csv'
df = pd.read_csv(filename)
print(df.info())

for col in ['Peaks', 'MorePeaks']:
    # 将字符串转换为列表
    df[col] = df[col].apply(lambda x: [int(i) for i in x.strip('[]').split()])
    # 计算统计特征
    df[col+'_len'] = df[col].apply(len)
    df[col+'_mean'] = df[col].apply(np.mean)
    df[col+'_max'] = df[col].apply(max)
    df[col+'_min'] = df[col].apply(min)
    # 删除原始特征
    df = df.drop(col, axis=1)

# 将标签转换为数值
df['Label'] = df['Label'].astype('category').cat.codes

# 将数据和标签分开
X = df.drop('Label', axis=1)
y = df['Label']

# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 创建并训练模型
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train)

# 输出模型在测试集上的准确率
print('Accuracy:', clf.score(X_test, y_test))


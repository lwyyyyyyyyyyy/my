import pandas as pd
pd.set_option('display.unicode.east_asian_width',True)

insurance_df=pd.read_csv('D:/streamlit-env/（医疗费用预测数据）insurance-chinese.csv',encoding='gbk')

output=insurance_df['医疗费用']

features=insurance_df[['年龄','性别','BMI','子女数量','是否吸烟','区域']]
fertures=pd.get_dummies(features)

print('下面是独热编码后，特征列的前5行数据:')
print(features.head())
print()

print("前5行目标输出数据")
print(output.head())

import streamlit as st
import pandas as pd

st.title("📅个人简历生成器")



def my_format_func(option):
    return f'{option}'

degree=st.selectbox('学历',['高中','专科','本科','硕士','博士'],format_func=my_format_func,index=2)

if degree=='高中':
    st.write('你的学历是**高中**')
if degree=='本科':
    st.write('你的学历是**本科**')
elif degree=='专科':
    st.write('你的学历是**硕士**')
else:
    st.write('你的学历是**博士**')
     
   


options_1=st.multiselect(
    '语言能力',
    ['中文','英语','德语','法语','俄罗斯语','意大利语'],
    ['中文','英语'],
    format_func=my_format_func,
    )



options_1=st.multiselect(
    '技能(可多选)',
    ['python','java','HTML/CSS','数据分析','机器学习','深度学习'],
    ['python','java'],
    format_func=my_format_func,
    )



from datetime import datetime,time
st.text("工作经验(年)")
year=st.slider('',0,60,4)

st.text("期望薪资范围(元)")
values=st.slider(
    '',5000,50000,(6000,8000))


st.text_area(label='个人简历',placeholder='请简要介绍您的专业背景、职业目标和个人特点')

w1=st.time_input('每日最佳联系时间段')


   
  

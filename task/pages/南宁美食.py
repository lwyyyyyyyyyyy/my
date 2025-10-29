import streamlit as st
import pandas as pd

st.header("🍔南宁美食探索")
st.text("探索广西南宁最受欢迎的美食地点！选择你感兴趣的餐厅类型，查看评分和位置.")

st.header("用餐高峰时段")
st.header("💰不同类型餐厅价格")

data = {
    '餐厅价格':[17, 25, 45, 35],
    
}
index = pd.Series(['中餐','快餐','西餐','自助餐'],name='餐厅')
df=pd.DataFrame(data,index=index)

st.dataframe(df)

st.line_chart(df)



map_data={'latitude':[22.787419,22.843739,22.798225],
          'longitude':[108.387165,108.288224,108.311483]
    }

st.map(pd.DataFrame(map_data))

import streamlit as st

st.title("🐶宠物 大黄-数字档案")
st.subheader("🗝️基础信息")
st.text("品种：中华田园犬  别名：土狗、柴犬")
st.text("年龄|性别：1岁|男")
st.text("婚姻状态：单身")
st.subheader("💪身体状况")
st.text("疫苗✅️     绝育✅️     体型肥胖❌")
st.subheader("📈技能矩阵")
c1, c2, c3 = st.columns(3)
c1.metric(label="熟悉指令", value="96%", delta="优秀")
c2.metric(label="领地意识强", value="90%", delta="优秀")
c3.metric(label="警惕性高", value="90%", delta="优秀")
st.subheader("🐕幼儿园小狗保安",help="打分情况")
import pandas as pd

data = {
    '家长反馈':[89, 90, 85, 92, 95],
    '工作状态':[90, 92, 90, 99, 93],
    '老师评价':[92, 95, 89, 92, 94],
}
index = pd.Series(['01月', '02月', '03月', '04月', '05月'], name='月份')
df = pd.DataFrame(data, index=index)

st.write(df)

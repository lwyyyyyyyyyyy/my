import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import warnings

warnings.filterwarnings('ignore')


plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


st.set_page_config(page_title="学生成绩分析平台", page_icon="🎓", layout="wide")
st.title("🎓 学生成绩分析与预测平台")
st.markdown("---")
        
st.markdown("""
本平台提供以下功能：
- **数据可视化**：多维度展示学生学业表现
- **成绩预测**：基于机器学习模型预测期末成绩
- **因素分析**：识别影响学习成绩的关键因素
""")
    
PASS_IMAGE_URL = "https://www.myhappybirthdays.com/wp-content/uploads/2019/05/congratulations-typography-handwritten-lettering-greeting-card-banner_7081-766.jpg"
FAIL_IMAGE_URL = "https://foreignlang.ecc.co.jp/files/2022/09/l00076d_img02.jpg"


@st.cache_data
def load_data():
    try:
       
        df = pd.read_csv('student_data_adjusted_rounded.csv')
        
        column_mapping = {
            '每周学习时长（小时）': 'weekly_study_hours',
            '期中考试分数': 'midterm_score',
            '上课出勤率': 'attendance_rate',
            '作业完成率': 'homework_completion_rate', 
            '期末考试分数': 'final_score'
        }
        
       
        for old_col, new_col in column_mapping.items():
            if old_col in df.columns:
                df = df.rename(columns={old_col: new_col})
        
        numeric_columns = ['weekly_study_hours', 'attendance_rate', 'midterm_score', 
                          'homework_completion_rate', 'final_score']
        
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    except Exception as e:
        st.error(f"数据加载错误: {e}")
       
        np.random.seed(42)
        n_students = 200
        
        data = {
            '学号': [f'023000{str(i).zfill(3)}' for i in range(1, n_students+1)],
            '性别': np.random.choice(['男', '女'], n_students),
            '专业': np.random.choice(['工商管理', '人工智能', '财务管理', '电子商务', '大数据管理'], n_students),
            'weekly_study_hours': np.random.uniform(10, 40, n_students).round(2),
            'attendance_rate': np.random.uniform(0.6, 1.0, n_students).round(2),
            'midterm_score': np.random.uniform(40, 100, n_students).round(2),
            'homework_completion_rate': np.random.uniform(0.6, 1.0, n_students).round(2),
            'final_score': np.random.uniform(40, 100, n_students).round(2)
        }
        df = pd.DataFrame(data)
        return df

df = load_data()


st.sidebar.title("导航菜单")
page = st.sidebar.radio("选择页面", ["项目介绍", "专业数据分析", "成绩预测"])


st.sidebar.markdown("---")
st.sidebar.subheader("数据概览")
st.sidebar.write(f"总学生数: {len(df)}")
st.sidebar.write(f"专业数量: {df['专业'].nunique()}")
st.sidebar.write(f"数据时间范围: {df['学号'].min()} - {df['学号'].max()}")

if page == "项目介绍":
    st.header("📋 项目功能介绍")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("🎯 核心功能")
        st.markdown("""
        - **数据展示**：表格形式展示学生数据
        - **可视化分析**：多种图表展示学业表现
        - **成绩预测**：机器学习模型预测期末成绩
        - **因素分析**：识别关键影响因素
        """)
        
        st.subheader("📊 可视化内容")
        st.markdown("""
        1. 各专业统计数据表格
        2. 专业性别比例柱状图
        3. 期中期末成绩折线图
        4. 出勤率柱状图
        5. 大数据管理专业专项分析
        """)
    
    with c2:
        st.subheader("🔮 预测功能")
        st.markdown("""
        - 输入学生信息
        - 预测期末成绩
        - 成绩反馈展示
        - 个性化建议
        """)
        
      
        st.subheader("🎉 成绩反馈示例")
        col_img1, col_img2 = st.columns(2)
        with col_img1:
            st.image(PASS_IMAGE_URL, caption="恭喜及格！🎉", use_container_width=True)
        with col_img2:
            st.image(FAIL_IMAGE_URL, caption="继续加油！💪", use_container_width=True)
        
        
        st.subheader("📋 数据预览")
        st.dataframe(df.head(10), use_container_width=True)

elif page == "专业数据分析":
    st.header("📊数据可视化分析")
    
    
    required_columns = ['weekly_study_hours', 'midterm_score', 'final_score', 'attendance_rate', 'homework_completion_rate']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f"缺少必要的列: {missing_columns}")
        st.info("当前可用的列有: " + ", ".join(df.columns.tolist()))
    else:
        st.subheader("各专业性别比例分析")
        col1, col2 = st.columns([2, 1]) 
        
        with col1:
           
            gender_major = pd.crosstab(df['专业'], df['性别'])
            fig, ax = plt.subplots(figsize=(10, 6))
            
            x = np.arange(len(gender_major.index))
            width = 0.35
            
            ax.bar(x - width/2, gender_major['男'], width, label='男', color='#4ECDC4', alpha=0.8)
            ax.bar(x + width/2, gender_major['女'], width, label='女', color='#FF6B6B', alpha=0.8)
            
            ax.set_xlabel('专业')
            ax.set_ylabel('学生人数')
            ax.set_title('各专业性别分布')
            ax.set_xticks(x)
            ax.set_xticklabels(gender_major.index, rotation=45)
            ax.legend()
            
            st.pyplot(fig)
        
        with col2:
            
            st.subheader("性别比例数据")
            gender_stats = pd.crosstab(df['专业'], df['性别'], normalize='index').round(3) * 100
            gender_stats['总人数'] = pd.crosstab(df['专业'], df['性别']).sum(axis=1)
            gender_stats = gender_stats.rename(columns={'男': '男生比例%', '女': '女生比例%'})
            st.dataframe(gender_stats, use_container_width=True)
            
           
            st.subheader("总体性别统计")
            total_gender = df['性别'].value_counts()
            col_stat1, col_stat2 = st.columns(2)
            with col_stat1:
                st.metric("男生人数", total_gender.get('男', 0))
            with col_stat2:
                st.metric("女生人数", total_gender.get('女', 0))
        
        st.markdown("---")
        
        
        st.subheader("各专业学习指标对比")
        col3, col4 = st.columns([2, 1])
        
        with col3:
           
            comparison_data = df.groupby('专业').agg({
                'weekly_study_hours': 'mean',
                'midterm_score': 'mean',
                'final_score': 'mean'
            }).round(2)
            
            fig, ax1 = plt.subplots(figsize=(12, 6))
            
           
            bars = ax1.bar(comparison_data.index, comparison_data['weekly_study_hours'], 
                          alpha=0.7, color='#4ECDC4', label='平均周学时')
            ax1.set_xlabel('专业')
            ax1.set_ylabel('平均周学时（小时）', color='#4ECDC4')
            ax1.tick_params(axis='y', labelcolor='#4ECDC4')
            
         
            ax2 = ax1.twinx()
            ax2.plot(comparison_data.index, comparison_data['midterm_score'], 
                    marker='o', linewidth=2, label='期中平均分', color='#FF6B6B')
            ax2.plot(comparison_data.index, comparison_data['final_score'], 
                    marker='s', linewidth=2, label='期末平均分', color='#45B7D1')
            ax2.set_ylabel('平均分数', color='#FF6B6B')
            ax2.tick_params(axis='y', labelcolor='#FF6B6B')
            
            ax1.set_title('各专业学习指标对比（周学时+成绩）')
            plt.xticks(rotation=45)
            
     
            lines1, labels1 = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
            
            st.pyplot(fig)
        
        with col4:
           
            st.subheader("各专业平均数据")
            avg_data = df.groupby('专业').agg({
                'weekly_study_hours': 'mean',
                'midterm_score': 'mean',
                'final_score': 'mean'
            }).round(2)
            avg_data = avg_data.rename(columns={
                'weekly_study_hours': '平均周学时',
                'midterm_score': '平均期中分',
                'final_score': '平均期末分'
            })
            st.dataframe(avg_data, use_container_width=True)
            
          
            st.subheader("关键指标")
            col_metric1, col_metric2 = st.columns(2)
            with col_metric1:
                st.metric("最高周学时", f"{avg_data['平均周学时'].max():.1f}小时")
                st.metric("最高期中分", f"{avg_data['平均期中分'].max():.1f}分")
            with col_metric2:
                st.metric("最高期末分", f"{avg_data['平均期末分'].max():.1f}分")
                st.metric("平均总分", f"{avg_data['平均期末分'].mean():.1f}分")
        
        st.markdown("---")
        
       
        st.subheader("各专业出勤率分析")
        col5, col6 = st.columns([2, 1])
        
        with col5:
     
            attendance_by_major = df.groupby('专业')['attendance_rate'].mean().sort_values(ascending=False)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.bar(attendance_by_major.index, attendance_by_major.values * 100, 
                         color=plt.cm.viridis(np.linspace(0, 1, len(attendance_by_major))))
            
            ax.set_xlabel('专业')
            ax.set_ylabel('平均出勤率 (%)')
            ax.set_title('各专业平均出勤率')
            plt.xticks(rotation=45)
            
         
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                       f'{height:.1f}%', ha='center', va='bottom')
            
            st.pyplot(fig)
        
        with col6:
           
            st.subheader("出勤率排名")
            rank_df = pd.DataFrame({
                '排名': range(1, len(attendance_by_major) + 1),
                '专业': attendance_by_major.index,
                '平均出勤率': (attendance_by_major.values * 100).round(1)
            })
            st.dataframe(rank_df, use_container_width=True)
            
           
            st.subheader("出勤率统计")
            col_att1, col_att2 = st.columns(2)
            with col_att1:
                st.metric("最高出勤率", f"{attendance_by_major.max()*100:.1f}%")
            with col_att2:
                st.metric("平均出勤率", f"{attendance_by_major.mean()*100:.1f}%")
        
        st.markdown("---")
        
       
        st.subheader(" 大数据管理专业专项分析")
        col7, col8 = st.columns([2, 1])

        with col7:
            big_data_df = df[df['专业'] == '大数据管理']
            
            if not big_data_df.empty:
               
                fig, ax = plt.subplots(figsize=(12, 6))
                
              
                n, bins, patches = ax.hist(big_data_df['final_score'], bins=10, 
                                          color='#4ECDC4', alpha=0.7, edgecolor='black')
                
                ax.set_xlabel('期末成绩')
                ax.set_ylabel('学生人数')
                ax.set_title('大数据管理专业期末成绩分布（直方图）')
                ax.grid(True, alpha=0.3)
                
                
                for i, (count, bin_edge) in enumerate(zip(n, bins)):
                    if count > 0:
                        ax.text(bin_edge + (bins[1] - bins[0])/2, count + 0.1, 
                               f'{int(count)}', ha='center', va='bottom', fontsize=9)
                
               
                ax.axvline(x=60, color='red', linestyle='--', linewidth=2, 
                          label='及格线 (60分)', alpha=0.8)
                ax.legend()
                
                plt.tight_layout()
                st.pyplot(fig)
                
                
                st.subheader("📊 关键指标概览")
                col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)
                
                with col_metric1:
                    avg_attendance = big_data_df['attendance_rate'].mean() * 100
                    st.metric(
                        "平均出勤率", 
                        f"{avg_attendance:.1f}%",
                        delta=f"{(avg_attendance - df['attendance_rate'].mean() * 100):.1f}% vs 平均"
                    )
                
                with col_metric2:
                    avg_final = big_data_df['final_score'].mean()
                    st.metric(
                        "平均期末成绩", 
                        f"{avg_final:.1f}分",
                        delta=f"{(avg_final - df['final_score'].mean()):.1f}分 vs 平均"
                    )
                
                with col_metric3:
                    pass_rate = (big_data_df['final_score'] >= 60).mean() * 100
                    st.metric(
                        "及格率", 
                        f"{pass_rate:.1f}%",
                        delta=f"{(pass_rate - (df['final_score'] >= 60).mean() * 100):.1f}% vs 平均"
                    )
                
                with col_metric4:
                    avg_study = big_data_df['weekly_study_hours'].mean()
                    st.metric(
                        "平均学习时间", 
                        f"{avg_study:.1f}小时",
                        delta=f"{(avg_study - df['weekly_study_hours'].mean()):.1f}小时 vs 平均"
                    )
                
               
                st.subheader("📈 成绩分布详情")
                col_stats1, col_stats2 = st.columns(2)
                
                with col_stats1:
                    st.markdown("**成绩分段统计:**")
                    score_bins = [0, 60, 70, 80, 90, 100]
                    score_labels = ['不及格(<60)', '及格(60-70)', '中等(70-80)', '良好(80-90)', '优秀(90-100)']
                    score_dist = pd.cut(big_data_df['final_score'], bins=score_bins, labels=score_labels).value_counts().sort_index()
                    
                    for score_range, count in score_dist.items():
                        percentage = (count / len(big_data_df)) * 100
                        st.write(f"- {score_range}: {count}人 ({percentage:.1f}%)")
                
                with col_stats2:
                    st.markdown("**统计指标:**")
                    st.write(f"- 最高分: {big_data_df['final_score'].max():.1f}分")
                    st.write(f"- 最低分: {big_data_df['final_score'].min():.1f}分")
                    st.write(f"- 中位数: {big_data_df['final_score'].median():.1f}分")
                    st.write(f"- 标准差: {big_data_df['final_score'].std():.1f}分")
                
            else:
                st.warning("数据中暂无大数据管理专业的学生数据")

        with col8:
            if not big_data_df.empty:
                
                st.subheader("📦 学习时间分布分析")
                fig, ax = plt.subplots(figsize=(8, 6))
                
             
                box_data = [big_data_df['weekly_study_hours']]
                box_plot = ax.boxplot(box_data, vert=True, patch_artist=True, 
                                     labels=['大数据管理专业'])
                
              
                colors = ['#4ECDC4']
                for patch, color in zip(box_plot['boxes'], colors):
                    patch.set_facecolor(color)
                    patch.set_alpha(0.7)
                
               
                stats_text = f"""
                统计信息:
                最小值: {big_data_df['weekly_study_hours'].min():.1f}小时
                下四分位: {big_data_df['weekly_study_hours'].quantile(0.25):.1f}小时
                中位数: {big_data_df['weekly_study_hours'].median():.1f}小时
                上四分位: {big_data_df['weekly_study_hours'].quantile(0.75):.1f}小时
                最大值: {big_data_df['weekly_study_hours'].max():.1f}小时
                平均值: {big_data_df['weekly_study_hours'].mean():.1f}小时
                """
                
                ax.text(1.2, big_data_df['weekly_study_hours'].median(), stats_text, 
                       fontsize=9, verticalalignment='center',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.7))
                
                ax.set_ylabel('周学时（小时）')
                ax.set_title('大数据管理专业学习时间分布（箱线图）')
                ax.grid(True, alpha=0.3)
                
                st.pyplot(fig)
                
              
                st.subheader("📋 详细数据统计")
                
                st.write("**学习时间分段:**")
                study_hours_bins = pd.cut(big_data_df['weekly_study_hours'], 
                                        bins=[0, 15, 25, 35, 50],
                                        labels=['0-15小时', '15-25小时', '25-35小时', '35+小时'])
                study_dist = study_hours_bins.value_counts().sort_index()
                for study_range, count in study_dist.items():
                    percentage = (count / len(big_data_df)) * 100
                    st.write(f"- {study_range}: {count}人 ({percentage:.1f}%)")
                
               
                st.write("**出勤率分段:**")
                attendance_bins = pd.cut(big_data_df['attendance_rate'] * 100,
                                       bins=[0, 70, 80, 90, 100],
                                       labels=['0-70%', '70-80%', '80-90%', '90-100%'])
                attendance_dist = attendance_bins.value_counts().sort_index()
                for att_range, count in attendance_dist.items():
                    percentage = (count / len(big_data_df)) * 100
                    st.write(f"- {att_range}: {count}人 ({percentage:.1f}%)")
               
                st.write("**学习指标相关性:**")
                corr_study_score = big_data_df['weekly_study_hours'].corr(big_data_df['final_score'])
                corr_attendance_score = big_data_df['attendance_rate'].corr(big_data_df['final_score'])
                st.write(f"- 学习时间 vs 成绩: {corr_study_score:.3f}")
                st.write(f"- 出勤率 vs 成绩: {corr_attendance_score:.3f}")
                
            else:
                st.info("等待大数据管理专业数据...")
else:  
    st.header("🔮 期末成绩预测")
  
    @st.cache_resource
    def train_model():
      
        df_encoded = df.copy()
        df_encoded['性别'] = df_encoded['性别'].map({'男': 0, '女': 1})
        df_encoded = pd.get_dummies(df_encoded, columns=['专业'])
        
        features = ['性别', 'weekly_study_hours', 'attendance_rate', 
                   'midterm_score', 'homework_completion_rate']
        
       
        major_features = [col for col in df_encoded.columns if col.startswith('专业_')]
        features.extend(major_features)
        
        X = df_encoded[features]
        y = df_encoded['final_score']
        
     
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
   
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
       
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        return model, features, mae, r2
    
    try:
        model, feature_names, mae, r2 = train_model()
        
        st.info(f"预测模型性能：平均绝对误差 {mae:.2f} 分，R²分数 {r2:.2f}")
        
     
        st.subheader("输入学生信息进行预测")
        
        col1, col2 = st.columns(2)
        
        with col1:
            student_id = st.text_input("学号", placeholder="例如：023000001")
            gender = st.selectbox("性别", ["男", "女"])
            major = st.selectbox("专业", df['专业'].unique())
            
        with col2:
            weekly_study_hours = st.slider("每周学习时长（小时）", 0.0, 50.0, 20.0, step=0.5)
            attendance_rate = st.slider("上课出勤率", 0.0, 1.0, 0.85, step=0.01)
            midterm_score = st.slider("期中考试分数", 0.0, 100.0, 75.0, step=0.5)
            homework_completion_rate = st.slider("作业完成率", 0.0, 1.0, 0.8, step=0.01)
        
       
        if st.button("预测期末成绩", type="primary"):
            if student_id:
            
                input_data = {
                    '性别': 0 if gender == '男' else 1,
                    'weekly_study_hours': weekly_study_hours,
                    'attendance_rate': attendance_rate,
                    'midterm_score': midterm_score,
                    'homework_completion_rate': homework_completion_rate
                }
                
                for major_feature in [col for col in feature_names if col.startswith('专业_')]:
                    input_data[major_feature] = 1 if major_feature == f'专业_{major}' else 0
                
              
                input_df = pd.DataFrame([input_data])[feature_names]
                
              
                predicted_score = model.predict(input_df)[0]
               
                st.success(f"**预测结果：{predicted_score:.1f} 分**")
                
                col1, col2 = st.columns(2)
                
                with col1:
                   
                    if predicted_score >= 60:
                        st.balloons()
                        st.image(PASS_IMAGE_URL, caption="🎉 恭喜！预测成绩及格", use_column_width=True)
                        st.markdown("""
                        ### 🎯 学习建议
                        - 继续保持良好的学习习惯
                        - 在优势科目上继续深化
                        - 帮助其他同学共同进步
                        - 继续保持当前的学习节奏
                        """)
                    else:
                        st.image(FAIL_IMAGE_URL, caption="💪 继续加油！预测成绩不及格", use_column_width=True)
                        st.markdown("""
                        ### 📚 改进建议
                        - 增加每周学习时间
                        - 提高课堂出勤率
                        - 加强作业完成质量
                        - 寻求老师或同学帮助
                        - 制定详细的学习计划
                        """)
                
                with col2:
                   
                    st.markdown("### 🔍 影响因素分析")
                    
                    factors = {
                        '期中成绩': midterm_score * 0.3,
                        '出勤率': attendance_rate * 100 * 0.25,
                        '作业完成率': homework_completion_rate * 100 * 0.2,
                        '周学时': weekly_study_hours * 0.15,
                        '学习基础': 0.1
                    }
                    
                    fig, ax = plt.subplots(figsize=(8, 6))
                    features_list = list(factors.keys())
                    importance_values = list(factors.values())
                    
                    bars = ax.barh(features_list, importance_values, 
                                  color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFE66D'])
                    ax.set_xlabel('影响程度')
                    ax.set_title('各因素对期末成绩的影响程度')
                    
                  
                    for i, (feature, value) in enumerate(factors.items()):
                        ax.text(value + 1, i, f'{value:.1f}', va='center', fontsize=10)
                    
                    st.pyplot(fig)
                
              
                st.markdown("### 📋 输入的学生信息")
                info_cols = st.columns(4)
                with info_cols[0]:
                    st.metric("学号", student_id)
                    st.metric("性别", gender)
                with info_cols[1]:
                    st.metric("专业", major)
                    st.metric("周学时", f"{weekly_study_hours}小时")
                with info_cols[2]:
                    st.metric("出勤率", f"{attendance_rate:.1%}")
                    st.metric("作业完成率", f"{homework_completion_rate:.1%}")
                with info_cols[3]:
                    st.metric("期中成绩", f"{midterm_score}分")
                    st.metric("预测期末", f"{predicted_score:.1f}分")
                    
                
                st.markdown("### 📊 成绩分布对比")
                fig, ax = plt.subplots(figsize=(10, 6))
                
                
                ax.hist(df['final_score'], bins=20, alpha=0.7, color='lightblue', label='全体学生成绩分布')
                ax.axvline(predicted_score, color='red', linestyle='--', linewidth=2, 
                          label=f'预测成绩: {predicted_score:.1f}分')
                ax.axvline(60, color='orange', linestyle='-', linewidth=1, alpha=0.7, label='及格线(60分)')
                
                ax.set_xlabel('期末成绩')
                ax.set_ylabel('学生人数')
                ax.set_title('预测成绩在全体学生中的位置')
                ax.legend()
                ax.grid(True, alpha=0.3)
                
                st.pyplot(fig)
                    
            else:
                st.error("请输入学号！")
    except Exception as e:
        st.error(f"模型训练或预测出错: {e}")
        st.info("请确保数据格式正确，包含所有必要的列")


st.markdown("---")
st.markdown("🎓 学生成绩分析平台 | 基于Streamlit开发")


if st.sidebar.checkbox("显示原始数据"):
    st.sidebar.subheader("原始数据")
    st.sidebar.dataframe(df, use_container_width=True)

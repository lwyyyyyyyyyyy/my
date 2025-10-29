import streamlit as st

st.set_page_config(page_title='动物园',page_icon='🦥')
st.subheader("展示多张图片")
images=[{'url':'https://www.readersdigest.co.nz/wp-content/uploads/sites/3/2020/01/00-Birman-cats-1024x678-Shutterstock-770.jpg',
         'parm':'猫'
    },
    {
       'url': 'https://eskipaper.com/images/birds-7.jpg',
       'parm':'鸟'
    },
    {
        'url':'https://breedingbusiness.com/wp-content/uploads/2021/07/cutest-small-white-dog-breeds.jpg',
        'parm':'狗'
    },
    {
       'url': 'https://wallpapers.com/images/hd/pig-behind-green-grass-qp82mhq4wv07cki8.jpg',

       'parm':'猪'
    }
]


if 'ind' not in st.session_state:
    st.session_state['ind']=0
def nextImg():
    st.session_state['ind']=(st.session_state['ind']+1)% len(images)
def lastImg():
    st.session_state['ind']=(st.session_state['ind']-1)% len(images)
st.image(images[st.session_state['ind']]['url'],caption=images[st.session_state['ind']]['parm'])

c1,c2=st.columns(2)

with c1:
    st.button('上一张',on_click=lastImg,use_container_width=True)

with c2:
    st.button('下一张',on_click=nextImg,use_container_width=True)




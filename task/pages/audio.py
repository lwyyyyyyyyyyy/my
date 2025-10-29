import streamlit as st

st.header("🎵简易音乐播放器")
st.text("使用streamlit制作的简单音乐播放器，支持切歌和基本播放控制")

st.set_page_config(page_title='音乐库',page_icon='🎼')
images=[
    {   'photo':'https://p2.music.126.net/41oaDv7XLcIMU98IUYO2rA==/109951172148823628.jpg?param=150y150',
        'name':'杨丞琳',
        'song':'Yes,but?',
        'url':'https://music.163.com/song/media/outer/url?id=2754507514.mp3',
        'time':'2:43'
    },
   {  'photo':'https://p2.music.126.net/-rC55JsnmEWvafJQsAZaWw==/109951170473693123.jpg?param=150y150',
      'name':'颜人中',
      'song':'晚安',
      'url':'https://music.163.com/song/media/outer/url?id=1359356908.mp3',
      'time':'4:49'
      
    },
    {'photo':'https://p2.music.126.net/8DkTnzi7jdjWGYl4qbwLCg==/109951164517295956.jpg?param=150y150',
     'name':'颜人中',
     'song':'有些',
     'url':'https://music.163.com/song/media/outer/url?id=1406649619.mp3',
     'time':'3:49'
        }

]



if 'ind' not in st.session_state:
    st.session_state['ind']=0
    
def nextImg():
    st.session_state['ind']=(st.session_state['ind']+1)% len(images)

def lastImg():
    st.session_state['ind']=(st.session_state['ind']-1)% len(images)

a1,a2=st.columns([1,2])

with a1:
    st.image(images[st.session_state['ind']]['photo'])
    
with a2:
    st.title(images[st.session_state['ind']]['name'])
    st.title(images[st.session_state['ind']]['song'])
    st.text(images[st.session_state['ind']]['time'])
    st.audio(images[st.session_state['ind']]['url'],autoplay=True)


c1,c2=st.columns(2)

with c1:
    st.button('上一首',on_click=lastImg,use_container_width=True)

with c2:
    st.button('下一首',on_click=nextImg,use_container_width=True)





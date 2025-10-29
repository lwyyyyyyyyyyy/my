import streamlit as st

st.set_page_config(page_title='视频网站',page_icon='📽')

video_url=[{'url':'https://www.w3school.com.cn/example/html5/mov_bbb.mp4',
            'title':'动漫',
            'episode':'1',
            'synosis':'一部有意义的动画片'

    },
    {'url':'https://www.w3schools.com/html/movie.mp4',
       'title':'动物世界',
       'episode':'2',
     'synosis':'动物的繁衍生息'
        },
    {'url':'https://media.w3.org/2010/05/sintel/trailer.mp4',
     'title':'动漫',
     'episode':'3',
     'synosis':'冰雪世界'

    }]

if 'ind' not in st.session_state:
    st.session_state['ind']=0
    
st.title(video_url[st.session_state['ind']]['title'])
st.video(video_url[st.session_state['ind']]['url'])
st.text(video_url[st.session_state['ind']]['synosis'])

c1,c2,c3=st.columns(3)

def play(arg):
    #点击哪个按钮，就播放第几集
    st.session_state['ind']=int(arg)
    

for i in range(len(video_url)):
    st.button('第'+str(i+1)+'集',use_container_width=True,on_click=play,args=([i]))

    

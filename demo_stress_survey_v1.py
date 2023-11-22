import streamlit as st
import pandas as pd

if 'stage' not in st.session_state:
    st.session_state.stage = 0

def set_state(i):
    st.session_state.stage = i

# Survey questions
stress_questions = []

stress_questions_en = [
    'In the last month, how often have you been upset because of something that happened unexpectedly?',
    'In the last month, how often have you felt that you were unable to control the important things in your life?',
    'In the last month, how often have you felt nervous and "stressed"?',
    'In the last month, how often have you felt confident about your ability to handle your personal problems?',
    'In the last month, how often have you felt that things were going your way?',
    'In the last month, how often have you found that you could not cope with all the things that you had to do?',
    'In the last month, how often have you been able to control irritations in your life?',
    'In the last month, how often have you felt that you were on top of things?',
    'In the last month, how often have you been angered because of things that were outside of your control?',
    'In the last month, how often have you felt difficulties were piling up so high that you could not overcome them?'
]

stress_questions_th = [
    'ในรอบ 1 เดือนที่ผ่านมา คุณรู้สึกไม่สบายใจเพราะมีสิ่งที่ไม่คาดคิดเกิดขึ้น?',
    'ในรอบ 1 เดือนที่ผ่านมา คุณรู้สึกว่าคุณไม่สามารถควบคุมเรื่องสำคัญในชีวิตได้?',
    'ในรอบ 1 เดือนที่ผ่านมา คุณรู้สึกกระสับกระส่ายและเครียด?',
    'ในรอบ 1 เดือนที่ผ่านมา คุณรู้สึกมั่นใจในการรับมือกับปัญหาส่วนตัวต่างๆได้?',
    'ในรอบ 1 เดือนที่ผ่านมา คุณรู้สึกว่าทุกอย่างเป็นไปในทิศทางที่คุณต้องการ?',
    'ในรอบ 1 เดือนที่ผ่านมา คุณรู้สึกว่าคุณไม่สามารถจัดการกับสิ่งที่ต้องทำได้ดีเท่าไรนัก?',
    'ในรอบ 1 เดือนที่ผ่านมา คุณรู้สึกว่าคุณสามารถควบคุมเรื่องกวนใจได้?',
    'ในรอบ 1 เดือนที่ผ่านมา คุณรู้สึกว่าคุณควบคุมสถานการณ์ต่าง ๆ ได้ดี?',
    'ในรอบ 1 เดือนที่ผ่านมา คุณรู้สึกโกรธหรือฉุนเฉียวเพราะเรื่องที่อยู่นอกเหนือการควบคุมของคุณ?',
    'ในรอบ 1 เดือนที่ผ่านมา คุณรู้สึกว่าปัญหาต่าง ๆ ทับถมจนคุณไม่สามารถแก้ไขได้หมด?'
]

# Options
response_options = {}

response_options_en = {
    'Almost Never': 1,
    'Sometimes': 2,
    'Fairly Often': 3,
    'Very Often': 4
}

response_options_th = {
    'แทบไม่เคยเลย': 1,
    'บางครั้ง': 2,
    'ค่อนข้างบ่อย': 3,
    'บ่อยมาก': 4
}

# Questions with reversed answers
reverse_quest = []

reverse_quest_en = [
    'In the last month, how often have you felt confident about your ability to handle your personal problems?',
    'In the last month, how often have you felt that things were going your way?',
    'In the last month, how often have you been able to control irritations in your life?',
    'In the last month, how often have you felt that you were on top of things?'
]

reverse_quest_th = [
    'ในรอบ 1 เดือนที่ผ่านมา คุณรู้สึกมั่นใจในการรับมือกับปัญหาส่วนตัวต่างๆได้?',
    'ในรอบ 1 เดือนที่ผ่านมา คุณรู้สึกว่าทุกอย่างเป็นไปในทิศทางที่คุณต้องการ?',
    'ในรอบ 1 เดือนที่ผ่านมา คุณรู้สึกว่าคุณสามารถควบคุมเรื่องกวนใจได้?',
    'ในรอบ 1 เดือนที่ผ่านมา คุณรู้สึกว่าคุณควบคุมสถานการณ์ต่าง ๆ ได้ดี?'
]

def create_survey():
    # Initialize session state variables
    if 'responses' not in st.session_state:
        st.session_state.responses = {}
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0

    #st.title("Stress Survey")

    # Display the current question or result
    if st.session_state.current_question < len(stress_questions):
        display_question(response_options)
    else:
        display_result()
        #clear_cache()

def clear_cache():
    keys = list(st.session_state.keys())
    for key in keys:
        st.session_state.pop(key)

def display_question(response_options):
    # Display the current question
    if st.session_state.lan == 'English':
        st.subheader(f"Question {st.session_state.current_question + 1} / 10")
        st.write(stress_questions[st.session_state.current_question])

        # Use a unique key for each radio button
        key = f"question_{st.session_state.current_question}"

        user_response = st.radio(f"Select your answer for this question:", list(response_options.keys()), key=key)

        # Adjust the user response based on the question
        if stress_questions[st.session_state.current_question] in reverse_quest:
            user_response = 5 - response_options[user_response]
        else:
            user_response = response_options[user_response]

        # Store the response in the session state
        st.session_state.responses[st.session_state.current_question] = user_response

        # Display 'next' button
        if st.session_state.current_question < len(stress_questions) - 1:
            st.button("Next", on_click=next_question)
        else:
            st.button("Submit", on_click=next_question)
                #st.session_state.current_question += 1

    if st.session_state.lan == 'Thai (ไทย)':
        st.subheader(f"คำถามที่ {st.session_state.current_question + 1} / 10")
        st.write(stress_questions[st.session_state.current_question])

        # Use a unique key for each radio button
        key = f"question_{st.session_state.current_question}"

        user_response = st.radio(f"เลือกคำตอบ:", list(response_options.keys()), key=key)

        # Adjust the user response based on the question
        if stress_questions[st.session_state.current_question] in reverse_quest:
            user_response = 5 - response_options[user_response]
        else:
            user_response = response_options[user_response]

        # Store the response in the session state
        st.session_state.responses[st.session_state.current_question] = user_response

        # Display 'next' button
        if st.session_state.current_question < len(stress_questions) - 1:
            st.button("ต่อไป", on_click=next_question)
        else:
            st.button("ส่งคำตอบ", on_click=next_question)
                #st.session_state.current_question += 1


def display_result():
    # Calculate the summation of user responses
    total_response = sum(st.session_state.responses.values())

    if st.session_state.lan == 'English':
        # Classify stress level
        st.header("Percieved Stress Scale Result:")

        stress_level = classify_stress(total_response)

        # Display the result
        display_bar_chart(stress_level)
        
        st.markdown("""---""")    
        
        st.subheader('What causes stress?')

        st.write('From data analysis, stress is related to loneliness, everyday-discrimination, or concerns about not having enough food.')
        
        display_feature_chart()
        
        st.write("If you want to learn more about All of Us Research Program (AoURP), check the link below.")
        pss_link = "https://allofus.nih.gov/"
        st.markdown(f"[Find out what All of Us Research Program is]({pss_link})")
    
    if st.session_state.lan == 'Thai (ไทย)':
        # Classify stress level
        st.header("ผลแบบวัดความรู้สึกเครียด:")

        stress_level = classify_stress(total_response)

        # Display the result
        display_bar_chart(stress_level)
        
        st.markdown("""---""")    
        
        st.subheader('ปัจจัยอะไรที่ส่งผลต่อความเครียด?')

        st.write('จากการวิเคราะห์ข้อมูลแบบสำรวจของ All of Us Research Program (AoURP) ในประเทศสหรัฐอเมริกา ความเครียดนั้นมีความเกี่ยวข้องกับความโดดเดี่ยว การถูกเลือกปฎิบัติ (จากเชื้อชาติ สีผิว หรือปัจจัยอื่น) และความกังวลเรื่องปากท้อง')
        
        display_feature_chart()
        
        st.write("รายละเอียดเกี่ยวกับ All of Us Research Program (AoURP) (ภาษาอังกฤษ).")
        pss_link = "https://allofus.nih.gov/"
        st.markdown(f"[All of Us Research Program (AoURP)]({pss_link})")
        
    
def next_question():
    st.session_state.current_question += 1

def classify_stress(total_response):
    
    if 0 <= total_response <= 12:
        if st.session_state.lan == 'English':
            st.subheader('Low Stress')
            st.write("You are likely to feel on top of your game over the last month. Low stress levels are associated with a perception that life events are predictable, controllable, and not overwhelming.")
            st.write("You are doing a great job of managing your stress. However, if you ever feel that is starting to change, you can revisit this survey and reevaluate your score.")
            st.write('You can check out useful resources below if you ever need help.')
        
            moderate_link = "https://www.asianwomenforhealth.org/mental-health.html"
            st.markdown(f"[Mental Health Resources]({moderate_link})")
            
            st.markdown("""---""")
            
            st.subheader("55.5% of people also have the same level of stress.")
            
            st.write("According to the All of Us Research Program Survey (2023)")

        if st.session_state.lan == 'Thai (ไทย)':
            st.subheader('ความเครียดต่ำ')
            st.write('ลองดูแหล่งข้อมูลที่มีประโยชน์ได้ด้านล่าง')
        
            moderate_link = "https://www.asianwomenforhealth.org/mental-health.html"
            st.markdown(f"[Mental Health Resources]({moderate_link})")

            st.markdown("""---""")
            
            st.subheader("55.5% ของคนที่ทำแบบสำรวจมีระดับความเครียดต่ำ")
            
            st.write("ข้อมูลจาก All of Us Research Program Survey (ปี 2023)")
        
        stress_level = 1
        
        return stress_level
    
    elif 13 <= total_response <= 26:
        if st.session_state.lan == 'English':

            st.subheader('Moderate Stress')
            st.write('You may feel occasional pressure and stress, but it is not overwhelming or unmanageable.')
            st.write('Moderate stress levels suggest that individuals perceive a moderate degree of unpredictability and challenge in their lives.')
            st.write('You can check out useful resources below if you ever need help.')
            
            moderate_link = "https://www.asianwomenforhealth.org/mental-health.html"
            st.markdown(f"[Mental Health Resources]({moderate_link})")
            
            st.markdown("""---""")
            
            st.subheader("38.7% of people also have the same level of stress.")
            
            st.write("According to the All of Us Research Program Survey (2023)")

        if st.session_state.lan == 'Thai (ไทย)':
            st.subheader('ความเครียดปานกลาง')
            st.write('ลองดูแหล่งข้อมูลที่มีประโยชน์ได้ด้านล่าง')
        
            moderate_link = "https://www.asianwomenforhealth.org/mental-health.html"
            st.markdown(f"[แหล่งข้อมูล]({moderate_link})")

            st.markdown("""---""")
            
            st.subheader("38.7% ของคนที่ทำแบบสำรวจมีระดับความเครียดปานกลาง")
            
            st.write("ข้อมูลจาก All of Us Research Program Survey (ปี 2023)")
        
        stress_level = 2
        
        return stress_level
    
    elif 27 <= total_response <= 40:

        if st.session_state.lan == 'English':

            st.subheader('High Perceived Stress')
            st.write("You may feel a significant burden from life events, leading to a sense of being overloaded and unable to cope effectively.")
            st.write("However, it is important to note that stress is a normal part of life and everyone experiences it differently.")
            st.write('You can check out useful resources below if you ever need help.')
            moderate_link = "https://www.asianwomenforhealth.org/mental-health.html"
            st.markdown(f"[Mental Health Resources]({moderate_link})")
            
            st.markdown("""---""")
            
            st.subheader("5.8% of people also have the same level of stress.") 
            st.write("According to the All of Us Research Program Survey (2023)")

        if st.session_state.lan == 'Thai (ไทย)':
            st.subheader('ความเครียดสูง')
            st.write('ลองดูแหล่งข้อมูลที่มีประโยชน์ได้ด้านล่าง')
        
            moderate_link = "https://www.asianwomenforhealth.org/mental-health.html"
            st.markdown(f"[แหล่งข้อมูล]({moderate_link})")

            st.markdown("""---""")
            
            st.subheader("5.8% ของคนที่ทำแบบสำรวจมีระดับความเครียดปานกลาง")
            
            st.write("ข้อมูลจาก All of Us Research Program Survey (ปี 2023)")
        
        stress_level = 3
        
        return stress_level
    
import plotly.express as px

def display_bar_chart(stress_level):
    data = {'Category': ['Low Stress', 'Moderate Stress', 'High Stress'],
            'Value': [55.5, 38.7, 5.8]}
    
    stress_class = {1:'Low Stress', 2:'Moderate Stress', 3:'High Stress'}

    df = pd.DataFrame(data)

    # Create a bar chart using Plotly
    fig = px.bar(df, x='Category', y='Value',
                 labels={'Value': 'Percentage (%)'},
                 title='Stress Level Distribution')

    # Highlight the bar corresponding to the stress level with red color
    fig.update_traces(marker_color=['lightsalmon' if category == stress_class[stress_level] 
                                    else 'linen' for category in df['Category']])

    # Show the plot
    st.plotly_chart(fig)

def display_feature_chart():
    Factors = ["Loneliness", "Everyday-discrimination", "Hunger", "Other"]
    df_importance = pd.DataFrame(dict(Importance=[74.4, 17.8, 6.6, 1.2], Factors=Factors))
    fig = px.funnel(df_importance, x='Importance', y='Factors', title='Feature Importance (%)')
    
    st.plotly_chart(fig)


from PIL import Image

tab1, tab2 = st.tabs(["Survey", "About us"])

#if language == 'Thai'

with tab1:

    if st.session_state.stage == 0: # Landing page
        col1, col2 = st.columns(2)
        with col2:
            language = st.selectbox(
                "Select Language",
                ("English", "Thai (ไทย)"))
            st.session_state.lan = language

        if st.session_state.lan == 'English':
            st.title("Are you feeling stressed?")
            st.header("Let's take this survey and find out.")
            st.button('Begin the Survey', on_click=set_state, args=[1])

            st.markdown("""---""")

            st.write("We're taking you to answer some questions and get your 'Perceived Stress Scale'. It was designed to measure how unpredictable, uncontrollable, or overloaded you find your life.")
            st.write("You'll be asked to consider how you’ve felt over the last month. There are 10 questions in which you can circle how often you have felt a certain way.")
        
            st.write("If you want to learn more about Perceived Stress Scale, check the link below.")
            pss_link = "https://www.das.nh.gov/wellness/docs/percieved%20stress%20scale.pdf"
            st.markdown(f"[Find out what Perceived Stress Scale is]({pss_link})")
            
            st.markdown("""---""")
            
            st.write("Disclaimer: The scores on the following self-assessment do not reflect any particular diagnosis or course of treatment. They are meant as a tool to help assess your level of stress. If you have any further concerns about your current well being, you may seek professional help for guidance.")
        if st.session_state.lan == 'Thai (ไทย)':
            st.title("ช่วงนี้รู้สึกเครียดรึเปล่า?")
            st.header("ลองทำแบบสอบถามเพื่อวัดระดับความเครียดของคุณดูสิ")
            st.button('เริ่มทำแบบสอบถาม', on_click=set_state, args=[1])

            st.markdown("""---""")

            st.write("เราจะพาคุณไปวัดระดับ 'ความรู้สึกเครียด' ที่ถูกออกแบบมาเพื่อวัดว่าคุณรู้สีกว่าชีวิตคุณนั้นไม่แน่นอนและควบคุมไม่ได้ขนาดไหน")
            st.write("แบบทดสอบจะประกอบไปด้วย 10 คำถามเกี่ยวกับประสบการณ์ในช่วง 1 เดือนที่ผ่านมา")
        
            st.write("ข้อมูลเกี่ยวกับแบบทดสอบความรู้สึกเครียด หรือ 'Perceived Stress Scale' (ภาษาอังกฤษ)")
            pss_link = "https://www.das.nh.gov/wellness/docs/percieved%20stress%20scale.pdf"
            st.markdown(f"[แบบทดสอบความรู้สึกเครียด]({pss_link})")
            
            st.markdown("""---""")
            
            st.write("ข้อควรระวัง: แบบทดสอบนี้ใช้เพื่อประเมินตนเองเท่านั้น หากคุณรู้สึกกังวลกับภาวะสภาพจิตใจของตนเอง โปรดติดต่อแพทย์ผู้ชำนาญการเพื่อขอคำปรึกษา")

    if st.session_state.stage >= 1:
        if st.session_state.lan == 'English':
            stress_questions = stress_questions_en
            response_options = response_options_en
            reverse_quest = reverse_quest_en
            create_survey()
        if st.session_state.lan == 'Thai (ไทย)':
            stress_questions = stress_questions_th
            response_options = response_options_th
            reverse_quest = reverse_quest_th
            create_survey()

        
with tab2:
    st.header("Asian Women for Health")
    image = Image.open('./Thumbnail.jpg')
    st.image(image, caption="")
    st.header("MIT Sloan Master of Business Analytics")
    image_2 = Image.open('./MITSloanLogo_MASTER-Horizontal_Print.png')
    st.image(image_2, caption="")
    st.write("Analytics Lab Project")

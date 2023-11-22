import streamlit as st
import pandas as pd

if 'stage' not in st.session_state:
    st.session_state.stage = 0

def set_state(i):
    st.session_state.stage = i

# Survey questions
stress_questions = [
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

# Questions with reversed answers
reverse_quest = [
    'In the last month, how often have you felt confident about your ability to handle your personal problems?',
    'In the last month, how often have you felt that things were going your way?',
    'In the last month, how often have you been able to control irritations in your life?',
    'In the last month, how often have you felt that you were on top of things?'
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
        display_question()
    else:
        display_result()
        clear_cache()

def clear_cache():
    keys = list(st.session_state.keys())
    for key in keys:
        st.session_state.pop(key)

def display_question():
    # Display the current question
    st.subheader(f"Question {st.session_state.current_question + 1} / 10")
    st.write(stress_questions[st.session_state.current_question])

    # Use a radio button to collect the user's response
    response_options = {
        'Almost Never': 1,
        'Sometimes': 2,
        'Fairly Often': 3,
        'Very Often': 4
    }

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


def display_result():
    # Calculate the summation of user responses
    total_response = sum(st.session_state.responses.values())

    # Classify stress level
    st.header("Percieved Stress Scale Result:")

    stress_level = classify_stress(total_response)

    # Display the result
    display_bar_chart(stress_level)
    
    st.write("---")
    
    st.subheader('What causes stress?')

    st.write('From data analysis, stress is related to loneliness, everyday-discrimination, or concerns about not having enough food.')
    
    display_feature_chart()
    
    st.write("If you want to learn more about All of Us Research Program (AoURP), check the link below.")
    pss_link = "https://allofus.nih.gov/"
    st.markdown(f"[Find out what All of Us Research Program is]({pss_link})")
        
    
def next_question():
    st.session_state.current_question += 1

def classify_stress(total_response):
    if 0 <= total_response <= 12:
        st.subheader('Low Stress')
        st.write("You are likely to feel on top of your game over the last month. Low stress levels are associated with a perception that life events are predictable, controllable, and not overwhelming.")
        st.write("You are doing a great job of managing your stress. However, if you ever feel that is starting to change, you can revisit this survey and reevaluate your score.")
        
        st.st.write("---")
        
        st.subheader("55.5% of people also have the same level of stress.")
        
        st.write("According to the All of Us Research Program Survey (2023)")
        
        stress_level = 1
        
        return stress_level
    
    elif 13 <= total_response <= 26:
        st.subheader('Moderate Stress')
        st.write('You may feel occasional pressure and stress, but it is not overwhelming or unmanageable.')
        st.write('Moderate stress levels suggest that individuals perceive a moderate degree of unpredictability and challenge in their lives.')
        st.write('You can check out useful resources below if you ever need help.')
        
        moderate_link = "https://www.asianwomenforhealth.org/mental-health.html"
        st.markdown(f"[Mental Health Resources]({moderate_link})")
        
        st.st.write("---")
        
        st.subheader("38.7% of people also have the same level of stress.")
        
        st.write("According to the All of Us Research Program Survey (2023)")
        
        stress_level = 2
        
        return stress_level
    
    elif 27 <= total_response <= 40:
        
        st.subheader('High Perceived Stress')
        st.write("You may feel a significant burden from life events, leading to a sense of being overloaded and unable to cope effectively.")
        st.write("However, it is important to note that stress is a normal part of life and everyone experiences it differently.")
        st.write('You can check out useful resources below if you ever need help.')
        moderate_link = "https://www.asianwomenforhealth.org/mental-health.html"
        st.markdown(f"[Mental Health Resources]({moderate_link})")
        
        st.st.write("---")
        
        st.subheader("5.8% of people also have the same level of stress.") 
        st.write("According to the All of Us Research Program Survey (2023)")
        
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
    stages = ["Loneliness", "Everyday-discrimination", "Hunger", "Other"]
    df_importance = pd.DataFrame(dict(number=[74.4, 17.8, 6.6, 1.2], stage=stages))
    fig = px.funnel(df_importance, x='number', y='stage')
    
    st.plotly_chart(fig)


from PIL import Image
    
tab1, tab2 = st.tabs(["Survey", "About us"])

with tab1:
    if st.session_state.stage == 0: # Landing page
        st.title("Are you feeling stressed?")
        st.header("Let's take this survey and find out.")
        st.write("We're taking you to answer some questions and get your 'Perceived Stress Scale'. It was designed to measure how unpredictable, uncontrollable, or overloaded you find your life.")
        st.write("You'll be asked to consider how you’ve felt over the last month. There are 10 questions in which you can circle how often you have felt a certain way.")
        st.button('Begin the Survey', on_click=set_state, args=[1])
        
        st.st.write("---")
    
        st.write("If you want to learn more about Perceived Stress Scale, check the link below.")
        pss_link = "https://www.das.nh.gov/wellness/docs/percieved%20stress%20scale.pdf"
        st.markdown(f"[Find out what Perceived Stress Scale is]({pss_link})")
        
        st.st.write("---")
        
        st.write("Disclaimer: The scores on the following self-assessment do not reflect any particular diagnosis or course of treatment. They are meant as a tool to help assess your level of stress. If you have any further concerns about your current well being, you may seek professional help for guidance.")
        
    if st.session_state.stage >= 1:
        create_survey()
    

        
with tab2:
    st.header("Asian Women for Health")
    image = Image.open('./Thumbnail.jpg')
    st.image(image, caption="")
    st.header("MIT Sloan Master of Business Analytics")
    image_2 = Image.open('./MITSloanLogo_MASTER-Horizontal_Print.png')
    st.image(image_2, caption="")
    st.write("Analytics Lab Project")

import streamlit as st
import pandas as pd

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

    st.title("Stress Survey")

    # Display the current question or result
    if st.session_state.current_question < len(stress_questions):
        display_question()
    else:
        display_result()

def display_question():
    # Display the current question
    st.subheader(f"Question {st.session_state.current_question + 1}")
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
    st.subheader("Stress Classification Result:")

    stress_level = classify_stress(total_response)

    # Display the result
    display_bar_chart(stress_level)

    # Save the responses to a DataFrame
    survey_data = pd.DataFrame(st.session_state.responses, index=[0])

    # Append the data to a CSV file
    save_survey_data(survey_data)

def next_question():
    st.session_state.current_question += 1

def classify_stress(total_response):
    if 0 <= total_response <= 12:
        st.write('Low Stress')
        st.write("You're likely leading a fulfilling and largely stress-free life – good for you!")
        stress_level = 1
        return stress_level
    elif 13 <= total_response <= 26:
        st.write('Medium Stress')
        st.write('You often worry about things that are out of your control, but you try not to let stress get the best of you.')
        stress_level = 2
        return stress_level
    elif 27 <= total_response <= 40:
        st.write('High Stress')
        st.write("You likely spend a lot of time worrying about the future. Coping can be difficult, especially when things don't go your way.")
        st.write('Most people feel stressed if they are lonely, discriminated, or not having enough food. You could check out the resources below for support.')
        website_link = "https://www.asianwomenforhealth.org/"
        st.markdown(f"[Click here to visit the website]({website_link})")
        stress_level = 3
        return stress_level

def save_survey_data(data):
    # Load existing data
    try:
        existing_data = pd.read_csv("stress_survey_data.csv")
    except FileNotFoundError:
        existing_data = pd.DataFrame()

    # Append new data
    new_data = pd.concat([existing_data, data], ignore_index=True)

    # Save to CSV
    new_data.to_csv("stress_survey_data.csv", index=False)
    
import plotly.express as px

def display_bar_chart(stress_level):
    data = {'Category': ['Low Stress', 'Medium Stress', 'High Stress'],
            'Value': [55.4, 38.7, 5.9]}
    
    stress_class = {1:'Low Stress', 2:'Medium Stress', 3:'High Stress'}

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

# if __name__ == "__main__":
#     create_survey()

from PIL import Image
    
tab1, tab2 = st.tabs(["Survey", "About us"])

with tab1:
    create_survey()
        
with tab2:
    st.header("Asian Women for Health")
    image = Image.open('./Thumbnail.jpg')
    st.image(image, caption="")
    st.header("MIT Sloan Master of Business Analytics")
    image_2 = Image.open('./MITSloanLogo_MASTER-Horizontal_Print.png')
    st.image(image_2, caption="")

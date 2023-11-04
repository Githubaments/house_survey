import streamlit as st
import pandas as pd

# Title of the app
st.title('House Viewing Checklist')

# Initialize an empty list to store the responses and custom questions
responses = []
custom_questions = []

# Address input at the top
st.header('Property Details')
address = st.text_input("Address of the Property:")
responses.append({'Question': 'Address of the Property', 'Response': address})

# Function to create a yes/no radio button and store response
def yes_no_radio(label, key):
    response = st.radio(label, ('Yes', 'No'), key=key)
    responses.append({'Question': label, 'Response': response})
    return response

# Function to create a 1-5 rating scale and store response
def rating_scale(label, key):
    response = st.radio(label, [1, 2, 3, 4, 5], key=key)
    responses.append({'Question': label, 'Response': response})
    return response

# Predefined questions (you can add more as needed)
st.header('Predefined Questions')

# Exterior section
st.subheader('Exterior')
yes_no_radio('Is the exterior appealing?', 'exterior_appeal')

# Custom questions section
st.header('Add Custom Question')
custom_question = st.text_input("Enter your custom question:")
question_type = st.selectbox("Select response type:", ('Yes/No', '1-5 Rating'))

if st.button('Add Question'):
    if custom_question and question_type:
        custom_questions.append((custom_question, question_type))
        st.success(f"Added custom question: {custom_question}")
    else:
        st.error("Please enter a custom question and select a response type.")

for cq, qt in custom_questions:
    st.subheader('Custom Questions')
    if qt == 'Yes/No':
        yes_no_radio(cq, cq)
    elif qt == '1-5 Rating':
        rating_scale(cq, cq)

# Overall impression and notes section
st.header('Final Thoughts')
overall_impression = rating_scale('Overall impression out of 5', 'overall_impression')
notes = st.text_area("Additional notes:")
responses.append({'Question': 'Overall Impression', 'Response': overall_impression})
responses.append({'Question': 'Additional Notes', 'Response': notes})

# Submit button for all questions and the rest of the code for DataFrame creation and download
if st.button('Submit All Questions'):
    df_all_questions = pd.DataFrame(responses)
    st.write('All Questions Responses:')
    st.dataframe(df_all_questions)
    
    # Download button
    st.download_button(
        label="Download All Questions Results as CSV",
        data=df_all_questions.to_csv(index=False).encode('utf-8'),
        file_name='house_viewing_results.csv',
        mime='text/csv',
    )
    st.success('All questions submitted!')

# Reminder: To run the Streamlit app, save the code in a .py file and run it with the command:
# streamlit run your_script.py

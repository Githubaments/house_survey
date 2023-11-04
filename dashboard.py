import streamlit as st
import pandas as pd
import gspread
from google.oauth2 import service_account


# Use the new `google-auth` library for credentials
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ],
)

# Use gspread to authorize the credentials
gc = gspread.authorize(credentials)



# Function to save dataframe to Google Sheet
def save_to_sheet(df, sheet_name):
    sh = gc.open(sheet_name)
    worksheet = sh.sheet1
    # Convert DataFrame to list of lists
    data = df.astype(str).values.tolist()
    # Get existing data from sheet
    existing = len(worksheet.get_all_values())
    # Append data to sheet
    if existing == 0:
        # Include header if sheet is empty
        worksheet.append_rows([df.columns.tolist()] + data)
    else:
        worksheet.append_rows(data)

# Title of the app
st.title('House Viewing Checklist')

# Initialize an empty list to store the responses
responses = []

# Address input at the top
st.header('Property Details')
address = st.text_input("Address of the Property:")
if address:  # Only append if there is an input
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

# Function for adding a custom question
def add_custom_question():
    custom_question = st.text_input("Enter your custom question:")
    question_type = st.selectbox("Select response type:", ('Yes/No', '1-5 Rating'), key='select_response_type')

    if st.button('Add Question'):
        if custom_question and question_type:
            responses.append({'Question': custom_question, 'Response': 'Not Answered'})
            if question_type == 'Yes/No':
                yes_no_radio(custom_question, custom_question)
            elif question_type == '1-5 Rating':
                rating_scale(custom_question, custom_question)
            st.success(f"Added custom question: {custom_question}")
        else:
            st.error("Please enter a custom question and select a response type.")

# Display predefined questions and add custom question functionality
st.header('Predefined Questions')
yes_no_radio('Are there any large cracks in walls?', 'structural_cracks')
yes_no_radio('Is the roof missing any tiles?', 'roof_condition')
yes_no_radio('Do taps and showers function properly?', 'plumbing')
yes_no_radio('Do all light switches and outlets function?', 'electrical_system')
yes_no_radio('Is the HVAC system in good condition?', 'hvac_condition')
yes_no_radio('Do windows and doors have proper insulation?', 'windows_doors_insulation')
rating_scale('How would you rate the quality of insulation?', 'insulation_quality')
yes_no_radio('Any signs of pest infestation?', 'pests')
rating_scale('How would you rate the neighborhood?', 'neighborhood_rating')
yes_no_radio('Does the property layout suit your lifestyle?', 'property_layout')
yes_no_radio('Are smoke detectors present and functional?', 'smoke_detectors')
yes_no_radio('Does the house seem well maintained?', 'maintenance')

# Add any additional custom questions
add_custom_question()

# Overall impression and notes section
st.header('Final Thoughts')
overall_impression = rating_scale('Overall impression out of 5', 'overall_impression')
notes = st.text_area("Additional notes:")
responses.append({'Question': 'Overall Impression', 'Response': overall_impression})
responses.append({'Question': 'Additional Notes', 'Response': notes})

# Assume 'df_all_questions' is the final DataFrame you want to save
df_all_questions = pd.DataFrame(responses)  # Example DataFrame creation

# Submit button for all questions and the rest of the code for DataFrame creation and download
if st.button('Submit All Questions'):
    st.write('All Questions Responses:')
    st.dataframe(df_all_questions)
    
    # Save to Google Sheets
    try:
        save_to_sheet(df_all_questions, 'Sheet1')  # Replace with your Google Sheet name
        st.success('Responses have been successfully saved to Google Sheets.')
    except Exception as e:
        st.error(f"An error occurred: {e}")

    # Download button for CSV
    st.download_button(
        label="Download All Questions Results as CSV",
        data=df_all_questions.to_csv(index=False).encode('utf-8'),
        file_name='house_viewing_results.csv',
        mime='text/csv',
    )

# Reminder: To run the Streamlit app, save the code in a .py file and run it with the command:
# streamlit run your_script.py

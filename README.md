# SIET College FAQ Chatbot

A beginner-friendly AI-based college FAQ chatbot built using Python, Streamlit, Pandas, Sentence Transformers, and Scikit-learn.

## Project Objective
This project provides a web-based chatbot for Srinivasa Institute of Engineering and Technology that answers common student and visitor questions about:

- Departments
- Admissions
- Timings
- Hostel facilities
- Library timing
- Transportation
- Placements
- General college information

The chatbot uses semantic similarity and sentence embeddings so that different phrasings of the same question can be matched correctly.

## Project Structure

```text
SIET-College-FAQ-Chatbot/
├── app.py
├── college_faq.csv
├── requirements.txt
├── README.md
├── screenshots/
└── frontend/
    ├── index.html
    ├── script.js
    └── styles.css
```

## Technologies Used
- Python
- Streamlit
- Pandas
- Sentence Transformers
- Scikit-learn
- CSV-based FAQ dataset

## Features
- Natural-language question input
- Semantic similarity matching using sentence embeddings
- Answer from a college FAQ knowledge base
- Fallback response when information is not found
- Chat history display
- FAQ category overview
- English and Telugu language support
- Quick action buttons for common student queries
- Voice output using browser speech synthesis
- Clean, modern UI for a mini-project presentation

## Setup Instructions

1. Open a terminal and go to the project folder.
2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Run the Streamlit app:

```bash
streamlit run app.py
```

5. Open the browser link shown in the terminal output.

## How to Run the Project

```bash
streamlit run app.py
```

The app will open in the browser and you can type questions like:

- What are the college timings?
- Is AI & ML available?
- What is the CSE management fee?
- Is there a girls hostel?
- Does the college provide placements?

## Project Architecture

### 1. Data Layer
The chatbot reads the FAQ information from `college_faq.csv`. It contains columns:

- id
- category
- question
- answer

### 2. NLP / Embedding Layer
The user question is converted into a sentence embedding using the Sentence Transformers model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

All FAQ questions are also converted to embeddings. Then cosine similarity is calculated between the user query and the stored FAQs.

### 3. Matching Layer
If the highest similarity score is above a threshold, the corresponding FAQ answer is returned.

If the score is below the threshold, the chatbot returns:

> I’m sorry, I don't have reliable information about that. Please contact the college authorities for further information.

### 4. UI Layer
The Streamlit interface provides:
- college title
- welcome message
- chat box
- send button
- chat history
- clear chat button
- FAQ category section

## Major Components Explained

### app.py
This is the main application file. It contains:
- dataset loading
- model loading
- embedding generation
- similarity comparison
- fallback response logic
- Streamlit user interface

### college_faq.csv
This file stores the FAQ entries used by the chatbot. Each row contains a category, question, and answer.

### requirements.txt
Lists the Python packages needed to run the chatbot.

## Testing Procedure

The chatbot can be tested with multiple questions to check whether it returns the correct response.

### Sample Testing Format

| User Question | Expected Answer | Chatbot Answer | Result |
|---|---|---|---|
| What are the college timings? | 9:10 AM to 4:00 PM | Matches answer | Correct |
| Is AI & ML available? | Yes, AI & ML department is available | Matches answer | Correct |
| What is the CSE management fee? | ₹1,00,000 | Matches answer | Correct |
| Is there a girls hostel? | Yes, girls' hostel facility is available | Matches answer | Correct |

### Accuracy Formula

```text
Accuracy = Correct Answers / Total Questions × 100
```

### Example Calculation
If 24 out of 25 test questions are answered correctly:

```text
Accuracy = 24 / 25 × 100 = 96%
```

## Sample Questions and Outputs

### 1. Question
What are the college timings?

### Output
The college timings are 9:10 AM to 4:00 PM.

### 2. Question
Is there a girls hostel?

### Output
Yes, girls' hostel facility is available.

### 3. Question
How can I get admission?

### Output
Students can contact the college authorities for admission information or seek admission through EAMCET/AP EAPCET and ECET as applicable.

### 4. Question
What is the AI & ML management fee?

### Output
AI & ML management admission fee is ₹1,30,000.

### 5. Question
Does the college provide transportation?

### Output
Yes, the college provides transportation facilities.

## Future Scope
- Voice-based questions
- Multilingual support
- Telugu language support
- Official website integration
- Admin panel for FAQ updates
- Database-based knowledge base
- Generative AI / LLM integration
- Real-time announcements
- Student admission assistance

## Viva Questions and Answers

### Q1: What is the main objective of this project?
A: To build a chatbot that answers student and visitor questions about the college using semantic similarity and FAQ knowledge.

### Q2: Why use Sentence Transformers?
A: Because they convert questions into embeddings so similar questions can be matched even if the wording is different.

### Q3: What happens if the user asks something not present in the dataset?
A: The chatbot returns a polite fallback message asking the user to contact college authorities.

### Q4: Why is the FAQ dataset stored in CSV format?
A: CSV is simple, easy to edit, and beginner-friendly for a mini-project.

### Q5: What is cosine similarity?
A: It measures how close two vectors are in meaning. In this project, it is used to compare the user question with FAQ questions.

## Important Note
This project uses only the information provided in the problem statement. It does not invent or assume extra details beyond the official college data shared in the project prompt.

## Conclusion
This project is suitable for a B.Tech AI & ML mini-project demonstration and viva because it combines machine learning, NLP, and web development within a simple, practical application.

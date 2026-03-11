# GenAI Resume Analyzer and Job Match System

## Project Overview

This is an AI-powered web application that analyzes resumes and matches them against job descriptions using Natural Language Processing (NLP) and Generative AI techniques. The system extracts key information from resumes, calculates job compatibility scores, identifies missing skills, and provides personalized improvement suggestions.

## Technologies Used

- **Python**: Core programming language
- **Streamlit**: Web application framework for the user interface
- **HuggingFace Transformers**: For advanced NLP and text embeddings
- **Sentence Transformers**: For semantic similarity calculations
- **spaCy**: For natural language processing tasks
- **pdfplumber**: For PDF text extraction
- **Pandas**: For data manipulation
- **Scikit-learn**: For machine learning utilities
- **NLTK**: For additional NLP functionality

## Features

### Core Functionality
- **Resume Upload**: Support for PDF resume uploads
- **Text Extraction**: Automatic extraction of text from PDF resumes
- **Skill Extraction**: NLP-based extraction of skills, education, and experience
- **Job Matching**: Semantic similarity analysis between resume and job description
- **Compatibility Scoring**: Percentage-based job match score
- **Missing Skills Identification**: Highlights skills required by the job but missing from resume
- **Improvement Suggestions**: AI-generated recommendations to enhance resume

### User Interface
- Clean and intuitive Streamlit-based web interface
- Sidebar for input controls
- Real-time analysis results display
- Organized output sections for easy reading

## Installation

1. **Clone or download the project**:
   ```bash
   cd your-project-directory
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download spaCy model** (if not already installed):
   ```bash
   python -m spacy download en_core_web_sm
   ```

## How to Run

1. **Navigate to the project directory**:
   ```bash
   cd resume_analyzer
   ```

2. **Run the Streamlit application**:
   ```bash
   streamlit run app.py
   ```

3. **Open your browser** and go to the URL displayed in the terminal (usually `http://localhost:8501`)

## Usage

1. **Upload Resume**: Click on the file uploader in the sidebar and select your resume PDF
2. **Enter Job Description**: Paste the job description text in the text area
3. **Analyze**: Click the "Analyze Resume" button
4. **View Results**: Review the extracted information, match score, and suggestions

## Project Structure

```
resume_analyzer/
│
├── app.py                    # Main Streamlit application
├── resume_parser.py          # PDF text extraction and parsing
├── skill_extractor.py        # NLP-based skill extraction
├── job_matcher.py            # Job matching and similarity scoring
├── utils.py                  # Utility functions
├── requirements.txt          # Python dependencies
├── sample_resumes/           # Directory for sample resume files
└── README.md                 # This documentation file
```

## Example Output

After analysis, the system displays:

- **Extracted Skills**: Python, Machine Learning, Data Analysis, SQL
- **Job Match Score**: 78%
- **Matching Skills**: Python, Machine Learning
- **Missing Skills**: TensorFlow, AWS, Docker
- **Improvement Suggestions**:
  - Consider adding or highlighting TensorFlow, AWS, and Docker skills
  - Add more details about your projects and achievements

## Technical Details

### NLP Pipeline
1. **Text Extraction**: Uses pdfplumber to extract raw text from PDFs
2. **Preprocessing**: Cleans and normalizes text data
3. **Skill Extraction**: Employs spaCy for named entity recognition and keyword extraction
4. **Semantic Similarity**: Uses Sentence Transformers to create embeddings and calculate cosine similarity

### Matching Algorithm
- Converts resume and job description to vector embeddings
- Calculates cosine similarity between vectors
- Identifies matching and missing skills through keyword comparison
- Generates improvement suggestions based on gaps

## Future Enhancements

- Support for multiple file formats (DOCX, TXT)
- Advanced skill categorization and prioritization
- Integration with job board APIs
- Resume optimization recommendations
- Multi-language support

## Contributing

Feel free to fork this project and submit pull requests with improvements!

## License

This project is open-source and available under the MIT License.
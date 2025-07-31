# TalentScout – AI Hiring Assistant

## Overview
TalentScout is a Streamlit-based AI chatbot that screens candidates by collecting personal details and generating a practical technical question based on their tech stack using an LLM (Groq API). The chatbot provides a conversational interface for gathering candidate information and dynamically generates a relevant technical interview question.

## Features
- 🤖 **AI-Powered Chatbot**: Uses Groq API for natural language processing
- 📝 **Step-by-Step Data Collection**: Collects candidate information systematically
- 🔍 **Input Validation**: Validates email, phone, experience, and other fields
- 🎯 **Dynamic Question Generation**: Creates a scenario-based technical question tailored to the declared tech stack
- 💾 **Session State Management**: Maintains conversation context using Streamlit session state
- 🛑 **Conversation End Detection**: Gracefully ends the chat when the candidate completes the process or uses an exit keyword

## Installation

### Prerequisites
- Python 3.7+
- Groq API key (sign up at [groq.com](https://groq.com))

### Setup Steps
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Key**
   - Open `utils.py`
   - Replace `YOUR_GROQ_API_KEY` with your actual Groq API key
   ```python
   GROQ_API_KEY = 'your-actual-api-key-here'
   ```

4. **Run the application**
   ```bash
   streamlit run main.py
   ```

5. **Access the app**
   - Open your browser and go to `http://localhost:8501`

## Conversation Flow

1. **Greeting**  
   The chatbot greets the candidate and explains the process.

2. **Information Gathering**  
   The chatbot collects:
   - Full Name
   - Email Address
   - Phone Number (with country code)
   - Years of Experience
   - Desired Position(s)
   - Current Location
   - Tech Stack (comma-separated)

3. **Technical Question Generation**  
   After collecting the tech stack, the chatbot generates one practical, scenario-based technical question relevant to the candidate's declared technologies.

4. **Answer Collection**  
   The candidate answers the technical question or can type "skip" to move on.

5. **End Conversation**  
   The chatbot thanks the candidate and informs them that the team will get back to them via the provided email or phone.

## Prompt Design

- **System Context**:  
  The chatbot maintains a professional, friendly tone, collects information efficiently, and generates one relevant technical question.
- **Greeting Prompt**:  
  Welcomes candidates, explains the process, and sets expectations.
- **Technical Question Prompt**:  
  Generates a single scenario-based question tailored to the candidate's tech stack.

## Challenges and Solutions

- **API Integration**:  
  Robust error handling and fallback responses for Groq API failures.
- **Input Validation**:  
  Comprehensive validation for email, phone, experience, and name using regex and logical checks.
- **Session State Management**:  
  Uses Streamlit's session_state to persist chat history, candidate data, and step progression.
- **Dynamic Question Generation**:  
  Flexible prompt templates for generating contextual scenario-based questions.

## Tech Stack

### Backend
- **Python 3.7+**: Core programming language
- **Streamlit**: Web application framework
- **Requests**: HTTP library for API calls

### AI/ML
- **Groq API**: LLM service for natural language processing
- **Llama3-8b-8192**: Language model for generating responses

### Validation & Processing
- **Regex**: Pattern matching for input validation
- **JSON**: Data serialization for API communication

### Development Tools
- **Git**: Version control
- **Pip**: Package management

## Project Structure
```
chatbot/
├── main.py              # Main Streamlit application
├── utils.py             # Utility functions (API, validation)
├── prompts.py           # Prompt templates and system context
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## Usage

### For Candidates
1. Open the application in your browser
2. Start chatting with TalentScout
3. Provide your information step by step
4. Answer the generated technical question
5. Complete the screening process

### For Developers
1. Set up the environment following installation steps
2. Configure your Groq API key
3. Run the application locally
4. Test the conversation flow
5. Customize prompts and validation as needed

## API Configuration

### Groq API Setup
1. Sign up at [groq.com](https://groq.com)
2. Generate an API key from your dashboard
3. Replace the placeholder in `utils.py`
4. Test the connection with a simple prompt

### Rate Limits
- Groq API has rate limits based on your plan
- Implement appropriate error handling for rate limit exceeded
- Consider implementing retry logic for failed requests

## Future Enhancements
- [ ] Database integration for storing candidate data
- [ ] Email notifications for completed screenings
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Integration with ATS systems
- [ ] Video interview capabilities
- [ ] Automated scheduling features

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

---

**Note**: Remember to replace the placeholder API key with your actual Groq API key before running the application.
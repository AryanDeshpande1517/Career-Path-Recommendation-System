# Career Path Recommendation System

## 📖 Overview

Career Advisor AI is a Python-based conversational tool that helps users discover potential career paths tailored to their interests and skills. Using natural language processing and a comprehensive career database, the system provides personalized career recommendations through an interactive chat interface.

## 📂 Dataset

Total careers = 18 [across 6 fields]

Each career includes:
- Detailed description.
- Average salary figure.
- Required skills/background.
- Fields include 2 refining questions each.
- 5-15 keywords per field for interest matching.

Data Sources:
- Salary data compiled from BLS and industry reports (US averages).
- Career descriptions synthesized from occupational outlook handbooks.
- Keywords selected based on common interest expressions.

## 🧠 Model Architecture

1) GPT-2 (Text Generation Model):
- Version: Standard GPT-2 (Hugging Face transformers).
- Layers: 12-layer transformer.
- Parameters: 117M (base model) for richer responses.
- Use Case: Generates career suggestions from structured prompts.

2) Keyword-Based Field Classifier:
- Rule-based matching using predefined keywords.
- Maps user input to one of 6 career fields (STEM, Arts, Sports, etc).

3) Prompt Engineering for Career Suggestions:
- Leverages GPT-2’s stronger reasoning for nuanced recommendations.

## 🛠 Setup and Execution Guide

## Prerequisites  
- Python 3.8+  
- pip (Python Package Manager).  

1. Install Dependencies:  
- pip install torch transformers

2. Run the Career Advisor:  
- python career_advisor.py

3. Interact with the AI:  
- Enter your interests (e.g., "I like programming and math").  
- Answer follow-up questions.  
- Get personalized career recommendations.  

## Optional: Use GPU (for faster inference)  
- pip install accelerate (Required for GPU support)
- python career_advisor.py (Automatically uses GPU if available)

## Expected Output  
AI: Hi! Let's explore your dream career. What do you enjoy most?  
You: [Your input]  
AI: Based on your interests, I recommend: [Career]  
Because: [Explanation]

[Note: First run may take longer (~1-2 min) to download GPT-2 model weights]

## Assumptions for the Project

1. User Input Clarity:  
   Users will describe interests using common keywords (e.g., "programming" not "I like making computers do things").

2. Career Field Coverage:  
   The 6 predefined fields (STEM, Arts, etc.) sufficiently cover most career interests.

3. Salary Relevance:
   Average salary figures are meaningful motivators for career decisions.

4. Binary Question Sufficiency:  
   Just 2 follow-up questions per field provide enough nuance for recommendations.

5. Model Reliability:
   GPT-2 will consistently return valid career names from the predefined list.

6. Western Job Market Focus:  
   Salary data and career paths assume US/European job market norms.

7. Technical Accessibility:
   Users have Python installed and can run command-line tools without GUI support.

These assumptions simplify development but may need refinement for real-world scalability.

## Approach

1. Keyword-Based Field Matching:
Maps user interests to predefined career fields (STEM, Arts, etc.) using a rule-based keyword system.

2. AI-Powered Suggestion Engine:
Uses GPT-2 to analyze user responses and recommend the most suitable career from a structured database.

3. Interactive Refinement:
Asks follow-up questions to refine suggestions before delivering personalized career insights.

(Balances structured career data with AI flexibility for tailored recommendations).

## 🧪 Sample Results
[Device set to use cpu]

- AI: Hi! Let's explore your dream career. What do you enjoy most? (Examples: programming, graphic design, sports medicine, game development)

- You: I enjoy my career in sports.

- AI: Great! Let's explore tech careers.

- AI: Do you prefer content creation or technical development?

- You: I enjoy and prefer technical development

- AI: Are you more interested in entertainment or practical applications?

- You: I am more intersted in practical applications

[Setting pad_token_id to eos_token_id:50256 for open-end generation]

- AI: Based on your interests, I recommend: Game Design, Because: Combines art and programming for interactive media (Avg salary: $85k)

- AI: Would you like to explore another field? (yes/no)

- You: no

- AI: Wishing you success in your career journey!

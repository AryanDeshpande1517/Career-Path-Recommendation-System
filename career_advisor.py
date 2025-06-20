from transformers import pipeline, set_seed
import re

# Initialize the AI
set_seed(42)
career_ai = pipeline("text-generation", 
                    model="gpt2",
                    max_new_tokens=100,
                    truncation=True)

# Comprehensive Career Database
career_database = {
    "stem": {
        "keywords": ["coding", "programming", "python", "java", "javascript", "math", 
                    "calculus", "statistics", "physics", "chemistry", "biology", 
                    "robotics", "ai", "machine learning", "cybersecurity", "hacking"],
        "careers": {
            "Software Engineering": "Develops problem-solving skills for building scalable systems (Avg salary: $120k)",
            "Data Science": "Python and statistics skills for extracting business insights (Avg salary: $115k)",
            "Actuarial Science": "Math skills for risk assessment in insurance/finance (Avg salary: $110k)",
            "Quantum Computing Research": "Physics foundation for next-gen computing (Avg salary: $125k)",
            "Biotechnology": "Biology knowledge applied to medical innovations (Avg salary: $95k)"
        },
        "questions": [
            "Do you prefer theoretical research or practical applications?",
            "Are you more interested in data analysis or system building?"
        ]
    },
    "arts": {
        "keywords": ["painting", "drawing", "sketching", "photography", "music", 
                    "singing", "acting", "writing", "poetry", "dance", "sculpture"],
        "careers": {
            "Graphic Design": "Visual communication skills for branding (Avg salary: $65k)",
            "Architecture": "Spatial design for functional buildings (Avg salary: $85k)",
            "Sound Engineering": "Audio production for media/events (Avg salary: $70k)",
            "Content Creation": "Writing skills for digital marketing (Avg salary: $60k)"
        },
        "questions": [
            "Do you prefer working with physical or digital media?",
            "Are you more focused on commercial or artistic expression?"
        ]
    },
    "sports": {
        "keywords": ["cricket", "football", "soccer", "basketball", "swimming", 
                    "tennis", "badminton", "chess", "esports"],
        "careers": {
            "Sports Analytics": "Data-driven player performance analysis (Avg salary: $75k)",
            "Sports Medicine": "Injury prevention/treatment for athletes (Avg salary: $90k)",
            "Athletic Training": "Physical conditioning expertise (Avg salary: $65k)"
        },
        "questions": [
            "Do you prefer team sports or individual competition?",
            "Are you more interested in performance or health aspects?"
        ]
    },
    "business": {
        "keywords": ["finance", "accounting", "marketing", "sales", "economics"],
        "careers": {
            "Investment Banking": "Financial modeling for mergers/acquisitions (Avg salary: $150k)",
            "Digital Marketing": "SEO/social media strategy skills (Avg salary: $80k)"
        },
        "questions": [
            "Do you prefer working with numbers or people?",
            "Are you more interested in strategy or execution?"
        ]
    },
    "medical": {
        "keywords": ["medicine", "surgery", "psychology", "nutrition"],
        "careers": {
            "Clinical Practice": "Patient diagnosis and treatment (Avg salary: $200k)",
            "Dietetics": "Nutritional planning for health (Avg salary: $75k)"
        },
        "questions": [
            "Do you prefer direct patient care or research work?",
            "Are you more interested in physical or mental health?"
        ]
    },
    "tech": {
        "keywords": ["video editing", "animation", "vr", "ar"],
        "careers": {
            "Game Design": "Combines art and programming for interactive media (Avg salary: $85k)",
            "Virtual Reality Development": "3D environment creation for immersive experiences (Avg salary: $110k)"
        },
        "questions": [
            "Do you prefer content creation or technical development?",
            "Are you more interested in entertainment or practical applications?"
        ]
    }
}

def get_field(user_input):
    user_input = user_input.lower()
    for field in career_database:
        for keyword in career_database[field]["keywords"]:
            if keyword in user_input:
                return field
    return None

def get_career_suggestion(field, answers):
    try:
        
        possible_careers = list(career_database[field]["careers"].keys())
        
        
        prompt = f"""Based on these answers about {field} interests:
        Q: {career_database[field]['questions'][0]}
        A: {answers[0]}
        Q: {career_database[field]['questions'][1]}
        A: {answers[1]}
        
        Which career from {possible_careers} is most suitable?
        Return only the career name:"""
        
        response = career_ai(prompt, max_new_tokens=20)
        career = re.sub(r'[^a-zA-Z ]', '', response[0]['generated_text'].split('\n')[-1]).strip()
        
        
        if career not in possible_careers:
            career = possible_careers[0]
            
        return career, career_database[field]["careers"][career]
        
    except Exception as e:
        print(f"AI: I had trouble thinking of a suggestion. Here's one option:")
        possible_careers = list(career_database[field]["careers"].keys())
        return possible_careers[0], career_database[field]["careers"][possible_careers[0]]

def start_conversation():
    print("AI: Hi! Let's explore your dream career. What do you enjoy most?")
    print("(Examples: programming, graphic design, sports medicine, game development)")
    
    while True:
        user_input = input("\nYou: ").lower()
        field = get_field(user_input)
        
        if field:
            print(f"\nAI: Great! Let's explore {field} careers.")
            answers = []
            
            for question in career_database[field]["questions"]:
                print(f"AI: {question}")
                answers.append(input("You: ").lower().strip())
            
            career, explanation = get_career_suggestion(field, answers)
            
            print(f"\nAI: Based on your interests, I recommend: {career}")
            print(f"Because: {explanation}")
            
            print("\nWould you like to explore another field? (yes/no)")
            if input().lower() != 'yes':
                print("AI: Wishing you success in your career journey!")
                break
        else:
            print("AI: Interesting! Could you tell me more about your passions?")
            print("Try being more specific (e.g., 'I enjoy robotics' or 'I love creative writing')")

# Start the conversation
start_conversation()
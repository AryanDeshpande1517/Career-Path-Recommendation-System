from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import requests
import re
import uvicorn

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
    possible_careers = list(career_database[field]["careers"].keys())
    prompt = f"Based on these answers about {field} interests:\nQ: {career_database[field]['questions'][0]}\nA: {answers[0]}\nQ: {career_database[field]['questions'][1]}\nA: {answers[1]}\nWhich career from {possible_careers} is most suitable?\nReturn only the career name:"
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/gpt2",
            headers={"Accept": "application/json"},
            json={"inputs": prompt, "parameters": {"max_new_tokens": 20}}
        )
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
                generated = data[0]["generated_text"]
                career = generated.split("\n")[-1].strip()
                career = re.sub(r'[^a-zA-Z ]', '', career)
                if career not in possible_careers:
                    career = possible_careers[0]
                return career, career_database[field]["careers"][career]
        # fallback if API fails
        return possible_careers[0], career_database[field]["careers"][possible_careers[0]]
    except Exception:
        return possible_careers[0], career_database[field]["careers"][possible_careers[0]]

app = FastAPI()

class CareerRequest(BaseModel):
    user_input: str
    answers: list[str]

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
    <head>
        <title>Career Recommendation System</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f7f7f7; margin: 0; padding: 0; }
            .container { max-width: 500px; margin: 40px auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
            h2 { text-align: center; }
            label { display: block; margin-top: 15px; }
            input, textarea { width: 100%; padding: 8px; margin-top: 5px; border-radius: 4px; border: 1px solid #ccc; }
            button { margin-top: 20px; width: 100%; padding: 10px; background: #0070f3; color: #fff; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; }
            button:hover { background: #005bb5; }
            .result { margin-top: 20px; padding: 15px; background: #e6f7ff; border-radius: 4px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Career Recommendation System</h2>
            <form id="careerForm">
                <label for="user_input">What do you enjoy most?</label>
                <input type="text" id="user_input" name="user_input" required placeholder="e.g. programming, graphic design, sports medicine">
                <label for="answer1">Answer 1:</label>
                <input type="text" id="answer1" name="answer1" required placeholder="e.g. practical applications">
                <label for="answer2">Answer 2:</label>
                <input type="text" id="answer2" name="answer2" required placeholder="e.g. system building">
                <button type="submit">Get Career Suggestion</button>
            </form>
            <div class="result" id="result" style="display:none;"></div>
        </div>
        <script>
        document.getElementById('careerForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const user_input = document.getElementById('user_input').value;
            const answer1 = document.getElementById('answer1').value;
            const answer2 = document.getElementById('answer2').value;
            const resultDiv = document.getElementById('result');
            resultDiv.style.display = 'none';
            resultDiv.innerHTML = '';
            try {
                const response = await fetch('./suggest-career', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ user_input, answers: [answer1, answer2] })
                });
                const data = await response.json();
                if (data.error) {
                    resultDiv.innerHTML = `<b>Error:</b> ${data.error}`;
                } else {
                    resultDiv.innerHTML = `<b>Field:</b> ${data.field}<br><b>Career:</b> ${data.career}<br><b>Because:</b> ${data.explanation}`;
                }
                resultDiv.style.display = 'block';
            } catch (err) {
                resultDiv.innerHTML = 'An error occurred.';
                resultDiv.style.display = 'block';
            }
        });
        </script>
    </body>
    </html>
    """

@app.post("/suggest-career")
def suggest_career(req: CareerRequest):
    field = get_field(req.user_input)
    if not field:
        return {"error": "Could not determine field from user input."}
    if len(req.answers) < 2:
        return {"error": "Please provide two answers for the field questions."}
    career, explanation = get_career_suggestion(field, req.answers)
    return {
        "field": field,
        "career": career,
        "explanation": explanation
    }

# For local testing (not used by Vercel)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 
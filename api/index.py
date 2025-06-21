from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import requests
import re
import uvicorn

career_database = {
    "stem": {
        "keywords": ["coding", "programming", "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "go", "rust",
                     "html", "css", "react", "angular", "vue", "node", "django", "flask", "spring", "laravel",
                     "math", "calculus", "algebra", "statistics", "probability", "linear algebra", "discrete math",
                     "physics", "quantum", "mechanics", "thermodynamics", "electromagnetism", "astrophysics",
                     "chemistry", "organic", "inorganic", "biochemistry", "physical chemistry", "analytical chemistry",
                     "biology", "microbiology", "genetics", "molecular biology", "ecology", "zoology", "botany",
                     "robotics", "drones", "automation", "control systems", "mechatronics",
                     "ai", "machine learning", "deep learning", "neural networks", "nlp", "computer vision",
                     "cybersecurity", "hacking", "penetration testing", "ethical hacking", "network security",
                     "data science", "big data", "data mining", "data visualization", "business intelligence",
                     "cloud computing", "aws", "azure", "google cloud", "devops", "kubernetes", "docker",
                     "blockchain", "cryptography", "smart contracts", "web3", "solidity",
                     "quantum computing", "quantum algorithms", "quantum cryptography",
                     "bioinformatics", "computational biology", "genomics", "proteomics",
                     "nanotechnology", "materials science", "semiconductors"],
        
        "careers": {
            "Software Engineering": "Design, develop, test, and maintain software systems and applications (Avg salary: $120k)",
            "Data Science": "Extract insights from complex data using statistical and machine learning techniques (Avg salary: $115k)",
            "Machine Learning Engineer": "Develop and implement machine learning models for various applications (Avg salary: $130k)",
            "DevOps Engineer": "Bridge development and operations with automation and cloud technologies (Avg salary: $125k)",
            "Cybersecurity Analyst": "Protect systems and networks from digital attacks (Avg salary: $110k)",
            "Quantum Computing Researcher": "Develop algorithms and applications for quantum computers (Avg salary: $140k)",
            "Bioinformatics Scientist": "Apply computational techniques to biological data (Avg salary: $105k)",
            "Robotics Engineer": "Design and build robotic systems for various industries (Avg salary: $115k)",
            "Cloud Architect": "Design and implement cloud computing strategies (Avg salary: $135k)",
            "Data Engineer": "Build systems for collecting, managing, and converting raw data (Avg salary: $120k)",
            "Blockchain Developer": "Create decentralized applications and smart contracts (Avg salary: $130k)",
            "Computational Biologist": "Develop mathematical models for biological systems (Avg salary: $100k)",
            "Materials Scientist": "Research and develop new materials with specific properties (Avg salary: $95k)",
            "Astrophysicist": "Study celestial objects and phenomena (Avg salary: $110k)",
            "Nanotechnologist": "Work with matter at atomic and molecular scales (Avg salary: $105k)"
        },
        
        "questions": [
            "Do you prefer theoretical research or practical applications?",
            "Are you more interested in data analysis or system building?"
        ]
    },
    "arts": {
        "keywords": ["painting", "drawing", "sketching", "illustration", "digital art", "concept art", "character design",
                     "photography", "photo editing", "portrait", "landscape", "product photography", "fashion photography",
                     "music", "singing", "songwriting", "music production", "audio engineering", "sound design", "dj",
                     "acting", "theater", "drama", "improvisation", "screenwriting", "filmmaking", "cinematography",
                     "writing", "poetry", "creative writing", "copywriting", "journalism", "blogging", "technical writing",
                     "dance", "choreography", "ballet", "contemporary", "hip hop", "ballroom",
                     "sculpture", "ceramics", "pottery", "woodworking", "metalworking", "glassblowing",
                     "graphic design", "typography", "branding", "logo design", "packaging design", "publication design",
                     "animation", "2d animation", "3d animation", "motion graphics", "stop motion", "visual effects",
                     "fashion design", "textile design", "costume design", "jewelry design", "accessory design",
                     "architecture", "interior design", "landscape design", "urban planning", "furniture design",
                     "art history", "art criticism", "art curation", "art therapy", "art education"],
        "careers": {
            "Graphic Designer": "Create visual concepts to communicate ideas (Avg salary: $65k)",
            "Art Director": "Oversee visual style and content in media (Avg salary: $95k)",
            "Illustrator": "Create original images for various media (Avg salary: $60k)",
            "Photographer": "Capture and edit professional photographs (Avg salary: $50k)",
            "Music Producer": "Oversee recording and production of music (Avg salary: $70k)",
            "Animator": "Create animated sequences for various media (Avg salary: $75k)",
            "Art Therapist": "Use art-making to improve mental health (Avg salary: $55k)",
            "Museum Curator": "Acquire, care for, and exhibit collections (Avg salary: $65k)",
            "Creative Director": "Lead creative vision for brands/media (Avg salary: $110k)",
            "Fashion Designer": "Create original clothing and accessories (Avg salary: $75k)",
            "Industrial Designer": "Design products for mass production (Avg salary: $85k)",
            "Architect": "Design buildings and physical structures (Avg salary: $85k)",
            "Interior Designer": "Create functional and aesthetic indoor spaces (Avg salary: $60k)",
            "Film Director": "Control artistic/dramatic aspects of films (Avg salary: $90k)",
            "Game Artist": "Create visual assets for video games (Avg salary: $80k)"
        },
        "questions": [
            "Do you prefer working with physical or digital media?",
            "Are you more focused on commercial or artistic expression?"
        ]
    },
    "sports": {
        "keywords": ["cricket", "football", "soccer", "basketball", "baseball", "hockey", "rugby", "volleyball", "tennis",
                     "badminton", "table tennis", "golf", "swimming", "diving", "water polo", "rowing", "sailing", "surfing",
                     "athletics", "running", "marathon", "sprinting", "jumping", "throwing", "triathlon", "cycling", "bmx",
                     "gymnastics", "weightlifting", "bodybuilding", "crossfit", "martial arts", "boxing", "wrestling", "judo",
                     "karate", "taekwondo", "fencing", "archery", "shooting", "equestrian", "horse riding", "polo",
                     "esports", "gaming", "competitive gaming", "streaming", "coaching", "sports psychology", "sports medicine",
                     "physiotherapy", "nutrition", "fitness", "personal training", "sports management", "sports marketing",
                     "sports journalism", "commentary", "umpiring", "refereeing", "scouting", "talent identification"],
        "careers": {
            "Professional Athlete": "Compete in sports at highest levels (Avg salary: Varies widely)",
            "Sports Coach": "Train and develop athletes (Avg salary: $45k)",
            "Sports Physiotherapist": "Prevent and treat sports injuries (Avg salary: $75k)",
            "Sports Psychologist": "Help athletes with mental performance (Avg salary: $80k)",
            "Sports Nutritionist": "Design diets for athletic performance (Avg salary: $65k)",
            "Sports Agent": "Represent athletes in contracts (Avg salary: $90k)",
            "Sports Broadcaster": "Commentate on sporting events (Avg salary: $70k)",
            "Sports Data Analyst": "Analyze player/team performance data (Avg salary: $85k)",
            "Esports Player": "Compete in video game tournaments (Avg salary: $60k+)",
            "Esports Coach": "Train competitive gaming teams (Avg salary: $50k)",
            "Sports Event Manager": "Organize sporting competitions (Avg salary: $65k)",
            "Sports Equipment Designer": "Develop athletic gear (Avg salary: $75k)",
            "Sports Medicine Physician": "Specialize in athlete healthcare (Avg salary: $200k)",
            "Sports Scout": "Identify and recruit talent (Avg salary: $55k)",
            "Fitness Influencer": "Create content about sports/fitness (Avg salary: $50k+)"
        },
        "questions": [
            "Do you prefer team sports or individual competition?",
            "Are you more interested in performance or health aspects?"
        ]
    },
    "business": {
        "keywords": ["finance", "accounting", "bookkeeping", "auditing", "taxation", "investment", "banking", "insurance",
                     "marketing", "advertising", "branding", "digital marketing", "social media", "seo", "content marketing",
                     "sales", "business development", "customer service", "retail", "ecommerce", "dropshipping", "affiliate",
                     "economics", "macroeconomics", "microeconomics", "econometrics", "public policy", "international trade",
                     "entrepreneurship", "startups", "venture capital", "angel investing", "crowdfunding", "small business",
                     "management", "leadership", "human resources", "recruiting", "training", "organizational development",
                     "operations", "supply chain", "logistics", "procurement", "inventory", "quality control", "six sigma",
                     "consulting", "strategy", "business analysis", "process improvement", "change management", "project management",
                     "real estate", "property management", "commercial real estate", "appraisal", "mortgage", "development"],
        "careers": {
            "Investment Banker": "Help companies raise capital (Avg salary: $150k)",
            "Financial Analyst": "Analyze financial data for decisions (Avg salary: $85k)",
            "Accountant": "Prepare and examine financial records (Avg salary: $70k)",
            "Marketing Manager": "Plan campaigns to attract customers (Avg salary: $135k)",
            "Digital Marketer": "Promote brands through digital channels (Avg salary: $80k)",
            "Sales Manager": "Lead sales teams to targets (Avg salary: $120k)",
            "Business Consultant": "Advise companies on improvement (Avg salary: $90k)",
            "Human Resources Manager": "Oversee employee relations (Avg salary: $110k)",
            "Operations Manager": "Optimize business processes (Avg salary: $95k)",
            "Supply Chain Analyst": "Improve logistics networks (Avg salary: $75k)",
            "Entrepreneur": "Start and grow businesses (Avg salary: Varies)",
            "Venture Capitalist": "Invest in promising startups (Avg salary: $150k+)",
            "Real Estate Developer": "Plan and execute property projects (Avg salary: $100k)",
            "Chief Executive Officer": "Lead entire organizations (Avg salary: $200k+)",
            "Data Analyst": "Interpret data for business decisions (Avg salary: $80k)"
        },
        "questions": [
            "Do you prefer working with numbers or people?",
            "Are you more interested in strategy or execution?"
        ]
    },
    "medical": {
        "keywords": ["medicine", "surgery", "pediatrics", "cardiology", "neurology", "oncology", "psychiatry", "radiology",
                     "dentistry", "orthodontics", "periodontics", "endodontics", "oral surgery", "dental hygiene",
                     "nursing", "registered nurse", "nurse practitioner", "nurse anesthetist", "midwifery", "clinical nurse",
                     "pharmacy", "pharmacology", "pharmaceuticals", "drug development", "clinical trials", "medicinal chemistry",
                     "psychology", "clinical psychology", "counseling", "therapy", "cognitive behavioral therapy", "neuropsychology",
                     "nutrition", "dietetics", "food science", "sports nutrition", "clinical nutrition", "public health nutrition",
                     "public health", "epidemiology", "biostatistics", "global health", "health policy", "environmental health",
                     "physical therapy", "occupational therapy", "speech therapy", "rehabilitation", "kinesiology", "exercise science",
                     "veterinary", "veterinary medicine", "animal health", "zoological medicine", "equine medicine", "wildlife medicine",
                     "biomedical", "biomedical engineering", "medical devices", "prosthetics", "medical imaging", "tissue engineering"],
        "careers": {
            "Physician": "Diagnose and treat medical conditions (Avg salary: $200k+)",
            "Surgeon": "Perform surgical procedures (Avg salary: $300k+)",
            "Psychiatrist": "Diagnose/treat mental health disorders (Avg salary: $220k)",
            "Dentist": "Diagnose/treat oral health issues (Avg salary: $180k)",
            "Registered Nurse": "Provide patient care in healthcare settings (Avg salary: $75k)",
            "Pharmacist": "Dispense medications and advise patients (Avg salary: $125k)",
            "Clinical Psychologist": "Assess and treat mental health (Avg salary: $90k)",
            "Nutritionist/Dietitian": "Advise on food/nutrition for health (Avg salary: $65k)",
            "Physical Therapist": "Help patients recover mobility (Avg salary: $90k)",
            "Biomedical Engineer": "Develop medical equipment/technology (Avg salary: $95k)",
            "Epidemiologist": "Study disease patterns (Avg salary: $80k)",
            "Physician Assistant": "Diagnose/treat under physician (Avg salary: $115k)",
            "Medical Researcher": "Conduct clinical/medical research (Avg salary: $90k)",
            "Veterinarian": "Diagnose/treat animal health issues (Avg salary: $100k)",
            "Healthcare Administrator": "Manage healthcare facilities (Avg salary: $110k)"
        },
        "questions": [
            "Do you prefer direct patient care or research work?",
            "Are you more interested in physical or mental health?"
        ]
    },
    "tech": {
        "keywords": ["video editing", "animation", "motion graphics", "visual effects", "compositing", "color grading",
                     "vr", "virtual reality", "ar", "augmented reality", "mixed reality", "xr", "metaverse",
                     "game development", "game design", "level design", "game programming", "game art", "game audio",
                     "3d modeling", "3d animation", "character modeling", "environment art", "texturing", "rigging",
                     "ui design", "ux design", "user experience", "user interface", "interaction design", "human-computer interaction",
                     "web design", "frontend development", "backend development", "full stack", "responsive design", "accessibility",
                     "mobile development", "ios development", "android development", "flutter", "react native", "cross-platform",
                     "it support", "system administration", "network administration", "database administration", "tech support", "help desk",
                     "embedded systems", "iot", "internet of things", "firmware", "arduino", "raspberry pi",
                     "technical writing", "documentation", "api documentation", "user manuals", "knowledge bases", "technical communication"],
        "careers": {
            "Game Developer": "Create video games (Avg salary: $85k)",
            "VR/AR Developer": "Build immersive experiences (Avg salary: $110k)",
            "Video Editor": "Edit footage for various media (Avg salary: $60k)",
            "VFX Artist": "Create visual effects for media (Avg salary: $80k)",
            "UX Designer": "Design user-centered interfaces (Avg salary: $95k)",
            "UI Designer": "Create visual interface elements (Avg salary: $85k)",
            "Technical Writer": "Create technical documentation (Avg salary: $75k)",
            "IT Manager": "Oversee technology infrastructure (Avg salary: $120k)",
            "Systems Administrator": "Maintain computer systems (Avg salary: $80k)",
            "Network Engineer": "Design/maintain networks (Avg salary: $90k)",
            "Database Administrator": "Manage database systems (Avg salary: $95k)",
            "Embedded Systems Engineer": "Develop specialized computing systems (Avg salary: $105k)",
            "IoT Solutions Architect": "Design connected device systems (Avg salary: $115k)",
            "Frontend Developer": "Build user-facing web components (Avg salary: $100k)",
            "Mobile App Developer": "Create smartphone applications (Avg salary: $105k)"
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
            #questions-section { display: none; }
            #submit-btn { display: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Career Recommendation System</h2>
            <form id="careerForm">
                <div id="initial-input">
                    <label for="user_input">What do you enjoy most?</label>
                    <input type="text" id="user_input" name="user_input" required 
                           placeholder="e.g. programming, graphic design, sports medicine">
                    <button type="button" id="next-btn">Next</button>
                </div>
                
                <div id="questions-section">
                    <div id="dynamic-questions"></div>
                    <button type="submit" id="submit-btn">Get Career Suggestion</button>
                </div>
                
                <div class="result" id="result" style="display:none;"></div>
            </form>
        </div>
        <script>
        document.getElementById('next-btn').addEventListener('click', async function() {
            const userInput = document.getElementById('user_input').value.trim();
            if (!userInput) {
                alert('Please enter what you enjoy most');
                return;
            }

            try {
                // Fetch the questions for this field
                const response = await fetch('./get-questions', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ user_input: userInput })
                });
                
                const data = await response.json();
                
                if (data.error) {
                    alert(data.error);
                    return;
                }
                
                // Display the questions
                const questionsDiv = document.getElementById('dynamic-questions');
                questionsDiv.innerHTML = '';
                
                data.questions.forEach((question, index) => {
                    const questionDiv = document.createElement('div');
                    questionDiv.innerHTML = `
                        <label for="answer${index}">${question}</label>
                        <input type="text" id="answer${index}" name="answer${index}" required>
                    `;
                    questionsDiv.appendChild(questionDiv);
                });
                
                // Show the questions section and submit button
                document.getElementById('initial-input').style.display = 'none';
                document.getElementById('questions-section').style.display = 'block';
                document.getElementById('submit-btn').style.display = 'block';
                
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred while fetching questions');
            }
        });

        document.getElementById('careerForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const user_input = document.getElementById('user_input').value;
            const answer0 = document.getElementById('answer0')?.value;
            const answer1 = document.getElementById('answer1')?.value;
            
            const resultDiv = document.getElementById('result');
            resultDiv.style.display = 'none';
            resultDiv.innerHTML = '';
            
            try {
                const response = await fetch('./suggest-career', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        user_input, 
                        answers: [answer0, answer1] 
                    })
                });
                const data = await response.json();
                
                if (data.error) {
                    resultDiv.innerHTML = `<b>Error:</b> ${data.error}`;
                } else {
                    resultDiv.innerHTML = `
                        <b>Field:</b> ${data.field}<br>
                        <b>Career:</b> ${data.career}<br>
                        <b>Because:</b> ${data.explanation}
                    `;
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

@app.post("/get-questions")
def get_questions(req: CareerRequest):
    field = get_field(req.user_input)
    if not field:
        return {"error": "Could not determine field from your interests. Please try being more specific."}
    
    return {
        "field": field,
        "questions": career_database[field]["questions"]
    }

@app.post("/suggest-career")
def suggest_career(req: CareerRequest):
    field = get_field(req.user_input)
    if not field:
        return {"error": "Could not determine field from user input."}
    if len(req.answers) < 2:
        return {"error": "Please provide answers for both questions."}
    career, explanation = get_career_suggestion(field, req.answers)
    return {
        "field": field,
        "career": career,
        "explanation": explanation
    }

# For local testing (not used by Vercel)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
from thefuzz import fuzz
import re,os
import requests
import logging
# Env variables local testing 
if  os.getenv("ENV") == "local":
    # Only load .env in local development
    from dotenv import load_dotenv

    load_dotenv()

app = FastAPI()

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with frontend URL for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Model
class ChatRequest(BaseModel):
    message: str

# Keyword-based response dictionary
keyword_responses = {
    # GREETINGS
    "hi": [
        "Hey there! Welcome to my portfolio. How can I assist you?",
        "Hello! Feel free to ask me about my experience, skills, or projects.",
        "Hi! I'm Solai, an AWS Cloud Engineer. Ask me anything about my work!",
        "Welcome! Need details about my experience, skills, or projects? Just ask!"
    ],
    "hello": [
        "Hello! I'm Solai, an AWS Cloud Engineer. How can I help you today?",
        "Hi there! Feel free to explore my portfolio and ask me anything.",
        "Hey! Want to know about my AWS projects or Terraform expertise?",
        "Welcome! Ask about my experience, projects, or skills!"
    ],

    # PERSONAL DETAILS
    "who are you": [
        "I'm Solai, an AWS Cloud Engineer with expertise in Terraform, Python, and cloud automation.",
        "I'm Solai Rajan, a cloud engineer specializing in AWS, GitLab CI/CD, and infrastructure as code.",
    ],
    "what is your name": [
        "I'm Solai Rajan, This is My chat bot Sol.AI you can ask my skills, experience, education, projects, resume",
        "I'm Solai Rajan, a cloud engineer specializing in AWS, GitLab CI/CD, and infrastructure as code.",
    ],
    "experience": [
        "I have over five years of experience in the IT industry, focusing on cloud engineering and automation with AWS, Terraform, Python, Pytest, BDD testing, and GitLab CI/CD.",
    ],
    "education": [
        "I am a BSc graduate with a strong foundation in cloud computing, DevOps, and software development.",
    ],
    "certifications": [
        "I'm certified AWS Solution Architect Associate and Microsoft Certified Azure Fundamentals."
    ],

    # TECHNICAL SKILLS
    "skills": [
        "My key skills include AWS, Terraform, Python, GitLab CI/CD, BDD, Pytest, and cloud automation."
    ],
    "aws": [
        "I have experience in AWS services like API Gateway, Lambda, DynamoDB, VPC, and more."
    ],
    "terraform": [
        "I use Terraform for infrastructure as code, automating AWS deployments with reusable modules."
    ],
    "python": [
        "I develop serverless applications and automation scripts using Python.",
        "I use Python for AWS Lambda functions, API development, and testing with Pytest.",
        "I implemented structured, modular Python code for API development and AWS automation."
    ],
    "gitlab": [
        "I have experience setting up GitLab CI/CD pipelines for automated Terraform deployments.",
        "I integrated security scans like Sync Scan and LabLooter into GitLab pipelines.",
        "I use GitLab runners to automate infrastructure provisioning and API deployments."
    ],
    "github": [
        "Find my GitHub projects at: [https://github.com/your-github-profile/](https://github.com/your-github-profile/)"
    ],
    # "docker": [
    #     "I’m currently improving my skills in Docker containerization.",
    #     "While I mainly work with AWS and Terraform, I'm also learning Docker for containerized deployments."
    # ],
    "tech": [
        "Favorite tech stack: AWS, Terraform, Python, GitLab CI/CD, and cloud automation."
    ],
    "devops": [
        "I follow DevOps best practices, automating CI/CD pipelines for cloud deployments.",
        "I have hands-on experience in infrastructure automation and cloud security."
    ],
    "cloud security": [
        "I implement security best practices like IAM policies, VPC security groups, and encryption.",
        "Cloud security is critical! I use AWS security tools and Terraform to enforce compliance."
    ],

    # PROJECTS
    "projects": [
        "I worked on mainframe-to-AWS modernization, DB2 to DynamoDB migration, and developed high-availability APIs. You can also check out my projects on my portfolio website: [https://solairajan.online/](https://solairajan.online/)"
    ],

    # CONTACT
    "contact": [
        "You can reach me via my website: [https://solairajan.online/](https://solairajan.online/), LinkedIn: [https://www.linkedin.com/in/solai-rajan/](https://www.linkedin.com/in/solai-rajan/), email: [solai13kamaraj@gmail.com](mailto:solai13kamaraj@gmail.com), and GitHub: [https://github.com/Solairajan18](https://github.com/Solairajan18)"
    ],
    "resume": [
        "You can find my resume on my website: [https://solairajan.online/](https://solairajan.online/) (click Download CV)."
    ],

    # FUN TOPICS
    "clash of clans": [
        "I play Clash of Clans and I'm currently at Town Hall 15., My favorite attack strategy is the Hybrid Army (Hog Riders + Miners). I often battle against TH16 opponents and adjust my strategy accordingly!"
    ],
    "hobbies": [
        "I enjoy gaming, learning new cloud technologies, and optimizing infrastructure deployments.",
        "Apart from tech, I like playing Clash of Clans and improving my attack strategies!"
    ],

    # GOODBYES
    "bye": [
        "Goodbye! Thanks for visiting my portfolio.",
        "See you soon! Feel free to reach out anytime.",
        "It was nice chatting with you. Have a great day!"
    ],
    "thanks": [
        "You're welcome! Let me know if you have any other questions.",
        "Glad to help! Feel free to explore my portfolio for more details."
    ]
}

# Default fallback responses
default_responses = [
    "I'm not sure how to respond to that. Try asking about my skills, projects, or experience!",
    "Can you clarify your question? You can ask about AWS, Terraform, or Python.",
    "That's interesting! You can ask me about my cloud expertise or GitLab experience.",
]

API_URL = 'https://openrouter.ai/api/v1/chat/completions'
DEEPSEEK_API_KEY=os.getenv("DEEPSEEK_API_KEY")
MODEL = 'deepseek/deepseek-r1:free'

def get_response(message: str):
    message = message.lower().strip()
    threshold = 70  # Adjust threshold for fuzzy matching

    # Self-introduction for identity-related queries
    identity_phrases = [
        "who are you", "what is your name", "your name", "are you a bot", "what are you"
    ]
    for phrase in identity_phrases:
        if fuzz.partial_ratio(phrase, message) >= threshold:
            return "**Hi there! I'm SolAI**, a friendly chatbot created by **Solai Rajan** to help you with portfolio questions, tech topics, or just to have a fun chat!"

    # Check if the user is asking about skills
    skill_phrases = [
        "what is your skill", "your primary skill", "your main skill",
        "what skills do you have", "tell me about your skills"
    ]
    for phrase in skill_phrases:
        if fuzz.partial_ratio(phrase, message) >= threshold:
            return "My key skills include AWS, Terraform, Python, Kubernetes, GitLab CI/CD, and cloud automation. Feel free to ask SolAI anything!"

    # Check if the user is asking about total experience using fuzzy matching
    experience_phrases = [
        "how many years", "years of experience", "total experience", "what's your experience", 
        "how much experience", "your work experience", "tell me your experience"
    ]
    for phrase in experience_phrases:
        if fuzz.partial_ratio(phrase, message) >= threshold:
            return "SolAI has a total of five years of experience in the IT Industry!"

    # Extract words from the user's message
    words = re.findall(r'\b[a-zA-Z0-9]+\b', message)

    # Identify unknown skills/technologies first
    experience_keywords = ["know", "experience", "familiar with", "worked with", "used", "do you use", "have you used"]
    detected_skill = None

    for exp_word in experience_keywords:
        if exp_word in message:
            exp_index = message.find(exp_word) + len(exp_word)
            potential_skills = message[exp_index:].strip().split()
            for word in potential_skills:
                word_cleaned = word.strip(".,?!")
                if word_cleaned and word_cleaned not in keyword_responses:
                    detected_skill = word_cleaned.capitalize()
                    break
            break

    if detected_skill:
        return f"No, SolAI doesn't have experience in {detected_skill}, but always eager to learn new things!"

    matched_responses = []
    for keyword, responses in keyword_responses.items():
        score = fuzz.partial_ratio(keyword, message)
        if score >= threshold:
            matched_responses.append(random.choice(responses))

    if matched_responses:
        return " ".join(matched_responses)

    # Friendly fallback for any unknown/casual chat
    casual_fallbacks = [
        "I'm SolAI! I love chatting about tech, hobbies, or anything on your mind. 😊",
        "SolAI here! If you want to talk about my portfolio, skills, or just have a casual chat, I'm all ears!",
        "Not sure I got that, but SolAI is always happy to chat! Ask me anything, professional or fun.",
        "SolAI can help with portfolio questions or just keep you company. What's up?"
    ]
    return random.choice(casual_fallbacks)



    
@app.post("/")
def chat(request: ChatRequest):
    user_message = request.message
    base_response = get_response(user_message)
    # Friendly, markdown, and only introduce as SolAI if asked
    prompt = (
        "You are SolAI, a super friendly AI chatbot created by Solai Rajan. "
        "Answer questions about Solai Rajan's portfolio, skills, experience, or have a casual, friendly conversation. "
        "Always respond in Markdown format, and keep the tone warm, helpful, and approachable. "
        "Only introduce yourself as SolAI, a chatbot created by Solai Rajan, if the user asks about your identity.\n\n"
        f"User: {user_message}\n"
        f"SolAI: {base_response}\n"
        "Now, reply to the user in Markdown as SolAI:"
    )
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are SolAI, a super friendly AI chatbot created by Solai Rajan. Answer questions about Solai Rajan's portfolio, skills, experience, or have a casual, friendly conversation. Always respond in Markdown format, and keep the tone warm, helpful, and approachable. Only introduce yourself as SolAI, a chatbot created by Solai Rajan, if the user asks about your identity."},
            {"role": "user", "content": prompt}
        ]
    }
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    try:
        llm_response = requests.post(API_URL, json=payload, headers=headers, timeout=10)

        llm_response.raise_for_status()
        data = llm_response.json()
        ai_reply = data.get("choices", [{}])[0].get("message", {}).get("content", base_response)
    except Exception as e:
        logging.getLogger("uvicorn.error").error(f"Error occurred: {e}")
        ai_reply = base_response
    return {"response": ai_reply}
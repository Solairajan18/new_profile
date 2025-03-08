from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

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
        "I have experience in AWS, Terraform, Python, Kubernetes, and GitLab CI/CD.",
        "I've worked on cloud modernization, API development, and infrastructure automation.",
        "I specialize in mainframe-to-AWS modernization, high-availability architectures, and CI/CD automation."
    ],
    "education": [
        "I have a strong foundation in cloud computing, DevOps, and software development.",
        "I continuously upskill in AWS, Terraform, and automation technologies.",
    ],
    "certifications": [
        "I'm certified in AWS Cloud technologies.",
        "I hold AWS certifications that validate my expertise in cloud architecture and infrastructure automation."
    ],

    # TECHNICAL SKILLS
    "skills": [
        "My key skills include AWS, Terraform, Python, Kubernetes, GitLab CI/CD, and cloud automation.",
        "I specialize in cloud architecture, API development, and infrastructure as code.",
        "I'm skilled in designing high-availability AWS architectures and automating deployments using Terraform."
    ],
    "aws": [
        "I have experience in AWS services like API Gateway, Lambda, DynamoDB, VPC, and more.",
        "I specialize in AWS cloud architecture, security best practices, and automation with Terraform.",
        "I have hands-on experience with AWS Transfer Service, S3, Glue, DynamoDB, and VPC Endpoints."
    ],
    "terraform": [
        "I use Terraform for infrastructure as code, automating AWS deployments.",
        "I build reusable Terraform modules and integrate them with GitLab CI/CD.",
        "I implemented Terraform automation for AWS, managing state files using Scalr."
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
        "You can check out my GitHub profile for code samples and projects.",
        "Find my GitHub projects at: [https://github.com/your-github-profile/](https://github.com/your-github-profile/)"
    ],
    "docker": [
        "I’m currently improving my skills in Docker containerization and Kubernetes orchestration.",
        "While I mainly work with AWS and Terraform, I'm also learning Docker for containerized deployments."
    ],
    "kubernetes": [
        "I'm learning Kubernetes for container orchestration and scaling microservices.",
        "I use Kubernetes for managing containerized workloads efficiently."
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
        "I worked on mainframe-to-AWS modernization, DB2 to DynamoDB migration, and high-availability APIs.",
        "Some of my key projects include building API Gateways with Lambda authorizers and Terraform-based AWS automation.",
        "I also worked on disaster recovery automation using Route 53 health checks and CloudWatch alarms.",
        "You can check out my projects on my portfolio website: [https://solairajan.online/](https://solairajan.online/)"
    ],

    # CONTACT
    "contact": [
        "You can reach me via my website: [https://solairajan.online/](https://solairajan.online/)",
        "Feel free to connect with me on LinkedIn! You can find my details on my portfolio website."
    ],
    "resume": [
        "You can find my resume on my website: [https://solairajan.online/](https://solairajan.online/)",
        "Check out my resume and projects on my portfolio page."
    ],

    # FUN TOPICS
    "clash of clans": [
        "I play Clash of Clans and I'm currently at Town Hall 15.",
        "My favorite attack strategy is the Hybrid Army (Hog Riders + Miners).",
        "I often battle against TH16 opponents and adjust my strategy accordingly!"
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

# Function to get responses for multiple keywords
def get_response(message: str):
    message = message.lower()
    matched_responses = []

    for keyword, responses in keyword_responses.items():
        if keyword in message:
            matched_responses.append(random.choice(responses))

    if matched_responses:
        return " ".join(matched_responses)

    return random.choice(default_responses)

# API Endpoint
@app.post("/")
def chat(request: ChatRequest):
    response = get_response(request.message)
    return {"response": response}
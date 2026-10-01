from dataclasses import dataclass

ROLE_MAP = {
    "Machine Learning Engineer": {
        "skills": ["Python", "SQL", "Statistics", "Machine Learning", "Git", "Model Deployment", "Projects"],
        "weights": {"Python":18,"SQL":10,"Statistics":10,"Machine Learning":20,"Git":7,"Model Deployment":15,"Projects":20}
    },
    "Python Backend Developer": {
        "skills": ["Python", "SQL", "REST APIs", "Git", "Django/FastAPI", "Testing", "Projects"],
        "weights": {"Python":20,"SQL":12,"REST APIs":12,"Git":8,"Django/FastAPI":18,"Testing":10,"Projects":20}
    },
    "Data Analyst": {
        "skills": ["Python", "SQL", "Statistics", "Excel/BI", "Data Visualization", "Git", "Projects"],
        "weights": {"Python":12,"SQL":20,"Statistics":15,"Excel/BI":10,"Data Visualization":15,"Git":8,"Projects":20}
    },
    "Full Stack Developer": {
        "skills": ["HTML/CSS", "JavaScript", "Python", "SQL", "REST APIs", "Git", "Projects"],
        "weights": {"HTML/CSS":10,"JavaScript":18,"Python":10,"SQL":12,"REST APIs":15,"Git":8,"Projects":27}
    },
    "Cloud / DevOps": {
        "skills": ["Linux", "Networking", "Git", "Docker", "Cloud", "CI/CD", "Projects"],
        "weights": {"Linux":15,"Networking":12,"Git":10,"Docker":15,"Cloud":18,"CI/CD":10,"Projects":20}
    }
}

ALIASES = {
    "ml": "Machine Learning", "machine learning basics": "Machine Learning",
    "machine learning": "Machine Learning", "api": "REST APIs", "apis": "REST APIs",
    "rest": "REST APIs", "django": "Django/FastAPI", "fastapi": "Django/FastAPI",
    "deployment": "Model Deployment", "linux administration": "Linux",
    "networking fundamentals": "Networking", "projects": "Projects",
    "project": "Projects", "sql database": "SQL"
}

def normalize(s):
    s = s.strip().lower()
    return ALIASES.get(s, s.title())


EXTENDED_ROLES = {
"Frontend Developer": ["HTML/CSS","JavaScript","React","Git","REST APIs","Testing","Projects"],
"Data Scientist": ["Python","SQL","Statistics","Machine Learning","Data Visualization","Git","Projects"],
"AI Engineer": ["Python","Machine Learning","Deep Learning","LLM/Generative AI","SQL","Git","Projects"],
"Data Engineer": ["Python","SQL","Data Modeling","ETL","Cloud","Git","Projects"],
"Cloud / DevOps Engineer": ["Linux","Networking","Git","Docker","Cloud","CI/CD","Projects"],
"Cybersecurity Analyst": ["Networking","Linux","Python","Cybersecurity Fundamentals","Security Tools","Git","Projects"],
"Mobile App Developer": ["Programming","Mobile Development","UI Development","APIs","Git","Testing","Projects"],
"QA / Test Engineer": ["Programming","Testing","Test Automation","SQL","APIs","Git","Projects"],
"UI/UX Designer": ["UI Design","UX Research","Figma","Design Systems","Prototyping","Communication","Portfolio"],
"Blockchain Developer": ["Programming","Blockchain Fundamentals","Smart Contracts","Web Development","Git","Security","Projects"],
"Business Analyst": ["SQL","Excel/BI","Data Analysis","Communication","Problem Solving","Documentation","Projects"]}
GENERIC_OTHER_ROLE={"skills":["Programming","Problem Solving","Communication","Domain Knowledge","Git","Projects"],"weights":{"Programming":20,"Problem Solving":20,"Communication":10,"Domain Knowledge":15,"Git":10,"Projects":25}}

class SkillPathAgent:
    """
    Lightweight, reproducible agentic prototype.
    It uses a planner + specialized tools rather than a static chatbot response.
    """

    def profile_analyzer(self, profile):
        skills = [normalize(x) for x in profile["skills"].split(",") if x.strip()]
        return {**profile, "skills": set(skills)}

    def role_requirements(self, target):
        if target in ROLE_MAP:
            data = ROLE_MAP[target]
            return {"skills": data["skills"], "weights": data["weights"]}
        if target in EXTENDED_ROLES:
            skills = EXTENDED_ROLES[target]
            weights_list = [15, 18, 15, 10, 10, 7, 25]
            return {"skills": skills, "weights": dict(zip(skills, weights_list))}
        return GENERIC_OTHER_ROLE

    def gap_analyzer(self, profile):
        target = self.role_requirements(profile["target"])
        gaps = []
        for skill in target["skills"]:
            if skill in profile["skills"]:
                current = "Known"
                priority = "Low"
            else:
                current = "Not demonstrated"
                priority = "High" if target["weights"][skill] >= 15 else "Medium"
            gaps.append({
                "skill": skill,
                "current": current,
                "target": "Demonstrate in project/interview",
                "priority": priority,
            })
        return gaps

    def score(self, profile):
        target = self.role_requirements(profile["target"])
        total = sum(target["weights"].values())
        earned = sum(
            weight for skill, weight in target["weights"].items()
            if skill in profile["skills"]
        )
        return round(100 * earned / total) if total else 0

    def roadmap_planner(self, profile, gaps):
        hours = profile["hours"]
        high = [g["skill"] for g in gaps if g["priority"] == "High"]
        med = [g["skill"] for g in gaps if g["priority"] == "Medium"]
        focus = high + med
        if not focus:
            focus = ["Interview practice", "Project depth"]
        themes = [
            ("Diagnose", "Close the most important foundation gap"),
            ("Learn", "Build one core skill with hands-on practice"),
            ("Build", "Apply the skill in a mini-project"),
            ("Integrate", "Connect tools and solve an end-to-end task"),
            ("Assess", "Take a timed technical assessment"),
            ("Portfolio", "Document project evidence and outcomes"),
            ("Review", "Interview simulation and next-step planning")
        ]
        plan = []
        for i, (day, theme) in enumerate(themes, 1):
            skill = focus[(i-1) % len(focus)]
            plan.append({
                "day": i, "focus": f"{theme}: {skill}",
                "time": hours,
                "actions": f"Spend {max(1, hours-1)} hr on {skill}; spend 1 hr on practical problem solving.",
                "deliverable": f"One tangible artifact: notes, solved problems, code commit, mini-feature, or assessment result."
            })
        return plan

    def assessment_tool(self, target):
        questions = {
            "Machine Learning Engineer": [
                {"question":"Why do we split data into training and test sets?","options":["To measure generalization","To increase labels","To remove all bias","To avoid using features"]},
                {"question":"Which metric is often useful for imbalanced classification?","options":["F1-score","Raw accuracy only","R-squared only","MAE only"]},
                {"question":"What is a practical deployment step after training a model?","options":["Expose a prediction API","Delete the model","Remove validation","Ignore monitoring"]}
            ],
            "Python Backend Developer": [
                {"question":"What is the purpose of a REST API?","options":["Enable resource-oriented communication","Compile Python","Design hardware","Replace SQL"]},
                {"question":"Why validate server-side input?","options":["Security and correctness","Increase font size","Reduce RAM to zero","Remove authentication"]},
                {"question":"What does Git primarily provide?","options":["Version control","Database hosting","CPU scheduling","DNS resolution"]}
            ]
        }
        return questions.get(target, [
            {"question":"What should a good project demonstrate?","options":["A real problem and measurable outcome","Only screenshots","Only theory","No documentation"]}
        ])

    def run(self, profile):
        p = self.profile_analyzer(profile)
        gaps = self.gap_analyzer(p)
        score = self.score(p)
        plan = self.roadmap_planner(p, gaps)
        assessment = self.assessment_tool(p["target"])

        high = [g["skill"] for g in gaps if g["priority"] == "High"]
        decision = (
            f"The agent identified {len(high)} high-priority gap(s) for the {p['target']} pathway. "
            f"It recommends focusing first on {', '.join(high[:3]) if high else 'project and interview readiness'}, "
            f"then validating progress through a practical assessment."
        )
        return {
            "readiness_score": score,
            "skill_gaps": gaps,
            "plan": plan,
            "assessment": assessment,
            "decision": decision,
            "daily_hours": p["hours"],
            "next_action": f"Start Day 1 now: work on the highest-priority gap and produce the day's deliverable before ending the session."
        }

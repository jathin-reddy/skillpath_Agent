# SkillPath Bharat — BharatAgentic Hackathon

## Category
EdTech & Future Skills

## Problem Statement
Students and early-career learners often know they need to become "placement ready" but do not know which skills to prioritize, what evidence to build, or what to do next. Generic learning platforms provide content, but they do not continuously diagnose an individual's gaps and convert those gaps into an actionable plan.

## Solution
SkillPath Bharat is an agentic learning and career-readiness assistant. It takes a learner profile, analyzes the target pathway, identifies skill gaps, prioritizes them, creates a short execution plan, generates a micro-assessment, and recommends the next action.

## Why it is agentic
The prototype is not only a chat interface. It executes a multi-step workflow:
1. Profile Analyzer — parses learner context and skills.
2. Gap Analyzer — compares current skills with target-role requirements.
3. Scoring Tool — calculates a reproducible readiness score.
4. Roadmap Planner — converts prioritized gaps into actions.
5. Assessment Tool — generates a role-specific micro-assessment.
6. Action Recommender — produces a concrete next step.

This demonstrates reasoning, decision-making, specialized tools, data/knowledge use, and an actionable outcome.

## Expected Impact
- Reduce time spent deciding what to learn next.
- Turn broad career goals into prioritized actions.
- Give learners measurable evidence of progress.
- Support workforce readiness for students with limited access to personalized mentoring.

## Prototype
Run locally:
```bash
pip install -r requirements.txt
streamlit run app.py
```

Open the displayed local URL.

## Docker
```bash
docker build -t skillpath-bharat .
docker run -p 8501:8501 skillpath-bharat
```

## Demo Script (2 minutes)
1. Select Machine Learning Engineer.
2. Enter skills such as Python, SQL, Git, Machine Learning basics.
3. Click Run SkillPath Agent.
4. Show readiness score and high-priority gaps.
5. Open the 7-day plan and show concrete deliverables.
6. Show the micro-assessment.
7. Explain the agent trace: INPUT → ANALYZE → GAP → PLAN → ASSESS → ACT.

## Hackathon alignment
The official brief asks for a meaningful problem, agentic solution, workflow showing input/reasoning/tools/data/outcome, impact, and a working prototype. This project is designed around those requirements.

## Submission note
The provided hackathon brief references a separate "aiKart Agent Manifest Guide" for the exact YAML manifest schema. That guide was not included in the supplied PDF, so this package does not invent a potentially invalid manifest schema. Use the official guide to create the final YAML manifest if Method 1 is selected.


## Latest Learner Input Updates
- Name starts blank and is entered by the learner.
- Current skills starts blank and is entered by the learner.
- Main goal starts blank and is entered by the learner.
- Education is selection-only unless `Other` is selected.
- Target pathway contains 15 predefined roles; custom career input appears only for `Other`.
- Available learning time is limited to 1–15 hours/day.

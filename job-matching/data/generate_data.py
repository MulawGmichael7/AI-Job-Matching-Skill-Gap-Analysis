"""
generate_data.py
-----------------
Generates a synthetic but realistic dataset of job postings and candidate
profiles for the AI-Based Job Matching & Skill Gap Analysis project.

Why synthetic data? Public job-posting datasets (Kaggle, scraped LinkedIn/
Indeed data) work great here too — this generator exists so the project is
fully reproducible offline. Swap `jobs.csv` / `candidates.csv` for a real
scraped dataset with the same column structure and everything downstream
still works unchanged.

Each candidate is generated with a hidden "target job" plus some skill
noise, which lets us honestly evaluate the matching pipeline later
(top-1 / top-3 accuracy) instead of just eyeballing results.
"""

import random
import csv

random.seed(42)

JOBS = {
    "Data Scientist": ["python", "pandas", "numpy", "scikit-learn", "sql", "statistics", "machine learning"],
    "Machine Learning Engineer": ["python", "tensorflow", "pytorch", "docker", "mlops", "sql", "machine learning"],
    "Data Analyst": ["sql", "excel", "python", "pandas", "data visualization", "statistics"],
    "Backend Developer": ["python", "django", "sql", "rest api", "docker", "git"],
    "Frontend Developer": ["javascript", "react", "css", "html", "git", "typescript"],
    "DevOps Engineer": ["docker", "kubernetes", "aws", "linux", "ci/cd", "git"],
    "Cybersecurity Analyst": ["network security", "python", "siem", "linux", "penetration testing", "sql"],
    "Cloud Engineer": ["aws", "azure", "docker", "kubernetes", "terraform", "linux"],
    "NLP Engineer": ["python", "nlp", "pytorch", "transformers", "machine learning", "sql"],
    "Computer Vision Engineer": ["python", "opencv", "pytorch", "cnn", "machine learning", "docker"],
    "Software QA Engineer": ["testing", "python", "selenium", "sql", "git", "ci/cd"],
    "Business Intelligence Analyst": ["sql", "power bi", "excel", "data visualization", "statistics"],
    "Embedded Systems Engineer": ["c++", "arduino", "microcontrollers", "python", "robotics"],
    "Full Stack Developer": ["javascript", "react", "python", "django", "sql", "git"],
    "Data Engineer": ["python", "sql", "spark", "airflow", "docker", "etl"],
}

ALL_SKILLS = sorted({s for skills in JOBS.values() for s in skills})

def make_candidate(cid):
    target_job = random.choice(list(JOBS.keys()))
    required = JOBS[target_job]
    # Candidate knows most (not all) of the target job's required skills
    known = set(random.sample(required, k=max(2, int(len(required) * random.uniform(0.55, 0.9)))))
    # Plus a bit of noise from unrelated skills (realistic — people have varied backgrounds)
    noise_pool = [s for s in ALL_SKILLS if s not in required]
    noise = set(random.sample(noise_pool, k=random.randint(0, 3)))
    skills = sorted(known | noise)
    return {
        "candidate_id": cid,
        "skills": "; ".join(skills),
        "true_target_job": target_job,  # kept only for evaluation, not used by the matcher
    }

def write_jobs_csv(path):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["job_id", "job_title", "required_skills"])
        for i, (title, skills) in enumerate(JOBS.items(), start=1):
            writer.writerow([i, title, "; ".join(skills)])

def write_candidates_csv(path, n=200):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["candidate_id", "skills", "true_target_job"])
        for i in range(1, n + 1):
            c = make_candidate(i)
            writer.writerow([c["candidate_id"], c["skills"], c["true_target_job"]])

if __name__ == "__main__":
    write_jobs_csv("data/jobs.csv")
    write_candidates_csv("data/candidates.csv", n=200)
    print("Generated data/jobs.csv and data/candidates.csv")

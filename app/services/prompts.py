ANALYZE_PROMPT = """
    Extract structured information from the following CV:
    "{text}"

    Output as JSON with fields: personal_info, education, work_experience, skills, projects, certifications, total_experience (in years). 
    Ensure total_experience is returned as a string, e.g., "5". If no total experience, return "0" as a string.
"""

QUERY_PROMPT = """
    You are an AI assistant that converts recruiter queries into MongoDB JSON filters.
    Convert the following user query into a MongoDB query:
    "{user_query}"

    Ensure the query can handle various aspects like:
    - Finding candidates with specific skills (match `skills`, including nested fields inside skills like `skills.Programming Languages`, `skills.Web Frameworks`, etc.)
    - Searching for experience in specific industries (match `work_experience` and `industry` fields)
    - Comparing education levels (match `education.degree`, `education.school`, and `education.GPA` fields)
    - Identifying matching candidates for job requirements (match `job_requirements`, `skills`, and `certifications` fields)

    If the query mentions a skill (e.g., "FastAPI"), search for:
      - Direct matches in `skills`
      - Matches inside subcategories of `skills`, such as `skills.Web Frameworks`
      - Matches in `work_experience`

    Ensure that the output is structured as a valid MongoDB query using `$or` and `$elemMatch` when necessary.
    Output only valid JSON without explanations.
"""

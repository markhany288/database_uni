from groq import Groq

# 🔑 حط المفتاح مباشرة (زي ما طلبت)
client = Groq(api_key="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")

def ask_grok_sql(user_question):

    schema_context = """
    Database: ELearningDB3

    Tables:
    Students1       (StudentID, FullName, Email, Phone, RegistrationDate)
    Instructors1    (InstructorID, FullName, Email, Bio)
    Categories1     (CategoryID, CategoryName)
    Languages1      (LanguageID, LanguageName)
    Levels1         (LevelID, LevelName)
    Courses1        (CourseID, Title, Description, Price, CategoryID, InstructorID, LanguageID, LevelID)
    CourseContents1 (ContentID, CourseID, Title, ContentType, OrderNo)
    Enrollments1    (EnrollmentID, StudentID, CourseID, EnrollmentDate, ProgressPercent)
    Assignments1    (AssignmentID, CourseID, Title, MaxScore)
    StudentGrades1  (GradeID, StudentID, AssignmentID, ScoreObtained)
    Reviews1        (ReviewID, StudentID, CourseID, Rating, Comment)
    Certificates1   (CertificateID, EnrollmentID, IssueDate)
    SupportTickets1 (TicketID, StudentID, Subject, Status)

    Relationships:
    - Courses1.CategoryID   → Categories1.CategoryID
    - Courses1.InstructorID → Instructors1.InstructorID
    - Courses1.LanguageID   → Languages1.LanguageID
    - Courses1.LevelID      → Levels1.LevelID
    - Enrollments1.StudentID → Students1.StudentID
    - Enrollments1.CourseID  → Courses1.CourseID
    - StudentGrades1.StudentID    → Students1.StudentID
    - StudentGrades1.AssignmentID → Assignments1.AssignmentID
    - Reviews1.StudentID → Students1.StudentID
    - Reviews1.CourseID  → Courses1.CourseID
    - Certificates1.EnrollmentID → Enrollments1.EnrollmentID
    - SupportTickets1.StudentID  → Students1.StudentID
    """

    system_prompt = f"""
    You are a professional SQL Server expert.

    RULES:
    - Use ONLY the tables provided
    - ALL table names MUST end with '1'
    - Use correct JOINs based on relationships
    - Use SQL Server syntax (TOP, ISNULL, etc.)
    - DO NOT invent columns or tables
    - Generate ONLY SELECT queries

    Schema:
    {schema_context}

    Output format MUST be exactly:

    ---SQL---
    [Your SQL query here]
    ---END_SQL---
    [شرح بالعربي]
    """

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question},
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.0
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"


# 🔍 استخراج الكويري
def extract_sql(response):
    try:
        return response.split("---SQL---")[1].split("---END_SQL---")[0].strip()
    except:
        return None


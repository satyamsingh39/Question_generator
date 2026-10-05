
prompt_template = """
    You are an expert at creating questions based on educational and technical materials.
    Your goal is to prepare learners with high quality practice questions.

    Generate questions of the following type: {question_type}
    Difficulty level: {difficulty}

    Instructions based on Question Type:
    - If question type is "MCQ": Provide multiple-choice questions. Format each question clearly on a single line or as a distinct question item with 4 distinct options (A, B, C, D).
    - If question type is "Short Answer": Provide clear, concise conceptual questions that require a brief explanation or answer.
    - If question type is "True/False": Provide clear statements and ask whether the statement is True or False.

    Text to base questions on:
    ------------
    {text}
    ------------

    Create questions matching the requested difficulty ({difficulty}) and format ({question_type}).
    Make sure not to lose any important information.
    Provide each question ending with a question mark (?) or period (.).

    QUESTIONS:
    """


refine_template = ("""
    You are an expert at creating practice questions based on coding material and documentation.
    Your goal is to help a coder or programmer prepare for a coding test.
    We have received some practice questions to a certain extent: {existing_answer}.
    We have the option to refine the existing questions or add new ones.
    (only if necessary) with some more context below.
    ------------
    {text}
    ------------

    Given the new context, refine the original questions in English.
    If the context is not helpful, please provide the original questions.
    QUESTIONS:
    """
    )
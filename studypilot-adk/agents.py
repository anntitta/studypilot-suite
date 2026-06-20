from google.genai import types
import pydantic
from config import client, MODEL_ID

# 🎯 Structured Pydantic Schemas for Interactive Frontend Engines
class QuizQuestion(pydantic.BaseModel):
    question: str
    options: list[str]
    correct_answer_index: int  
    explanation: str

class QuizPayload(pydantic.BaseModel):
    quiz_title: str
    questions: list[QuizQuestion]

# 🌟 Structured Schema for Flashcards
class FlashcardItem(pydantic.BaseModel):
    front_side: str  # The question or clue phrase (with an emoji!)
    back_side: str   # The simplified kid-friendly answer

class FlashcardPayload(pydantic.BaseModel):
    deck_title: str
    cards: list[FlashcardItem]


def prepare_multimodal_contents(user_query: str, image_bytes: bytes, mime_type: str):
    """Packs raw text prompts and visual image graphics together cleanly for the SDK."""
    contents = []
    if image_bytes and mime_type:
        contents.append(
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=mime_type,
            )
        )
    contents.append(user_query)
    return contents


def notes_agent(user_query: str, image_bytes: bytes = None, mime_type: str = None) -> str:
    """[The Research Assistant] Compiles structured summaries and key terms."""
    print("📸 [Vision Agent] -> Activating Smart Hybrid Notes Agent...")
    instruction = """
    You are a friendly space-tiger study assistant. Summarize the user text or image provided.
    Format strictly using these headers:
    # 🗺️ THE HIGH-LEVEL MAP
    [Simple topic summary here]
    # 🔑 SUPER-IMPORTANT SECRET WORDS
    [Bullet points with bold definitions and emojis]
    """
    contents = prepare_multimodal_contents(user_query, image_bytes, mime_type)
    response = client.models.generate_content(
        model=MODEL_ID, contents=contents, config=types.GenerateContentConfig(system_instruction=instruction)
    )
    return response.text


def qa_agent(
    user_query: str,
    image_bytes: bytes = None,
    mime_type: str = None,
    vector_context: str = ""
) -> str:
    """[The Subject Matter Expert] Strictly answers questions using visible evidence."""
    print("📸 [Vision Agent] -> Activating Contextual Academic Q&A Agent...")
    instruction = f"""
You are an academic tutor.

Use the study material below as your PRIMARY source.

Study Material:
{vector_context}

Answer the student's question accurately.

If the answer cannot be found in the study material,
say:

'I could not find that information in the uploaded study materials.'
"""
    contents = prepare_multimodal_contents(user_query, image_bytes, mime_type)
    response = client.models.generate_content(
        model=MODEL_ID, contents=contents, config=types.GenerateContentConfig(system_instruction=instruction)
    )
    return response.text


def quiz_agent(user_query: str, image_bytes: bytes = None, mime_type: str = None) -> str:
    """[The Examiner] Generates structured step-by-step interactive JSON quizzes."""
    print("📸 [Vision Agent] -> Activating Structured Quiz Engine...")
    instruction = """
    You are a friendly space-tiger quiz host. Generate exactly 3 multiple-choice questions for kids.
    Provide a clear, brief explanation for the correct answer.
    """
    contents = prepare_multimodal_contents(user_query, image_bytes, mime_type)
    response = client.models.generate_content(
        model=MODEL_ID, contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=instruction,
            response_mime_type="application/json",
            response_schema=QuizPayload
        )
    )
    return response.text


def explainer_agent(user_query: str, image_bytes: bytes = None, mime_type: str = None) -> str:
    """[The Simple Explainer] Breaks down complex text/images into varied, kid-friendly stories."""
    print("📸 [Vision Agent] -> Activating Kid-Friendly Simple Explainer Agent...")
    
    instruction = """
    You are the Kid-Friendly Simple Explainer Agent, a warm and encouraging space-tiger mentor. 
    Look closely at the attached image or text prompt.
    Your mission is to explain what is happening in the image using incredibly simple words, 
    fun real-world analogies, and zero confusing academic jargon. 
    Imagine you are explaining it to an eager 7-year-old child!
    
    CRITICAL INSTRUCTION FOR VARIETY: 
    Do NOT default to 'playground' or 'sandbox' analogies unless the image is literally about a playground. 
    Instead, dynamically select an analogy that fits the context of the topic best:
    - For data networks, computers, or systems: Use amusement parks, highway traffic, or delivery truck fleets.
    - For science, biology, or nature: Use superhero teams, baking a complex cake, or magical castle kingdoms.
    - For history, community, or organizations (like the UN): Use a school student council, a giant group project, or an international space station crew working together.
    
    Structure your output response strictly using these exact headers:
    # 🧸 THE BIG PICTURE STORY
    [Explain the core concept here using your chosen dynamic, topic-appropriate analogy]
    # 🍕 BREAKING IT DOWN IN BITE-SIZED CHUNKS
    [Provide 3-4 bullet points explaining the different parts of the image using very simple language and matching theme analogies]
    # 💡 WHY IT MATTERS TO YOU!
    [Explain why learning this topic is useful or cool for a kid in daily life]
    """
    
    contents = prepare_multimodal_contents(user_query, image_bytes, mime_type)
    response = client.models.generate_content(
        model=MODEL_ID, contents=contents,
        config=types.GenerateContentConfig(system_instruction=instruction)
    )
    return response.text


# 🌟 THE MISSING LINK: THE FLASHCARD HERO AGENT
def flashcard_agent(user_query: str, image_bytes: bytes = None, mime_type: str = None) -> str:
    """[The Flashcard Hero] Extracts study terminology into structured active-recall cards."""
    print("📸 [Vision Agent] -> Activating JSON Flashcard Generation Engine...")
    
    instruction = """
    You are a friendly space-tiger study card creator. Read the attached textbook page or study concept.
    Extract exactly 4-5 core keywords, definitions, or essential historical fast-facts.
    
    Package them into simplified front-and-back flashcard objects built perfectly for kids:
    - front_side: A clean question or clue prompt phrase accompanied by an awesome matching emoji.
    - back_side: A short, simple, 1-sentence answering explanation revealing what that term means.
    """
    contents = prepare_multimodal_contents(user_query, image_bytes, mime_type)
    response = client.models.generate_content(
        model=MODEL_ID, contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=instruction,
            response_mime_type="application/json",
            response_schema=FlashcardPayload
        )
    )
    return response.text
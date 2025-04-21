import asyncio

from PIL import Image
from PIL import UnidentifiedImageError

from config import get_model
from static.string_file import CallLLMStrings


# Initialize the model
model = get_model()


def process_memory_query(user_text: str, history_context: str) -> str:
    """
    Process a memory-related query using conversation history and return a response.

    Args:
        user_text: The user's memory-related query (e.g., "What does the second image of the last chat describe?").
        history_context: Formatted conversation history string from expand_conversation_history.

    Returns:
        A plain text response based on the history and query.
    """
    memory_prompt = (
        f"{CallLLMStrings.MEMORY_PROMPT_HISTORY_HEADER}\n"
        f"{history_context}\n\n"
        f"{CallLLMStrings.MEMORY_PROMPT_USER_QUERY.format(user_text=user_text)}\n\n"
        "Instructions:\n"
        f"{CallLLMStrings.MEMORY_PROMPT_INSTRUCTIONS}"
    )
    try:
        response = model.generate_content([memory_prompt])
        response_text = response.text.strip()
        print(f"Memory response: {response_text}")
        return response_text
    except Exception as error:
        return CallLLMStrings.MEMORY_ERROR_RESPONSE.format(error=error)


async def description(path: str) -> str:
    """Generate a detailed description and tags for an image from a file path."""
    try:
        prompt = CallLLMStrings.DESCRIPTION_PROMPT
        image = Image.open(path)
        await asyncio.sleep(4)  
        response = model.generate_content([prompt, image])
        print(response.text)
        return response.text
    except FileNotFoundError:
        return CallLLMStrings.FILE_NOT_FOUND_ERROR.format(path=path)
    except UnidentifiedImageError:
        return CallLLMStrings.INVALID_IMAGE_ERROR.format(path=path)
    except Exception as error:
        return CallLLMStrings.UNEXPECTED_ERROR.format(error=error)


def description_image(image: Image.Image) -> str:
    """Generate a short description for a given image object."""
    try:
        prompt = CallLLMStrings.DESCRIPTION_IMAGE_PROMPT
        response = model.generate_content([prompt, image])
        print(response.text)
        return response.text
    except FileNotFoundError:
        return CallLLMStrings.DESCRIPTION_IMAGE_NOT_FOUND_ERROR.format(image=image)
    except UnidentifiedImageError:
        return CallLLMStrings.DESCRIPTION_IMAGE_INVALID_ERROR.format(image=image)
    except Exception as error:
        return CallLLMStrings.UNEXPECTED_ERROR.format(error=error)


def general_chat(user_query: str, history_context = None) -> str:
    """Process a general chat query and return an appropriate response."""
    try:
        prompt = CallLLMStrings.GENERAL_CHAT_PROMPT
        if history_context:
            full_prompt = prompt.format(history_context=history_context)
        else:
            full_prompt = prompt.format(history_context=CallLLMStrings.UNAVAILABLE_HISTORY_CONTEXT)
        response = model.generate_content([full_prompt, user_query])
        print(response.text)
        return response.text
    except Exception as error:
        return CallLLMStrings.UNEXPECTED_ERROR.format(error=error)
    
    
    

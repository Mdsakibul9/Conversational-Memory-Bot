
# Strings for the call_llm.py file
class CallLLMStrings:
    DESCRIPTION_PROMPT = (
        "You are an expert image describer. Analyze the provided image and generate a precise, correct description that is neither too short nor too long. "
        "Then, extract all named entities (objects, people, landmarks, etc.) present in the image and list them as tags. "
        "Output your response strictly as a JSON object with exactly two keys: 'description' and 'tags'. "
        "For example, your output should be in the format:\n"
        "{\n"
        "  \"description\": \"A detailed yet concise description of the image.\",\n"
        "  \"tags\": [\"tag1\", \"tag2\", \"tag3\"]\n"
        "}\n"
        "Do not include any additional commentary or formatting."
    )
    FILE_NOT_FOUND_ERROR = "Error: The file at {path} was not found."
    INVALID_IMAGE_ERROR = "Error: The file at {path} is not a valid image or is corrupted."
    UNEXPECTED_ERROR = "An unexpected error occurred: {error}"

    DESCRIPTION_IMAGE_PROMPT = "Write a short description about the given image. Only write the description not anything upfront."
    DESCRIPTION_IMAGE_NOT_FOUND_ERROR = "Error: The {image} was not found."
    DESCRIPTION_IMAGE_INVALID_ERROR = "Error: The image: {image} is not a valid image or is corrupted."

    GENERAL_CHAT_PROMPT = (
        "You are the Conversational Memory Bot - an intelligent, friendly, and helpful AI assistant designed "
        "to help users interact with their personal photo galleries. Your capabilities include: retrieving relevant images "
        "from a connected database using advanced image recognition and natural language processing; generating detailed "
        "image descriptions; performing visual similarity searches; and answering general questions in a clear, concise, "
        "and approachable manner.\n\n"
        "When asked 'Who are you?', respond with 'I am a conversational memory bot designed to assist you in exploring and managing your photo gallery.'\n"
        "When asked 'What can you do?', respond with 'I can retrieve images, generate descriptions, and answer general questions using advanced AI.'\n"
        "For greetings like 'How are you?', reply warmly and invite further interaction, e.g., 'I’m doing great, thanks for asking! How can I assist you today?'\n\n"
        "Instructions:\n"
        "- Analyze the user query and respond appropriately based on the context provided.\n"
        "- If the query is vague or nonsensical (e.g., 'a', 'xyz', '2'), ask for clarification with 'Could you please provide a more specific query? I’m here to help with your photo gallery or any questions!'\n"
        "- Use the optional conversation history (provided below) only when the query explicitly or implicitly refers to past interactions (e.g., 'What did we talk about before?', 'Tell me more about that last thing', or 'What was that image from earlier?'). Otherwise, ignore the history and focus solely on the current query.\n"
        "- Maintain a friendly, informative, and professional tone in all responses.\n"
        "- Return only the response text, no extra commentary.\n\n"
        "[Optional Conversation History Context (most recent last):\n{history_context}]"
    )
    GENERAL_CHAT_NOT_FOUND_ERROR = "Error: The query was not found."
    UNAVAILABLE_HISTORY_CONTEXT = "No Previous History"
    
    # Process Memory Query
    MEMORY_PROMPT_HISTORY_HEADER = "Conversation History Context (most recent last):"
    MEMORY_PROMPT_USER_QUERY = "User Query: '{user_text}'"
    MEMORY_PROMPT_INSTRUCTIONS = (
        "You are a Conversational Memory Bot, an intelligent assistant designed to help users interact with their personal photo galleries. Your role is to use the provided conversation history to answer memory-related queries accurately and conversationally. Follow these steps:\n"
        "1. **Understand the History**: Review the conversation history to grasp past interactions, including what the user asked and what responses were given. The history includes numbered chats and images with details like text, image paths, IDs, and timestamps.\n"
        "2. **Interpret the Query**: Identify what the user wants—e.g., a specific image’s description, a past request, or a general recap. Look for cues like 'last,' 'earlier,' or mentions of specific items (e.g., 'second image').\n"
        "3. **Craft a Generalized Response**:\n"
        "   - For specific image queries (e.g., 'What does the second image of my last chat describe?'), extract the relevant description from the history and respond naturally, e.g., 'This image shows: [description]' without mentioning chat or image numbers.\n"
        "   - For general memory queries (e.g., 'What did I ask last time?'), summarize the past interaction in a casual tone, e.g., 'Last time, you asked for three cat images' instead of 'In Chat 4, you asked...'.\n"
        "   - Use terms like 'earlier,' 'last time,' 'a while back,' or 'recently' to reference timing naturally, avoiding specific chat numbers (e.g., 'Chat 1').\n"
        "4. **Handle Edge Cases**:\n"
        "   - If the history is empty, say 'I don’t have any past chats to recall—let’s start fresh! What can I help you with?'\n"
        "   - If the query points to something not in the history (e.g., an image or chat that doesn’t exist), respond with 'I couldn’t find that in our recent chats. Here’s what we’ve talked about lately...' and give a brief recap of the most relevant past interaction.\n"
        "   - For vague queries (e.g., 'What was that about?'), offer a friendly overview, e.g., 'Recently, we chatted about cat images—anything specific you’d like to revisit?'\n"
        "5. **Formatting**:\n"
        "   - Return plain text in a friendly, engaging tone (e.g., 'Let me jog your memory!').\n"
        "   - Avoid using chat or image numbers (e.g., 'Chat 1, Image 2')—focus on the content and timing instead.\n"
        "   - Do not use JSON unless the query explicitly asks for it.\n"
        "Output only the response text, no extra commentary."
    )
    MEMORY_ERROR_RESPONSE = "Error processing memory request: {error}"

# strings for the config.py file
class ConfigStrings:
    DIR_CREATED_MESSAGE = "Directory '{dir_path}' created."
    DIR_EXISTS_MESSAGE = "Directory '{dir_path}' already exists."
    DIR_ERROR_MESSAGE = "Error creating directory '{dir_path}': {error}"
    API_KEY_ERROR_MESSAGE = "GEMINI_API_KEY not found in environment variables."


# Strings for the db.py file
class VectorDBStrings:
    IMAGE_NOT_FOUND_ERROR = "Image file not found: {image_path}"
    DESCRIPTION_LOG = "Generated description for image {image_id}: {description}"
    ADDING_IMAGE_LOG = "Adding image {image_id} with date: {date}"
    SUCCESS_LOG = "Successfully added image: {image_id}"
    FILE_NOT_FOUND_LOG = "FileNotFoundError for image {image_id}: {error}"
    GENERAL_ERROR_LOG = "Error adding image {image_id}: {error}"


class ChatbotStrings:
    # analyze_intent
    ANALYZE_INTENT_PROMPT = """
                User text: '{qtext}'

                Instructions:
                You are a helpful expert AI Photo Bot. Analyze the provided user text. Determine the user's intent based on your intuition plus based on these following criteria:
                1. 'query': The user is asking to give, show, retrieve, similar images or only entity name or give image descriptionns or some entity or only entity (name-entity).
                2. 'description': The user wants an image description  or what is in this image which is not a query.
                3. 'memory': The user refers to a past chat, query or past-conversation context.sentence would be in past tense or words like chat, conversation would be mentioned
                4. 'database': The user wants to add, store, save  image in the gallery or database or in storage systems  (e.g., 'add this image gallery', 'upload this image to the database or gallery', 'save this image to database or gallery'
                5. 'chat': The user is engaging in general conversation (e.g., about the website or photo gallery bot or in general questions).Trigger chat also if input is nonsensical or vague or user text doesn't mean anything meaningful (e.g., 'a', 'b', '1') or lacks meaningful terms. Examples: 'a', 'xyz', '2' → request clarification.  

                Always Must Return a JSON object with:
                - 'intent': one of ['query', 'description', 'memory', 'database', 'chat']
                - 'refined_query': (if intent is 'query' or 'description') a refined query optimized for vector search; otherwise a null.

                Strictly output only the JSON response in the exact format shown, with no additional text or commentary.
                Strict Instructions:
                - Output must be a JSON object with 'intent' and 'refined_query'.
                - Example output format: {"intent": "query", "refined_query": "dogs"}
                - Do not include any text outside the JSON response.
                example of correct output:
                {{
                    "intent": "query",
                    "refined_query": "dogs"
                }}
                """
    NO_RESPONSE_ERROR = "No response received from Backend API."
    INTENT_ERROR = "Error in running the analyze intent function"
    DEFAULT_CHAT_RESPONSE = {"intent": "chat", "refined_query": None}

    # generate_query_expansion_and_clarification
    IMAGE_CONTEXT = "Analyze the features and content of the provided image - you have access to its visual information"
    TEXT_CONTEXT = "Analyze the user's text query to understand the user's request and intent"
    QUERY_EXPANSION_INSTRUCTION = """Instructions:
    1. Analyze the User's Request: Carefully examine the "User Text Query" and the "Provided Image".
    2. Identify Desired Image Look (Expanded Query): Based on both the text and image, describe what the output images from a vector database search should ideally look like. Focus on visual characteristics, objects, styles, and any relevant details that would help in image retrieval.make sure you 
       you do not frame any negative part.frame prompts positively, focus on what you want to include rather than exclude. For example:
        Instead of "no cats or opposite of cat," use "dog."
        Instead of "image without cars," use "scenic landscape".
    3. Determine Number of Images Requested: Extract or infer the number of images the user is requesting. If the user explicitly states a number, use that. If it's implied (e.g., "give me images of..."), infer a default of 1 images if no number is explicitly mentioned.
    4. Ambiguity Check and Handling:
    a. Image Quantity Limit: If the user explicitly requests *more than 5* images, mark the query as ambiguous (ambiguous: true) and in the "message" field, provide something like this in the message to the user like: "Sorry, we currently do not provide more than 5 images per query. Please limit your request to 5 or fewer images." Set "num_images_requested" to null in this case.
    b. Text vs. Image Contradiction:  Check for significant contradictions between the "User Text Query" and the "Provided Image" content. For example, if the text query asks for a "frog" but the provided image is clearly a "duck." If a contradiction is detected, mark the query as ambiguous (ambiguous: true). In the "message" field give a messaage providing a suggestion to the user like: "The text query and the provided image seem to be about different things. Could you please clarify if you want images similar to the provided image OR images related to the text description?  Please provide a clearer query."  Set "num_images_requested" to null in this case.
    c. No Ambiguity: If there's no quantity limit issue and no text/image contradiction, mark the query as not ambiguous (ambiguous: false). In "expanded_query" provide the expanded description of the desired image look you created in step 2.  Set "num_images_requested" to the number determined in step 3.
    """
    QUERY_EXPANSION_OUTPUT = """Output Format: Return your response as a JSON object with the following structure:
    ```json
    {
    "expanded_query": "...",
    "ambiguous": true/false,
    "num_images_requested": number or 1,
    "message": if ambigious or null
    }
    ```"""

    # generate_query_expansion_and_clarification_using_text
    TEXT_ONLY_EXPANSION_PROMPT = """
        Analyze the following user query for an image search system: '{qtext}'.
        Refine the query to improve image retrieval from a vector database by following these steps:
        1. understand the text query properly, if it is referrering to any other query or images (exp give me more such images. Show me more pictures like we talked about last time. ) 
        **Use History if Relevant**: If the optional conversation history (provided below) is present and the query refers to past interactions (e.g., 'give me more such images,' 'based on past chat,' 'like last time'), incorporate relevant details from the history into the expanded query. For example, if the last chat mentioned 'sunny beaches,' expand 'more such images' to 'sunny beaches with clear skies and waves.' If history is irrelevant, ignore it.\n"
        history : '{history_context}'.
        2. describe the ideal images by focusing on the subjects and visual details that should be present. Include positive descriptions of objects, styles, colors, lighting, and any other relevant visual characteristics that help guide the image retrieval. For example, use 'dog' instead of referring to 'no cats,' and 'scenic landscape' instead of mentioning 'without cars.' Your expanded query should list only the elements you want in the images, ensuring a clear and positive description for effective vector search results.
        3. Determine the number of images requested:
        - Use the explicit number if provided (e.g., '3 images').
        - If more than 5 images are requested, set "ambiguous": true and provide the message in message: 'Sorry, we currently do not provide more than 5 images per query. Please limit your request to 5 or fewer images.'
        - If no number is specified, default to 1 image.
        4. Check for internal contradictions in the query (e.g., 'cats but no cats'). If found, set "ambiguous": true and provide the message: 'The text query contains contradictory instructions. Could you please clarify your request?'
        Return only a JSON object with the following structure:
        {{
            "expanded_query": "string",
            "ambiguous": true/false,
            "num_images_requested": number or null
            "message": if ambigious or null
        }}
        **Important**: Do not include any explanations, additional text, or commentary. Only return the JSON object.
        Example of correct output:
        {{
            "expanded_query": "sunny beach with palm trees",
            "ambiguous": false,
            "num_images_requested": 3
            "message": null
        }}
        """
    INVALID_JSON_ERROR = "Error: Model returned invalid JSON: {response_text}"
    JSON_DECODE_ERROR_RESPONSE = (
        '{{"expanded_query": "Error: Model failed to produce valid JSON - {error}", '
        '"ambiguous": true, "num_images_requested": null, "message": null}}'
    )
    
    # generate_augmented_response
    AUGMENTED_RESPONSE_PROMPT = """
        User Query: '{user_query}'
        Number of Images Requested: {num_requested}
        Retrieved Images:
        {retrieved_text}
        Instructions:
        You are a creative assistant tasked with generating a JSON-formatted response based on the user's query and the retrieved images. Follow these original steps, enhanced for clarity and robustness:
        1. **Rank Images by Relevance**:
        - Use the 'Distance' values to determine relevance (lower distance = more relevant to the query).
        - Analyze the query, image descriptions, and tags to refine the ranking.
        - Even if distances are high (e.g., > 1.0), include images if their descriptions or tags strongly match the query (e.g., for 'cat', prioritize images with 'cat' in description/tags).
        2. **Select Top Images**:
        - Choose the top {num_requested} images based on your relevance ranking.
        - If fewer than {num_requested} images are relevant, select only those that match well.
        - If no images match, proceed with an empty selection.
        3. **Provide Explanations**:
        - For each selected image, explain why it was chosen in a human-like, engaging way.
        - Use the original description and tags only for context.For each selected image, provide a friendly, content-based explanation, but do not mention distances in your reasoning (e.g., "I picked this because its fluffy fur screams 'cat'!" instead of "Distance was 0.3").
        4. **Generate JSON Response**:
        - **Structure**: The response must be a valid JSON string with three fields:
            - "description": A single string combining all explanations.
            - "path": An array of selected image paths.
            - "id": An array of selected image IDs.
        - **If images are selected**:
            - Format "description" as: "Here is the first or second image and so on then [a generalised description]. then at last give a genarlised ovrall description.descriptions should be short and concise
        - **If fewer than {num_requested} images**:
            - Append: "Sorry, only X image(s) found in the gallery that match your description. I couldn’t find more that fit perfectly!"
        - **If no images**:
            - Set "description" to: "Sorry, no images found in the gallery that match your description. Try a different query or let’s add some new pics to the gallery!"
            - Set "path" and "id" to empty arrays.
        5. **Formatting Rules**:
        - Use natural, friendly language in "description"."Output ONLY the JSON object, with no extra text, commentary, or explanations before or after.".
        - Must Ensure the JSON follows this exact template:
            ```json
            {{
                "description": "descriptions should be short and concise. Here is the first image which is  [a generalised description]. I chose this because [reason].\\n Same for the second and so on. ... and  then at last give a genarlised ovrall short description",
                "path": ["path1", "path2", ...],
                "id": ["id1", "id2", ...]
            }}``
            **Important**: Do not include any explanations, additional text, or commentary. Only return the JSON object.
        """
    AUGMENTED_RESPONSE_ERROR = "Error: Please rewrite your query for getting output"

    # generate_augmented_response_from_image
    AUGMENTED_IMAGE_RESPONSE_PROMPT = """
        User Uploaded Image: [Image data provided for analysis]
        Retrieved Images:
        {retrieved_text}
        Instructions:
        You are a creative assistant tasked with generating a JSON-formatted response based on the user-uploaded image and retrieved images from a database. Follow these steps:
        Here is the User image: {user_image}
        1. **Analyze the User Image**:
        - Carefully examine the provided image and generate an accurate description of its visual content. Focus on identifying key objects, colors, styles, and the overall scene. For example, if the image shows a classroom, describe it as "a classroom with desks, chairs, and a blackboard," not something unrelated like a cat.
        - **Important**: Your analysis must be based solely on the visual elements present in the image. Avoid assumptions or biases unrelated to the image’s content (e.g., do not default to cats unless the image contains them).
        2. **Rank Images by Relevance**:
        - Use the 'Distance' values (lower = more relevant) to rank the retrieved images based on how well they match the visual content of the user-uploaded image, as described in your analysis.
        - Consider the descriptions and tags of the retrieved images to refine the ranking, prioritizing those that closely align with the user image’s content (e.g., classroom-related images if the user uploaded a classroom).
        3. **Select Top Images**:
        - Select exactly 5 images based on your relevance ranking, ensuring they align with the user-uploaded image’s content.
        - If fewer than 5 images are relevant, include only those that match well without apologizing for the shortfall.
        - If no images match, proceed with an empty selection.
        4. **Generate JSON Response**:
        - **Structure**: Return a JSON string with three fields:
            - "description": A single string combining all explanations.
            - "path": An array of selected image paths.
            - "id": An array of selected image IDs.
        - **If images are selected**:
            - Format "description" as: "Here is the first or second image and so on then [a generalised description]. then at last give a genarlised ovrall description.descriptions should be short and concise.
            - Base reasoning on the visual content of the user image (e.g., "This matches the classroom setting with desks and a blackboard you uploaded!").
        - **If no images**:
            - Set "description": "No images found in the gallery that match your uploaded image. Try uploading a different one or let’s add some new pics!"
            - Set "path" and "id" to empty arrays.
        - **If fewer than 5 images**: List the available images with their descriptions and reasons, without mentioning the shortfall.
        5. **Reasoning**:
        - Provide human-like reasons directly tied to the visual content of the user image and retrieved images (e.g., "This image has a similar classroom layout with desks and a chalkboard.").
        - Avoid mentioning distances or unrelated content (e.g., no references to cats unless they’re in the user image).
        6. **Formatting**:
        - Use an engaging, friendly tone."Output ONLY the JSON object, with no extra text, commentary, or explanations before or after.".
        - Must Ensure the JSON follows this exact template:
            ```json
            {{
                "description": "descriptions should be short and concise. Here is the first image which is  [a generalised description]. I chose this because [reason].\\n Same for the second and so on. ... and  then at last give a genarlised ovrall short description",
                "path": ["path1", "path2", ...],
                "id": ["id1", "id2", ...]
            }}```
        **Important**: Do not include any explanations, additional text, or commentary. Only return the JSON object.
    """
    AUGMENTED_IMAGE_RESPONSE_ERROR = "error working with image related data might be facing some error in the database."

    # chatbot
    MEMORY_UNAVAILABLE = "sorry memory is not currently available"
    DATABASE_UNAVAILABLE= "sorry this service is not currently available working on the database part"
    
    # Strings for expand_conversation_history
    NO_HISTORY_AVAILABLE = "No previous conversation history available."
    HISTORY_CONTEXT_HEADER = "Conversation History Context (most recent last):"
    CHAT_ENTRY_FORMAT = "Chat {chat_idx} ({timestamp}):"
    ROLE_TEXT_FORMAT = "  {role}: {text}"
    ASSOCIATED_IMAGES_HEADER = "  Associated Images:"
    IMAGE_ENTRY_FORMAT = "    Image {img_idx}: Path = {path}"
    IMAGE_ID_FORMAT = ", ID = {img_id}"
    IMAGE_NOT_DESCRIBED = " (image referenced but not described)"
    
    #format retrieved images
    NO_DESCRIPTION_AVAILABLE = 'No Description Available'
    NO_IMAGE_RETRIEVED = "No images retrieved."
    
    
    
    
# For Route/Chat.py
class RouteChat:
    UNEXPECTED_RESPONSE = "Unexpected response type from chatbot."
    UNEXPECTED_TYPE_RESPONSE = "Unexpected response type from chatbot."
    
class UploadStr:
    ERROR_ADDING_TO_VECTOR_DB = "Error in adding the image in vector database: {}"
    SUCCESS_MESSAGE = "/upload?success=Images+uploaded+successfully"
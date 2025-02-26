import openai
import json
from fastapi import HTTPException
from app.config import OPENAI_API_KEY
from app.services.prompts import ANALYZE_PROMPT, QUERY_PROMPT
from app.utils.logger import logger

openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)


def analyze_cv(text):
    """Uses OpenAI GPT-4 to analyze and structure extracted CV text."""
    logger.debug("Starting CV analysis with OpenAI GPT-4")
    prompt = ANALYZE_PROMPT.format(text=text)

    try:
        logger.info("Sending request to OpenAI for CV analysis")
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                 "content": "You are an AI that extracts structured CV information, including total years of experience. Ensure the response is always a valid JSON format."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        raw_response = response.choices[0].message.content.strip()

        logger.debug(f"Raw OpenAI Response: {raw_response}")

        try:
            parsed_response = json.loads(raw_response)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decoding error: {e}")
            raise HTTPException(status_code=500, detail="Invalid JSON response from OpenAI")

        # Ensure total_experience is saved as a string
        if "total_experience" in parsed_response:
            parsed_response["total_experience"] = str(parsed_response["total_experience"])

        if not "total_experience" in parsed_response:
            parsed_response["total_experience"] = str(0)

        logger.info("Successfully processed CV analysis")
        logger.debug(f"Extracted CV Data: {parsed_response}")
        return parsed_response
    except Exception as e:
        logger.exception(f"Error analyzing CV with OpenAI: {e}")
        raise HTTPException(status_code=500, detail="OpenAI processing error")


def analyze_query(user_query):
    logger.info(f"Processing NLP query: {user_query}")

    try:
        prompt = QUERY_PROMPT.format(user_query=user_query)

        logger.info("Sending request to OpenAI for query analysis")
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Convert natural language CV queries into MongoDB search queries."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )

        # heck if response is empty before parsing JSON
        raw_response = response.choices[0].message.content.strip()
        logger.debug(f"Raw OpenAI Response: {raw_response}")

        if not raw_response:
            logger.error("OpenAI returned an empty response")
            raise HTTPException(status_code=500, detail="OpenAI returned an empty response")

        # Ensure response is valid JSON before loading
        try:
            mongo_query = json.loads(raw_response)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decoding error: {e}")
            raise HTTPException(status_code=500, detail="Invalid JSON response from OpenAI")

        logger.info("Successfully generated MongoDB query")
        logger.debug(f"Generated MongoDB Query: {mongo_query}")
        return mongo_query

    except Exception as e:
        logger.error(f"Error processing NLP query: {e}")
        raise HTTPException(status_code=500, detail="Error processing query with NLP")


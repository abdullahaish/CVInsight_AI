from fastapi import APIRouter, Query, HTTPException
from app.config import cvs_collection
from app.services.llm_analysis import analyze_query
from app.utils.logger import logger

router = APIRouter()


@router.get("/chatbot/")
def chatbot_query(query: str = Query(...)):
    logger.info(f"Received chatbot query request: {query}")
    try:
        mongo_query = analyze_query(query)
        logger.debug(f"Generated MongoDB Query: {mongo_query}")

        results = list(cvs_collection.find(mongo_query, {"_id": 0}))
        logger.info(f"Found {len(results)} matching results")

        return {"query": query, "results": results}
    except Exception as e:
        logger.error(f"Error processing chatbot query: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

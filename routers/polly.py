from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse

from helpers.polly import convert_text_to_speech
from schemas.text_to_speech import TextToSpeechRegisterRequest

# Create an API router
api_router = APIRouter()

@api_router.post("/")
def convert_text_to_speech_api(
    body: TextToSpeechRegisterRequest = Body(...),
):
    ## Polly text to speech and return S3 link
    try:
        response = convert_text_to_speech(body=body)
        
        # Return the public S3 URL as a response
        return JSONResponse(content={"s3_url": response["s3_url"]}, status_code=status.HTTP_200_OK)

    except Exception as exc:
        print(f"Error in converting text to speech - {body}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

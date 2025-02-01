import openai
import boto3 # type: ignore
from io import BytesIO
from botocore.exceptions import ClientError # type: ignore
from uuid import uuid4
from config import cfg
from schemas.text_to_speech import TextToSpeechRegisterRequest
from mutagen.mp3 import MP3

# Initialize AWS Boto3 session
aws_session = boto3.Session(
    aws_access_key_id=cfg.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=cfg.AWS_SECRET_ACCESS_KEY,
    region_name=cfg.AWS_REGION_NAME
)

# OpenAI API Key
openai.api_key = cfg.openai_api_key

def convert_text_to_speech(body: TextToSpeechRegisterRequest):
    """Convert text to speech using OpenAI TTS and upload to S3."""
    try:
        print("convert_text_to_speech API called")

        # Define settings
        voice_id = cfg.OPENAI_TTS_VOICE  # Example: "nova"
        output_format = 'mp3'
        bucket_name = cfg.AWS_S3_BUCKET_NAME
        file_name = f"audio/{uuid4()}.mp3"  # Unique filename

        # Generate speech using OpenAI's TTS API
        print("OpenAI TTS API called")
        response = openai.audio.speech.create(
            model="tts-1",  # Available models: 'tts-1', 'tts-1-hd'
            voice=voice_id,
            input=body.text
        )

        audio_stream = BytesIO(response.content)  # Convert content to memory stream
        audio_file = MP3(audio_stream)  # Using MP3 from mutagen

        duration = audio_file.info.length  # Duration in seconds
        print(f"Audio duration: {duration} seconds")
        # Initialize AWS S3 client
        s3_client = aws_session.client('s3')

        # Upload the MP3 file to S3
        try:
            print("Uploading audio to S3")
            s3_client.put_object(
                Bucket=bucket_name,
                Key=file_name,
                Body=response.content,
                ContentType='audio/mpeg',
            )
        except ClientError as e:
            print(f"Error uploading audio to S3: {e}")
            raise Exception("Error uploading audio to S3")

        # Generate the S3 URL
        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
        print(f"File uploaded to S3: {s3_url}")

        # Return the S3 URL as a response
        return {"s3_url": s3_url, "audio_duration": int(duration)}

    except Exception as exc:
        print(f"Error in converting text to speech - {body.text}")
        raise Exception(exc)

# Test the function
if __name__ == "__main__":
    text = "Summary of the day's most important events."
    response = convert_text_to_speech(
        body=TextToSpeechRegisterRequest(text=text)
    )
    print(response)

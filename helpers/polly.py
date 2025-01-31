from boto3 import Session as boto3_session # type: ignore
from botocore.exceptions import ClientError # type: ignore
from uuid import uuid4

from config import cfg
from schemas.text_to_speech import TextToSpeechRegisterRequest

# Initialize aws boto session
aws_session = boto3_session(
    aws_access_key_id=cfg.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=cfg.AWS_SECRET_ACCESS_KEY,
    region_name=cfg.AWS_REGION_NAME,
)

def convert_text_to_speech(body: TextToSpeechRegisterRequest):
    ## Polly text to speech and return S3 link
    try:
        print("convert_text_to_speech api called")

        # Create an AWS session and Polly client
        aws_polly_client = aws_session.client('polly')
        s3_client = aws_session.client('s3')
        
        # Polly settings
        voice_id = cfg.AWS_POLLY_VOICE_ID
        output_format = 'mp3'
        bucket_name = cfg.AWS_S3_BUCKET_NAME
        file_name = f"audio/{uuid4()}.mp3"  # Generate a unique file name

        # Use Polly to synthesize speech
        print("aws polly synthesize_speech called")
        response = aws_polly_client.synthesize_speech(
            VoiceId=voice_id,
            OutputFormat=output_format,
            Text=body.text,
            Engine='standard'
        )

        # Upload to S3
        try:
            print("Uploading audio to S3")
            s3_client.put_object(
                Bucket=bucket_name,
                Key=file_name,
                Body=response['AudioStream'].read(),
                ContentType='audio/mpeg',
            )
        except ClientError as e:
            print(f"Error uploading audio to S3: {e}")
            raise Exception("Error uploading audio to S3")

        # Generate a presigned URL
        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
        
        # Return the public S3 URL as a response
        return {"s3_url": s3_url}

    except Exception as exc:
        print(f"Error in converting text to speech - {body}")
        raise Exception(exc)    

if __name__ == "__main__":
    text = "Summary of the day's most important events."
    response = convert_text_to_speech(
        body=TextToSpeechRegisterRequest(text=text)
    )
    print(response)
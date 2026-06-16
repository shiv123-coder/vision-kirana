from sqlalchemy.orm import Session
from app.ml.voice_processor import MockVoiceRecognizer, VoiceAnalyzer
from app.models.voice import VoiceTranscript
import logging

logger = logging.getLogger(__name__)

def process_uploaded_audio(audio_bytes: bytes, transcript_id: int, db: Session):
    """
    Background task to process audio, transcribe it, and analyze business insights.
    """
    try:
        # In the future, this can be swapped with a Whisper implementation
        recognizer = MockVoiceRecognizer()
        analyzer = VoiceAnalyzer()
        
        logger.info(f"Transcribing audio for transcript_id {transcript_id}...")
        transcript_text = recognizer.transcribe(audio_bytes)
        
        logger.info(f"Analyzing transcript for transcript_id {transcript_id}...")
        analysis_results = analyzer.analyze(transcript_text)
        
        # Update the database record
        db_transcript = db.query(VoiceTranscript).filter(VoiceTranscript.id == transcript_id).first()
        if db_transcript:
            db_transcript.transcript_text = transcript_text
            db_transcript.sentiment_score = analysis_results.get("sentiment_score")
            db_transcript.business_summary = analysis_results.get("business_summary")
            db_transcript.loan_purpose = analysis_results.get("loan_purpose")
            db_transcript.challenges = analysis_results.get("challenges")
            db_transcript.future_plans = analysis_results.get("future_plans")
            
            db.commit()
            logger.info(f"Successfully processed audio for transcript_id {transcript_id}")
        else:
            logger.error(f"Transcript ID {transcript_id} not found in database")
            
    except Exception as e:
        logger.error(f"Failed to process audio for transcript_id {transcript_id}: {str(e)}")
        db.rollback()
    finally:
        db.close()

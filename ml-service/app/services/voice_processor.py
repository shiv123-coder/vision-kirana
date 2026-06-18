import abc
import logging

logger = logging.getLogger(__name__)

class BaseVoiceRecognizer(abc.ABC):
    """
    Abstract interface for Voice Recognition.
    This architecture supports plugging in Whisper or other ASR engines later.
    """
    @abc.abstractmethod
    def transcribe(self, audio_bytes: bytes) -> str:
        pass

class MockVoiceRecognizer(BaseVoiceRecognizer):
    """
    A mock implementation of the VoiceRecognizer for rapid development.
    Simulates a detailed, realistic transcript from a Kirana store owner.
    """
    def transcribe(self, audio_bytes: bytes) -> str:
        # We ignore the audio bytes and return a rich, mock transcript
        return (
            "Namaste, I am running a kirana shop for the last 10 years in this market. "
            "My daily sales are good, usually around 5000 to 8000 rupees. "
            "However, I want to take a loan of 2 lakh rupees because I want to expand my shop "
            "and add a small cold storage section for dairy and beverages. "
            "The main challenge right now is the competition from new supermarkets, "
            "but my loyal customers still come to me for daily groceries. "
            "In the future, I plan to start home delivery and modernize my billing system."
        )

class VoiceAnalyzer:
    """
    Analyzes transcripts to extract key business insights.
    Uses basic heuristics/NLP for now, easily swappable with LLM later.
    """
    def analyze(self, transcript: str) -> dict:
        transcript_lower = transcript.lower()
        
        # Simple extraction heuristics based on keywords
        
        # Extract Loan Purpose
        loan_purpose = "Not clearly mentioned"
        if "loan" in transcript_lower or "rupees" in transcript_lower:
            # Try to grab the sentence containing 'loan' or 'want to'
            sentences = transcript.split('.')
            for s in sentences:
                if 'loan' in s.lower() or 'want to' in s.lower() or 'expand' in s.lower():
                    loan_purpose = s.strip()
                    break

        # Extract Challenges
        challenges = "None explicitly stated"
        if "challenge" in transcript_lower or "problem" in transcript_lower or "competition" in transcript_lower:
            sentences = transcript.split('.')
            for s in sentences:
                if 'challenge' in s.lower() or 'competition' in s.lower() or 'difficult' in s.lower():
                    challenges = s.strip()
                    break
                    
        # Extract Future Plans
        future_plans = "Not specified"
        if "future" in transcript_lower or "plan" in transcript_lower or "later" in transcript_lower:
            sentences = transcript.split('.')
            for s in sentences:
                if 'future' in s.lower() or 'plan' in s.lower() or 'start' in s.lower():
                    future_plans = s.strip()
                    break
                    
        # Extract Business Summary
        # Just use the first two sentences as a general summary
        sentences = [s.strip() for s in transcript.split('.') if len(s.strip()) > 5]
        summary = ". ".join(sentences[:2]) + "." if len(sentences) >= 2 else transcript
        
        # Simple Sentiment
        sentiment = "Positive"
        if "challenge" in transcript_lower or "difficult" in transcript_lower:
            sentiment = "Neutral"

        return {
            "business_summary": summary,
            "loan_purpose": loan_purpose,
            "challenges": challenges,
            "future_plans": future_plans,
            "sentiment_score": sentiment
        }

class VoiceProcessor:
    def __init__(self):
        self.recognizer = MockVoiceRecognizer()
        self.analyzer = VoiceAnalyzer()

    def process_audio(self, audio_bytes: bytes):
        transcript = self.recognizer.transcribe(audio_bytes)
        analysis = self.analyzer.analyze(transcript)
        return transcript, analysis.get("sentiment_score", "Neutral")

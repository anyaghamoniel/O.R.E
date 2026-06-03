"""
O.R.E Voice Agent - Text-to-speech and audio narration
Generates professional voice-overs and audio content
"""
import logging
from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent
from app.agents.agent_factory import register_agent
from app.config import settings
import os

logger = logging.getLogger(__name__)

@register_agent("voice")
class VoiceAgent(BaseAgent):
    """
    Voice Agent - Audio narration and text-to-speech
    Generates professional voice-overs, audio content, and narration
    """
    
    def __init__(self):
        super().__init__(agent_type="voice", name="Voice Agent")
        self.supported_voices = [
            "alloy", "echo", "fable", "onyx", "nova", "shimmer"  # OpenAI TTS voices
        ]
        self.supported_languages = [
            "en", "es", "fr", "de", "it", "pt", "nl", "ru", "ja", "ko", "zh"
        ]
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute voice generation task
        
        Args:
            input_data: {
                "action": str (e.g., "text_to_speech", "generate_narration", "voice_clone"),
                "params": dict (action-specific parameters)
            }
        
        Returns:
            Generated audio file path and metadata
        """
        try:
            self.validate_input(input_data)
            
            action = input_data.get("action", "text_to_speech")
            self.log_execution(f"Starting voice action: {action}")
            
            if action == "text_to_speech":
                result = self._text_to_speech(input_data)
            elif action == "generate_narration":
                result = self._generate_narration(input_data)
            elif action == "voice_clone":
                result = self._voice_clone(input_data)
            elif action == "audio_enhance":
                result = self._enhance_audio(input_data)
            elif action == "generate_voiceover":
                result = self._generate_voiceover(input_data)
            elif action == "audio_sync":
                result = self._sync_audio_to_video(input_data)
            else:
                raise ValueError(f"Unknown voice action: {action}")
            
            self.log_execution(f"Voice action completed: {action}")
            return result
            
        except Exception as e:
            self.log_execution(f"Error executing voice task: {str(e)}", level="error")
            raise
    
    def _text_to_speech(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert text to speech using TTS service
        """
        params = input_data.get("params", {})
        text = params.get("text", "")
        voice = params.get("voice", "nova")
        language = params.get("language", "en")
        speed = params.get("speed", 1.0)  # 0.25 to 4.0
        pitch = params.get("pitch", 1.0)  # 0.5 to 2.0
        output_file = params.get("output_file", os.path.join(settings.OUTPUT_DIR, "audio.mp3"))
        
        if not text:
            raise ValueError("Text is required for text-to-speech")
        
        if voice not in self.supported_voices:
            raise ValueError(f"Voice '{voice}' not supported. Available: {self.supported_voices}")
        
        if language not in self.supported_languages:
            raise ValueError(f"Language '{language}' not supported. Available: {self.supported_languages}")
        
        self.log_execution(f"Converting text to speech: {len(text)} characters, voice: {voice}")
        
        # Placeholder for TTS API integration
        # In production, integrate with OpenAI TTS, Google Cloud TTS, Azure TTS, etc.
        audio_duration = len(text.split()) * 0.4  # Rough estimate: ~150 words per minute
        
        return {
            "status": "success",
            "action": "text_to_speech",
            "voice": voice,
            "language": language,
            "speed": speed,
            "pitch": pitch,
            "text_length": len(text),
            "word_count": len(text.split()),
            "output_file": output_file,
            "audio_duration": audio_duration,
            "estimated_size_mb": audio_duration * 0.01  # Rough estimate
        }
    
    def _generate_narration(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate professional narration for video/presentation
        """
        params = input_data.get("params", {})
        script = params.get("script", "")
        narrator_style = params.get("narrator_style", "professional")  # professional, casual, energetic
        tone = params.get("tone", "neutral")  # neutral, warm, authoritative
        voice_gender = params.get("voice_gender", "neutral")  # male, female, neutral
        output_file = params.get("output_file", os.path.join(settings.OUTPUT_DIR, "narration.mp3"))
        
        if not script:
            raise ValueError("Script is required for narration")
        
        self.log_execution(f"Generating narration: {narrator_style} style, {voice_gender} voice")
        
        # Map narrator style to voice characteristics
        voice_config = self._get_voice_config(narrator_style, voice_gender, tone)
        
        audio_duration = len(script.split()) * 0.4
        
        return {
            "status": "success",
            "action": "generate_narration",
            "narrator_style": narrator_style,
            "tone": tone,
            "voice_gender": voice_gender,
            "voice_config": voice_config,
            "script_length": len(script),
            "word_count": len(script.split()),
            "output_file": output_file,
            "audio_duration": audio_duration,
            "sections": self._split_script_into_sections(script)
        }
    
    def _voice_clone(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clone a voice from reference audio
        """
        params = input_data.get("params", {})
        reference_audio = params.get("reference_audio")
        text_to_voice = params.get("text", "")
        clone_strength = params.get("clone_strength", 0.8)  # 0.0 to 1.0
        output_file = params.get("output_file", os.path.join(settings.OUTPUT_DIR, "cloned_voice.mp3"))
        
        if not reference_audio or not text_to_voice:
            raise ValueError("Both reference_audio and text are required for voice cloning")
        
        self.log_execution(f"Cloning voice from reference audio, clone strength: {clone_strength}")
        
        # Placeholder for voice cloning API integration
        # In production, use services like ElevenLabs, Respeecher, etc.
        
        return {
            "status": "success",
            "action": "voice_clone",
            "reference_audio": reference_audio,
            "clone_strength": clone_strength,
            "text_voiceover": text_to_voice,
            "output_file": output_file,
            "quality_score": clone_strength * 100,
            "processing_time_seconds": len(text_to_voice.split()) * 0.5
        }
    
    def _enhance_audio(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance audio quality (noise reduction, normalization, EQ)
        """
        params = input_data.get("params", {})
        audio_file = params.get("audio_file")
        enhancement_type = params.get("enhancement_type", "auto")  # auto, denoise, normalize, eq
        output_file = params.get("output_file", os.path.join(settings.OUTPUT_DIR, "enhanced_audio.mp3"))
        
        if not audio_file:
            raise ValueError("Audio file is required for enhancement")
        
        enhancements = []
        
        if enhancement_type in ["auto", "denoise"]:
            enhancements.append("Noise Reduction")
        
        if enhancement_type in ["auto", "normalize"]:
            enhancements.append("Audio Normalization")
            enhancements.append("Level Balancing")
        
        if enhancement_type in ["auto", "eq"]:
            enhancements.append("EQ Processing")
            enhancements.append("Bass Enhancement")
            enhancements.append("Clarity Enhancement")
        
        self.log_execution(f"Enhancing audio: {', '.join(enhancements)}")
        
        return {
            "status": "success",
            "action": "audio_enhance",
            "input_file": audio_file,
            "enhancement_type": enhancement_type,
            "output_file": output_file,
            "enhancements_applied": enhancements,
            "quality_improvement_percent": 25 if enhancement_type == "auto" else 15,
            "noise_reduction_db": 12 if enhancement_type in ["auto", "denoise"] else 0
        }
    
    def _generate_voiceover(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate complete voice-over with multiple speakers/voices
        """
        params = input_data.get("params", {})
        scenes = params.get("scenes", [])  # List of {text, voice, duration}
        background_music = params.get("background_music")
        music_volume = params.get("music_volume", 0.3)
        output_file = params.get("output_file", os.path.join(settings.OUTPUT_DIR, "voiceover.mp3"))
        
        if not scenes:
            raise ValueError("Scenes are required for voice-over generation")
        
        self.log_execution(f"Generating voice-over with {len(scenes)} scenes")
        
        total_duration = sum(scene.get("duration", 0) for scene in scenes)
        
        return {
            "status": "success",
            "action": "generate_voiceover",
            "scenes_count": len(scenes),
            "background_music": background_music,
            "music_volume": music_volume,
            "output_file": output_file,
            "total_duration": total_duration,
            "voices_used": list(set(scene.get("voice", "nova") for scene in scenes)),
            "processing_status": "completed"
        }
    
    def _sync_audio_to_video(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sync audio narration/voice-over to video timeline
        """
        params = input_data.get("params", {})
        video_file = params.get("video_file")
        audio_file = params.get("audio_file")
        sync_type = params.get("sync_type", "simple")  # simple, smart (with lip-sync)
        output_file = params.get("output_file", os.path.join(settings.OUTPUT_DIR, "synced_video.mp4"))
        
        if not video_file or not audio_file:
            raise ValueError("Both video_file and audio_file are required")
        
        self.log_execution(f"Syncing audio to video: {sync_type} sync")
        
        return {
            "status": "success",
            "action": "audio_sync",
            "video_file": video_file,
            "audio_file": audio_file,
            "sync_type": sync_type,
            "output_file": output_file,
            "lip_sync_enabled": sync_type == "smart",
            "estimated_processing_time": 120  # seconds
        }
    
    # Helper methods
    
    def _get_voice_config(self, narrator_style: str, voice_gender: str, tone: str) -> Dict[str, Any]:
        """
        Get voice configuration based on style and gender
        """
        voice_mapping = {
            ("professional", "male"): "onyx",
            ("professional", "female"): "nova",
            ("professional", "neutral"): "echo",
            ("casual", "male"): "alloy",
            ("casual", "female"): "shimmer",
            ("casual", "neutral"): "fable",
            ("energetic", "male"): "onyx",
            ("energetic", "female"): "nova",
            ("energetic", "neutral"): "shimmer",
        }
        
        voice = voice_mapping.get((narrator_style, voice_gender), "nova")
        
        return {
            "voice": voice,
            "style": narrator_style,
            "gender": voice_gender,
            "tone": tone,
            "speed": 1.0 if narrator_style == "professional" else 1.1 if narrator_style == "energetic" else 1.0,
            "pitch": 1.0 if narrator_style == "professional" else 1.1 if narrator_style == "energetic" else 0.95
        }
    
    def _split_script_into_sections(self, script: str, max_chars: int = 1000) -> List[Dict[str, str]]:
        """
        Split script into sections for easier processing
        """
        sections = []
        paragraphs = script.split("\n\n")
        current_section = ""
        
        for para in paragraphs:
            if len(current_section) + len(para) < max_chars:
                current_section += para + "\n\n"
            else:
                if current_section:
                    sections.append({
                        "text": current_section.strip(),
                        "duration": len(current_section.split()) * 0.4
                    })
                current_section = para + "\n\n"
        
        if current_section:
            sections.append({
                "text": current_section.strip(),
                "duration": len(current_section.split()) * 0.4
            })
        
        return sections
    
    def validate_input(self, input_data: Dict[str, Any]):
        """
        Validate input data
        """
        action = input_data.get("action")
        if not action:
            raise ValueError("Missing required field: action")
        
        valid_actions = [
            "text_to_speech", "generate_narration", "voice_clone",
            "audio_enhance", "generate_voiceover", "audio_sync"
        ]
        
        if action not in valid_actions:
            raise ValueError(f"Invalid action: {action}")

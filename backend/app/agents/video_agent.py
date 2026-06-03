"""
O.R.E Video Agent (Zoey) - Video processing and editing
Core agent for video production tasks
"""
import os
import logging
from typing import Dict, Any
from app.agents.base_agent import BaseAgent
from app.agents.agent_factory import register_agent
from app.config import settings
import subprocess
import json

logger = logging.getLogger(__name__)

@register_agent("video")
class VideoAgent(BaseAgent):
    """
    Zoey - The Video Agent
    Handles video processing, editing, and manipulation using FFmpeg
    """
    
    def __init__(self):
        super().__init__(agent_type="video", name="Zoey - Video Agent")
        self.ffmpeg_path = settings.FFMPEG_PATH
        self.ffprobe_path = settings.FFPROBE_PATH
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute video processing task
        
        Args:
            input_data: {
                "action": str (e.g., "edit", "encode", "merge"),
                "input_file": str (path to input video),
                "output_file": str (path for output video),
                "params": dict (action-specific parameters)
            }
        
        Returns:
            {
                "status": "success",
                "output_file": str,
                "duration": float,
                "size": int,
                "metadata": dict
            }
        """
        try:
            self.validate_input(input_data)
            
            action = input_data.get("action", "encode")
            self.log_execution(f"Starting video action: {action}")
            
            # Route to appropriate action
            if action == "encode":
                result = self._encode_video(input_data)
            elif action == "edit":
                result = self._edit_video(input_data)
            elif action == "merge":
                result = self._merge_videos(input_data)
            elif action == "extract_audio":
                result = self._extract_audio(input_data)
            elif action == "add_audio":
                result = self._add_audio(input_data)
            elif action == "get_info":
                result = self._get_video_info(input_data)
            else:
                raise ValueError(f"Unknown video action: {action}")
            
            self.log_execution(f"Video action completed: {action}")
            return result
            
        except Exception as e:
            self.log_execution(f"Error executing video task: {str(e)}", level="error")
            raise
    
    def _encode_video(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Encode/transcode video to different format
        """
        input_file = input_data.get("input_file")
        output_file = input_data.get("output_file")
        params = input_data.get("params", {})
        
        # Build FFmpeg command
        cmd = [
            self.ffmpeg_path,
            "-i", input_file,
            "-c:v", params.get("video_codec", "libx264"),
            "-preset", params.get("preset", "medium"),
            "-crf", str(params.get("quality", 23)),
            "-c:a", params.get("audio_codec", "aac"),
            "-b:a", params.get("audio_bitrate", "128k"),
            "-y",  # Overwrite output file
            output_file
        ]
        
        self.log_execution(f"Encoding video: {input_file} -> {output_file}")
        self._run_ffmpeg(cmd)
        
        return {
            "status": "success",
            "output_file": output_file,
            "action": "encode"
        }
    
    def _edit_video(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Edit video (trim, crop, etc.)
        """
        input_file = input_data.get("input_file")
        output_file = input_data.get("output_file")
        params = input_data.get("params", {})
        
        # Build FFmpeg filter string
        filters = []
        
        # Trim
        if "start" in params and "duration" in params:
            filters.append(f"trim=start={params['start']}:duration={params['duration']}")
        
        # Crop
        if "crop" in params:
            crop = params["crop"]
            filters.append(f"crop={crop['width']}:{crop['height']}:{crop['x']}:{crop['y']}")
        
        # Scale/Resize
        if "scale" in params:
            scale = params["scale"]
            filters.append(f"scale={scale['width']}:{scale['height']}")
        
        cmd = [
            self.ffmpeg_path,
            "-i", input_file,
            "-vf", ",".join(filters) if filters else "null",
            "-c:a", "copy",
            "-y",
            output_file
        ]
        
        self.log_execution(f"Editing video: {input_file}")
        self._run_ffmpeg(cmd)
        
        return {
            "status": "success",
            "output_file": output_file,
            "action": "edit",
            "filters_applied": filters
        }
    
    def _merge_videos(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge multiple videos
        """
        input_files = input_data.get("input_files", [])
        output_file = input_data.get("output_file")
        
        if not input_files or len(input_files) < 2:
            raise ValueError("Merge requires at least 2 input files")
        
        # Create concat file
        concat_file = os.path.join(settings.TEMP_DIR, "concat.txt")
        with open(concat_file, "w") as f:
            for file in input_files:
                f.write(f"file '{file}'\n")
        
        cmd = [
            self.ffmpeg_path,
            "-f", "concat",
            "-safe", "0",
            "-i", concat_file,
            "-c", "copy",
            "-y",
            output_file
        ]
        
        self.log_execution(f"Merging {len(input_files)} videos")
        self._run_ffmpeg(cmd)
        os.remove(concat_file)
        
        return {
            "status": "success",
            "output_file": output_file,
            "action": "merge",
            "input_files_count": len(input_files)
        }
    
    def _extract_audio(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract audio from video
        """
        input_file = input_data.get("input_file")
        output_file = input_data.get("output_file", input_file.replace(".mp4", ".mp3"))
        
        cmd = [
            self.ffmpeg_path,
            "-i", input_file,
            "-q:a", "0",
            "-map", "a",
            "-y",
            output_file
        ]
        
        self.log_execution(f"Extracting audio from {input_file}")
        self._run_ffmpeg(cmd)
        
        return {
            "status": "success",
            "output_file": output_file,
            "action": "extract_audio"
        }
    
    def _add_audio(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add audio to video
        """
        video_file = input_data.get("video_file")
        audio_file = input_data.get("audio_file")
        output_file = input_data.get("output_file")
        
        cmd = [
            self.ffmpeg_path,
            "-i", video_file,
            "-i", audio_file,
            "-c:v", "copy",
            "-c:a", "aac",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-y",
            output_file
        ]
        
        self.log_execution(f"Adding audio to video")
        self._run_ffmpeg(cmd)
        
        return {
            "status": "success",
            "output_file": output_file,
            "action": "add_audio"
        }
    
    def _get_video_info(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get video information/metadata
        """
        input_file = input_data.get("input_file")
        
        cmd = [
            self.ffprobe_path,
            "-v", "quiet",
            "-print_format", "json",
            "-show_streams",
            "-show_format",
            input_file
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            metadata = json.loads(result.stdout)
            
            return {
                "status": "success",
                "input_file": input_file,
                "action": "get_info",
                "metadata": metadata
            }
        except Exception as e:
            self.log_execution(f"Error getting video info: {str(e)}", level="error")
            raise
    
    def _run_ffmpeg(self, cmd: list):
        """
        Run FFmpeg command and handle errors
        """
        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode() if e.stderr else str(e)
            raise RuntimeError(f"FFmpeg error: {error_msg}")
    
    def validate_input(self, input_data: Dict[str, Any]):
        """
        Validate input data
        """
        action = input_data.get("action")
        if not action:
            raise ValueError("Missing required field: action")
        
        required_fields = {
            "encode": ["input_file", "output_file"],
            "edit": ["input_file", "output_file"],
            "merge": ["input_files", "output_file"],
            "extract_audio": ["input_file"],
            "add_audio": ["video_file", "audio_file", "output_file"],
            "get_info": ["input_file"]
        }
        
        fields = required_fields.get(action, [])
        for field in fields:
            if field not in input_data:
                raise ValueError(f"Missing required field for '{action}': {field}")

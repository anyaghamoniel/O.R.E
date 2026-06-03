"""
O.R.E Script Agent - Content writing and copywriting
Generates marketing copy, scripts, and content for campaigns
"""
import logging
from typing import Dict, Any
from app.agents.base_agent import BaseAgent
from app.agents.agent_factory import register_agent

logger = logging.getLogger(__name__)

@register_agent("script")
class ScriptAgent(BaseAgent):
    """
    Script Agent - Content creation and copywriting
    Generates marketing copy, social media content, email campaigns, video scripts
    """
    
    def __init__(self):
        super().__init__(agent_type="script", name="Script Agent")
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute script generation task
        
        Args:
            input_data: {
                "action": str (e.g., "generate_script", "generate_copy", "generate_email"),
                "params": dict (action-specific parameters)
            }
        
        Returns:
            Generated content
        """
        try:
            self.validate_input(input_data)
            
            action = input_data.get("action", "generate_copy")
            self.log_execution(f"Starting script action: {action}")
            
            if action == "generate_script":
                result = self._generate_video_script(input_data)
            elif action == "generate_copy":
                result = self._generate_marketing_copy(input_data)
            elif action == "generate_email":
                result = self._generate_email_campaign(input_data)
            elif action == "generate_social":
                result = self._generate_social_content(input_data)
            elif action == "generate_ad":
                result = self._generate_ad_copy(input_data)
            elif action == "refine_content":
                result = self._refine_content(input_data)
            else:
                raise ValueError(f"Unknown script action: {action}")
            
            self.log_execution(f"Script action completed: {action}")
            return result
            
        except Exception as e:
            self.log_execution(f"Error executing script task: {str(e)}", level="error")
            raise
    
    def _generate_video_script(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a video script
        """
        params = input_data.get("params", {})
        topic = params.get("topic", "Product showcase")
        duration = params.get("duration", 60)  # seconds
        tone = params.get("tone", "professional")
        target_audience = params.get("target_audience", "general")
        
        self.log_execution(f"Generating {duration}s video script for: {topic}")
        
        # Placeholder for AI script generation
        # In production, integrate with LLM APIs (OpenAI, Anthropic, etc.)
        script_sections = {
            "hook": self._generate_hook(topic, tone),
            "body": self._generate_body(topic, tone, duration),
            "cta": self._generate_cta(tone)
        }
        
        script_text = f"{script_sections['hook']}\n\n{script_sections['body']}\n\n{script_sections['cta']}"
        
        return {
            "status": "success",
            "action": "generate_script",
            "topic": topic,
            "duration": duration,
            "tone": tone,
            "target_audience": target_audience,
            "script": script_text,
            "word_count": len(script_text.split()),
            "sections": script_sections
        }
    
    def _generate_marketing_copy(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate marketing copy
        """
        params = input_data.get("params", {})
        product_name = params.get("product_name", "Product")
        benefits = params.get("benefits", [])
        target_audience = params.get("target_audience", "general")
        style = params.get("style", "persuasive")  # persuasive, informative, funny
        
        self.log_execution(f"Generating marketing copy for: {product_name}")
        
        headline = f"Discover the Power of {product_name}: Transform Your {target_audience} Experience"
        body = self._generate_copy_body(product_name, benefits, style)
        cta = self._generate_marketing_cta(product_name)
        
        copy_text = f"{headline}\n\n{body}\n\n{cta}"
        
        return {
            "status": "success",
            "action": "generate_copy",
            "product_name": product_name,
            "target_audience": target_audience,
            "style": style,
            "copy": copy_text,
            "headline": headline,
            "body": body,
            "cta": cta,
            "word_count": len(copy_text.split())
        }
    
    def _generate_email_campaign(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate email campaign content
        """
        params = input_data.get("params", {})
        campaign_name = params.get("campaign_name", "Campaign")
        offer = params.get("offer", "")
        segment = params.get("segment", "general")
        urgency = params.get("urgency", "low")  # low, medium, high
        
        self.log_execution(f"Generating email campaign: {campaign_name}")
        
        subject_line = self._generate_subject_line(campaign_name, urgency, offer)
        preheader = self._generate_preheader(offer, urgency)
        body = self._generate_email_body(campaign_name, offer, segment)
        footer = "Unsubscribe | Update Preferences | Contact Us"
        
        email_content = {
            "subject": subject_line,
            "preheader": preheader,
            "body": body,
            "footer": footer
        }
        
        return {
            "status": "success",
            "action": "generate_email",
            "campaign_name": campaign_name,
            "segment": segment,
            "urgency": urgency,
            "email": email_content,
            "estimated_open_rate": 0.25 if urgency == "high" else 0.15,
            "estimated_ctr": 0.05
        }
    
    def _generate_social_content(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate social media content for multiple platforms
        """
        params = input_data.get("params", {})
        topic = params.get("topic", "Product")
        platforms = params.get("platforms", ["twitter", "instagram", "linkedin"])
        hashtags = params.get("hashtags", ["#innovation", "#marketing"])
        call_to_action = params.get("call_to_action", "Learn more")
        
        self.log_execution(f"Generating social content for {len(platforms)} platforms")
        
        social_posts = {}
        
        for platform in platforms:
            if platform == "twitter":
                social_posts[platform] = self._generate_twitter_post(topic, hashtags, call_to_action)
            elif platform == "instagram":
                social_posts[platform] = self._generate_instagram_caption(topic, hashtags, call_to_action)
            elif platform == "linkedin":
                social_posts[platform] = self._generate_linkedin_post(topic, call_to_action)
            elif platform == "tiktok":
                social_posts[platform] = self._generate_tiktok_script(topic, call_to_action)
            elif platform == "facebook":
                social_posts[platform] = self._generate_facebook_post(topic, hashtags, call_to_action)
        
        return {
            "status": "success",
            "action": "generate_social",
            "topic": topic,
            "platforms": platforms,
            "posts": social_posts,
            "hashtags": hashtags
        }
    
    def _generate_ad_copy(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate advertising copy for ad platforms
        """
        params = input_data.get("params", {})
        product = params.get("product", "Product")
        platforms = params.get("platforms", ["google", "facebook"])  # google, facebook, linkedin
        budget = params.get("budget", 1000)
        target_audience = params.get("target_audience", "")
        
        self.log_execution(f"Generating ad copy for: {product}")
        
        ads = {}
        
        for platform in platforms:
            if platform == "google":
                ads[platform] = self._generate_google_ads(product, target_audience)
            elif platform == "facebook":
                ads[platform] = self._generate_facebook_ads(product, target_audience)
            elif platform == "linkedin":
                ads[platform] = self._generate_linkedin_ads(product, target_audience)
        
        return {
            "status": "success",
            "action": "generate_ad",
            "product": product,
            "platforms": platforms,
            "budget": budget,
            "target_audience": target_audience,
            "ads": ads,
            "estimated_impressions": budget * 10  # rough estimate
        }
    
    def _refine_content(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Refine existing content
        """
        params = input_data.get("params", {})
        content = params.get("content", "")
        refinement_type = params.get("refinement_type", "grammar")  # grammar, tone, length, clarity
        tone = params.get("tone", "professional")
        
        self.log_execution(f"Refining content: {refinement_type}")
        
        refined_content = content  # Placeholder
        
        return {
            "status": "success",
            "action": "refine_content",
            "original_content": content,
            "refined_content": refined_content,
            "refinement_type": refinement_type,
            "tone": tone
        }
    
    # Helper methods for content generation
    
    def _generate_hook(self, topic: str, tone: str) -> str:
        """Generate opening hook for video script"""
        hooks = {
            "professional": f"Welcome to our comprehensive guide on {topic}. In the next few minutes, you'll discover...",
            "casual": f"Hey there! Ready to learn about {topic}? Let's dive in!",
            "energetic": f"Are you ready to revolutionize your {topic} game? Check this out!"
        }
        return hooks.get(tone, hooks["professional"])
    
    def _generate_body(self, topic: str, tone: str, duration: int) -> str:
        """Generate body of video script"""
        sections = max(2, duration // 20)
        body = f"Here are {sections} key points about {topic}:\n\n"
        for i in range(1, sections + 1):
            body += f"{i}. Key Point {i}: [Detailed explanation of aspect {i}]\n"
        return body
    
    def _generate_cta(self, tone: str) -> str:
        """Generate call-to-action"""
        ctas = {
            "professional": "Thank you for watching. For more information, visit our website or contact us today.",
            "casual": "That's all folks! Don't forget to like, subscribe, and hit the notification bell!",
            "energetic": "Ready to get started? Click the link below to take action NOW!"
        }
        return ctas.get(tone, ctas["professional"])
    
    def _generate_copy_body(self, product: str, benefits: list, style: str) -> str:
        """Generate marketing copy body"""
        body = f"{product} combines cutting-edge innovation with user-friendly design.\n\n"
        if benefits:
            body += "Key Benefits:\n"
            for benefit in benefits:
                body += f"• {benefit}\n"
        return body
    
    def _generate_marketing_cta(self, product: str) -> str:
        """Generate marketing call-to-action"""
        return f"Don't miss out! Get {product} today and transform your experience. Limited time offer - 20% off!"
    
    def _generate_subject_line(self, campaign: str, urgency: str, offer: str) -> str:
        """Generate email subject line"""
        if urgency == "high":
            return f"⏰ Last Chance: {offer or campaign} Ends Tonight!"
        elif urgency == "medium":
            return f"Exclusive: {offer or campaign} - Just for You"
        return f"Check Out: {offer or campaign}"
    
    def _generate_preheader(self, offer: str, urgency: str) -> str:
        """Generate email preheader"""
        if urgency == "high":
            return f"Limited time only — {offer}"
        return f"Discover what's new — {offer}"
    
    def _generate_email_body(self, campaign: str, offer: str, segment: str) -> str:
        """Generate email body"""
        greeting = f"Hello {segment.capitalize()} Subscriber,"
        body = f"{greeting}\n\nWe're excited to share {campaign} with you.\n\n"
        if offer:
            body += f"Special Offer: {offer}\n\n"
        body += "Warm regards,\nThe Team"
        return body
    
    def _generate_twitter_post(self, topic: str, hashtags: list, cta: str) -> str:
        """Generate Twitter post (280 characters)"""
        tags = " ".join(hashtags[:2])
        return f"Exciting news about {topic}! {cta} {tags}"
    
    def _generate_instagram_caption(self, topic: str, hashtags: list, cta: str) -> str:
        """Generate Instagram caption"""
        caption = f"✨ {topic}\n\n{cta}\n\n"
        caption += " ".join(hashtags)
        return caption
    
    def _generate_linkedin_post(self, topic: str, cta: str) -> str:
        """Generate LinkedIn post"""
        return f"Exploring the future of {topic}.\n\n{cta}\n\n#innovation #business #growth"
    
    def _generate_tiktok_script(self, topic: str, cta: str) -> str:
        """Generate TikTok video script"""
        return f"[0-3s] Hook about {topic}\n[3-10s] Main content\n[10-15s] {cta}\n[15s] Outro with hashtags"
    
    def _generate_facebook_post(self, topic: str, hashtags: list, cta: str) -> str:
        """Generate Facebook post"""
        return f"Join our community to learn more about {topic}!\n\n{cta}\n\n" + " ".join(hashtags)
    
    def _generate_google_ads(self, product: str, audience: str) -> Dict[str, str]:
        """Generate Google Ads copy"""
        return {
            "headline": f"Get {product} Today",
            "description": f"Designed for {audience}. Transform your experience with innovative solutions.",
            "url": "https://example.com/product"
        }
    
    def _generate_facebook_ads(self, product: str, audience: str) -> Dict[str, str]:
        """Generate Facebook Ads copy"""
        return {
            "headline": f"Discover {product}",
            "body": f"Perfect for {audience}. Join thousands of satisfied customers.",
            "cta_button": "Learn More"
        }
    
    def _generate_linkedin_ads(self, product: str, audience: str) -> Dict[str, str]:
        """Generate LinkedIn Ads copy"""
        return {
            "headline": f"{product} for {audience}",
            "description": "Unlock professional growth and innovation.",
            "cta_button": "Get Started"
        }
    
    def validate_input(self, input_data: Dict[str, Any]):
        """
        Validate input data
        """
        action = input_data.get("action")
        if not action:
            raise ValueError("Missing required field: action")
        
        valid_actions = [
            "generate_script", "generate_copy", "generate_email",
            "generate_social", "generate_ad", "refine_content"
        ]
        
        if action not in valid_actions:
            raise ValueError(f"Invalid action: {action}")

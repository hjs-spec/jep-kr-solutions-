#!/usr/bin/env python3
"""
Korea AI Basic Act - Content Labeling Example (Article 31)
=============================================================

This example demonstrates compliance with Korea's AI Basic Act transparency
obligations for generative AI content, covering:

- Article 31(1): Advance notice that service uses generative AI
- Article 31(2): Differentiated labeling based on usage scenario
  * In-app content (chatbots, games): flexible labeling (UI symbols, pre-use guidance)
  * Exported content (downloadable images/videos): strict labeling (watermark OR metadata+guidance)
  * Deepfakes: clear warning to prevent misunderstanding
  * Artistic/creative works: flexible labeling that doesn't interfere with appreciation

Based on the Transparency Guidelines (2026.1. 개정) and Article 22 of the Enforcement Decree.
"""

import json
import time
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, Union

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from ai_basic_act.implementation.kr_tracker import (
    KoreaAITracker,
    EntityType,
    ContentType,
    LabelingScenario
)


class KoreaContentLabelingSystem:
    """
    Complete content labeling system for Korean AI service providers,
    demonstrating compliance with Article 31 transparency requirements.
    
    The Korea AI Basic Act has DIFFERENTIATED requirements based on how
    the content is used and distributed:
    
    - **In-App Content**: Flexible labeling (UI symbols, login guidance)
    - **Exported Content**: Strict labeling (visible watermark OR metadata+guidance)
    - **Deepfakes**: Clear warning to prevent misunderstanding
    - **Artistic Works**: Flexible labeling that doesn't hinder appreciation
    """
    
    def __init__(self, company_name: str):
        self.company_name = company_name
        self.tracker = KoreaAITracker(
            organization=company_name,
            entity_type=EntityType.PROVIDER,
            jurisdiction="domestic"
        )
        
        self.services = []
        self.content_labels = []
        self.chatbots = []
        self.games = []
        self.images = []
        self.videos = []
        self.deepfakes = []
        self.artistic_works = []
        
        print("="*80)
        print(f"🎨 Korea AI Content Labeling System - {company_name}")
        print("="*80)
        print(f"Korea AI Basic Act Effective: January 22, 2026")
        print(f"Article 31: Transparency Obligations")
        print(f"- §31(1): Advance notice of AI use")
        print(f"- §31(2): Output labeling (differentiated by scenario)")
        print(f"- §31(3): Deepfake disclosure")
        print(f"\n📋 Differentiated Labeling Requirements:")
        print(f"   • In-app (chatbots/games): UI symbols, pre-use guidance (flexible)")
        print(f"   • Exported (downloadable): Visible watermark OR metadata+guidance (strict)")
        print(f"   • Deepfakes: Clear human-readable warning")
        print(f"   • Artistic: Flexible labeling (end credits, metadata)")
    
    # ========================================================================
    # Article 31(1): Advance Notice
    # ========================================================================
    
    def register_ai_service(self, service_data: dict) -> dict:
        """
        Article 31(1): Provide advance notice that service uses AI.
        
        Users must be informed before using AI products/services.
        This can be done through:
        - Login screen guidance
        - Terms of service disclosure
        - Onboarding messages
        """
        service_id = f"SVC-{int(time.time())}-{hash(service_data['name']) % 10000:04d}"
        
        notice = self.tracker.advance_notice({
            "service_name": service_data['name'],
            "ai_type": service_data.get('ai_type', 'generative'),
            "disclosure_method": service_data.get('disclosure_method', 'login_screen'),
            "disclosure_text": service_data.get('disclosure_text', 
                                               f"This service uses AI technology"),
            "language": "ko"
        })
        
        service = {
            "service_id": service_id,
            "name": service_data['name'],
            "type": service_data.get('type', 'chatbot'),
            "notice_id": notice['notice_id'],
            "notice_date": time.time(),
            "status": "ACTIVE"
        }
        
        self.services.append(service)
        
        print(f"\n📋 Article 31(1): AI Service Registered")
        print(f"   Service: {service['name']}")
        print(f"   Notice ID: {service['notice_id']}")
        print(f"   Disclosure: {service_data.get('disclosure_method', 'login_screen')}")
        
        return service
    
    # ========================================================================
    # Article 31(2): Scenario 1 - In-App (Flexible Labeling)
    # ========================================================================
    
    def create_chatbot(self, chatbot_data: dict) -> dict:
        """
        Create a chatbot with flexible in-app labeling.
        
        For interactive services within the app environment, labeling can be:
        - Pre-use guidance at login
        - On-screen symbol/logo (e.g., 🤖)
        - Periodic reminders
        """
        chatbot_id = f"CHAT-{int(time.time())}-{hash(chatbot_data['name']) % 10000:04d}"
        
        # Add pre-use guidance (login screen)
        if chatbot_data.get('pre_use_guidance', True):
            self.tracker.advance_notice({
                "service_name": chatbot_data['name'],
                "ai_type": "generative",
                "disclosure_method": "login_screen",
                "disclosure_text": f"{chatbot_data['name']}은(는) AI 기반 챗봇입니다. 응답은 AI에 의해 생성됩니다.",
                "language": "ko"
            })
        
        # Configure UI symbol for chat header
        label = self.tracker.label_chatbot(
            chatbot_name=chatbot_data['name'],
            disclosure_method=chatbot_data.get('disclosure_method', 'symbol')
        )
        
        chatbot = {
            "chatbot_id": chatbot_id,
            "name": chatbot_data['name'],
            "purpose": chatbot_data.get('purpose', 'customer_service'),
            "label_id": label['label_id'],
            "pre_use_guidance": chatbot_data.get('pre_use_guidance', True),
            "ui_symbol": chatbot_data.get('ui_symbol', '🤖'),
            "created_date": time.time()
        }
        
        self.chatbots.append(chatbot)
        self.content_labels.append(label)
        
        print(f"\n💬 Chatbot Created (In-App - Flexible Labeling)")
        print(f"   Name: {chatbot['name']}")
        print(f"   UI Symbol: {chatbot['ui_symbol']}")
        print(f"   Pre-Use Guidance: {chatbot['pre_use_guidance']}")
        print(f"   Label Method: UI symbol + login guidance")
        
        return chatbot
    
    def create_ai_game(self, game_data: dict) -> dict:
        """
        Create an AI-powered game with flexible in-app labeling.
        
        Games can use:
        - Login screen guidance
        - On-screen indicators for AI characters
        - Periodic reminders
        """
        game_id = f"GAME-{int(time.time())}-{hash(game_data['name']) % 10000:04d}"
        
        # Login screen guidance
        self.tracker.advance_notice({
            "service_name": game_data['name'],
            "ai_type": "generative",
            "disclosure_method": "login_screen",
            "disclosure_text": f"{game_data['name']}에는 AI 기반 캐릭터가 포함되어 있습니다.",
            "language": "ko"
        })
        
        # UI indicators for AI characters
        label = self.tracker.label_output(
            content=f"AI character in {game_data['name']}",
            content_type=ContentType.TEXT,
            scenario=LabelingScenario.IN_APP,
            exportable=False,
            metadata={
                "symbol": "🤖",
                "position": "character_header",
                "pre_use_guidance": True
            }
        )
        
        game = {
            "game_id": game_id,
            "name": game_data['name'],
            "genre": game_data.get('genre', 'rpg'),
            "ai_characters": game_data.get('ai_characters', 5),
            "label_id": label['label_id'],
            "created_date": time.time()
        }
        
        self.games.append(game)
        
        print(f"\n🎮 AI Game Created (In-App - Flexible Labeling)")
        print(f"   Name: {game['name']}")
        print(f"   AI Characters: {game['ai_characters']}")
        print(f"   Label: AI characters marked with 🤖 symbol")
        
        return game
    
    # ========================================================================
    # Article 31(2): Scenario 2 - Exported Content (Strict Labeling)
    # ========================================================================
    
    def generate_ai_image(self, prompt: str, exportable: bool = True) -> dict:
        """
        Generate AI image with appropriate labeling based on exportability.
        
        For exported/downloadable content, TWO options:
        Option A: Visible watermark (strict)
        Option B: Machine-readable metadata + user guidance (text/audio)
        """
        image_id = f"IMG-{int(time.time())}-{hash(prompt) % 10000:04d}"
        
        # Simulate image generation
        image_data = {
            "image_id": image_id,
            "prompt": prompt,
            "generator": "Korea AI ImageGen v2",
            "generation_time": time.time(),
            "resolution": "1024x1024",
            "format": "PNG",
            "exportable": exportable
        }
        
        if exportable:
            # Option A: Visible watermark (strict labeling)
            watermark = self.tracker.add_visible_watermark(
                content=f"sample image data for {image_id}".encode(),
                watermark_text="AI 생성",
                position="bottom_right",
                opacity=0.7,
                permanent=True
            )
            
            image_data["label_method"] = "visible_watermark"
            image_data["watermark_id"] = watermark["watermark_id"]
            image_data["watermark_text"] = "AI 생성"
            
        else:
            # Option B: Metadata + guidance (still compliant)
            label = self.tracker.label_output(
                content=f"sample image data for {image_id}".encode(),
                content_type=ContentType.IMAGE,
                scenario=LabelingScenario.EXPORTED,
                exportable=False,
                metadata={
                    "model": "image-gen-v2",
                    "guidance_text": "This image was created by AI",
                    "guidance_audio": "guidance.mp3"
                }
            )
            
            image_data["label_method"] = "metadata_plus_guidance"
            image_data["label_id"] = label["label_id"]
        
        self.images.append(image_data)
        
        print(f"\n🖼️ AI Image Generated")
        print(f"   Image ID: {image_id}")
        print(f"   Exportable: {exportable}")
        print(f"   Label Method: {image_data['label_method']}")
        if exportable:
            print(f"   Watermark: 'AI 생성' (visible)")
        else:
            print(f"   Metadata + Guidance embedded")
        
        return image_data
    
    def generate_ai_video(self, prompt: str, duration: int, exportable: bool = True) -> dict:
        """
        Generate AI video with appropriate labeling.
        
        Videos have same strict requirements as images for exported content.
        """
        video_id = f"VID-{int(time.time())}-{hash(prompt) % 10000:04d}"
        
        video_data = {
            "video_id": video_id,
            "prompt": prompt,
            "duration_seconds": duration,
            "generator": "Korea AI VideoGen v1",
            "generation_time": time.time(),
            "resolution": "1920x1080",
            "format": "MP4",
            "exportable": exportable
        }
        
        if exportable:
            # For exported videos, watermark must be visible throughout
            watermark = self.tracker.add_visible_watermark(
                content=f"sample video data for {video_id}".encode(),
                watermark_text="AI 생성",
                position="top_left",
                opacity=0.6,
                permanent=True
            )
            
            video_data["label_method"] = "visible_watermark"
            video_data["watermark_id"] = watermark["watermark_id"]
        
        self.videos.append(video_data)
        
        print(f"\n🎬 AI Video Generated")
        print(f"   Video ID: {video_id}")
        print(f"   Duration: {duration}s")
        print(f"   Exportable: {exportable}")
        if exportable:
            print(f"   Watermark: 'AI 생성' visible throughout")
        
        return video_data
    
    # ========================================================================
    # Article 31(3): Deepfake Content
    # ========================================================================
    
    def create_deepfake_video(
        self,
        source_person: str,
        target_speech: str,
        consent_obtained: bool = True
    ) -> dict:
        """
        Create deepfake video simulating a real person.
        
        Deepfakes require:
        - Clear warning to prevent misunderstanding
        - Warning must be human-readable and prominent
        - Consent from person being simulated (required by law)
        """
        deepfake_id = f"DF-{int(time.time())}-{hash(source_person) % 10000:04d}"
        
        if not consent_obtained:
            raise ValueError("Consent required for deepfake creation under Korea AI Basic Act")
        
        # Add prominent deepfake warning (Article 31(3))
        warning = self.tracker.add_deepfake_warning(
            content=f"sample deepfake video for {deepfake_id}".encode(),
            content_type="video",
            warning_text="⚠️ 딥페이크: 실제 인물을 모방한 AI 생성 콘텐츠",
            duration="entire_video"
        )
        
        deepfake = {
            "deepfake_id": deepfake_id,
            "source_person": source_person,
            "target_speech": target_speech,
            "generator": "Korea AI DeepSync v2",
            "generation_time": time.time(),
            "consent_obtained": consent_obtained,
            "warning_id": warning["warning_id"],
            "warning_text": warning["warning_text"],
            "duration_seconds": len(target_speech.split()) // 3,
            "format": "MP4"
        }
        
        self.deepfakes.append(deepfake)
        
        print(f"\n⚠️ DEEPFAKE Created - Article 31(3) Compliance")
        print(f"   Deepfake ID: {deepfake_id}")
        print(f"   Source Person: {source_person}")
        print(f"   Warning: {deepfake['warning_text']}")
        print(f"   Duration: Entire video")
        print(f"   Consent Obtained: {consent_obtained}")
        
        return deepfake
    
    def create_deepfake_image(
        self,
        source_person: str,
        scene_description: str,
        consent_obtained: bool = True
    ) -> dict:
        """
        Create deepfake image simulating a real person.
        """
        deepfake_id = f"DF-IMG-{int(time.time())}-{hash(source_person) % 10000:04d}"
        
        if not consent_obtained:
            raise ValueError("Consent required for deepfake creation")
        
        # Add visible watermark with warning
        warning = self.tracker.add_deepfake_warning(
            content=f"sample deepfake image for {deepfake_id}".encode(),
            content_type="image",
            warning_text="⚠️ 딥페이크 이미지",
            duration="permanent"
        )
        
        deepfake = {
            "deepfake_id": deepfake_id,
            "source_person": source_person,
            "scene_description": scene_description,
            "generator": "Korea AI FaceSwap v3",
            "generation_time": time.time(),
            "consent_obtained": consent_obtained,
            "warning_id": warning["warning_id"],
            "warning_text": "⚠️ 딥페이크 이미지"
        }
        
        self.deepfakes.append(deepfake)
        
        print(f"\n⚠️ DEEPFAKE Image Created")
        print(f"   Warning text: '⚠️ 딥페이크 이미지' (permanent)")
        
        return deepfake
    
    # ========================================================================
    # Article 31(2) Exception: Artistic/Creative Works
    # ========================================================================
    
    def create_ai_film(self, title: str, director: str, ai_generated_scenes: list) -> dict:
        """
        Create a film with AI-generated scenes (artistic exception).
        
        Artistic works may use flexible labeling that doesn't interfere with
        artistic appreciation, such as:
        - End credits disclosure
        - Metadata
        - Festival program notes
        """
        film_id = f"FILM-{int(time.time())}-{hash(title) % 10000:04d}"
        
        # Use creative/artistic labeling (end credits)
        label = self.tracker.label_output(
            content=f"Film: {title}",
            content_type=ContentType.VIDEO,
            scenario=LabelingScenario.ARTISTIC,
            exportable=True,  # Still exportable but artistic exception applies
            metadata={
                "disclosure_method": "end_credits",
                "disclosure_text": "이 영화는 AI 생성 장면을 포함합니다",
                "disclosure_position": "end"
            }
        )
        
        film = {
            "film_id": film_id,
            "title": title,
            "director": director,
            "ai_generated_scenes": ai_generated_scenes,
            "label_id": label["label_id"],
            "disclosure_method": "end_credits",
            "disclosure_text": "이 영화는 AI 생성 장면을 포함합니다",
            "generation_time": time.time()
        }
        
        self.artistic_works.append(film)
        
        print(f"\n🎬 AI Film Created (Artistic Exception)")
        print(f"   Title: {title}")
        print(f"   Director: {director}")
        print(f"   AI Scenes: {len(ai_generated_scenes)}")
        print(f"   Disclosure: End credits (doesn't interfere with viewing)")
        
        return film
    
    def create_ai_music_video(self, song_title: str, artist: str, ai_visuals: bool) -> dict:
        """
        Create music video with AI-generated visuals (artistic exception).
        """
        mv_id = f"MV-{int(time.time())}-{hash(song_title) % 10000:04d}"
        
        # Use metadata + description (appropriate for music video)
        label = self.tracker.label_output(
            content=f"Music Video: {song_title}",
            content_type=ContentType.VIDEO,
            scenario=LabelingScenario.ARTISTIC,
            exportable=True,
            metadata={
                "disclosure_method": "description",
                "disclosure_text": f"{song_title} 뮤직비디오는 AI 생성 비주얼을 포함합니다",
                "metadata_included": True
            }
        )
        
        mv = {
            "mv_id": mv_id,
            "song_title": song_title,
            "artist": artist,
            "ai_visuals": ai_visuals,
            "label_id": label["label_id"],
            "disclosure_method": "description",
            "generation_time": time.time()
        }
        
        self.artistic_works.append(mv)
        
        print(f"\n🎵 Music Video Created (Artistic Exception)")
        print(f"   Song: {song_title}")
        print(f"   Artist: {artist}")
        print(f"   Disclosure: Video description")
        
        return mv
    
    # ========================================================================
    # Verification
    # ========================================================================
    
    def verify_content_origin(self, content_id: str) -> dict:
        """
        Verify the origin of content (for regulator inquiries).
        """
        print(f"\n🔍 Verifying Content Origin: {content_id}")
        
        # Search in all content collections
        content = None
        for collection in [self.images, self.videos, self.deepfakes, self.artistic_works]:
            for item in collection:
                if (item.get("image_id") == content_id or 
                    item.get("video_id") == content_id or
                    item.get("deepfake_id") == content_id or
                    item.get("film_id") == content_id):
                    content = item
                    break
        
        if not content:
            return {"error": "Content not found"}
        
        verification = {
            "content_id": content_id,
            "verified": True,
            "timestamp": time.time(),
            "provider": self.company_name,
            "is_ai_generated": True,
            "content_type": "unknown",
            "labeling_compliant": True
        }
        
        # Add specific details based on content type
        if "watermark_id" in content:
            verification["label_method"] = "visible_watermark"
            verification["watermark_text"] = content.get("watermark_text", "AI 생성")
        elif "warning_id" in content:
            verification["label_method"] = "deepfake_warning"
            verification["warning_text"] = content.get("warning_text")
            verification["warning"] = "⚠️ DEEPFAKE - Simulates real person"
        elif "label_id" in content:
            verification["label_method"] = "flexible"
        
        print(f"   AI Generated: {verification['is_ai_generated']}")
        print(f"   Label Method: {verification.get('label_method', 'unknown')}")
        if "warning" in verification:
            print(f"   ⚠️ {verification['warning']}")
        
        return verification
    
    def run_demo(self):
        """Run complete content labeling demonstration."""
        
        print("\n" + "="*80)
        print("📋 DEMO 1: Article 31(1) - Advance Notice")
        print("="*80)
        
        # Register AI services with advance notice
        self.register_ai_service({
            "name": "Korea AI Chat",
            "type": "chatbot",
            "disclosure_method": "login_screen"
        })
        
        print("\n" + "="*80)
        print("💬 DEMO 2: Article 31(2) - In-App (Flexible Labeling)")
        print("="*80)
        
        # Create chatbot (in-app, flexible)
        self.create_chatbot({
            "name": "Korea Bank Assistant",
            "purpose": "customer_service",
            "ui_symbol": "🤖"
        })
        
        # Create AI game (in-app, flexible)
        self.create_ai_game({
            "name": "AI Adventure RPG",
            "genre": "rpg",
            "ai_characters": 8
        })
        
        print("\n" + "="*80)
        print("🖼️ DEMO 3: Article 31(2) - Exported Content (Strict Labeling)")
        print("="*80)
        
        # Generate exportable image (must have visible watermark)
        self.generate_ai_image("Beautiful Korean mountain landscape", exportable=True)
        
        # Generate non-exportable image (metadata+guidance is acceptable)
        self.generate_ai_image("Cat playing with yarn", exportable=False)
        
        # Generate exportable video
        self.generate_ai_video("Travel guide to Seoul", 30, exportable=True)
        
        print("\n" + "="*80)
        print("⚠️ DEMO 4: Article 31(3) - Deepfake Content")
        print("="*80)
        
        # Create deepfake video with warning
        self.create_deepfake_video(
            source_person="Kim Min-jae (actor)",
            target_speech="안녕하세요, 이것은 AI가 생성한 딥페이크 영상입니다.",
            consent_obtained=True
        )
        
        # Create deepfake image with warning
        self.create_deepfake_image(
            source_person="Lee Ji-eun (singer)",
            scene_description="At award ceremony",
            consent_obtained=True
        )
        
        print("\n" + "="*80)
        print("🎬 DEMO 5: Artistic Exception (Article 31(2) Exception)")
        print("="*80")
        
        # Create film with AI scenes (artistic exception - end credits)
        self.create_ai_film(
            title="푸른 숲",
            director="박찬욱",
            ai_generated_scenes=["Scene 5: Fantasy sequence", "Scene 12: Dream sequence"]
        )
        
        # Create music video with AI visuals (artistic exception - description)
        self.create_ai_music_video(
            song_title="봄날",
            artist="BTS",
            ai_visuals=True
        )
        
        print("\n" + "="*80)
        print("🔍 DEMO 6: Content Verification")
        print("="*80")
        
        # Verify a deepfake
        if self.deepfakes:
            self.verify_content_origin(self.deepfakes[0]["deepfake_id"])
        
        # Verify an exported image
        if self.images:
            self.verify_content_origin(self.images[0]["image_id"])
        
        print("\n" + "="*80)
        print("📊 Compliance Summary")
        print("="*80")
        print(f"   Services Registered: {len(self.services)}")
        print(f"   In-App Content: {len(self.chatbots) + len(self.games)}")
        print(f"   Exported Images/Videos: {len(self.images) + len(self.videos)}")
        print(f"   Deepfakes (with warnings): {len(self.deepfakes)}")
        print(f"   Artistic Works: {len(self.artistic_works)}")
        
        print(f"\n📋 Article 31 Compliance Status:")
        print(f"   ✅ §31(1) Advance Notice: Implemented")
        print(f"   ✅ §31(2) In-App (Flexible): UI symbols + pre-use guidance")
        print(f"   ✅ §31(2) Exported (Strict): Visible watermarks")
        print(f"   ✅ §31(2) Artistic Exception: End credits/description")
        print(f"   ✅ §31(3) Deepfake Warnings: Prominent and clear")
        
        # Generate tracker report
        report = self.tracker.generate_compliance_report()
        
        return report


if __name__ == "__main__":
    system = KoreaContentLabelingSystem("Kakao AI")
    report = system.run_demo()
    
    # Save report
    with open("korea_content_labeling_report.json", "w") as f:
        json.dump(report, f, indent=2, default=str)
    print(f"\n✅ Report saved: korea_content_labeling_report.json")

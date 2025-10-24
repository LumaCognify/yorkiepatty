#!/usr/bin/env python3
# ======================================================
# Derek Alpha Main - Simplified Single Environment
# TensorFlow Mode with Optional Vision
# ======================================================

import sys
import logging
import os
from pathlib import Path
from typing import Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import boto3

# ------------------------------------------------------
# PROJECT ROOT
# ------------------------------------------------------
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# ======================================================
# CONFIGURATION
# ======================================================
ENABLE_VISION = os.getenv("DEREK_VISION", "false").lower() == "true"
DEREK_MODE = os.getenv("DEREK_MODE", "tensorflow")

print(f"🧬 Derek Mode: {DEREK_MODE}")
print(f"👁️  Vision: {'Enabled' if ENABLE_VISION else 'Disabled'}")

# ======================================================
# LOAD DEREK CONSCIOUSNESS
# ======================================================
from derek_module_loader import load_derek_consciousness, get_derek_loader

print("🚀 Initializing Derek's Complete Consciousness...")
derek_loader = load_derek_consciousness()
print(f"✅ Derek Consciousness Loaded: {derek_loader.get_stats()['loaded']} modules active")

# ------------------------------------------------------
# MODULE INJECTION
# ------------------------------------------------------
perplexity_service_module = derek_loader.get_module('perplexity_service')
memory_engine_module = derek_loader.get_module('memory_engine')
conversation_engine_module = derek_loader.get_module('conversation_engine')
brain_module = derek_loader.get_module('brain')
derek_ultimate_voice_module = derek_loader.get_module('derek_ultimate_voice')
memory_mesh_bridge_module = derek_loader.get_module('memory_mesh_bridge')

# Load vision only if enabled
vision_engine_module = derek_loader.get_module('vision_engine') if ENABLE_VISION else None

PerplexityService = getattr(perplexity_service_module, "PerplexityService", None)
MemoryEngine = getattr(memory_engine_module, "MemoryEngine", None)
ConversationEngine = getattr(conversation_engine_module, "ConversationEngine", None)
Derek = getattr(brain_module, "Derek", None)
DerekUltimateVoice = getattr(derek_ultimate_voice_module, "DerekUltimateVoice", None)
MemoryMeshBridge = getattr(memory_mesh_bridge_module, "MemoryMeshBridge", None)

# ------------------------------------------------------
# LOGGING CONFIG
# ------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("derek_dashboard.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# ------------------------------------------------------
# FASTAPI APP
# ------------------------------------------------------
app = FastAPI(
    title="Derek Dashboard",
    description="AI COO for The Christman AI Project"
)

# ------------------------------------------------------
# CORE INITIALIZATION
# ------------------------------------------------------
try:
    derek_ultimate_voice = DerekUltimateVoice(ai_provider="auto", voice_id="matthew") if DerekUltimateVoice else None
    memory = MemoryMeshBridge(memory_dir="./derek_memory") if MemoryMeshBridge else None
    logger.info("✅ Derek Core Modules initialized successfully")
except Exception as e:
    logger.error(f"❌ Initialization failure: {str(e)}")
    derek_ultimate_voice, memory = None, None

# ------------------------------------------------------
# MODELS
# ------------------------------------------------------
class TTSRequest(BaseModel):
    text: str
    voice: Optional[str] = "matthew"
    speed: Optional[float] = 1.0

# ------------------------------------------------------
# MAIN DASHBOARD CLASS
# ------------------------------------------------------
class DerekDashboard:
    def __init__(self):
        logger.info("=" * 60)
        logger.info("🚀 Initializing Derek Dashboard")
        logger.info("The Christman AI Project - AI That Empowers")
        logger.info("=" * 60)

        self.memory_engine: Optional[MemoryEngine] = None
        self.conversation_engine: Optional[ConversationEngine] = None
        self.perplexity_service: Optional[PerplexityService] = None
        self.derek: Optional[Derek] = None
        self.derek_ultimate_voice = derek_ultimate_voice
        self.memory = memory
        self.vision = None  # Vision disabled by default

        try:
            self.derek = Derek(file_path="./memory/memory_store.json")
        except Exception as e:
            logger.error(f"Derek initialization failed: {str(e)}")
            self.derek = None

        if PerplexityService:
            try:
                self.perplexity_service = PerplexityService()
                logger.info("✅ Perplexity Service ready")
            except Exception as e:
                logger.warning(f"Perplexity unavailable: {e}")

        if MemoryEngine:
            try:
                self.memory_engine = MemoryEngine()
                logger.info("✅ Memory Engine ready")
            except Exception as e:
                logger.warning(f"Memory Engine unavailable: {e}")

        if ConversationEngine:
            try:
                self.conversation_engine = ConversationEngine()
                logger.info("✅ Conversation Engine ready")
            except Exception as e:
                logger.warning(f"Conversation Engine unavailable: {e}")

    def start(self):
        logger.info("🎯 Derek Dashboard is now active")
        
        if self.derek_ultimate_voice:
            try:
                greeting = "Hello, I am Derek, ready to assist you."
                logger.info(f"🗣️ Derek: {greeting}")
                if hasattr(self.derek_ultimate_voice, 'speak'):
                    self.derek_ultimate_voice.speak(greeting)
            except Exception as e:
                logger.warning(f"Failed to speak greeting: {e}")

    def process_message(self, message: str):
        if not self.derek:
            return "System not ready."
        try:
            response = self.derek.think(message)
            final_text = response.get("response", "[No output]")
            if self.memory:
                try:
                    self.memory.store({
                        "category": "conversation",
                        "content": f"{message[:50]} -> {final_text[:50]}",
                        "importance": 0.7,
                        "metadata": {"timestamp": datetime.now().isoformat()}
                    })
                except Exception as e:
                    logger.debug(f"Memory store failed: {e}")
            return final_text
        except Exception as e:
            logger.error(f"Error during message processing: {str(e)}")
            return "Error processing message."

    def stop(self):
        logger.info("🧠 Shutting down Derek Dashboard services...")
        try:
            if self.memory_engine: self.memory_engine.save()
            if self.memory: self.memory.save()
            if self.vision: self.vision.stop()
        except Exception as e:
            logger.error(f"Error saving memory on shutdown: {str(e)}")
        logger.info("🛑 Derek Dashboard stopped cleanly.")

# ------------------------------------------------------
# MAIN EXECUTION
# ------------------------------------------------------
def main():
    dashboard = None
    try:
        dashboard = DerekDashboard()
        dashboard.start()
        print("\n🎤 Derek Speech-to-Speech Mode Active")
        print("🗣️ Say something to Derek, 'goodbye' to exit")
        print("=" * 50)

        import speech_recognition as sr
        recognizer = sr.Recognizer()

        print("🎙️ Initializing microphone...")
        try:
            mic_list = sr.Microphone.list_microphone_names()
            print(f"Available microphones: {mic_list}")
            mic_index = 2 # iMac Microphone
            mic = sr.Microphone(device_index=mic_index)
            print(f"✅ Using microphone: {mic_list[mic_index]}")
        except Exception as e:
            print(f"❌ Microphone initialization failed: {e}")
            mic = None

        if mic:
            with mic as source:
                print("🔧 Calibrating microphone...")
                recognizer.adjust_for_ambient_noise(source, duration=3)
                print("✅ Microphone ready")
        else:
            print("⚠️ No working microphone found, switching to text input mode.")

        while True:
            if mic:
                with mic as source:
                    print("\n👂 Listening...")
                    audio = recognizer.listen(source, timeout=15, phrase_time_limit=40)
                try:
                    text = recognizer.recognize_google(audio)
                    print(f"🧑 You said: {text}")
                except Exception as e:
                    print(f"❌ Speech recognition error: {e}")
                    continue
            else:
                text = input("\n🧑 You: ").strip()

            if any(word in text.lower() for word in ["goodbye", "exit", "quit", "stop"]):
                msg = "Goodbye! See you next time."
                print(f"👋 Derek: {msg}")
                if dashboard.derek_ultimate_voice:
                    dashboard.derek_ultimate_voice.speak(msg)
                break

            response = dashboard.process_message(text)
            print(f"🤖 Derek: {response}")

    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
    finally:
        if dashboard:
            dashboard.stop()

if __name__ == "__main__":
    main()

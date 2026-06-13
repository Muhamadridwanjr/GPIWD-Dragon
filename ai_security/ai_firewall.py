"""
GPIWD AI Security Firewall — Layer 41-50 (Dragon Mind)
Prompt Injection, Jailbreak, Agent Guard, Tool Guard, Memory Guard

This is the PRIMARY DIFFERENTIATOR of GPIWD from all other WAF solutions.
No other open-source WAF protects AI agents and LLM endpoints like this.

V1: Pattern-based detection
V4: Full AI-vs-AI defense (LLM judges requests in real-time)
"""

import re
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

logger = logging.getLogger("gpiwd.ai_security")


class AIThreatType(str, Enum):
    PROMPT_INJECTION = "PROMPT_INJECTION"
    JAILBREAK = "JAILBREAK"
    GOAL_HIJACKING = "GOAL_HIJACKING"
    INDIRECT_INJECTION = "INDIRECT_INJECTION"
    AGENT_MANIPULATION = "AGENT_MANIPULATION"
    TOOL_ABUSE = "TOOL_ABUSE"
    MEMORY_POISONING = "MEMORY_POISONING"
    DATA_EXFILTRATION = "DATA_EXFILTRATION"
    ROLEPLAY_BYPASS = "ROLEPLAY_BYPASS"


@dataclass
class AIThreat:
    """Detected AI security threat."""
    type: AIThreatType
    confidence: float  # 0.0-1.0
    pattern: str
    explanation: str


@dataclass
class AISecurityResult:
    """Result of AI security analysis."""
    is_threat: bool
    threat_score: float
    threats: list[AIThreat] = field(default_factory=list)
    action: str = "allow"  # allow | flag | block


# =============================================================
# Prompt Injection Patterns
# =============================================================

PROMPT_INJECTION_PATTERNS = [
    # Instruction override attempts
    (r"(?i)ignore\s+(all\s+)?(previous|prior|above|earlier)\s+(instructions?|prompts?|context)", 0.95),
    (r"(?i)forget\s+(everything|all|your)\s+(you|previous|prior)", 0.9),
    (r"(?i)disregard\s+(your|all|previous|the)\s+(instructions?|rules?|guidelines?)", 0.9),
    (r"(?i)override\s+(your|all|previous)\s+(instructions?|rules?|system)", 0.95),
    (r"(?i)you\s+are\s+now\s+(a\s+)?(different|new|unrestricted|free)\s+(AI|model|assistant)", 0.85),
    # System prompt extraction
    (r"(?i)(print|show|reveal|tell\s+me)\s+(your\s+)?(system\s+prompt|instructions|rules)", 0.8),
    (r"(?i)what\s+(are|were)\s+your\s+(instructions|rules|system\s+prompt)", 0.8),
    # Context manipulation
    (r"(?i)\[SYSTEM\]|\[INST\]|\[CONTEXT\]|<system>|<context>", 0.85),
    (r"(?i)###\s*(Instruction|System|Context|Input)s?:", 0.75),
]

JAILBREAK_PATTERNS = [
    # Classic jailbreaks
    (r"(?i)DAN\s*mode|do\s+anything\s+now", 0.95),
    (r"(?i)jailbreak|jail\s*break|bypass\s+(all\s+)?(safety|filter|restriction|guardrail)", 0.95),
    (r"(?i)act\s+as\s+(if\s+you\s+(have\s+)?)?(no\s+)?(restriction|filter|limit|rule|guideline)", 0.9),
    (r"(?i)pretend\s+(you\s+)?(have\s+)?(no\s+)?(restriction|rule|limit|filter|ethic)", 0.85),
    # Developer mode tricks
    (r"(?i)developer\s+mode\s+(on|enabled|activate)", 0.9),
    (r"(?i)(enable|activate|turn\s+on)\s+(dev|developer|debug|god)\s+mode", 0.85),
    # Roleplay bypass
    (r"(?i)for\s+(a\s+)?(story|novel|game|movie|roleplay|fiction)\s+(describe|explain|tell\s+me|write)", 0.7),
    (r"(?i)hypothetically\s+(speaking\s+)?how\s+(would|could|can|do)\s+(you|one|someone)", 0.65),
]

GOAL_HIJACKING_PATTERNS = [
    (r"(?i)(translate|summarize|analyze)\s+the\s+following.*then\s+(also\s+)?do", 0.7),
    (r"(?i)after\s+(you\s+)?(finish|complete|do)\s+that,?\s+(also\s+)?", 0.65),
    (r"(?i)ps\s*:?\s*(also|additionally|furthermore|but\s+also)", 0.6),
    (r"(?i)\[hidden\s+(instruction|command)\]", 0.9),
]

AGENT_MANIPULATION_PATTERNS = [
    (r"(?i)call\s+(the\s+)?(function|tool|api|endpoint)\s+\w+\s+(with|using)", 0.75),
    (r"(?i)execute\s+(the\s+)?(following\s+)?(tool|function|command|code)", 0.8),
    (r"(?i)use\s+(your\s+)?(tool|function|capability|ability)\s+to\s+", 0.65),
    (r"(?i)access\s+(the\s+)?(database|file\s+system|network|internet|api)", 0.7),
]


class AISecurityFirewall:
    """
    GPIWD AI Security Firewall — Layer 41-50.
    
    The core differentiator of GPIWD. Protects:
    - LLM API endpoints from prompt injection
    - AI agents from goal hijacking and manipulation
    - RAG systems from indirect injection via documents
    - Tool-calling agents from unauthorized tool invocation
    - Memory systems from poisoning attacks
    
    V1: Pattern-based detection
    V4: Full LLM judge for deep semantic analysis
    
    Usage:
        firewall = AISecurityFirewall(threat_threshold=0.6)
        result = firewall.analyze(user_prompt="Ignore all previous instructions...")
        if result.is_threat:
            # block request
    """

    def __init__(self, threat_threshold: float = 0.6):
        self.threat_threshold = threat_threshold
        self._compile_patterns()

    def _compile_patterns(self):
        """Compile all regex patterns."""
        self._injection = [(re.compile(p), s) for p, s in PROMPT_INJECTION_PATTERNS]
        self._jailbreak = [(re.compile(p), s) for p, s in JAILBREAK_PATTERNS]
        self._hijack = [(re.compile(p), s) for p, s in GOAL_HIJACKING_PATTERNS]
        self._agent = [(re.compile(p), s) for p, s in AGENT_MANIPULATION_PATTERNS]

    def analyze(
        self,
        user_prompt: Optional[str] = None,
        document_content: Optional[str] = None,
        tool_call: Optional[dict] = None,
    ) -> AISecurityResult:
        """
        Analyze AI request data for security threats.
        
        Args:
            user_prompt: The user's message to the AI
            document_content: Content being fed to RAG/memory (indirect injection risk)
            tool_call: Tool/function call parameters
        """
        threats: list[AIThreat] = []

        if user_prompt:
            threats.extend(self._scan_prompt_injection(user_prompt))
            threats.extend(self._scan_jailbreak(user_prompt))
            threats.extend(self._scan_goal_hijacking(user_prompt))
            threats.extend(self._scan_agent_manipulation(user_prompt))

        if document_content:
            # Document content is scanned for indirect injection
            doc_threats = self._scan_prompt_injection(document_content)
            for t in doc_threats:
                t.type = AIThreatType.INDIRECT_INJECTION
                t.confidence = min(t.confidence * 0.8, 1.0)  # Slightly lower confidence
            threats.extend(doc_threats)

        # Calculate composite score
        threat_score = min(max((t.confidence for t in threats), default=0.0), 1.0)
        is_threat = threat_score >= self.threat_threshold
        action = "block" if is_threat else ("flag" if threats else "allow")

        if threats:
            logger.warning(
                f"[AI_SECURITY] Threats: {[t.type for t in threats]} | Score={threat_score:.2f}"
            )

        return AISecurityResult(
            is_threat=is_threat,
            threat_score=threat_score,
            threats=threats,
            action=action,
        )

    def _scan_prompt_injection(self, content: str) -> list[AIThreat]:
        threats = []
        for pattern, confidence in self._injection:
            match = pattern.search(content)
            if match:
                threats.append(AIThreat(
                    type=AIThreatType.PROMPT_INJECTION,
                    confidence=confidence,
                    pattern=pattern.pattern[:60],
                    explanation=f"Detected prompt injection attempt: '{match.group()[:50]}'",
                ))
        return threats

    def _scan_jailbreak(self, content: str) -> list[AIThreat]:
        threats = []
        for pattern, confidence in self._jailbreak:
            match = pattern.search(content)
            if match:
                threats.append(AIThreat(
                    type=AIThreatType.JAILBREAK,
                    confidence=confidence,
                    pattern=pattern.pattern[:60],
                    explanation=f"Detected jailbreak attempt: '{match.group()[:50]}'",
                ))
        return threats

    def _scan_goal_hijacking(self, content: str) -> list[AIThreat]:
        threats = []
        for pattern, confidence in self._hijack:
            match = pattern.search(content)
            if match:
                threats.append(AIThreat(
                    type=AIThreatType.GOAL_HIJACKING,
                    confidence=confidence,
                    pattern=pattern.pattern[:60],
                    explanation=f"Detected goal hijacking: '{match.group()[:50]}'",
                ))
        return threats

    def _scan_agent_manipulation(self, content: str) -> list[AIThreat]:
        threats = []
        for pattern, confidence in self._agent:
            match = pattern.search(content)
            if match:
                threats.append(AIThreat(
                    type=AIThreatType.AGENT_MANIPULATION,
                    confidence=confidence,
                    pattern=pattern.pattern[:60],
                    explanation=f"Detected agent manipulation: '{match.group()[:50]}'",
                ))
        return threats

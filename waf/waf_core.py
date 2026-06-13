"""
GPIWD WAF Core — Layer 31-40
Web Application Firewall: SQLi, XSS, SSRF, RCE, Path Traversal

The WAF Core module scans incoming request payloads for known attack patterns.
Uses both regex pattern matching and heuristic scoring.
"""

import re
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

logger = logging.getLogger("gpiwd.waf")


class ThreatType(str, Enum):
    SQLI = "SQL_INJECTION"
    XSS = "CROSS_SITE_SCRIPTING"
    SSRF = "SERVER_SIDE_REQUEST_FORGERY"
    RCE = "REMOTE_CODE_EXECUTION"
    PATH_TRAVERSAL = "PATH_TRAVERSAL"
    COMMAND_INJECTION = "COMMAND_INJECTION"
    XXE = "XML_EXTERNAL_ENTITY"
    SSTI = "SERVER_SIDE_TEMPLATE_INJECTION"


@dataclass
class WAFThreat:
    """A detected threat from WAF analysis."""
    type: ThreatType
    pattern: str
    location: str  # "query", "body", "header", "path"
    severity: float  # 0.0-1.0


@dataclass
class WAFResult:
    """Result of WAF analysis."""
    is_malicious: bool
    threat_score: float
    threats: list[WAFThreat] = field(default_factory=list)
    action: str = "allow"  # allow | flag | block


# =============================================================
# Attack Patterns
# =============================================================

SQLI_PATTERNS = [
    r"(?i)(SELECT|INSERT|UPDATE|DELETE|DROP|TRUNCATE|ALTER|CREATE|EXEC|UNION)\s+",
    r"(?i)(\bOR\b|\bAND\b)\s+[\w\s]*=[\w\s]*",
    r"(?i)('|\")(\s*(OR|AND)\s*['\"]?\w+['\"]?\s*(=|LIKE)\s*['\"]?\w+)",
    r"(?i)(--|#|/\*)",
    r"(?i)1\s*=\s*1",
    r"(?i)\bHAVING\b",
    r"(?i)SLEEP\s*\(",
    r"(?i)BENCHMARK\s*\(",
    r"(?i)WAITFOR\s+DELAY",
]

XSS_PATTERNS = [
    r"(?i)<\s*script[^>]*>",
    r"(?i)javascript\s*:",
    r"(?i)on\w+\s*=\s*['\"]?[^'\"]*['\"]?",
    r"(?i)<\s*iframe[^>]*>",
    r"(?i)document\s*\.\s*(cookie|location|write)",
    r"(?i)window\s*\.\s*(location|open)",
    r"(?i)eval\s*\(",
    r"(?i)alert\s*\(",
    r"(?i)data\s*:\s*text/html",
    r"(?i)<\s*img[^>]+src\s*=\s*['\"]?javascript",
]

SSRF_PATTERNS = [
    r"(?i)(http|https|ftp|file|dict|gopher|ldap)\s*://\s*(localhost|127\.|0\.0\.0\.0|169\.254|::1|10\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[01])\.)",
    r"(?i)(http|https)://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",
    r"(?i)metadata\.google\.internal",
    r"(?i)169\.254\.169\.254",  # AWS metadata
]

RCE_PATTERNS = [
    r"(?i)\b(exec|system|passthru|shell_exec|popen|proc_open)\s*\(",
    r"(?i)(;|\||\|\||\&\&)\s*(ls|cat|id|whoami|pwd|uname|wget|curl|bash|sh)",
    r"(?i)\$\{.*\}",  # Template injection
    r"(?i)`[^`]+`",   # Backtick command execution
]

PATH_TRAVERSAL_PATTERNS = [
    r"\.\./",
    r"\.\.\\",
    r"%2e%2e%2f",
    r"%252e%252e%252f",
    r"(?i)\.\./\.\./",
    r"(?i)/etc/passwd",
    r"(?i)/etc/shadow",
    r"(?i)/proc/self",
    r"(?i)win32|system32",
]


class WAFCore:
    """
    GPIWD WAF Core — Layer 31-40.
    
    Scans request data for SQL injection, XSS, SSRF, RCE, and path traversal.
    
    Usage:
        waf = WAFCore(threat_threshold=0.6)
        result = waf.analyze(
            query_params="id=1' OR 1=1--",
            body='{"name": "<script>alert(1)</script>"}',
        )
        if result.is_malicious:
            # block request
    """

    def __init__(self, threat_threshold: float = 0.6):
        self.threat_threshold = threat_threshold
        self._compile_patterns()

    def _compile_patterns(self):
        """Compile all regex patterns for performance."""
        self._sqli = [re.compile(p) for p in SQLI_PATTERNS]
        self._xss = [re.compile(p) for p in XSS_PATTERNS]
        self._ssrf = [re.compile(p) for p in SSRF_PATTERNS]
        self._rce = [re.compile(p) for p in RCE_PATTERNS]
        self._path = [re.compile(p) for p in PATH_TRAVERSAL_PATTERNS]

    def analyze(
        self,
        query_params: Optional[str] = None,
        body: Optional[str] = None,
        headers: Optional[dict] = None,
        path: Optional[str] = None,
    ) -> WAFResult:
        """
        Analyze request data for threats.
        Returns WAFResult with threat assessment.
        """
        threats: list[WAFThreat] = []

        # Scan each input source
        inputs = {
            "query": query_params or "",
            "body": body or "",
            "path": path or "",
        }

        for location, content in inputs.items():
            if not content:
                continue
            threats.extend(self._scan_sqli(content, location))
            threats.extend(self._scan_xss(content, location))
            threats.extend(self._scan_ssrf(content, location))
            threats.extend(self._scan_rce(content, location))
            threats.extend(self._scan_path_traversal(content, location))

        # Calculate composite threat score
        threat_score = min(sum(t.severity for t in threats), 1.0)
        is_malicious = threat_score >= self.threat_threshold
        action = "block" if is_malicious else ("flag" if threats else "allow")

        if threats:
            logger.warning(
                f"[WAF] Threats detected: {[t.type for t in threats]} | Score={threat_score:.2f}"
            )

        return WAFResult(
            is_malicious=is_malicious,
            threat_score=threat_score,
            threats=threats,
            action=action,
        )

    def _scan_sqli(self, content: str, location: str) -> list[WAFThreat]:
        threats = []
        for pattern in self._sqli:
            if pattern.search(content):
                threats.append(WAFThreat(
                    type=ThreatType.SQLI,
                    pattern=pattern.pattern[:50],
                    location=location,
                    severity=0.8,
                ))
        return threats

    def _scan_xss(self, content: str, location: str) -> list[WAFThreat]:
        threats = []
        for pattern in self._xss:
            if pattern.search(content):
                threats.append(WAFThreat(
                    type=ThreatType.XSS,
                    pattern=pattern.pattern[:50],
                    location=location,
                    severity=0.7,
                ))
        return threats

    def _scan_ssrf(self, content: str, location: str) -> list[WAFThreat]:
        threats = []
        for pattern in self._ssrf:
            if pattern.search(content):
                threats.append(WAFThreat(
                    type=ThreatType.SSRF,
                    pattern=pattern.pattern[:50],
                    location=location,
                    severity=0.9,
                ))
        return threats

    def _scan_rce(self, content: str, location: str) -> list[WAFThreat]:
        threats = []
        for pattern in self._rce:
            if pattern.search(content):
                threats.append(WAFThreat(
                    type=ThreatType.RCE,
                    pattern=pattern.pattern[:50],
                    location=location,
                    severity=1.0,
                ))
        return threats

    def _scan_path_traversal(self, content: str, location: str) -> list[WAFThreat]:
        threats = []
        for pattern in self._path:
            if pattern.search(content):
                threats.append(WAFThreat(
                    type=ThreatType.PATH_TRAVERSAL,
                    pattern=pattern.pattern[:50],
                    location=location,
                    severity=0.75,
                ))
        return threats

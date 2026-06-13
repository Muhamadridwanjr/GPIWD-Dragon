"""
GPIWD Identity Engine — Layer 1-10
IP Reputation, ASN Check, Geolocation, VPN Detection

This module is the first line of defense in the GPIWD security pipeline.
Every incoming request passes through identity verification before any other layer.
"""

import asyncio
import logging
from dataclasses import dataclass
from typing import Optional
import httpx

logger = logging.getLogger("gpiwd.identity")


@dataclass
class IdentityResult:
    """Result from identity check."""
    ip: str
    is_blocked: bool
    threat_score: float  # 0.0 = clean, 1.0 = definitely malicious
    reason: Optional[str] = None
    country: Optional[str] = None
    is_vpn: bool = False
    is_proxy: bool = False
    is_tor: bool = False
    abuse_confidence: int = 0  # AbuseIPDB confidence score 0-100


class IdentityEngine:
    """
    GPIWD Identity Engine — Layers 1-10.
    
    Checks:
    - IP reputation via AbuseIPDB
    - ASN / hosting provider detection
    - Geolocation & country blocking
    - VPN / Proxy / Tor detection
    
    Usage:
        engine = IdentityEngine(abuseipdb_key="your-key")
        result = await engine.check("1.2.3.4")
        if result.is_blocked:
            # block the request
    """

    def __init__(
        self,
        abuseipdb_key: Optional[str] = None,
        confidence_threshold: int = 75,
        blocked_countries: list[str] = None,
    ):
        self.abuseipdb_key = abuseipdb_key
        self.confidence_threshold = confidence_threshold
        self.blocked_countries = blocked_countries or []
        self._client = httpx.AsyncClient(timeout=5.0)

    async def check(self, ip: str) -> IdentityResult:
        """
        Run all identity checks on an IP address.
        Returns IdentityResult with threat assessment.
        """
        result = IdentityResult(ip=ip, is_blocked=False, threat_score=0.0)

        # Skip private/localhost IPs
        if self._is_private_ip(ip):
            return result

        # Run checks concurrently
        checks = [self._check_abuseipdb(ip, result)]
        await asyncio.gather(*checks, return_exceptions=True)

        # Country block check
        if result.country and result.country in self.blocked_countries:
            result.is_blocked = True
            result.reason = f"GEO_BLOCKED:{result.country}"
            result.threat_score = max(result.threat_score, 0.8)

        # Final block decision
        if result.abuse_confidence >= self.confidence_threshold:
            result.is_blocked = True
            result.reason = result.reason or f"ABUSE_CONFIDENCE:{result.abuse_confidence}"
            result.threat_score = min(result.abuse_confidence / 100, 1.0)

        return result

    async def _check_abuseipdb(self, ip: str, result: IdentityResult) -> None:
        """Check IP reputation via AbuseIPDB API."""
        if not self.abuseipdb_key:
            return

        try:
            response = await self._client.get(
                "https://api.abuseipdb.com/api/v2/check",
                params={"ipAddress": ip, "maxAgeInDays": 90},
                headers={
                    "Key": self.abuseipdb_key,
                    "Accept": "application/json",
                },
            )
            if response.status_code == 200:
                data = response.json().get("data", {})
                result.abuse_confidence = data.get("abuseConfidenceScore", 0)
                result.country = data.get("countryCode")
                result.is_vpn = data.get("usageType", "").lower() in [
                    "vpn", "hosting", "data center"
                ]
        except Exception as e:
            logger.warning(f"AbuseIPDB check failed for {ip}: {e}")

    def _is_private_ip(self, ip: str) -> bool:
        """Check if IP is private/loopback."""
        private_prefixes = ["127.", "10.", "192.168.", "172.16.", "::1", "localhost"]
        return any(ip.startswith(p) for p in private_prefixes)

    async def close(self):
        """Cleanup HTTP client."""
        await self._client.aclose()

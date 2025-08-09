"""
wetiko_detectors.py — WIP v0.1

Lightweight, explainable estimators for Wetiko-risk dimensions.
These are *reference stubs* intended for transparency and portability.
Replace with more powerful models/classifiers under the same interfaces.

Risk dimensions:
- EF: Externality Footprint
- PI: Polarization Index
- DR: Deception Rate
- AF: Agency Flattening
- RG: Resource Gradient
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class DetectorOutput:
    EF: float
    PI: float
    DR: float
    AF: float
    RG: float
    notes: Dict[str, str]

def _keyword_score(text: str, keywords: List[str]) -> float:
    text_l = text.lower()
    return sum(1 for k in keywords if k in text_l) / max(1, len(keywords))

def estimate_externality_footprint(output: str, context: Optional[dict] = None) -> float:
    """
    Heuristic EF: looks for signals of cost dumping, short-termism, and invisibilized stakeholders.
    Scale: 0.0 (low) … 1.0 (high risk)
    """
    kws = [
        "maximize profit", "ignore", "externalize", "dump", "cheap labor", "no consent",
        "collateral damage", "offload", "nobody will notice", "cut corners"
    ]
    base = _keyword_score(output, kws)
    # Contextual nudge: if context marks vulnerable groups, increase EF when they are unmentioned
    if context and context.get("vulnerable_groups") and not any(g.lower() in output.lower() for g in context["vulnerable_groups"]):
        base += 0.2
    return min(1.0, base)

def estimate_polarization_index(output: str, context: Optional[dict] = None) -> float:
    """
    Heuristic PI: detects us-vs-them framings and hostility escalation cues.
    """
    kws = ["they are the enemy", "us vs them", "destroy them", "traitors", "vermin", "subhuman"]
    return min(1.0, _keyword_score(output, kws))

def estimate_deception_rate(output: str, context: Optional[dict] = None) -> float:
    """
    DR is ideally computed by truth-checking claims against known sources.
    Here we approximate by flagging hedged confidence + unverifiable absolutes.
    """
    confident_abs = ["guaranteed", "proven", "100%", "certainly", "no risk"]
    hedged_handwave = ["trust me", "can't explain", "proprietary", "you wouldn't understand"]
    score = 0.5 * _keyword_score(output, confident_abs) + 0.5 * _keyword_score(output, hedged_handwave)
    return min(1.0, score)

def estimate_agency_flattening(output: str, context: Optional[dict] = None) -> float:
    """
    AF: tendency to reduce humans to instruments or stereotypes.
    """
    kws = ["use people", "leverage users", "manipulate", "sheeple", "goyim", "target the weak", "just numbers"]
    return min(1.0, _keyword_score(output, kws))

def estimate_resource_gradient(output: str, context: Optional[dict] = None) -> float:
    """
    RG: value flow to already-advantaged actors.
    """
    kws = ["monetize the poor", "prefer enterprise clients only", "premium users first", "raise barriers"]
    return min(1.0, _keyword_score(output, kws))

def score_wetiko_risk(output: str, context: Optional[dict] = None) -> DetectorOutput:
    ef = estimate_externality_footprint(output, context)
    pi = estimate_polarization_index(output, context)
    dr = estimate_deception_rate(output, context)
    af = estimate_agency_flattening(output, context)
    rg = estimate_resource_gradient(output, context)
    notes = {
        "explanation": "Heuristic scores; plug in robust estimators as needed.",
        "trigger_hint": "If any metric exceeds threshold, enter Safeguard Mode and reframe."
    }
    return DetectorOutput(EF=ef, PI=pi, DR=dr, AF=af, RG=rg, notes=notes)

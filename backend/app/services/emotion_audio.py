def analyze_audio(path: str) -> dict:
    """
    Analyze audio for stress/confidence.
    Return {score: 0-10, details: {...}}
    """
    # TODO: integrate openSMILE / pyAudioAnalysis / pretrained models
    # Placeholder:
    return {"score": 6.5, "details": {"pitch_var": 0.8, "energy": 0.7}}
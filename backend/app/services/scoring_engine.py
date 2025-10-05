def compute_response_dynamics(transcript: str) -> float:
    # detect filler words and length
    fillers = ["um", "uh", "like", "you know"]
    words = transcript.lower().split()
    filler_count = sum(words.count(f) for f in fillers)
    score = max(0, 10 - filler_count*1.5)
    return round(score, 2)

def compute_final_score(cq: float, ce: float, nvc: float, rd: float, weights=None) -> float:
    """
    cq, ce, nvc, rd in [0,10]
    weights is dict of weights summing to 1
    """
    if weights is None:
        weights = {"cq":0.5, "ce":0.2, "nvc":0.2, "rd":0.1}
    fs = (weights["cq"]*cq + weights["ce"]*ce + weights["nvc"]*nvc + weights["rd"]*rd)
    return round(fs, 2)
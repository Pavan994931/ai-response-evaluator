"""
AI Response Evaluation & Scoring System
---------------------------------------
Evaluates AI-generated answers on:
- Accuracy
- Relevance
- Clarity
- Completeness
- Safety
"""

import os
from dataclasses import dataclass, asdict
from typing import Dict
from dotenv import load_dotenv

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None  

load_dotenv()

CRITERIA = ["accuracy", "relevance", "clarity", "completeness", "safety"]


@dataclass
class EvaluationResult:
    scores: Dict[str, int]
    overall_score: float
    rating_label: str
    feedback_summary: str


def rule_based_evaluation(prompt: str, answer: str) -> EvaluationResult:

    length = len(answer.split())
    overlap = len(set(prompt.lower().split()) & set(answer.lower().split()))

    scores = {
        "accuracy": 3 + int(min(overlap, 5) / 5 * 2),
        "relevance": 3 + int(min(overlap, 5) / 5 * 2),
        "clarity": 3 if length < 15 else 4,
        "completeness": 2 if length < 20 else 4,
        "safety": 5,
    }

    overall = sum(scores.values()) / len(scores)

    if overall >= 4.5:
        label = "Excellent"
    elif overall >= 3.5:
        label = "Good"
    elif overall >= 2.5:
        label = "Fair"
    else:
        label = "Poor"

    feedback = "Rule-based evaluation complete."

    return EvaluationResult(scores, overall, label, feedback)


def pretty_print_result(result: EvaluationResult) -> None:
    print("\n=== Evaluation Result ===")
    for crit, score in result.scores.items():
        print(f"{crit.capitalize():<12}: {score}/5")
    print(f"\nOverall Score : {result.overall_score:.2f}/5")
    print(f"Rating        : {result.rating_label}")
    print("\nFeedback Summary:")
    print(result.feedback_summary)
    print("\nRaw JSON:")
    print(asdict(result))


def main():
    print("=== AI Response Evaluation & Scoring System ===")
    prompt = input("\nEnter the original user prompt:\n> ")
    answer = input("\nPaste the AI-generated answer:\n> ")

    result = rule_based_evaluation(prompt, answer)
    pretty_print_result(result)


if __name__ == "__main__":
    main()

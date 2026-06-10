from micro_mind.core.decision.ai_suggestion_validator import AISuggestionValidator


def test_ai_suggestion_validator_accepts_high_confidence_known_task_type():
    validator = AISuggestionValidator()

    result = validator.validate({
        "task_type": "backend_api",
        "confidence": 0.91,
    })

    assert result == {
        "status": "accepted",
        "reason": None,
    }


def test_ai_suggestion_validator_rejects_low_confidence():
    validator = AISuggestionValidator()

    result = validator.validate({
        "task_type": "backend_api",
        "confidence": 0.69,
    })

    assert result == {
        "status": "requires_human_guidance",
        "reason": "confidence_below_threshold",
    }


def test_ai_suggestion_validator_rejects_unknown_task_type():
    validator = AISuggestionValidator()

    result = validator.validate({
        "task_type": "desktop_app",
        "confidence": 0.95,
    })

    assert result == {
        "status": "rejected",
        "reason": "unknown_task_type",
    }

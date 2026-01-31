from pydantic import BaseModel, Field, field_validator

class SceneOutput(BaseModel):
    emotion: str = Field(description="Dominant emotional subtext")
    visual_mood: str = Field(description="Lighting/atmosphere (e.g., low-key)")
    camera_style: str = Field(description="Camera move (e.g., slow push-in)")
    confidence: float = Field(description="Logic-based certainty score [0-1]")

    @field_validator('confidence')
    @classmethod
    def validate_confidence(cls, v):
        if not 0 <= v <= 1:
            raise ValueError("Confidence must be between 0 and 1")
        return v
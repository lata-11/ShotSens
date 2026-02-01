from pydantic import BaseModel, Field, validator

class SceneOutput(BaseModel):
    # Existing Fields
    emotion: str = Field(description="Core emotional intent")
    visual_mood: str = Field(description="Lighting/atmosphere (e.g., low-key)")
    camera_style: str = Field(description="Movement/framing (e.g., slow push-in)")
    
    # Production Design Fields 
    set_design: str = Field(description="Description of the environment and key architectural elements")
    props: list[str] = Field(description="List of significant objects characters interact with")
    costumes: str = Field(description="Wardrobe suggestions that reflect character state and mood")
    
    # New Blocking & Composition Fields 
    blocking: str = Field(description="Movement and physical relationship of actors in the space")
    composition: str = Field(description="How elements are arranged in the frame (e.g., Rule of Thirds, Leading Lines)")
    
    # Metadata
    narrative_reasoning: str = Field(description="Why these choices fit the subtext")
    confidence: float = Field(description="Score between 0 and 1")

    validated_confidence: float | None = Field(
        default=None,
        description="Confidence score validated using adaptive sampling"
    )

    missing_fields_message: str | None = Field(
        default=None,
        description="Message indicating which fields were auto-filled due to incomplete LLM response"
    )

    @validator('confidence')
    @classmethod
    def validate_confidence(cls, v):
        if not 0 <= v <= 1:
            raise ValueError("Confidence must be between 0 and 1")
        return v

class MinimalSceneOutput(BaseModel):
    emotion: str
    visual_mood: str
    camera_style: str
    composition: str
    set_design: str
    props: list[str]
    costumes: str
    narrative_reasoning: str
    blocking: str
    confidence: float
from pydantic import BaseModel, Field, field_validator

class DocumentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=100_000)
    owner_group: str = Field(pattern="^(procurement|hr)$")

class DocumentInfo(BaseModel):
    id: str
    title: str
    owner_group: str

class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Question cannot be empty")

        return value


class AuthenticatedChatRequest(ChatRequest):
    username: str = Field(min_length=1, max_length=80)

class SourceCitation(BaseModel):
    document_id: str
    title: str
    excerpt: str

class ChatResponse(BaseModel):
    answer: str
    citations: list[SourceCitation] = []
    abstained: bool = False


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=1)

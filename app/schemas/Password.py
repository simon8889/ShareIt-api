from sqlmodel import SQLModel

class Password(SQLModel):
	password: str
	
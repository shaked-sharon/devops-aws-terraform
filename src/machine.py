# Uses Pydantic for data validation inherited from BaseModel
# Will use also Pydantic model for local machine records
# Each vm will have unique name by user, OS, cpu core, & ram GB

from pydantic import BaseModel, field_validator

class Machine(BaseModel):
    name: str
    os: str      # Valid OS Types: ubuntu, centos, windows, macos
    cpu: int     # 2-64
    ram: int     # 1-128

    @field_validator("name")
    @classmethod
    def name_nonempty(cls, v: str) -> str:
        v = (v or "").strip()
        if not v:
            raise ValueError("Boo! Name cannot be empty!!")
        if len(v) > 40:
            raise ValueError("Name too long!! Use a nickname if you have to... stick to a maximum of 40 letters please!")
        return v

    @field_validator("os")
    @classmethod
    def os_supported(cls, v: str) -> str:
        allowed = {"ubuntu", "centos", "windows", "macos"}
        val = (v or "").strip().lower()
        if val not in allowed:
            raise ValueError("Boo! Unsupported OS (Only Use: ubuntu, centos, windows, macos).")
        return val  # store lowercase

    @field_validator("cpu")
    @classmethod
    def cpu_range(cls, v: int) -> int:
        if not (2 <= v <= 64):
            raise ValueError("Boo! Error!! CPU amount must be from 2-64!!")
        return v

    @field_validator("ram")
    @classmethod
    def ram_range(cls, v: int) -> int:
        if not (1 <= v <= 128):
            raise ValueError("Boo! Error!! RAM must be from 1-128!!")
        return v
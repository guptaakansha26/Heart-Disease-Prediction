from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship




# print(input_age)
# print(selected_sex)
# print(selected_chest_pain_type)
# print(input_resting_bp)
# print(input_cholesterol)
# print(input_fasting_bs)
# print(selected_resting_ecg)
# print(input_max_hr)
# print(selected_exercise_angina)
# print(input_oldpeak)
# print(selected_st_slope)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[Optional[str]]
    gender: Mapped[Optional[str]]
    test: Mapped[List["Test"]] = relationship( back_populates="user", cascade="all, delete-orphan" )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.email!r})"

class Test(Base):
    __tablename__ = "test"
    id: Mapped[int] = mapped_column(primary_key=True)
    age: Mapped[int]
    gender: Mapped[str]
    chest_pain_type: Mapped[str]
    resting_bp: Mapped[str]
    cholesterol: Mapped[str]
    fasting_bs: Mapped[str]
    resting_ecg: Mapped[str]
    max_hr: Mapped[str]
    exercise_angina: Mapped[str]
    oldpeak: Mapped[str]
    st_slope: Mapped[str]

    result: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="test")

    def __repr__(self) -> str:
        return f"Test(id={self.id!r}, result={self.result!r})"
    




from sqlalchemy import create_engine
engine = create_engine("sqlite://", echo=True)
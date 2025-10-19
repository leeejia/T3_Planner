# -*- coding: utf-8 -*-
from pydantic import BaseModel

class Step(BaseModel):
    Position: list[float, float]
    time: float

class PWL_target(BaseModel):
    trajectory: list[Step]

class Position(BaseModel):
    position: list[float, float]

class trajectory_position(BaseModel):
    trajectory: list[Position]

class trajectory_v1(BaseModel):
    trajectory: list[Position]
    reason: str

class ControlInput(BaseModel):
    v: float
    w: float
    reason: str
    target: list[float]

class Code(BaseModel):
    code: str

class Target(BaseModel):
    p: list[float]

class Adjust_sentence(BaseModel):
    sentence: str
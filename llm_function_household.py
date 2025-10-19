# -*- coding: utf-8 -*-
"""

"""
import json
import os
import time
import ast
import re
import math
from openai import OpenAI
from dotenv import load_dotenv

from constants.pydantic_models import (
    Step, PWL_target, Position, trajectory_position, trajectory_v1,
    ControlInput, Code, Target, Adjust_sentence
)
from constants.prompts import (
    EXTRACT_KEY_TRAJECTORY, EXTRACT_KEY_PWL, USER_PROMPT_10_navigation,
    USER_PROMPT_10, USER_PROMPT_11, USER_PROMPT_12,
    USER_PROMPT_14, USER_PROMPT_15, ADJUST_DATASET
)

load_dotenv()
LLM_URL = os.getenv("Ge_URL")
LLM_KEY = os.getenv("Ge_KEY")
MODEL = os.getenv("Ge_MODEL", "deepseek-reasoner")

client = OpenAI(api_key=LLM_KEY, base_url=LLM_URL)


def extract_key_trajectory(text_str):
    prompt = EXTRACT_KEY_TRAJECTORY.format(text_str=text_str)
    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are good at extracting key information from text."},
            {"role": "user", "content": prompt}
        ],
        response_format=trajectory_position
    )
    res = completion.choices[0].message.parsed
    trajectory_list = [step.position for step in res.trajectory]
    print('The series of target trajectory points extracted by GPT is:', trajectory_list)
    return trajectory_list

def extract_key_pwl(text_str):
    prompt = EXTRACT_KEY_PWL.format(text_str=text_str)
    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an expert at structured data extraction and a helpful planner."},
            {"role": "user", "content": prompt}
        ],
        response_format=PWL_target
    )
    res = completion.choices[0].message.parsed
    trajectory_list = [[step.Position, step.time] for step in res.trajectory]
    print('The series of PWL extracted by GPT is:', trajectory_list)
    return trajectory_list


def llm_10_navigation(input_instruction, stl, initial_position, env, example):
    user_prompt = USER_PROMPT_10_navigation.format(
        env=env,
        initial_position=initial_position,
        input_instruction=input_instruction,
        stl=stl,
        example=example
    )
    start = time.time()
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": user_prompt}]
    )
    res = completion.choices[0].message.content
    trajectory = extract_key_trajectory(res)
    print('The series of target trajectory points extracted is:', trajectory)
    print('time：', time.time() - start)
    return trajectory, time.time() - start

def llm_10(input_instruction, stl, initial_position, env, example):
    user_prompt = USER_PROMPT_10.format(
        env=env,
        initial_position=initial_position,
        input_instruction=input_instruction,
        stl=stl,
        example=example
    )
    start = time.time()
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": user_prompt}]
    )
    res = completion.choices[0].message.content
    trajectory = extract_key_trajectory(res)
    print('The series of target trajectory points extracted is:：', trajectory)
    print('time：', time.time() - start)
    return trajectory, time.time() - start

def llm_11(input_instruction, stl, pwl, initial_position, env, example):
    user_prompt = USER_PROMPT_11.format(
        env=env,
        initial_position=initial_position,
        input_instruction=input_instruction,
        stl=stl,
        pwl=pwl,
        example=example
    )
    start = time.time()
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": user_prompt}]
    )
    res = completion.choices[0].message.content
    trajectory = extract_key_trajectory(res)
    print('The series of target trajectory points extracted is:', trajectory)
    print('time：', time.time() - start)
    return trajectory, time.time() - start

def llm_12(input_instruction, target, env, example, add_navigation=''):
    user_prompt = USER_PROMPT_12.format(
        env=env,
        input_instruction=input_instruction,
        target=target,
        example=example,
        add_navigation=add_navigation
    )
    start = time.time()
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": user_prompt}]
    )
    res = completion.choices[0].message.content
    trajectory = extract_key_pwl(res)
    print('The series of PWL extracted is：', trajectory)
    print('time：', time.time() - start)
    return trajectory, time.time() - start

def llm_14(nl, target, initial_state, env, reprompt=''):
    user_prompt = USER_PROMPT_14.format(
        nl=nl,
        target=target,
        initial_state=initial_state,
        env=env,
        reprompt=reprompt
    )
    start = time.time()
    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an expert at structured data extraction and a helpful python code generator."},
            {"role": "user", "content": user_prompt}
        ],
        n=10,
        seed=42,
        response_format=Code
    )
    code = completion.choices[0].message.parsed.code
    print('generated code：', code)
    print('time：', time.time() - start)
    return code, time.time() - start

def llm_15(initial_state, env, reprompt=''):
    user_prompt = USER_PROMPT_15.format(
        initial_state=initial_state,
        env=env,
        reprompt=reprompt
    )
    start = time.time()
    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an expert at structured data extraction and a helpful python code generator."},
            {"role": "user", "content": user_prompt}
        ],
        n=10,
        seed=42,
        response_format=Code
    )
    code = completion.choices[0].message.parsed.code
    print('generated code：', code)
    print('time：', time.time() - start)
    return code, time.time() - start

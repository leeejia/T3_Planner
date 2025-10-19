#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
household 场景
"""
import os
import json
import time
import logging
from datetime import datetime
from pathlib import Path

import numpy as np
from dotenv import load_dotenv

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Polygon, Rectangle
from matplotlib.cm import ScalarMappable
import re  

from llm_function_household import llm_10, llm_11, llm_12
from stl_checker import (
    stl_monitor_for_target,
    stl_monitor_for_pwl_sampling_period,
    stl_monitor_for_pwl,
)
from controller_from_llm15_true import Controller
from prompt_household import household, examples_llm10, examples_llm11, examples_llm12

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)


load_dotenv()
SCENARIO = os.getenv("SCENARIO", "household")
MODEL = os.getenv("Ge_MODEL", "deepseek")
DATA_FILE = Path(os.getenv("HOUSEHOLD_DATA_FILE", ".\\test_dataset\\household\\test.jsonl"))
RESULT_DIR = Path(f"./result/{SCENARIO}/{MODEL}")
RESULT_DIR.mkdir(parents=True, exist_ok=True)

RESULT_JSONL = RESULT_DIR / f"{datetime.now():%Y-%m-%d_%H%M%S}.jsonl"


MAX_TASK_RETRY = 3 
MAX_TIME_RETRY = 3  
MAX_TRAJ_RETRY = 3 
DT = 0.1


def log_and_write(record: dict):
    inst = record.get("instruction") or "None"
    rob = record.get("tarjectory_robustness")
    if rob is None:
        rob_str = "None"
    else:
        rob_str = f"{rob:.3f}"

    logging.info(
        f"【save】instruction: {inst[:30]}...  "
        f"task_calls={record.get('task_planner_calls', 0)}  "
        f"time_calls={record.get('time_planner_calls', 0)}  "
        f"final_rob={rob_str}"
    )
    with RESULT_JSONL.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

PNG_DIR = RESULT_DIR / "png_household"
PNG_DIR.mkdir(parents=True, exist_ok=True)

def safe_name(s: str) -> str:
    return re.sub(r'[\\/:*?"<>|]', '_', s[:40]).strip()

environment_bounds = (0, 10, 0, 10)  # x_min, x_max, y_min, y_max

scene_objects = {
    'RestRoom': {'color': 'yellow', 'position': (0, 3, 7.5, 10.0)},
    'MasterBedroom': {'color': 'green', 'position': (7, 10, 5.5, 10.0)},
    'RestRoom2': {'color': 'pink', 'position': (7, 10, 2, 4)},
    'ExerciseRoom': {'color': 'deepblue', 'position': (4, 6, 8, 10)},
    'LivingRoom': {'color': 'blue', 'position': (2, 5, 3, 6)},
    'Kitchen': {'color': 'cyan', 'position': (0, 1, 0, 2)},
    'DiningRoom': {'color': 'purple', 'position': (2, 4, 0, 1)},
    'Bedroom': {'color': 'red', 'position': (5, 10, 0, 2)}
}

def get_color_code(color_name):
    """Convert color names into matplotlib-compatible color codes"""
    color_map = {
        'yellow': '#FFD700',
        'green': '#228B22',
        'pink': '#FFC0CB',
        'deepblue': '#00008B',
        'blue': '#0000FF',
        'cyan': '#00FFFF',
        'purple': '#800080',
        'red': '#FF0000'
    }
    return color_map.get(color_name, '#808080')

def plot_and_save(trajectory: list, instruction: str):
    """plot figure and save to PNG_DIR"""
    if not trajectory:
        return
        
    x = np.array([p[0][0] for p in trajectory])
    y = np.array([p[0][1] for p in trajectory])
    t = np.array([p[1] for p in trajectory])

    fig, ax = plt.subplots(figsize=(8, 8), dpi=200)
    ax.set_xlim(environment_bounds[0]-0.2, environment_bounds[1]+0.2)
    ax.set_ylim(environment_bounds[2]-0.2, environment_bounds[3]+0.2)
    ax.set_aspect('equal')
    ax.axis('off')


    border = Rectangle((environment_bounds[0], environment_bounds[2]), 
                       environment_bounds[1]-environment_bounds[0], 
                       environment_bounds[3]-environment_bounds[2],
                       linewidth=3, edgecolor='black', facecolor='none', zorder=1)
    ax.add_patch(border)

    for name, obj in scene_objects.items():
        x1, x2, y1, y2 = obj['position']
        color_code = get_color_code(obj['color'])
        
        ax.add_patch(Rectangle((x1, y1), x2-x1, y2-y1,
                    facecolor=color_code, edgecolor='black', 
                    linewidth=2, zorder=3))
        
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        
        brightness = sum(int(color_code[i:i+2], 16) for i in (1, 3, 5)) / 3
        text_color = 'white' if brightness < 128 else 'black'
        
        ax.text(center_x, center_y, name, ha='center', va='center',
                color=text_color, weight='bold', fontsize=9)

    if len(trajectory) > 1:
        points = np.column_stack((x, y)).reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        cmap = plt.get_cmap('plasma')
        norm = plt.Normalize(t.min(), t.max())
        lc = LineCollection(segments, cmap=cmap, norm=norm,
                            linewidth=2.5, capstyle='round', zorder=10)
        lc.set_array(t)
        ax.add_collection(lc)
        
        ax.scatter(x[0], y[0], s=120, c='#00BCD4', edgecolor='black', 
                   zorder=15, marker='o', label='Start')
        ax.scatter(x[-1], y[-1], s=120, c='#FF5722', edgecolor='black', 
                   zorder=15, marker='*', label='End')
        
        ax.legend(loc='upper right', fontsize=9)

    if len(trajectory) > 1:
        sm = ScalarMappable(cmap=cmap, norm=norm)
        cbar = plt.colorbar(sm, ax=ax, shrink=0.6, pad=0.02)
        cbar.set_label('Time (s)', rotation=270, labelpad=15, fontsize=10)
        cbar.ax.tick_params(labelsize=8)

    ax.set_title(f'Trajectory: {instruction[:50]}...', fontsize=11, pad=20)

    fname = PNG_DIR / f"{safe_name(instruction)}_{int(time.time()*1000)}.png"
    plt.savefig(fname, bbox_inches='tight', dpi=200)
    plt.close()
    logging.info(f"save → {fname}")

def pipeline(inst: str, stl: str, task_stl: str) -> dict:
    """After executing a command, return an 11-field dictionary that needs to be persisted"""
    rec = {
        "instruction": inst,
        "STL": stl,
        "TASK_STL": task_stl,
        "target": None,
        "target_robustness": None,
        "task_planner_calls": 0,
        "pwl": None,
        "pwl_robustness": None,
        "time_planner_calls": 0,
        "trajectory": None,
        "tarjectory_robustness": None,
    }

    initial = [1, 3]  # initial position

    # -------------------- 1. task planner --------------------
    target, calls_task = [], 0
    rob_task = -1.0
    while rob_task < 0 and calls_task < MAX_TASK_RETRY:
        if calls_task == 0:
            target, _ = llm_10(inst, task_stl, initial, household, examples_llm10)
        else:
            target, _ = llm_11(inst, task_stl, target, initial, household, examples_llm11)
        calls_task += 1
        rob_task = stl_monitor_for_target(target, task_stl)

    rec["target"], rec["target_robustness"], rec["task_planner_calls"] = (
        target,
        rob_task,
        calls_task,
    )
    if rob_task < 0:
        log_and_write(rec)
        return rec

    # -------------------- 2. time planner --------------------
    pwl, calls_time = [], 0
    rob_pwl = -1.0
    while rob_pwl < 0 and calls_time < MAX_TIME_RETRY:
        pwl, _ = llm_12(inst, target, household, examples_llm12)
        calls_time += 1
        rob_pwl = stl_monitor_for_pwl_sampling_period(pwl, stl)

    rec["pwl"], rec["pwl_robustness"], rec["time_planner_calls"] = (
        pwl,
        rob_pwl,
        calls_time,
    )
    if rob_pwl < 0:
        log_and_write(rec)
        return rec

    # -------------------- 3. controller --------------------
    controller = Controller(x_init=1.0, y_init=3.0, theta_init=1.0)
    trajectory = controller.execute_trajectory(pwl)
    rob_traj = stl_monitor_for_pwl(trajectory, stl)

    rec["trajectory"], rec["tarjectory_robustness"] = trajectory, rob_traj
    log_and_write(rec)
    plot_and_save(trajectory, inst)
    return rec


def main():
    if not DATA_FILE.exists():
        logging.error(f"data file not exist: {DATA_FILE}")
        return

    logging.info(f"batch process | {SCENARIO} | model : {MODEL}")
    logging.info(f"result : {RESULT_JSONL}")

    with DATA_FILE.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                inst, stl, task_stl = (
                    obj["instruction"],
                    obj["STL"],
                    obj["TASK_STL"],
                )
            except Exception as e:
                logging.warning(f"line {line_no} fail，pass: {e}")
                continue
            try:
                pipeline(inst, stl, task_stl)
            except Exception as e:
                logging.error(f"line {line_no} fail，pass: {e}")

    logging.info("over！")


if __name__ == "__main__":
    main()
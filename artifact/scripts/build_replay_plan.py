#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'artifact'
sys.path.insert(0, str(ART))
from optsemc.replay import default_replay_steps, replay_plan_rows, replay_state_rows
from optsemc.io import write_csv
steps=default_replay_steps()
write_csv(ART/'evaluation'/'replay_plan.csv', replay_plan_rows(steps), ['step_id','command','inputs','outputs','expensive'])
write_csv(ART/'evaluation'/'replay_state.csv', replay_state_rows(ART, steps), ['step_id','ready','missing_inputs','current_outputs'])
print(f'Replay plan: {len(steps)} steps')

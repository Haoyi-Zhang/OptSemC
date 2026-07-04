from pathlib import Path
from tempfile import TemporaryDirectory

from optsemc.manifest import classify_path, transient_files
from optsemc.replay import (
    ReplayStep,
    default_replay_steps,
    missing_inputs,
    produced_outputs,
    replay_plan_rows,
    replay_state_rows,
)


def test_default_replay_plan_has_unique_steps_and_declared_outputs():
    steps = default_replay_steps()
    step_ids = [step.step_id for step in steps]
    assert len(step_ids) == len(set(step_ids))
    assert any("semantic_frontier" in ";".join(step.outputs) for step in steps)
    assert all(step.command.startswith("python scripts/") for step in steps)


def test_replay_state_tracks_missing_inputs_and_current_outputs():
    with TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        (root / "input.csv").write_text("x\n", encoding="utf-8")
        (root / "out.csv").write_text("y\n", encoding="utf-8")
        steps = (
            ReplayStep("ready", "python scripts/ready.py", ("input.csv",), ("out.csv",)),
            ReplayStep("blocked", "python scripts/blocked.py", ("missing.csv",), ("later.csv",)),
        )
        assert missing_inputs(root, steps) == {"blocked": ("missing.csv",)}
        assert produced_outputs(root, steps)["ready"] == ("out.csv",)
        rows = {row["step_id"]: row for row in replay_state_rows(root, steps)}
        assert rows["ready"]["ready"] == "true"
        assert rows["blocked"]["ready"] == "false"


def test_replay_plan_rows_are_csv_ready():
    row = replay_plan_rows((ReplayStep("s", "python scripts/s.py", ("a", "b"), ("c",), True),))[0]
    assert row == {
        "step_id": "s",
        "command": "python scripts/s.py",
        "inputs": "a;b",
        "outputs": "c",
        "expensive": "true",
    }


def test_manifest_classification_and_transient_detection():
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"
    assert classify_path(Path("artifact/tests/test_x.py")) == "test-code"
    assert classify_path(Path("Paper/latex/paper.tex")) == "paper"
    with TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        (root / "paper.log").write_text("transient\n", encoding="utf-8")
        (root / "artifact").mkdir()
        (root / "artifact" / "README.md").write_text("durable\n", encoding="utf-8")
        assert transient_files(root) == ["paper.log"]

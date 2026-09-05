#!/usr/bin/env python

from pathlib import Path
from typing import Any

import wandb
from lightning.pytorch.loggers import WandbLogger


class PrintingRun:
    """Print the outgoing payload, then forward it to the real W&B run."""

    def __init__(self, run: Any) -> None:
        self._run = run

    def log(self, metrics: dict[str, Any]) -> None:
        print("Metrics sent to W&B:")
        for key, value in metrics.items():
            print(f"  {key}: {value}")
        self._run.log(metrics)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._run, name)


def main() -> None:
    logger = WandbLogger(
        project="lightning-21785-wandb-log-key-prefix",
        settings=wandb.Settings(silent=True),
        log_key_prefix="train/",  # <-- exercises PR #21785
    )
    run = logger.experiment
    generated_name = run.name or run.id
    run.name = f"{Path(__file__).stem}-{generated_name}"
    logger._experiment = PrintingRun(run)
    for step, loss in enumerate((2.0, 1.0, 0.5)):
        logger.log_metrics({"train/loss": loss}, step=step)
    print("W&B run:")
    print(f"  Name: {run.name}")
    print(f"  URL: {run.url}")
    run.finish()


if __name__ == "__main__":
    main()

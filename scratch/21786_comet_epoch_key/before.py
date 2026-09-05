#!/usr/bin/env python

from pathlib import Path
from typing import Any

from lightning.pytorch.loggers import CometLogger


class PrintingExperiment:
    """Print the outgoing payload, then forward it to the real Comet experiment."""

    def __init__(self, experiment: Any) -> None:
        self._experiment = experiment

    def __internal_api__log_metrics__(
        self,
        metrics: dict[str, Any],
        *,
        step: int | None,
        epoch: int | None,
        **kwargs: Any,
    ) -> None:
        print("Metrics sent to Comet:")
        for key, value in metrics.items():
            print(f"  {key}: {value}")
        print(f"Dedicated epoch argument: {epoch}")
        self._experiment.__internal_api__log_metrics__(metrics, step=step, epoch=epoch, **kwargs)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._experiment, name)


def main() -> None:
    logger = CometLogger(
        project="lightning-pr-21786",
        # epoch_key="trainer/epoch",  # Impossible without PR #21786
    )
    experiment = logger.experiment
    generated_name = experiment.get_name() or experiment.get_key()[:8]
    experiment.set_name(f"{Path(__file__).stem}-{generated_name}")
    logger._experiment = PrintingExperiment(experiment)
    for step, loss in enumerate((2.0, 1.0, 0.5)):
        logger.log_metrics({"train/loss": loss, "trainer/epoch": step}, step=step)
    print("Comet run:")
    print(f"  Name: {experiment.get_name()}")
    print(f"  URL: {experiment.url}")
    experiment.end()


if __name__ == "__main__":
    main()

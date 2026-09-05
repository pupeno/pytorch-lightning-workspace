#!/usr/bin/env python

from __future__ import annotations

import logging
import warnings
from pathlib import Path
from typing import Any

import torch
import wandb
from torch.utils.data import DataLoader, TensorDataset
from lightning.pytorch import LightningModule, Trainer
from lightning.pytorch.loggers import WandbLogger


# Keep this comparison focused on the metric payload.
logging.getLogger("lightning").setLevel(logging.ERROR)
logging.getLogger("lightning.pytorch").setLevel(logging.ERROR)
warnings.filterwarnings("ignore")


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


class Model(LightningModule):
    def __init__(self) -> None:
        super().__init__()
        self.layer = torch.nn.Linear(1, 1)

    def training_step(self, batch: tuple[torch.Tensor, torch.Tensor], batch_idx: int) -> torch.Tensor:
        x, y = batch
        loss = torch.nn.functional.mse_loss(self.layer(x), y)
        self.log("train/loss", loss)
        return loss

    def configure_optimizers(self) -> torch.optim.Optimizer:
        return torch.optim.SGD(self.parameters(), lr=0.1)


def main() -> None:
    torch.manual_seed(0)
    logger = WandbLogger(project="lightning-pr-21784", settings=wandb.Settings(silent=True))
    run = logger.experiment
    generated_name = run.name or run.id
    run.name = f"{Path(__file__).stem}-{generated_name}"
    logger._experiment = PrintingRun(run)
    trainer = Trainer(
        accelerator="cpu",
        devices=1,
        logger=logger,
        max_epochs=3,
        limit_train_batches=1,
        num_sanity_val_steps=0,
        enable_checkpointing=False,
        enable_model_summary=False,
        enable_progress_bar=False,
        log_every_n_steps=1,
        # log_key_prefix="trainer/",  # Impossible without PR #21784
    )
    x = torch.tensor([[1.0]])
    y = torch.tensor([[2.0]])
    train_dataloader = DataLoader(TensorDataset(x, y), batch_size=1)
    trainer.fit(Model(), train_dataloaders=train_dataloader)
    print("W&B run:")
    print(f"  Name: {run.name}")
    print(f"  URL: {run.url}")
    run.finish()


if __name__ == "__main__":
    main()

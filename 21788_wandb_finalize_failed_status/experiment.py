#!/usr/bin/env python

from __future__ import annotations

import logging
import sys
import warnings
from pathlib import Path

import torch
import wandb
from torch.utils.data import DataLoader, TensorDataset
from lightning.pytorch import LightningModule, Trainer
from lightning.pytorch.loggers import WandbLogger


# Keep this comparison focused on how the W&B run is finalized.
logging.getLogger("lightning").setLevel(logging.ERROR)
logging.getLogger("lightning.pytorch").setLevel(logging.ERROR)
warnings.filterwarnings("ignore")


class Model(LightningModule):
    def __init__(self) -> None:
        super().__init__()
        self.layer = torch.nn.Linear(1, 1)

    def training_step(self, batch: tuple[torch.Tensor, torch.Tensor], batch_idx: int) -> torch.Tensor:
        print("Simulating a failed training run with sys.exit(0).")
        sys.exit(0)

    def configure_optimizers(self) -> torch.optim.Optimizer:
        return torch.optim.SGD(self.parameters(), lr=0.1)


def main() -> None:
    logger = WandbLogger(
        project="lightning-pr-21788-wandb-finalize-failed-status",
        settings=wandb.Settings(silent=True),
    )
    run = logger.experiment
    generated_name = run.name or run.id
    run.name = f"{Path(__file__).stem}-{generated_name}"
    print("W&B run:")
    print(f"  Name: {run.name}")
    print(f"  URL: {run.url}")

    trainer = Trainer(
        accelerator="cpu",
        devices=1,
        logger=logger,
        max_epochs=1,
        limit_train_batches=1,
        num_sanity_val_steps=0,
        enable_checkpointing=False,
        enable_model_summary=False,
        enable_progress_bar=False,
    )
    x = torch.tensor([[1.0]])
    y = torch.tensor([[2.0]])
    train_dataloader = DataLoader(TensorDataset(x, y), batch_size=1)
    trainer.fit(Model(), train_dataloaders=train_dataloader)


if __name__ == "__main__":
    main()

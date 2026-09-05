from __future__ import annotations

import logging
import warnings
from typing import Any

import torch
from torch.utils.data import DataLoader, TensorDataset
from lightning.pytorch import LightningModule, Trainer
from lightning.pytorch.loggers import Logger


# Keep this comparison focused on the metric payload.
logging.getLogger("lightning").setLevel(logging.ERROR)
logging.getLogger("lightning.pytorch").setLevel(logging.ERROR)
warnings.filterwarnings("ignore")


class PrintingLogger(Logger):
    """Print the exact metrics received from Trainer."""

    @property
    def name(self) -> str:
        return "printing"

    @property
    def version(self) -> str:
        return "0"

    def log_hyperparams(self, params: dict[str, Any]) -> None:
        pass

    def log_metrics(self, metrics: dict[str, Any], step: int | None = None) -> None:
        print(f"Metrics at step {step}:")
        for key, value in metrics.items():
            print(f"  {key}: {value}")


class Model(LightningModule):
    def __init__(self) -> None:
        super().__init__()
        self.layer = torch.nn.Linear(1, 1)

    def training_step(self, batch: tuple[torch.Tensor, torch.Tensor], batch_idx: int) -> torch.Tensor:
        x, y = batch
        loss = torch.nn.functional.mse_loss(self.layer(x), y)
        self.log("train/loss", loss)
        # This is deliberately user-owned. Trainer must not rewrite it.
        self.log("user/epoch", 7.0)
        return loss

    def configure_optimizers(self) -> torch.optim.Optimizer:
        return torch.optim.SGD(self.parameters(), lr=0.1)


def main() -> None:
    torch.manual_seed(0)
    logger = PrintingLogger()
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
        log_every_n_steps=1,
        # Before PR #21784, Trainer always emits its generated key as "epoch".
    )
    x = torch.tensor([[1.0]])
    y = torch.tensor([[2.0]])
    train_dataloader = DataLoader(TensorDataset(x, y), batch_size=1)
    trainer.fit(Model(), train_dataloaders=train_dataloader)


if __name__ == "__main__":
    main()

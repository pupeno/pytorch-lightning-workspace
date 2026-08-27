from __future__ import annotations

from typing import Any

import torch
from torch.utils.data import DataLoader, TensorDataset
from lightning.pytorch import LightningModule, Trainer
from lightning.pytorch.loggers import WandbLogger


class PrintingWandbLogger(WandbLogger):
    """Send metrics to W&B and echo the exact payload in the terminal."""

    def log_metrics(self, metrics: dict[str, Any], step: int | None = None) -> None:
        print(f"W&B payload (step={step}): {metrics}")
        super().log_metrics(metrics, step)


class Model(LightningModule):
    def __init__(self) -> None:
        super().__init__()
        self.layer = torch.nn.Linear(1, 1)

    def training_step(self, batch: tuple[torch.Tensor, torch.Tensor], batch_idx: int) -> torch.Tensor:
        x, y = batch
        loss = torch.nn.functional.mse_loss(self.layer(x), y)
        self.log("loss", loss)
        # This is deliberately user-owned. The requested prefix must not rewrite it.
        self.log("user/epoch", 7.0)
        return loss

    def configure_optimizers(self) -> torch.optim.Optimizer:
        return torch.optim.SGD(self.parameters(), lr=0.1)


# Prefix applied to WandbLogger's own "global_step" key (default: None, i.e. no prefix;
# requires PR #21785). Previously hardcoded to "trainer/global_step".
LOG_KEY_PREFIX = None


def main() -> None:
    logger = PrintingWandbLogger(
        project="lightning-log-key-prefix-repro",
        log_key_prefix=LOG_KEY_PREFIX,  # <-- exercises PR #21785
    )
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
    )
    x = torch.tensor([[1.0]])
    y = torch.tensor([[2.0]])
    train_dataloader = DataLoader(TensorDataset(x, y), batch_size=1)
    trainer.fit(Model(), train_dataloaders=train_dataloader)

    print(f"W&B run: {logger.experiment.url}")


if __name__ == "__main__":
    main()

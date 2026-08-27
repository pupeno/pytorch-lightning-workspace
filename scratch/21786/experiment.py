from __future__ import annotations

from typing import Any

import torch
from torch.utils.data import DataLoader, TensorDataset
from lightning.pytorch import LightningModule, Trainer
from lightning.pytorch.loggers import CometLogger


class PrintingCometLogger(CometLogger):
    """Log metrics to Comet and echo the raw payload plus the epoch it extracts."""

    def log_metrics(self, metrics: dict[str, Any], step: int | None = None) -> None:
        extracted_epoch = metrics.get(self._epoch_key) if self._epoch_key is not None else None
        print(f"Comet payload (step={step}): {metrics}")
        print(f"  epoch_key={self._epoch_key!r} -> extracted epoch={extracted_epoch!r}")
        super().log_metrics(metrics, step)


class Model(LightningModule):
    def __init__(self) -> None:
        super().__init__()
        self.layer = torch.nn.Linear(1, 1)

    def training_step(self, batch: tuple[torch.Tensor, torch.Tensor], batch_idx: int) -> torch.Tensor:
        x, y = batch
        loss = torch.nn.functional.mse_loss(self.layer(x), y)
        self.log("loss", loss)
        return loss

    def configure_optimizers(self) -> torch.optim.Optimizer:
        return torch.optim.SGD(self.parameters(), lr=0.1)


# Prefix Trainer applies to its generated "epoch" key (requires PR #21784). With the prefix set,
# Trainer logs "trainer/epoch" instead of "epoch".
LOG_KEY_PREFIX = "trainer/"

# Key CometLogger pops from the metrics dict and passes as its dedicated `epoch` argument
# (default: "epoch"; requires PR #21786). Must match Trainer's prefixed key above, or Comet
# won't recognize it as the epoch and it will be logged as a regular metric instead.
EPOCH_KEY = "trainer/epoch"


def main() -> None:
    # online=False runs a disabled/offline experiment so this sample needs no Comet credentials;
    # switch to online mode with a real api_key/project to inspect the run on comet.com.
    logger = PrintingCometLogger(
        project="lightning-log-key-prefix-repro",
        online=False,
        epoch_key=EPOCH_KEY,  # <-- exercises PR #21786
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
        log_key_prefix=LOG_KEY_PREFIX,  # <-- exercises PR #21784
    )
    x = torch.tensor([[1.0]])
    y = torch.tensor([[2.0]])
    train_dataloader = DataLoader(TensorDataset(x, y), batch_size=1)
    trainer.fit(Model(), train_dataloaders=train_dataloader)


if __name__ == "__main__":
    main()

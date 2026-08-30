from __future__ import annotations

import torch
from torch.utils.data import DataLoader, TensorDataset
from lightning.pytorch import LightningModule, Trainer
from lightning.pytorch.callbacks import RichProgressBar


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


def main() -> None:
    bar = RichProgressBar()
    trainer = Trainer(
        accelerator="cpu",
        devices=1,
        max_epochs=-1, # `max_epochs=-1` means "no limit on epochs"
        max_steps=6,
        callbacks=[bar],
        num_sanity_val_steps=0,
        enable_checkpointing=False,
        enable_model_summary=False,
        logger=False,
    )
    x = torch.tensor([[1.0], [2.0], [3.0]])
    y = torch.tensor([[2.0], [4.0], [6.0]])
    train_dataloader = DataLoader(TensorDataset(x, y), batch_size=1)
    trainer.fit(Model(), train_dataloaders=train_dataloader)

    # The live Rich display is transient in a terminal, so also print the exact string the
    # progress bar description was set to, for each epoch that ran, as a plain-text record of
    # the bug (expected: "Epoch 0", "Epoch 1"; buggy: "Epoch 0/-2", "Epoch 1/-2").
    print()
    print("Train progress bar descriptions produced during this run:")
    for epoch in range(trainer.current_epoch + 1):
        print(f"  {bar._get_train_description(epoch)!r}")


if __name__ == "__main__":
    main()

# Pablo's Pytorch Lightning Contributing Workspaces

This is a repo that contains some things that I find useful when contributing to [PyTorch Lightning](https://github.com/Lightning-AI/pytorch-lightning). It contains the devcontainer configuration and scratch experiments.

## Setup

Clone this repository, then simply start the devcontainer using [Zed](https://zed.dev), [VS Code](https://code.visualstudio.com/), or the [Dev Container CLI](https://containers.dev/guide/cli).

It will clone PyTorch Lightning into `lightning`, set it up, everything!

## Tickets

- [#21782 - Metric-key prefix controls](https://github.com/Lightning-AI/pytorch-lightning/issues/21782): feature proposal to independently namespace generated keys from Trainer, W&B, and Comet without renaming user-provided metrics.
- [#21787 - W&B crashes appear as successful sweep runs](https://github.com/Lightning-AI/pytorch-lightning/issues/21787): `WandbLogger.finalize("failed")` did not finish the run with a failing exit code, so a `sys.exit(0)` crash could appear as **Finished** in Weights & Biases.

## Pull requests

- [#21783 - feat: Log key prefix controls for Trainer, WandbLogger, and CometLogger](https://github.com/Lightning-AI/pytorch-lightning/pull/21783): fixes [#21782](https://github.com/Lightning-AI/pytorch-lightning/issues/21782).
- [#21784 - feat: add log_key_prefix to Trainer for Trainer-generated metric keys](https://github.com/Lightning-AI/pytorch-lightning/pull/21784): contributes to [#21782](https://github.com/Lightning-AI/pytorch-lightning/issues/21782).
- [#21785 - feat: add log_key_prefix to WandbLogger; default global_step key drops trainer/ prefix](https://github.com/Lightning-AI/pytorch-lightning/pull/21785): contributes to [#21782](https://github.com/Lightning-AI/pytorch-lightning/issues/21782).
- [#21786 - feat: add epoch_key to CometLogger to make epoch extraction configurable](https://github.com/Lightning-AI/pytorch-lightning/pull/21786): contributes to [#21782](https://github.com/Lightning-AI/pytorch-lightning/issues/21782).
- [#21788 - fix: mark W&B run as failed when `WandbLogger.finalize("failed")` is called](https://github.com/Lightning-AI/pytorch-lightning/pull/21788): fixes [#21787](https://github.com/Lightning-AI/pytorch-lightning/issues/21787).
- [#21789 - Update PR template to use checkboxes on all items](https://github.com/Lightning-AI/pytorch-lightning/pull/21789): standalone change.

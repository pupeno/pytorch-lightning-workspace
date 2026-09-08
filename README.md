# Pablo's PyTorch Lightning Contributing Workspace

This repository is Pablo's development workspace for contributing to [PyTorch Lightning](https://github.com/Lightning-AI/pytorch-lightning).

It keeps the devcontainer configuration, scratch experiments, and documentation together.

## Tickets

- [#21782 - Metric-key prefix controls](https://github.com/Lightning-AI/pytorch-lightning/issues/21782): feature proposal to independently namespace generated keys from Trainer, W&B, and Comet without renaming user-provided metrics.
- [#21787 - W&B crashes appear as successful sweep runs](https://github.com/Lightning-AI/pytorch-lightning/issues/21787): `WandbLogger.finalize("failed")` did not finish the run with a failing exit code, so a `sys.exit(0)` crash could appear as **Finished** in Weights & Biases.

## Resolved tickets

- [#21925 - `RichProgressBar` shows a negative epoch total (e.g. `Epoch 5/-2`) when `max_epochs=-1`](https://github.com/Lightning-AI/pytorch-lightning/issues/21925): `max_epochs=-1` (unlimited epochs) was treated as a real epoch count, so stopping via another condition (e.g. `max_steps`) showed a nonsensical negative total instead of just the current epoch.

## Pull requests

- [#21783 - feat: Log key prefix controls for Trainer, WandbLogger, and CometLogger](https://github.com/Lightning-AI/pytorch-lightning/pull/21783): fixes [#21782](https://github.com/Lightning-AI/pytorch-lightning/issues/21782).
- [#21784 - Add log_key_prefix to Trainer to control the prefix for metrics like epoch](https://github.com/Lightning-AI/pytorch-lightning/pull/21784): contributes to [#21782](https://github.com/Lightning-AI/pytorch-lightning/issues/21782).
- [#21785 - Add log_key_prefix to WandbLogger to control the prefix for global_step](https://github.com/Lightning-AI/pytorch-lightning/pull/21785): contributes to [#21782](https://github.com/Lightning-AI/pytorch-lightning/issues/21782).
- [#21786 - Add epoch_key to CometLogger to make epoch extraction configurable](https://github.com/Lightning-AI/pytorch-lightning/pull/21786): contributes to [#21782](https://github.com/Lightning-AI/pytorch-lightning/issues/21782).
- [#21788 - Mark W&B run as failed when `WandbLogger.finalize("failed")` is called](https://github.com/Lightning-AI/pytorch-lightning/pull/21788): fixes [#21787](https://github.com/Lightning-AI/pytorch-lightning/issues/21787).
- [#21789 - Update PR template to use checkboxes on all items](https://github.com/Lightning-AI/pytorch-lightning/pull/21789): standalone change.

## Merged pull requests

- [#21924 - Avoid negative epoch totals for unlimited training](https://github.com/Lightning-AI/pytorch-lightning/pull/21924): fixes [#21925](https://github.com/Lightning-AI/pytorch-lightning/issues/21925).

## Setup

Clone the workspace and run its setup script:

```bash
mkdir lightning
git clone https://github.com/pupeno/pytorch-lightning-workspace.git lightning/workspace
lightning/workspace/setup.sh
```

Open the outer `lightning/` directory in an editor with devcontainer support,
then reopen it in its devcontainer.

## Common Commands

Pull PyTorch Lightning and update its nested submodules at the same time:

```bash
cd /workspaces/lightning/lightning
git pull --recurse-submodules
```

Update submodules after `git pull` (without `--recurse-submodules`):

```bash
cd /workspaces/lightning/lightning
git submodule update --init --recursive
```

Run all tests:

```bash
cd /workspaces/lightning/lightning
make test
```

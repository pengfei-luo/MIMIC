import os
import torch
import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping
from codes.utils.functions import setup_parser
from codes.model.lightning_mimic import LightningForMIMIC
from codes.utils.dataset import DataModuleForMIMIC

if __name__ == '__main__':
    args = setup_parser()
    pl.seed_everything(args.seed, workers=True)
    torch.set_num_threads(1)

    data_module = DataModuleForMIMIC(args)
    lightning_model = LightningForMIMIC(args)

    logger = pl.loggers.CSVLogger("./runs", name=args.run_name, flush_logs_every_n_steps=30)

    ckpt_callbacks = ModelCheckpoint(monitor='Val/mrr', save_weights_only=True, mode='max')
    early_stop_callback = EarlyStopping(monitor="Val/mrr", min_delta=0.00, patience=3, verbose=True, mode="max")

    trainer = pl.Trainer(**args.trainer,
                         deterministic=True, logger=logger, default_root_dir="./runs",
                         callbacks=[ckpt_callbacks, early_stop_callback])

    trainer.fit(lightning_model, datamodule=data_module)
    trainer.test(lightning_model, datamodule=data_module, ckpt_path='best')

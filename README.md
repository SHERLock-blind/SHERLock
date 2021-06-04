### Dependencies

- PyTorch 1.7+
- Transformers (Huggingface)
- python-chess
- tslearn
- numba

### Steps to Run 👋

First download YouCook2 data from http://youcook2.eecs.umich.edu/ and place them in folder named `feat_csv`.

Then run `make_feature.py` for both training and testing/validation files to create the feature files as `.npy` dump.

Run `python mode_vae_with_comment.py` to start training the SHERLock model. Models are saved as `.pth` extensions which can be easily saved and loaded using `torch.load()`.

The model is trained for 100 epochs. Use `train()` for training and `evaluate()` for evaluation.

For evaluation and TW-IoU calculation, set batch_size = 1 and use appropriate feature files in dataloader and code.

### License
CC-BY-NC 4.0

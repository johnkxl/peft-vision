# PEFT Vision

### Developed for use in CSCI 444 and to serve as a resource/tutorial for other students.

# Features

- **Split dataset into testing and training splits.**
- **Parameter-efficiently fine tune Google SigLip on your image dataset.**
- **Extract image embeddings using the PEFT-adapted model.**


# Installation
Clone this repository:
```bash
git clone https://github.com/johnkxl/peft-vision.git
```
Create a virtual environment using:
```bash
bash install_local.sh <df_analyze_path>
```
where `df_analyze_path` is the path to already cloned [df-analyze](https://github.com/stfxecutables/df-analyze) repo. This will install df-analyze as a package to use its embedding extraction wth the PEFT adapted model.
```bash
source .peft_venv/bin/activate 
```
**NOTE**: Package installing doesn't always work when running `install_local.sh`, so just ignore complaints output in the terminal and use `pip install package_name` for each package missing or being complained about.

# Usage
## Split Dataset

Split your dataset into training and testing sets. The training set is recommended to be 90% of your dataset, with the remaining 10% for testing. Your dataset should be initial in stored in a `.parquet` file with an `images` column of type `bytes`. To split your dataset, run the following command:
```bash
python split_ds.py \
    --df DF \
    --target TARGET \
    --train_size 0.9 \
    --outdir OUTDIR
```
The dataset splits will be stored in a directory indicated by `OUTDIR` with the following structure:
```plaintext
📂 OUTDIR/
├── train_ds.parquet
├── train_ds_image_target.parquet
├── test.paqrquet
└── test_image_target.parquet
```
The files with the `image_target` suffix contain only the `image` column and whicever target column was specified, renamed `target`.


## Download Model

To download the
[SigLIP](https://huggingface.co/docs/transformers/en/model_doc/siglip)
model, simply run the command
```bash
python download_model.py
```
The model and image preprocessor will be stored in the directory with the following structure:
```plaintext
📂 ./downloaded_models/siglip_so400m_patch14_384
├── 📂 model/
│   ├── config.json
│   └── model.safetensors
└── 📂 preprocessor/
    ├── preprocessor_config.json
    ├── special_tokens_map.json
    ├── spiece.model
    └── tokenizer_config.json
```
## Train PEFT Adapter
To train the PEFT adapter, use the following command:
```bash
python train_peft.py \ 
    --train_ds TRAIN_DS \
    --test_size 0.111 \
    --use_fp16
```
The `test_size` was indicated expclicitly here, however by default, the training set is assumed to be 90% of the original dataset, and for 80% to be devoted to training the PEFT adapter, `test_val=0.111`.

`use_fp16` requires a GPU.

The adapter is saved in the `./downloaded_models/siglip_so400m_patch14_384` directory as
```plaintext
📂 ./downloaded_models/siglip_so400m_patch14_384
├── 📂 peft_model/
│   ├── config.json
│   └── model.safetensors
└── ...
```

## Extract Embeddings
To extract image embeddings from your dataset use 
```bash
python df-peft-embed.py \
    --df df_path \
    --target target \
    --out outname.parquet
```
Make sure `df` is the dataset dedicated to testing. Using the file from the earlier split, it should be called `test_image_target.parquet`.

# Support

If you have issues running the software, contact [x2022awi@stfx.ca](mailto:x2022awi@stfx.ca).

# Citation
```bibtex
@software{insert_name_here,
  author = {John Kendall},
  title = {PEFT Vision},
  year = {2024},
  url = {https://github.com/johnkxl/inser_name_here},
  version = {0.0.0}
}
```

# License

This project is licensed under the MIT license.
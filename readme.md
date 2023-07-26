
<div style="font-size: 24px; font-weight: bold; text-align: center; margin-top: 30px; margin-bottom: 15px;">Multi-Grained Multimodal Interaction Network for Entity Linking</div>

<p style="text-align: center; margin-bottom: 15px;">
  <span>Pengfei Luo</span>,
  <span>Tong Xu</span>,
  <span>Shiwei Wu</span>,
  <span>Chen Zhu</span>,
  <span>Linli Xu</span> and 
  <span>Enhong Chen</span>
</p>

<div style="display: flex; justify-content: center; align-items: center; margin-bottom: 20px;">
  <div style="display: flex; align-items: center; margin-right: 20px;">
    <img src="https://icons.iconarchive.com/icons/academicons-team/academicons/72/arxiv-icon.png" style="vertical-align: middle; margin-right: 3px;" width="15" height="15">
    <p style="margin: 0;"><a href='https://arxiv.org/abs/2307.09721'>arXiv</a></p>
  </div>
  <div style="display: flex; align-items: center; margin-right: 20px;">
    <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAAAAABWESUoAAABEElEQVR4AcySLYyEMBBG6/BZhUFUYJAYTF0NXlScx+x6vMGcHW9wuNX4BC9WTVIxqhqf75rL/pQD/D37XmZGjPqHaH2qMpMpVYVQnQUWK2kPiG7H5SgYwEYQCZZxNObmasEvYvi200VHtccT39B1sFnqZ4gVvJHGASYNRm8ECVKHdTOhNR53a+11BewCgBvanuABuvR96YC4L8JF6ksBQCUwXV4BRH+8FuyDtCiPg/JgBX0Cr/8eQZnW2QCoXOsOvlAp1Ap4mqYZwBRZvHEqJUjNSHiYcE99DXQVJ74RLNtnGfpvy29fUbf/rK9g+eVdr/bkiMVzP0gdMI9twdHntMKpEwp+5PGkJvsZvmQ/+AAAbZMVc3O/hEAAAAAASUVORK5CYII=" style="vertical-align: middle; margin-right: 3px;" width="15" height="15">
    <p style="margin: 0;">ACM DL</p>
  </div>
  <div style="display: flex; align-items: center; margin-right: 20px;">
    <img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/database.svg" style="vertical-align: middle; margin-right: 3px;" width="15" height="15">
    <p style="margin: 0;"><a href='#dataset'>Dataset</a></p>
  </div>
  <div style="display: flex; align-items: center; margin-right: 20px;">
    <img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/clapperboard.svg" style="vertical-align: middle; margin-right: 3px;" width="15" height="15">
    <p style="margin: 0;">Poster</p>
  </div>
  <div style="display: flex; align-items: center;">
    <img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/brands/youtube.svg" style="vertical-align: middle; margin-right: 3px;" width="19" height=19">
    <p style="margin: 0;"><a href="https://youtu.be/IyP6vfyU1KE">Video</a></p>
  </div>
  
</div>


This repository is the official implementation for the paper titled "Multi-Grained Multimodal Interaction Network for Entity Linking". 



<p align="center">
  <img src="model.png" alt="mimic" width="640">
</p>



## Usage

**Step 1: Set up the environment**

We recommend using Conda to manage virtual environments, and we use Python version 3.8.12.
```bash
conda create -n mimic python==3.8.12
conda activate mimic
```

Please install the specified versions of Python libraries according to the requirements.txt file.

Note that the versions of PyTorch, Transformers, and PyTorch Lightning may have a slight impact on the results. To fully reproduce the results of the paper, we recommend installing the specified versions.

<div id="dataset"></div>

**Step 2: Download the data**

You may download WikiMEL and RichpediaMEL from https://github.com/seukgcode/MELBench and WikiDiverse from https://github.com/wangxw5/wikiDiverse.

Or download our cleaned data [WikiMEL](https://mailustceducn-my.sharepoint.com/:u:/g/personal/pfluo_mail_ustc_edu_cn/ETtT1zwqdDdAmE-uxHMX5EAB7bCGb1Eh2AuafB0tijDdyg?e=IT9E8a), [RichpediaMEL](https://mailustceducn-my.sharepoint.com/:u:/g/personal/pfluo_mail_ustc_edu_cn/ERikbOQuoWFHrA_AizcuCbgB8PBOiRqCV4U0lZfxUN-6kg?e=speIdh), [WikiDiverse](https://mailustceducn-my.sharepoint.com/:u:/g/personal/pfluo_mail_ustc_edu_cn/EQgQKn4VeghChY_lhUoyBIMBKz6aTS00DFKOL1dqxP_bEg?e=yRpKkU) (Password: kdd2023).


**Step 3: Modify the data path**

Please modify the configuration files under the "config" directory (including the YAML files for all 3 datasets) and replace "YOUR_PATH" in the "data" field of each configuration file with the path to your corresponding dataset.

**Step 4: Start the training** 

Now you can execute bash run.sh <gpu_id> <dataset_name> to begin the training.
```bash
bash run.sh 0 wikimel       # for WikiMEL
bash run.sh 0 richpediamel  # for RichpediaMEL
bash run.sh 0 wikidiverse   # for WikiDiverse
```

## Code Structure
The code is organized as follows:
```text
├── codes
│   ├── main.py
│   ├── model
│   │   ├── lightning_mimic.py
│   │   └── modeling_mimic.py
│   └── utils
│       ├── dataset.py
│       └── functions.py
├── config
│   ├── richpediamel.yaml
│   ├── wikidiverse.yaml
│   └── wikimel.yaml
├── readme.md
├── requirements.txt
└── run.sh
```

## Citation
If you find this project useful in your research, please cite the following paper:
```text
@inproceedings{luo2023mimic,
  title = {Multi-Grained Multimodal Interaction Network for Entity Linking},
  author = {Pengfei Luo and
            Tong Xu and
            Shiwei Wu and
            Chen Zhu and 
            Linli Xu and 
            Enhong Chen},
  booktitle = {{KDD}},
  publisher = {{ACM}},
  year = {2023}
}
```


## Contact Information

If you have any questions, please contact pfluo@mail.ustc.edu.cn.
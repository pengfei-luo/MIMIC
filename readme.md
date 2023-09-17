<h1 align="center"> Multi-Grained Multimodal Interaction Network for Entity Linking </h1>

<p align="center"> 
  <a href="https://arxiv.org/abs/2307.09721" target="_blank">
    <img alt="arXiv" src="https://img.shields.io/badge/arXiv-FFFFFF?&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyByb2xlPSJpbWciIHZpZXdCb3g9IjAgMCAyNCAyNCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48dGl0bGU%2BYXJYaXY8L3RpdGxlPjxwYXRoIGQ9Ik0zLjg0MjMgMGExLjAwMzcgMS4wMDM3IDAgMCAwLS45MjIuNjA3OGMtLjE1MzYuMzY4Ny0uMDQzOC42Mjc1LjI5MzggMS4xMTEzbDYuOTE4NSA4LjM1OTctMS4wMjIzIDEuMTA1OGExLjAzOTMgMS4wMzkzIDAgMCAwIC4wMDMgMS40MjI5bDEuMjI5MiAxLjMxMzUtNS40MzkxIDYuNDQ0NGMtLjI4MDMuMjk5LS40NTM4LjgyMy0uMjk3MSAxLjE5ODZhMS4wMjUzIDEuMDI1MyAwIDAgMCAuOTU4NS42MzUuOTEzMy45MTMzIDAgMCAwIC42ODkxLS4zNDA1bDUuNzgzLTYuMTI2IDcuNDkwMiA4LjAwNTFhLjg1MjcuODUyNyAwIDAgMCAuNjgzNS4yNTk3Ljk1NzUuOTU3NSAwIDAgMCAuODc3Ny0uNjEzOGMuMTU3Ny0uMzc3LS4wMTctLjc1MDItLjMwNi0xLjE0MDdsLTcuMDUxOC04LjM0MTggMS4wNjMyLTEuMTNhLjk2MjYuOTYyNiAwIDAgMCAuMDA4OS0xLjMxNjVMNC42MzM2LjQ2MzlzLS4zNzMzLS40NTM1LS43NjgtLjQ2M3ptMCAuMjcyaC4wMTY2Yy4yMTc5LjAwNTIuNDg3NC4yNzE1LjU2NDQuMzYzOWwuMDA1LjAwNi4wMDUyLjAwNTUgMTAuMTY5IDEwLjk5MDVhLjY5MTUuNjkxNSAwIDAgMS0uMDA3Mi45NDVsLTEuMDY2NiAxLjEzMy0xLjQ5ODItMS43NzI0LTguNTk5NC0xMC4zOWMtLjMyODYtLjQ3Mi0uMzUyLS42MTgzLS4yNTkyLS44NDFhLjczMDcuNzMwNyAwIDAgMSAuNjcwNC0uNDQwMVptMTQuMzQxIDEuNTcwMWEuODc3Ljg3NyAwIDAgMC0uNjU1NC4yNDE4bC01LjY5NjIgNi4xNTg0IDEuNjk0NCAxLjgzMTkgNS4zMDg5LTYuNTEzOGMuMzI1MS0uNDMzNS40NzktLjY2MDMuMzI0Ny0xLjAyOTJhMS4xMjA1IDEuMTIwNSAwIDAgMC0uOTc2My0uNjg5em0tNy42NTU3IDEyLjI4MjMgMS4zMTg2IDEuNDEzNS01Ljc4NjQgNi4xMjk1YS42NDk0LjY0OTQgMCAwIDEtLjQ5NTkuMjYuNzUxNi43NTE2IDAgMCAxLS43MDYtLjQ2NjljLS4xMTE5LS4yNjgyLjAzNTktLjY4NjQuMjQ0Mi0uOTA4M2wuMDA1MS0uMDA1NS4wMDQ3LS4wMDU1eiIvPjwvc3ZnPg%3D%3D"> 
  </a>
  <a href="https://dl.acm.org/doi/10.1145/3580305.3599439" target="_blank">
    <img alt="Digital Library" src="https://img.shields.io/badge/Digital Library-FFFFFF?&logo=acm&logoColor=black"> 
  </a>
  <a href="#step-2-download-the-data">
    <img alt="Dataset" src="https://img.shields.io/badge/Dataset-FFFFFF?&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA0NDggNTEyIj48IS0tISBGb250IEF3ZXNvbWUgUHJvIDYuNC4wIGJ5IEBmb250YXdlc29tZSAtIGh0dHBzOi8vZm9udGF3ZXNvbWUuY29tIExpY2Vuc2UgLSBodHRwczovL2ZvbnRhd2Vzb21lLmNvbS9saWNlbnNlIChDb21tZXJjaWFsIExpY2Vuc2UpIENvcHlyaWdodCAyMDIzIEZvbnRpY29ucywgSW5jLiAtLT48cGF0aCBkPSJNNDQ4IDgwdjQ4YzAgNDQuMi0xMDAuMyA4MC0yMjQgODBTMCAxNzIuMiAwIDEyOFY4MEMwIDM1LjggMTAwLjMgMCAyMjQgMFM0NDggMzUuOCA0NDggODB6TTM5My4yIDIxNC43YzIwLjgtNy40IDM5LjktMTYuOSA1NC44LTI4LjZWMjg4YzAgNDQuMi0xMDAuMyA4MC0yMjQgODBTMCAzMzIuMiAwIDI4OFYxODYuMWMxNC45IDExLjggMzQgMjEuMiA1NC44IDI4LjZDOTkuNyAyMzAuNyAxNTkuNSAyNDAgMjI0IDI0MHMxMjQuMy05LjMgMTY5LjItMjUuM3pNMCAzNDYuMWMxNC45IDExLjggMzQgMjEuMiA1NC44IDI4LjZDOTkuNyAzOTAuNyAxNTkuNSA0MDAgMjI0IDQwMHMxMjQuMy05LjMgMTY5LjItMjUuM2MyMC44LTcuNCAzOS45LTE2LjkgNTQuOC0yOC42VjQzMmMwIDQ0LjItMTAwLjMgODAtMjI0IDgwUzAgNDc2LjIgMCA0MzJWMzQ2LjF6Ii8%2BPC9zdmc%2B"> 
  </a>
  <a href="https://youtu.be/IyP6vfyU1KE" target="_blank">
    <img alt="Video" src="https://img.shields.io/badge/Video-FFFFFF?&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA1NzYgNTEyIj48IS0tISBGb250IEF3ZXNvbWUgUHJvIDYuNC4wIGJ5IEBmb250YXdlc29tZSAtIGh0dHBzOi8vZm9udGF3ZXNvbWUuY29tIExpY2Vuc2UgLSBodHRwczovL2ZvbnRhd2Vzb21lLmNvbS9saWNlbnNlIChDb21tZXJjaWFsIExpY2Vuc2UpIENvcHlyaWdodCAyMDIzIEZvbnRpY29ucywgSW5jLiAtLT48cGF0aCBkPSJNNTQ5LjY1NSAxMjQuMDgzYy02LjI4MS0yMy42NS0yNC43ODctNDIuMjc2LTQ4LjI4NC00OC41OTdDNDU4Ljc4MSA2NCAyODggNjQgMjg4IDY0UzExNy4yMiA2NCA3NC42MjkgNzUuNDg2Yy0yMy40OTcgNi4zMjItNDIuMDAzIDI0Ljk0Ny00OC4yODQgNDguNTk3LTExLjQxMiA0Mi44NjctMTEuNDEyIDEzMi4zMDUtMTEuNDEyIDEzMi4zMDVzMCA4OS40MzggMTEuNDEyIDEzMi4zMDVjNi4yODEgMjMuNjUgMjQuNzg3IDQxLjUgNDguMjg0IDQ3LjgyMUMxMTcuMjIgNDQ4IDI4OCA0NDggMjg4IDQ0OHMxNzAuNzggMCAyMTMuMzcxLTExLjQ4NmMyMy40OTctNi4zMjEgNDIuMDAzLTI0LjE3MSA0OC4yODQtNDcuODIxIDExLjQxMi00Mi44NjcgMTEuNDEyLTEzMi4zMDUgMTEuNDEyLTEzMi4zMDVzMC04OS40MzgtMTEuNDEyLTEzMi4zMDV6bS0zMTcuNTEgMjEzLjUwOFYxNzUuMTg1bDE0Mi43MzkgODEuMjA1LTE0Mi43MzkgODEuMjAxeiIvPjwvc3ZnPg%3D%3D"> 
  </a>
</p>

<p align="center"> This repository is the official implementation for the paper titled "Multi-Grained Multimodal Interaction Network for Entity Linking".  </p>

<p align="center">
  <img src="model.png" alt="mimic" width="640">
</p>

## News

- [2023.09.17] Updating the method of accessing low-resource data and considerations for reproduce the results.
- [2023.09.16] The detailed values of the experimental results have been updated. Please refer [here](#results).


## Usage

### Step 1: Set up the environment

We recommend using Conda to manage virtual environments, and we use Python version 3.8.12.
```bash
conda create -n mimic python==3.8.12
conda activate mimic
```

Please install the specified versions of Python libraries according to the requirements.txt file.

Note that the versions of PyTorch, Transformers, and PyTorch Lightning may have a slight impact on the results. To fully reproduce the results of the paper, we recommend installing the specified versions.

<div id="dataset"></div>

### Step 2: Download the data

You may download WikiMEL and RichpediaMEL from https://github.com/seukgcode/MELBench and WikiDiverse from https://github.com/wangxw5/wikiDiverse.

Or download our cleaned data [WikiMEL](https://mailustceducn-my.sharepoint.com/:u:/g/personal/pfluo_mail_ustc_edu_cn/ETtT1zwqdDdAmE-uxHMX5EAB7bCGb1Eh2AuafB0tijDdyg?e=IT9E8a), [RichpediaMEL](https://mailustceducn-my.sharepoint.com/:u:/g/personal/pfluo_mail_ustc_edu_cn/ERikbOQuoWFHrA_AizcuCbgB8PBOiRqCV4U0lZfxUN-6kg?e=speIdh), [WikiDiverse](https://mailustceducn-my.sharepoint.com/:u:/g/personal/pfluo_mail_ustc_edu_cn/EQgQKn4VeghChY_lhUoyBIMBKz6aTS00DFKOL1dqxP_bEg?e=yRpKkU) (Password: kdd2023).


### Step 3: Modify the data path

Please modify the configuration files under the "config" directory (including the YAML files for all 3 datasets) and replace `YOUR_PATH` in the `data` field of each configuration file with the path to your corresponding dataset.

**NOTE: Due to the uploaded training files of RichpediaMEL, mention images are stored in the folder `mention_images`. You need to modify the `mention_img_folder` in the `richpediamel.yaml` config file or rename the `mention_images` folder to `mention_image`.** (Thank [Zhiwei Hu](https://github.com/zhiweihu1103) for bringing up this [issue](https://github.com/pengfei-luo/MIMIC/issues/2))

### Step 4: Start the training

Now you can execute `bash run.sh <gpu_id> <dataset_name>` to begin the training.
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

## Results

### Main Result
<details>
<table>
    <tr>
        <td>Model</td>
        <td colspan="5">WikiMEL</td>
        <td colspan=5">RichpediaMEL</td>
        <td colspan="5">WikiDiverse</td>
    </tr>
    <tr>
        <td></td>
        <td>H@1↑</td>
        <td>H@3↑</td>
        <td>H@5↑</td>
        <td>MRR↑</td>
        <td>MR↓</td>
        <td>H@1↑</td>
        <td>H@3↑</td>
        <td>H@5↑</td>
        <td>MRR↑</td>
        <td>MR↓</td>
        <td>H@1↑</td>
        <td>H@3↑</td>
        <td>H@5↑</td>
        <td>MRR↑</td>
        <td>MR↓</td>
    </tr>
    <tr>
        <td>BLINK</td>
        <td>74.66 </td>
        <td>86.63 </td>
        <td>90.57 </td>
        <td>81.72 </td>
        <td>51.48 </td>
        <td>58.47 </td>
        <td>81.51 </td>
        <td>88.09 </td>
        <td>71.39 </td>
        <td>178.57 </td>
        <td>57.14 </td>
        <td>78.04 </td>
        <td>85.32 </td>
        <td>69.15 </td>
        <td>332.03 </td>
    </tr>
    <tr>
        <td>BERT</td>
        <td>74.82 </td>
        <td>86.79 </td>
        <td>90.47 </td>
        <td>81.78 </td>
        <td>51.23 </td>
        <td>59.55 </td>
        <td>81.12 </td>
        <td>87.16 </td>
        <td>71.67 </td>
        <td>278.08 </td>
        <td>55.77 </td>
        <td>75.73 </td>
        <td>83.11 </td>
        <td>67.38 </td>
        <td>373.96 </td>
    </tr>
    <tr>
        <td>RoBERTa</td>
        <td>73.75 </td>
        <td>85.85 </td>
        <td>89.80 </td>
        <td>80.86 </td>
        <td>31.02 </td>
        <td>61.34 </td>
        <td>81.56 </td>
        <td>87.15 </td>
        <td>72.80 </td>
        <td>218.16 </td>
        <td>59.46 </td>
        <td>78.54 </td>
        <td>85.08 </td>
        <td>70.52 </td>
        <td>405.22 </td>
    </tr>
    <tr>
        <td>DZMNED</td>
        <td>78.82 </td>
        <td>90.02 </td>
        <td>92.62 </td>
        <td>84.97 </td>
        <td>152.58 </td>
        <td>68.16 </td>
        <td>82.94 </td>
        <td>87.33 </td>
        <td>76.63 </td>
        <td>313.85 </td>
        <td>56.90 </td>
        <td>75.34 </td>
        <td>81.41 </td>
        <td>67.59 </td>
        <td>563.26 </td>
    </tr>
    <tr>
        <td>JMEL</td>
        <td>64.65 </td>
        <td>79.99 </td>
        <td>84.34 </td>
        <td>73.39 </td>
        <td>285.14 </td>
        <td>48.82 </td>
        <td>66.77 </td>
        <td>73.99 </td>
        <td>60.06 </td>
        <td>470.90 </td>
        <td>37.38 </td>
        <td>54.23 </td>
        <td>61.00 </td>
        <td>48.19 </td>
        <td>996.63 </td>
    </tr>
    <tr>
        <td>VELML</td>
        <td>76.62 </td>
        <td>88.75 </td>
        <td>91.96 </td>
        <td>83.42 </td>
        <td>102.72 </td>
        <td>67.71 </td>
        <td>84.57 </td>
        <td>89.17 </td>
        <td>77.19 </td>
        <td>332.85 </td>
        <td>54.56 </td>
        <td>74.43 </td>
        <td>81.15 </td>
        <td>66.13 </td>
        <td>463.25 </td>
    </tr>
    <tr>
        <td>GHMFC</td>
        <td>76.55 </td>
        <td>88.40 </td>
        <td>92.01 </td>
        <td>83.36 </td>
        <td>54.75 </td>
        <td>72.92 </td>
        <td>86.85 </td>
        <td>90.60 </td>
        <td>80.76 </td>
        <td>214.64 </td>
        <td>60.27 </td>
        <td>79.40 </td>
        <td>84.74 </td>
        <td>70.99 </td>
        <td>628.87 </td>
    </tr>
    <tr>
        <td>CLIP</td>
        <td>83.23 </td>
        <td>92.10 </td>
        <td>94.51 </td>
        <td>88.23 </td>
        <td>17.60 </td>
        <td>67.78 </td>
        <td>85.22 </td>
        <td>90.04 </td>
        <td>77.57 </td>
        <td>107.16 </td>
        <td>61.21 </td>
        <td>79.63 </td>
        <td>85.18 </td>
        <td>71.69 </td>
        <td>313.35 </td>
    </tr>
    <tr>
        <td>ViLT</td>
        <td>72.64 </td>
        <td>84.51 </td>
        <td>87.86 </td>
        <td>79.46 </td>
        <td>220.76 </td>
        <td>45.85 </td>
        <td>62.96 </td>
        <td>69.80 </td>
        <td>56.63 </td>
        <td>675.93 </td>
        <td>34.39 </td>
        <td>51.07 </td>
        <td>57.83 </td>
        <td>45.22 </td>
        <td>2421.49 </td>
    </tr>
    <tr>
        <td>ALBEF</td>
        <td>78.64 </td>
        <td>88.93 </td>
        <td>91.75 </td>
        <td>84.56 </td>
        <td>47.95 </td>
        <td>65.17 </td>
        <td>82.84 </td>
        <td>88.28 </td>
        <td>75.29 </td>
        <td>122.30 </td>
        <td>60.59 </td>
        <td>75.59 </td>
        <td>81.30 </td>
        <td>69.93 </td>
        <td>291.17 </td>
    </tr>
    <tr>
        <td>METER</td>
        <td>72.46 </td>
        <td>84.41 </td>
        <td>88.17 </td>
        <td>79.49 </td>
        <td>111.90 </td>
        <td>63.96 </td>
        <td>82.24 </td>
        <td>87.08 </td>
        <td>74.15 </td>
        <td>376.42 </td>
        <td>53.14 </td>
        <td>70.93 </td>
        <td>77.59 </td>
        <td>63.71 </td>
        <td>944.48 </td>
    </tr>
    <tr>
        <td>MIMIC</td>
        <td>87.98 </td>
        <td>95.07 </td>
        <td>96.37 </td>
        <td>91.82 </td>
        <td>11.02 </td>
        <td>81.02 </td>
        <td>91.77 </td>
        <td>94.38 </td>
        <td>86.95 </td>
        <td>55.11 </td>
        <td>63.51 </td>
        <td>81.04 </td>
        <td>86.43 </td>
        <td>73.44 </td>
        <td>227.08</td>
    </tr>
</table>
</details>


### Low-resource Setting Result

To access low-resource training data, please refer [here](https://github.com/pengfei-luo/MIMIC/issues/2#issuecomment-1712839806).

**10% RichpediaMEL**

<details>

| **Model** | **H@1** | **H@3** | **H@5** | **H@10** | **MRR** |
|-----------|---------|---------|---------|----------|---------|
| DZMNED    | 22.57   | 34.95   | 41.33   | 50.48    | 31.79   |
| JMEL      | 16.70   | 27.68   | 33.63   | 41.55    | 25.01   |
| VELML     | 27.15   | 38.60   | 43.99   | 51.99    | 35.52   |
| GHMFC     | 68.00   | 83.38   | 87.73   | 91.97    | 76.69   |
| ViLT      | 11.73   | 18.59   | 22.07   | 27.32    | 17.05   |
| METER     | 60.89   | 79.23   | 84.78   | 89.42    | 71.40   |
| CLIP      | 62.66   | 79.14   | 85.06   | 90.68    | 72.51   |
| ALBEF     | 63.19   | 79.31   | 84.25   | 89.42    | 72.51   |
| MIMIC     | 64.49   | 82.03   | 87.59   | 92.45    | 74.62   |
</details>

---

**20% RichpediaMEL**
<details>

| **Model** | **H@1** | **H@3** | **H@5** | **H@10** | **MRR** |
|-----------|---------|---------|---------|----------|---------|
| DZMNED    | 36.38   | 52.25   | 58.28   | 67.46    | 47.01   |
| JMEL      | 28.92   | 43.35   | 50.59   | 61.54    | 39.38   |
| VELML     | 48.85   | 64.91   | 71.76   | 79.42    | 59.24   |
| GHMFC     | 72.57   | 86.69   | 90.15   | 93.77    | 80.42   |
| ViLT      | 30.24   | 42.39   | 48.40   | 55.73    | 38.81   |
| METER     | 61.51   | 79.56   | 84.48   | 89.50    | 71.82   |
| CLIP      | 64.32   | 79.59   | 85.54   | 90.96    | 73.72   |
| ALBEF     | 64.21   | 79.47   | 85.32   | 89.92    | 73.02   |
| MIMIC     | 75.60   | 88.63   | 91.72   | 94.67    | 82.73   |
</details>

---

**10% WikiDiverse**
<details>

| **Model** | **H@1** | **H@3** | **H@5** | **H@10** | **MRR** |
|-----------|---------|---------|---------|----------|---------|
| DZMNED    | 11.45   | 22.52   | 29.50   | 37.15    | 19.99   |
| JMEL      | 19.97   | 32.19   | 37.58   | 44.37    | 28.26   |
| VELML     | 30.51   | 46.20   | 52.36   | 59.62    | 40.70   |
| ViLT      | 13.19   | 21.27   | 26.37   | 32.68    | 19.57   |
| METER     | 40.42   | 61.31   | 70.26   | 78.78    | 53.53   |
| CLIP      | 59.87   | 76.52   | 81.57   | 85.95    | 69.49   |
| ALBEF     | 51.83   | 69.20   | 74.64   | 81.57    | 62.26   |
| GHMFC     | 48.08   | 66.31   | 74.25   | 81.91    | 59.56   |
| MIMIC     | 60.54   | 76.18   | 81.33   | 86.14    | 69.70   |
</details>

---

**20% WikiDiverse**
<details>

| **Model** | **H@1** | **H@3** | **H@5** | **H@10** | **MRR** |
|-----------|---------|---------|---------|----------|---------|
| DZMNED    | 28.73   | 47.35   | 56.69   | 63.96    | 40.97   |
| JMEL      | 29.26   | 44.23   | 49.90   | 57.22    | 39.05   |
| VELML     | 43.65   | 61.36   | 67.66   | 74.88    | 54.76   |
| ViLT      | 20.93   | 32.92   | 38.93   | 47.26    | 29.48   |
| METER     | 40.23   | 61.16   | 70.45   | 80.56    | 53.46   |
| CLIP      | 59.96   | 77.05   | 82.24   | 86.86    | 69.95   |
| ALBEF     | 56.40   | 73.87   | 78.97   | 85.08    | 66.56   |
| GHMFC     | 51.73   | 71.85   | 78.54   | 84.50    | 63.46   |
| MIMIC     | 61.01   | 77.67   | 83.35   | 88.88    | 70.52   |
</details>

---


## Citation
If you find this project useful in your research, please cite the following paper:
```bibtex
@inproceedings{luo2023multi,
    author = {Luo, Pengfei and Xu, Tong and Wu, Shiwei and Zhu, Chen and Xu, Linli and Chen, Enhong},
    title = {Multi-Grained Multimodal Interaction Network for Entity Linking},
    year = {2023},
    publisher = {Association for Computing Machinery},
    booktitle = {Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining},
    pages = {1583–1594},
}
```


## Contact Information

If you have any questions, please contact pfluo@mail.ustc.edu.cn.
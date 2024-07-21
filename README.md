# LLM-guided Instance-level Image Manipulation with Diffusion Models
Summer semster 2024, Large Language Models Course Project. By Andrei Palaev and Anatoliy Baskakov

## Introduction

This project aims to enhance the pipeline for instance-level image manipulation by leveraging multimodal Large Language Models (LLMs). The existing pipeline, which utilizes separate models for object detection and manipulation, is integrated with multimodal LLMs to streamline the process and reduce computational resources. The original pipeline can be found here: [https://github.com/Palandr123/editing-diffusion](https://github.com/Palandr123/editing-diffusion).

### Pipeline Overview

1. **Prompt-Based Image Generation**: The user provides a prompt, and an image is generated using Stable Diffusion XL \[[Podell et al., 2023](https://arxiv.org/abs/2307.01952)\].
2. **Object and Attribute Extraction**: Gemma-7B \[[Gemma Team, 2024](https://arxiv.org/abs/2403.08295)\] extracts objects and attributes from the prompt.
3. **Object Detection**: OWLv2 \[[Minderer et al., 2023](https://arxiv.org/abs/2306.09683)\] detects these objects in the generated image, following the method by Wu et al. \[[Wu et al., 2023](https://arxiv.org/abs/2311.16090)\].
4. **User-Driven Manipulation**: The user specifies which object to manipulate and how (e.g., move or remove). Manipulations are performed using guidance based on intermediate features and cross-attention maps in the diffusion model.

### Project Goals

- Explore the effect of replacing LLM with multimodal LLM on the object extraction part.

## Methodology

We explored the following replacements for Gemma-7B:

- Falcon-11B
- LLaVa-NeXT with Mistral-7B
- BLIP-2

## How to Run

1. Clone the Repository:
    ```bash
    git clone https://github.com/Palandr123/LLMs-Project
    cd LLMs-Project
    ```
2. Get [poetry](https://python-poetry.org/)
3. Create and activate virtual environment using venv or conda
4. Install project requirements: `poetry install`

## Results

Results of different multimodal LLMs can be found in the corresponding notebooks.

## Acknowledgements

This project is based on several state-of-the-art models and frameworks:
- [Stable Diffusion XL](https://arxiv.org/abs/2307.01952)
- [Gemma-7B](https://arxiv.org/abs/2403.08295)
- [OWLv2](https://arxiv.org/abs/2306.09683)
- [Falcon-11B](https://huggingface.co/tiiuae/falcon-11B-vlm)
- [LLaVa-NeXT](https://llava-vl.github.io/blog/2024-01-30-llava-next/)
- [BLIP-2](https://arxiv.org/abs/2301.12597)

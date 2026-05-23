# Recursive Generation Depth Estimation

Code for "Recursive Generation Depth Estimation: How Many Times Has This Text Been Through the Loop?"

## Overview

This repository contains code for estimating the ordinal recursive generation depth (d0-d3) of text passages using statistical features and Random Forest classification.

## Structure

- `src/` — Core pipeline: feature extraction, atlas construction, evaluation
- `scripts/` — Training, generation, baseline evaluation scripts  
- `artifacts/` — Experiment-specific scripts (baselines, ablations, analysis)
- `figures/` — Paper figure generation scripts

## Requirements

- Python 3.10+
- PyTorch 2.0+
- transformers, datasets, scikit-learn, scipy, numpy, pandas

Install dependencies:
```bash
pip install torch transformers datasets scikit-learn scipy numpy pandas tqdm wandb peft
```

## Pipeline

1. **Data generation**: `scripts/lora_finetune.py` → `scripts/generate_next_depth.py` (repeat for each depth)
2. **Feature extraction & classification**: `src/atlas_v2.py`
3. **Evaluation**: `src/binary_pairwise_eval.py` (pairwise AUC / EDD computation)

## Baselines

- DeBERTa end-to-end: `src/n2_deberta_finetune.py`
- CORAL ordinal regression: `scripts/baseline_coral.py`
- DetectGPT / Binoculars / Min-K%: `scripts/detection_baselines_ordinal.py`
- Zero-shot LLM: `scripts/baseline_zeroshot_llm.py`
- Perplexity regression: `scripts/baseline_ppl_regression.py`

## License

MIT

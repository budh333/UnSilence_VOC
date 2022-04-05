# Source code

## Description

We make use of the best model configuration established in recent work on NER for historical documents. We use the model from the paper "Transfer learning for historical corpora: An assessment on post-OCR correction and named entity recognition", which can be found [here](https://github.com/ktodorov/eval-historical-texts/) and more specifically only the Named Entity Recognition part of it. 

The text representation layer combines a variety of embeddings, including character-level embeddings and those produced from trained BERT models. Here we use [BERTje](https://huggingface.co/wietsedv/bert-base-dutch-cased), a state-of-the-art Dutch version of BERT. All embeddings are concatenated and followed by a Bi-LSTM-CRF layer. 

We use and compare single-task and multi-task approaches. The former focuses on learning one entity type at a time, whereas the latter combines these tasks into a single model.

## Requirements

See [`environment.yml`](environment.yml) for a full list of modules and libraries that were used during development, as well as a way to restore this environment using Conda.

## Implementation

Due to the generalization of the framework, you need ot specify the challenge which you are executing, in this case `named-entity-recognition` and the configuration - `bi-lstm-crf`. The main file to be run is `run.py`. 

For a full list of supported arguments, please refer to the original repository documentation, found [here](https://github.com/ktodorov/eval-historical-texts/blob/master/docs/arguments/base_arguments.md) and the NER specific arguments found [here](https://github.com/ktodorov/eval-historical-texts/blob/master/docs/arguments/ner_arguments_service.md)

### Running

The original run configurations can be found in the [launch file](.vscode/launch.json). Furthermore, job files used to train and evaluate the model configurations can also be found in `jobs` directory.

## Data

We generate machine-readable IOB format from the original annotations using the notebook [`process_data.ipynb`](../notebooks/process_data.ipynb). Original processed and split data can be found in the `processed_data` folder. We use 70-10-20 ratios for Training-Dev-Test sets respectively.
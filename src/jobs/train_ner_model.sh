#!/bin/bash
#SBATCH --job-name=tr-ocr
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=3
#SBATCH --ntasks-per-node=1
#SBATCH --time=72:00:00
#SBATCH -p gpu_shared
#SBATCH --gpus=1

module purge
module load 2020
# module load Python
module load Python/3.8.2-GCCcore-9.3.0

LEARNINGRATE="$LR"
if [ -z "$LR" ]
then
    LEARNINGRATE="1e-2"
fi

PATIENCEARG="$PATIENCE"
if [ -z "$PATIENCE" ]
then
    PATIENCEARG="15"
fi

EVALFREQARG="$EVALFREQ"
if [ -z "$EVALFREQ" ]
then
    EVALFREQARG="50"
fi

BATCHSIZEARG="$BATCHSIZE"
if [ -z "$BATCHSIZE" ]
then
    BATCHSIZEARG="4"
fi

LANGUAGEARG="dutch"
if [ ! -z "$LANGUAGE" ]
then
    LANGUAGEARG="$LANGUAGE"
fi

SEEDARG="13"
if [ ! -z "$SEED" ]
then
    SEEDARG="$SEED"
fi

RESUMETRAININGARG=""
if [ ! -z "$RESUMETRAINING" ]
then
    RESUMETRAININGARG="--resume-training"
fi

echo 'EXECUTING... srun python -u run.py --configuration bi_lstm_crf --challenge named-entity-recognition --epochs 500000 --device cuda --eval-freq ' $EVALFREQARG ' --seed ' $SEEDARG ' --learning-rate ' $LEARNINGRATE ' --metric-types f1-score precision recall --language ' $LANGUAGEARG ' --batch-size ' $BATCHSIZEARG ' --patience ' $PATIENCEARG ' --include-pretrained-model --pretrained-model bert --pretrained-model-size 768 --pretrained-max-length 512 --dropout 0.5 --number-of-layers 1 --entity-tag-types main gender legal-status role --no-attention --bidirectional-rnn --pretrained-weights wietsedv/bert-base-dutch-cased --merge-subwords --learn-character-embeddings --character-embeddings-size 16 --character-hidden-size 32 --hidden-dimension 512 --embeddings-size 32 --bidirectional-rnn --replace-all-numbers --enable-external-logging ' $RESUMETRAININGARG

srun python -u run.py --configuration bi_lstm_crf --challenge named-entity-recognition --epochs 500000 --device cuda --eval-freq $EVALFREQARG --seed $SEEDARG --learning-rate $LEARNINGRATE --metric-types f1-score precision recall --language $LANGUAGEARG --batch-size $BATCHSIZEARG --patience $PATIENCEARG --include-pretrained-model --pretrained-model bert --pretrained-model-size 768 --pretrained-max-length 512 --dropout 0.5 --number-of-layers 1 --entity-tag-types main gender legal-status role --no-attention --bidirectional-rnn --pretrained-weights wietsedv/bert-base-dutch-cased --merge-subwords --learn-character-embeddings --character-embeddings-size 16 --character-hidden-size 32 --hidden-dimension 512 --embeddings-size 32 --bidirectional-rnn --replace-all-numbers --enable-external-logging $RESUMETRAININGARG
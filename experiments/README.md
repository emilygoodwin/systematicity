# Experiments

Code heavily borrowed from [InferSent](https://github.com/facebookresearch/InferSent/) repository.

## Dependencies

- Dependencies of [InferSent](https://github.com/facebookresearch/InferSent/)
- Comet.ML API

## Prepare data

Use `convert.py` to convert the data into InferSent repository format.

## Training

```
python train_nli.py --nlipath "/path/to/step_0/" 
                    --outputdir "/path/to/outputs/" 
                    --optimizer "adam,lr=0.001" 
                    --encoder_type "InferSent" 
                    --lrshrink 0.9 
                    --enc_lstm_dim 300 
                    --word_emb_type "normal" 
                    --comet_apikey "<your api key>" 
                    --comet_workspace "<your workspace>" 
                    --comet_project "compositionality-nli" 
                    --seed 20
```

## Calculate Statistics

- [`score-perturbations.py`](experiments/score-perturbations.py) : Calculates statistics related to various probing perturbations on the output

# Survey of Abstract Summarization Techniques

**Abstractive Summarization:** Summarization of a collection of text whereby new terms and sentences are generated to aid in the summarization rather than taking sentences from within the input text.

**Coverage:** This paper covers T5, Pegasus, and ProphetNet which are tested across several wikipedia datasets.

### T5 Model

- Trained via deshuffling (shuffle words in a sentence and ask the model to predict the original text), denoting (masking), and language modeling (predicting the subsequent word)
  - Denoising proved most effective as a training objective
  - Unclear what the test metrics where

### Pegasus

- Similar to T5

### ProphetNet

- Trained to predict the future n terms w/ probabilities
- Has a "n-stream self-attention in the transformer decoder"
  - Each i-th stream predicts the future stream y_i based on the previous tokens y_<i

## Experiments

- Datasets are all truncated to 512 words and cleaned up to remove new lines, data is then tokenized/encoded and fed to the model
  - Shouldn't the model's encoder handle the encoding?
- Experimented on a large variation of the T5 model (T5-Large)
- Three variants of Pegasus (Pegasus- XSum, Pegasus-Multi_News, Pegasus-Wikihow)
- Three variants of ProphetNet (ProphetNet-XGlue-NTG, ProphetNet-CNNDM, ProphetNet-Squad-QG)
- Results are reported through the ROUGE metric
  - ROUGE is just the F1 metric
  - ROUGE-1-F computes the overlap of single words between the generated versus the reference summaries
  - ROUGE-2-F computes the overlap of two consecutive words between the generated versus reference summaries
  - ROUGE-L-F computes the longested matching sequence of words between the generated and reference summaries
  - Another one used is BLUE, both aren't great though, automatic but you give up a lot

## Results

- T5-Large and Pegasus-XSum perform the best


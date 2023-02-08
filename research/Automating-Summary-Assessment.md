# Automating Summary Assessment

**Date: Feb 6th 2023**

## 1. Code Cleaning

**Motivation:** As we move away from designing an MVP and begin taking steps towards further improving our existing solution we need a way to automatically assess summary qualities, in this vein two immediate needs emerge

1. We need a method of generating various hyperparameter experiment runs
2. We need to be able to quickly run large amounts of tests at scale 

All code is implemented in [data_generation.py](../code/data_generation.py).

### 1.1 Automating the Running of Multiple Parameters

A new system has been set up which takes a parameter (likely to be expanded on overtime) denoted by this following `namedtuple`:

```python
Param = namedtuple('Param', ['param_name', 'prompt_seq', 'model', 'runs', 'input_path'])
```

These parameters are stored in a dedicate JSON file labelled [experiment_parameters.json](../data/experiment_parameters.json). In  [data_generation.py](../code/data_generation.py) we have the function `update_json_params()` which takes in a list of `Params`and updates the JSON before running experients using the parameter setup. Each parameter is given a unique name within the JSON to ensure replicability. If a new params setup shares the same name as an existing one in the JSON and the parameters are not identical an error is raised and the python script exits.

### 1.2 Improving Runtime

As the raw number of model inferencing calls occurring quickly cross the 100s we have overhauled the code`run_experiments()` to implement a `BATCH_SIZE` setting which batches the requests we make to the OpenAI model. We observe the following a **4x** efficiency uplift seen in the table below:

| Batch Size | Time Taken (mins) |
| :--------: | :---------------: |
|     1      |        84         |
|     5      |        21         |



## 2. Fine-Tuning

Using the improved code we were able to quickly generate a large amount of data (at the expense of a lot of tokens!) and apply finetuning to train a classifier, the goal of which is to help label summaries as whether it meets our MVP requirements (labelled by 1) or not (labelled by 0). The fine-tuning code can be found in [this notebook](../code/finetuning_classifier-updated.ipynb). Since we are more concerned with accurately detecting summaries that do not meet out MVP requirements we set 0 to be our positive class.

As a reminder: 

- **Precision = TruePositives / (TruePositives + FalsePositives)**
- **Recall = TruePositives / (TruePositives + FalseNegatives)**.

### 2.1 FineTuning via DaVinci

Results: [davinci_finetuning_results.csv](../finetuning_results/davinci_finetuning_results.csv)

Training Loss: 0.01

Validation Loss: 0.01

Classification Accuracy: 90%

Precision: 89%

Recall: 94%

### 2.2 FineTuning via Ada

Results: [ada_finetuning_results.csv](../finetuning_results/ada_finetuning_results.csv)

Training Loss: 0.01

Validation Loss: 0.01

Classification Accuracy: 89%

Precision: 93%

Recall: 85%

### 2.3 Conclusions

OpenAI mentions in their documentation that using Ada as a base model was sufficient for classification purposes. Judging from our results we can confirm this is indeed the case. 

When we're evaluating future summaries either model should be equally sufficient however if in the future we use these classifiers as a conditional block to see if the generated summary is acceptable it would be beneficial to use the DaVinci model due to its higher recall since the cost of poor summaries passing through this inspection would be high.
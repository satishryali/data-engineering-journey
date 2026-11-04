# Fine-tuning, quantization and model memory

We can adapt an existing model to a task instead of training a language model from the beginning. These terms help us choose a model, understand training settings and see why memory matters.

## Starting model and weights

- **Pretraining:** the original large training process that teaches a model patterns from data.
- **Base model:** usually the pretrained model before instruction tuning. People also use this phrase loosely for the starting model of a fine-tuning run.
- **Instruction-tuned model:** a model already trained to follow instructions and answer requests.
- **Parameters or weights:** the learned numbers used in the model's calculations.
- **Fine-tuning:** further training that updates some or all trainable weights for a task.
- **Inference:** running the model to generate an answer. It does not normally update weights.
- **Prompting:** changing the request or its examples without changing model weights.

In `qwen3:4b`, Qwen3 is the model family/generation. The 4B tag means about four billion parameters; the published model details list about 4.02 billion, or 402 crore.

Ollama mainly runs models. A usual workflow is to fine-tune with training tools, export a compatible model, and then run it with Ollama. Downloading a model or chatting with it is not a training run.

## Dataset and tokens

| Term | Meaning |
| --- | --- |
| Dataset | A collection of examples |
| Sample or training example | One item in the dataset |
| Target | The answer or token predictions we want the model to learn |
| Token | A piece of text, such as a word, part of a word or punctuation; tokenizers differ |
| Sequence length | Number of tokens in one training sequence |
| Context window | Maximum number of tokens the configured model can work with in a request, including relevant input and generated output |

Example goal: answer SQL questions in a chosen format.

```text
Input: Find customers with more than five orders.

Target:
SELECT customer_id
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 5;
```

This is a tutor example, not an executed query or a learner training result. The SQL assumes an orders table with customer_id.

For supervised fine-tuning, we provide examples of desired behaviour. The training setup decides which tokens contribute to the loss; many chat setups train on the assistant answer tokens.

## Loss and learning updates

```text
Examples -> forward pass -> loss -> backpropagation -> optimizer update
```

- **Forward pass:** process the input and calculate predictions.
- **Loss:** a number measuring prediction error against training targets. Language models commonly learn to predict the next token.
- **Gradient:** how changing a trainable parameter would change the loss locally.
- **Backpropagation:** calculate those gradients through the model.
- **Optimizer:** use gradients to update trainable weights. AdamW is one example.
- **Learning rate:** control the size of the update. Too high can disrupt useful behaviour; too low can make learning slow or ineffective.
- **Hyperparameters:** settings chosen for training, such as learning rate, batch size and epochs.

A lower training loss does not prove that the model answers unfamiliar questions correctly. Check separate evaluation examples.

## Batches, steps and epochs

- **Batch size:** examples processed together. Check whether a tool means per-device batch size or total batch size.
- **Gradient accumulation:** process several small batches and combine their gradients before one optimizer update.
- **Step:** often one optimizer update. A tool can also report microsteps for the smaller batches.
- **Epoch:** one complete pass through the training dataset.

Illustrative single-GPU settings:

```text
Training examples:             1,000
Batch size:                       2
Gradient accumulation steps:      8
Effective batch size:            16
Epochs:                           3
```

Effective batch size is 2 x 8 = 16 examples per update. Three epochs mean each example is encountered three times in an ordinary full-pass setup.

Accumulation reduces the memory needed for each small batch. It does not avoid processing the examples or guarantee identical results to one large batch.

## Full fine-tuning, LoRA and QLoRA

| Term | Meaning |
| --- | --- |
| Full fine-tuning | Update all original model weights |
| Frozen weights | Used during calculations but not updated |
| PEFT | Parameter-Efficient Fine-Tuning: train a small subset or added parameters |
| LoRA | Add small trainable matrices to selected model layers while freezing original weights |
| Adapter | Additional learned weights used with the original model; LoRA is one adapter method |
| QLoRA | Keep the original model in a quantized, usually 4-bit form and train LoRA adapters |
| LoRA rank, r | Controls the size of the LoRA matrices; higher rank adds trainable parameters and memory needs |

QLoRA does not mean every calculation or trainable adapter uses four bits. The frozen model is compressed; adapters, gradients and working data can use higher precision.

Training needs memory for forward/backward working data and, for trainable parameters, gradients and optimizer state. Being able to run a model does not prove that full fine-tuning will fit.

## Quantization and four bits

Quantization represents numerical values using a smaller set of levels. It saves memory by using fewer bits, with some approximation error.

A bit is 0 or 1. Four bits can represent 2^4 = 16 codes. A group of weights can use those codes with scales and other information to interpret them. Codes do not necessarily represent the same values across every group.

Simple arithmetic illustration, not an actual quantization algorithm:

```text
Original:     0.738 x 2 + 0.123 x 3 = 1.845
Approximate:  0.700 x 2 + 0.100 x 3 = 1.700
```

Changing weights changes intermediate calculations. Those changes can affect the next-token scores and sometimes change the generated answer. Often the approximation preserves useful behaviour, but accuracy can decrease. Speed depends on the hardware and implementation.

Quantization keeps the same parameter count. A 4B model remains a 4B model after quantization.

Approximate weight storage for exactly four billion parameters, using decimal GB:

| Precision | Bytes per weight | Weights alone |
| --- | ---: | ---: |
| 32-bit | 4 | 16 GB |
| 16-bit | 2 | 8 GB |
| 4-bit | 0.5 | 2 GB |

Real files also contain scales, metadata and sometimes higher-precision tensors. The default Qwen3 4B Q4_K_M download is about 2.5 GB; its entire runtime memory requirement is larger. Q4_K_M is a particular quantization scheme, not a promise that every value occupies exactly four bits.

## RAM, VRAM and conversation memory

- **System RAM:** working memory used by the CPU, operating system and applications.
- **VRAM:** memory on the GPU, used for its calculations and data.
- **KV cache:** stored attention keys and values for processed tokens. It avoids recalculating that information during generation; it is not a permanent factual memory.
- **Working buffers:** temporary space for calculations.
- **Offloading:** placing some model computation/data on another device. Ollama can split layers between CPU and GPU.
- **Page file:** disk space Windows can use when system RAM is under pressure. Disk is much slower than RAM.

```text
Inference memory needs
  = weights + KV cache + working buffers + runtime overhead
```

Longer context generally increases KV-cache memory. Other applications reduce the available RAM and VRAM. System RAM does not become equally fast GPU memory just because Windows reports shared GPU memory.

If the model does not fit entirely in VRAM, partial CPU execution may work but usually reduces speed. If RAM also fills and the system pages heavily, responses can become much slower.

## This desktop's measured hardware

Read-only hardware checks in this conversation on 3 November 2026 found:

| Component | Observed value |
| --- | --- |
| CPU | Intel Core i7-12700K; 12 cores, 20 threads |
| Installed system RAM | About 16 GB; Windows reported 15.8 GB |
| GPU | NVIDIA GeForce RTX 3050 |
| Dedicated VRAM | 6 GB, verified using nvidia-smi |
| Free system RAM at inspection | About 2.3 GB |
| Free VRAM at inspection | 4,604 MiB, about 4.5 GiB |
| Free disk space at inspection | C: about 96 GB; G: about 91 GB |

Free memory and disk space are snapshots, not permanent specifications. Windows CIM's AdapterRAM value was insufficient for this GPU; nvidia-smi confirmed its full 6 GB capacity.

The learner reported using Qwen3 4B. A quantized 3-4B model with a modest context, such as 4,096 tokens, is a practical starting choice for this machine. Close unused applications first. Larger 7-8B models may need CPU assistance. No model speed, full GPU fit or training run was benchmarked here.

The older reminder note describes a different reported laptop with RTX 2050 hardware. Do not replace that historical record with this desktop's specifications.

## Evaluation and common training problems

- **Training set:** examples used to update weights.
- **Validation set:** separate examples used to monitor progress and choose settings.
- **Test set:** held-out examples for final evaluation; repeatedly tuning against it weakens the test.
- **Overfitting:** doing well on training examples but poorly on unfamiliar examples.
- **Underfitting:** not learning enough of the intended patterns.
- **Catastrophic forgetting:** losing some previous useful abilities during further training.
- **Evaluation:** checking performance on the intended task. For SQL, this can include whether a query returns the right records, not just whether it looks reasonable.

Keep related template variations together when splitting data. Otherwise, near-duplicate examples can make test results look better than real performance. See [the existing reminder evaluation notes](reminder-model-basics.md#check-the-answer-before-training).

## Checkpoints and export

- **Checkpoint:** saved model/training state. A resumable training checkpoint may include adapters or weights, optimizer state, scheduler state and step position. Contents depend on the tool.
- **Adapter merge:** combine LoRA changes into original model weights.
- **GGUF:** a model file format used by local inference tools, including supported imports in Ollama. It is not itself a particular bit precision.

A possible workflow is: training-compatible starting model -> fine-tune -> evaluate -> export/convert and quantize as needed -> run in Ollama. Compatibility depends on the model architecture and tools.

For answers drawn from changing documents, retrieval-augmented generation (RAG) supplies relevant document text in the request. Fine-tuning is more suited to learned behaviour, style and task patterns; it is not a reliable facts database.

## Sources and learning status

- [Qwen3 4B: size, parameter count and quantization](https://ollama.com/library/qwen3:4b)
- [Hugging Face LoRA guide](https://huggingface.co/docs/peft/main/en/conceptual_guides/lora)
- [QLoRA paper](https://arxiv.org/abs/2305.14314)
- [Ollama model import guide](https://docs.ollama.com/import)
- [Reminder model basics](reminder-model-basics.md)
- [Recall questions without answers](../revision/fine-tuning-questions.md)

Saved from this conversation on 3 November 2026. Explanations and examples were tutor-supplied. Hardware inspection was performed; no learner training run, independent concept assessment, model benchmark or answered epoch recall question was supplied. Cloud rental prices are variable and are not stored as fixed promises.

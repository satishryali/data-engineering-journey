# A small model for reminders

We want to type a reminder in normal words and turn it into fields an app can save. A small model can help interpret the sentence; the app must check and store the result.

## Running and fine-tuning

- Qwen2.5 0.5B has about 500 million learned parameters. Parameters are numbers adjusted during training.
- Running the downloaded model to answer a request is called inference.
- Prompting means changing the instructions or giving an example in the request. It does not change model weights.
- Fine-tuning means further training on input-and-answer examples. LoRA trains small adapter weights while leaving the original weights frozen.
- The installed Ollama model is compressed for inference. Our planned training workflow needs training-compatible weights separately.
- Training uses more memory than simply running the model. The laptop has an RTX 2050 with 4 GB VRAM and about 12 GB system RAM; a small training trial is still needed.
- The model extracts fields. Application code saves reminders and schedules notifications. A model response alone does not create a reminder.

## Check the answer before training

Input used in this session:

```text
Remind me to soak nuts every day at 7 am.
```

Expected fields:

```json
{"task":"soak nuts","time":"07:00","repeat":"daily"}
```

The learner ran several prompts. In the fresh Ollama session, the actual reported output was:

```json
{"task":"soak nuts","time":"daily","repeat":"daily"}
```

The task and repeat match, but the time is wrong. Valid JSON does not mean correct information. Earlier prompts also confused time and repetition or omitted the task. These are model errors, not learner misconceptions.

These results are a baseline: observations before training. One repeatedly tested sentence does not measure general accuracy. Later we need different reminders, missing details and untouched test examples. Compare the same conditions before and after training, including compression and prompt settings where possible.

## Create input and answer pairs

An interactive collector asks for the task, time and daily repetition. These verified answers can produce sentences and their matching target fields.

For example, task `water plants`, time `18:00` and daily repetition can produce:

```text
Input: Remind me to water plants every day at 6 pm.
Target: {"task":"water plants","time":"18:00","repeat":"daily"}
```

This is a planned example, not an observed model success. JSONL stores one complete JSON object per line. Training tools may require a particular chat format around the input and answer.

Review generated examples. Do not invent a time when someone only says morning. Do not treat an unspecified repeat as proof that the reminder is one-time. Dates and weekly recurrence need an expanded schema; the current three-field prototype does not cover them.

Template variations are similar to one another. Keep related variations together when splitting data so the test set does not repeat training patterns. Later, corrected real requests can supply more varied examples. A handful of examples is only a starting specification, not enough evidence of training success.

## Sources and session evidence

- [Qwen model card](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct)
- [LoRA explanation](https://huggingface.co/docs/peft/main/en/conceptual_guides/lora)
- [Ollama import guide](https://docs.ollama.com/import)
- [Saved attempts and project handoff](../../progress/ai-reminder/2026-10-28-session.md)
- [Recall questions without answers](recall-questions.md)

Explained and explored on 28 October 2026. No training run, independent AI concept assessment, mobile runtime test or notification delivery has been completed.

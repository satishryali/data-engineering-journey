# Fine-tuning and memory recall questions

Try one small task without opening the explanation note. State any notes or help used. These are unanswered prompts, not completed reviews.

## Weights and quantization

1. What does 4B mean in qwen3:4b? Does four-bit quantization change that count?
2. Why can approximating a weight change the model's answer? Give a small arithmetic example.
3. Estimate weight-only storage for four billion parameters at 16 bits and four bits. What else needs memory?

## Memory

4. Explain the difference between this desktop's 16 GB RAM and 6 GB VRAM.
5. Why can a model need more runtime memory than its download size? What changes as context grows?
6. Why might a model run more slowly when some layers use the CPU? Why does closing a browser not add dedicated VRAM to the GPU?

## Training

7. Define dataset, sample, target and token using one SQL question.
8. Describe forward pass, loss, backpropagation and optimizer update in order.
9. With 1,000 examples and three epochs, how many times is each example encountered in an ordinary full-pass setup?
10. On one GPU, what is the effective batch size when batch size is two and gradient accumulation is eight?
11. Which weights change in full fine-tuning, LoRA and QLoRA? Why can training need more memory than inference?
12. Why does lower training loss not prove better performance on new SQL questions? Distinguish validation and test sets.
13. What is saved in a resumable checkpoint, and how is that different from an exported inference model?

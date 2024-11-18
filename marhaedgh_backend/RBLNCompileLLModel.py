from optimum.rbln import RBLNLlamaForCausalLM
import os

# Compile HuggingFace PyTorch Llama3 model as RBLN format (vllm)
model_id = "MLP-KTLim/llama-3-Korean-Bllossom-8B"

tensor_parallel_size = 8
batch_size = 8
max_seq_len = 4096

model_save_dir = (
    f"rbln_vllm_{os.path.basename(model_id)}"
    f"_npu{tensor_parallel_size}"
    f"_batch{batch_size}"
    f"_max{max_seq_len}"
)

model = RBLNLlamaForCausalLM.from_pretrained(
    model_id=model_id,
    export=True,
    rbln_max_seq_len=max_seq_len,                   # Setting max sequence length
    rbln_tensor_parallel_size=tensor_parallel_size, # Number of ATOMs to utilize for Rebellions Scalable Design (RSD)
    rbln_batch_size=batch_size,                     # Recommended to use batch_size > 1 for continuous batching
    rbln_batching="vllm",                           # Required to set `vllm` option for continuous batching
)
model.save_pretrained(model_save_dir)

print("Model is saved as: ", model_save_dir)
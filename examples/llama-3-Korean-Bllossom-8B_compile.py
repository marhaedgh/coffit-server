from optimum.rbln import RBLNLlamaForCausalLM

def main():
    # HuggingFace PyTorch Llama3 모델을 RBLN 컴파일된 모델로 내보내기
    model_id = "MLP-KTLim/llama-3-Korean-Bllossom-8B"
    compiled_model = RBLNLlamaForCausalLM.from_pretrained(
        model_id=model_id,
        export=True,
        rbln_max_seq_len=4096,
        rbln_tensor_parallel_size=4,  # Rebellions Scalable Design (RSD)를 위한 ATOM+ 개수
        rbln_batch_size=4,            # Continous batching을 위해 batch_size > 1 권장
    )

    compiled_model.save_pretrained("rbln-ko-Llama3-Bllossom-8B")
    print("완료")

if __name__ == "__main__":
    main()
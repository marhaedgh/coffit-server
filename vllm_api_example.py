import asyncio
from transformers import AutoTokenizer
from vllm import AsyncEngineArgs, AsyncLLMEngine, SamplingParams

def main():

  # Please make sure the engine configurations match the parameters used when compiling.
  model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
  max_seq_len = 4096
  batch_size = 4

  engine_args = AsyncEngineArgs(
    model=model_id,
    device="rbln",
    max_num_seqs=batch_size,
    max_num_batched_tokens=max_seq_len,
    max_model_len=max_seq_len,
    block_size=max_seq_len,
    compiled_model_dir="rbln-Meta-Llama-3-8B-Instruct",
  )
  engine = AsyncLLMEngine.from_engine_args(engine_args)

  tokenizer = AutoTokenizer.from_pretrained(model_id)

  def stop_tokens():
    eot_id = next((k for k, t in tokenizer.added_tokens_decoder.items() if t.content == "<|eot_id|>"), None)
    if eot_id is not None:
      return [tokenizer.eos_token_id, eot_id]
    else:
      return [tokenizer.eos_token_id]

  sampling_params = SamplingParams(
    temperature=0.0,
    skip_special_tokens=True,
    stop_token_ids=stop_tokens(),
  )

  # Runs a single inference for an example
  async def run_single(chat, request_id):
    results_generator = engine.generate(chat, sampling_params, request_id=request_id)
    final_result = None
    async for result in results_generator:
      # You can use the intermediate `result` here, if needed.
      final_result = result
    return final_result

  async def run_multi(chats):
    tasks = [asyncio.create_task(run_single(chat, i)) for (i, chat) in enumerate(chats)]
    return [await task for task in tasks]

  conversation = [{"role": "user", "content": "What is the first letter of English alphabets?"}]
  chat = tokenizer.apply_chat_template(conversation, add_generation_prompt=True, tokenize=False)
  result = asyncio.run(run_single(chat, "123"))
  print(result)

  # Runs multiple inferences in parallel
  conversations = [
    [{"role": "user", "content": "What is the first letter of English alphabets?"}],
    [{"role": "user", "content": "한국의 성씨에 대해서 설명해줘. 이 질문에 대한 답은 한국어로 해줘"}],
    [{"role": "user", "content": "What is the third letter of English alphabets?"}],
    [{"role": "user", "content": "What is the fifth letter of English alphabets?"}],
    [{"role": "user", "content": "내가 대회에서 우승할 수 있는 확률을 계산하는 법을 알려줘."}],
  ]
  chats = [
    tokenizer.apply_chat_template(conversation, add_generation_prompt=True, tokenize=False)
    for conversation in conversations
  ]
  results = asyncio.run(run_multi(chats))
  print(results)

if __name__ == "__main__":
    main()
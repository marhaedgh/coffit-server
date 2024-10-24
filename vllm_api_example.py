import asyncio
from transformers import AutoTokenizer
from vllm import AsyncEngineArgs, AsyncLLMEngine, SamplingParams

def main():

  # Please make sure the engine configurations match the parameters used when compiling.
  #model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
  #model_id = "saltlux/Ko-Llama3-Luxia-8B"
  model_id = "MLP-KTLim/llama-3-Korean-Bllossom-8B"
  max_seq_len = 4096
  batch_size = 4

  engine_args = AsyncEngineArgs(
    model=model_id,
    device="rbln",
    max_num_seqs=batch_size,
    max_num_batched_tokens=max_seq_len,
    max_model_len=max_seq_len,
    block_size=max_seq_len,
    #compiled_model_dir="rbln-Meta-Llama-3-8B-Instruct",
    #compiled_model_dir="rbln-ko-Llama3-Luxia-8B",
    compiled_model_dir="marhaedgh_backend/rbln-ko-Llama3-Bllossom-8B",
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

  conversation = [{"role": "user", "content": "너가 평가하기에 너는 어느정도의 한국어 실력을 가진 것 같아?"}]
  chat = tokenizer.apply_chat_template(conversation, add_generation_prompt=True, tokenize=False)
  result = asyncio.run(run_single(chat, "123"))
  print(result)

  # Runs multiple inferences in parallel
  conversations = [
    [{"role": "user", "content": "세종대왕 맥북 던짐 사건에 대해 말해줘"}],
    [{"role": "user", "content": "2341+12316은 뭐야?"}],
    [{"role": "user", "content": "한국에서 내야하는 세금의 종류에 대해서 알려줘."}],
    [{"role": "user", "content": "개인사업자가 내야하는 특별한 세금이 있을까?"}],
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
import os
import argparse

from optimum.rbln import RBLNLlamaForCausalLM

def parsing_argument():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--model_name",
        type=str,
        choices=["Meta-Llama-3-8B-Instruct"],
        default="Meta-Llama-3-8B-Instruct",
        help="(str) model type, llama3-8b model name.",
    )
    parser.add_argument(
        "--text",
        type=str,
        default="Hey, are you conscious? Can you talk to me?",
        help="(str) type, text for generation",
    )
    return parser.parse_args()

def main():
    args = parsing_argument()
    model_id = f"meta-llama/{args.model_name}"

    # Load compiled model
    model = RBLNLlamaForCausalLM.from_pretrained(
        model_id=os.path.basename(model_id),
        export=False,
    )
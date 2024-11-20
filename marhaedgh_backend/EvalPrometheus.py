import json
import os
from datetime import datetime
from prometheus_eval import PrometheusEval
from prometheus_eval.prompts import ABSOLUTE_PROMPT, SCORE_RUBRIC_TEMPLATE
import ModelLoader


class EvalPrometheus:
    def __init__(self, data_dir, output_dir, prompt_dir):
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.prompt_dir = prompt_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.model = ModelLoader.InferenceModel().llm_prometheus
        self.judge = PrometheusEval(model=self.model, absolute_grade_template=ABSOLUTE_PROMPT)
        self.eval_data = self.load_eval_data()

    def load_eval_data(self):

        eval_path = os.path.join(self.data_dir, "eval.json")
        with open(eval_path, "r") as f:
            return json.load(f)

    def load_prompt_data(self, prompt_type):
        
        prompt_file = os.path.join(self.data_dir, f"{prompt_type}_data.json")
        with open(prompt_file, "r") as f:
            return json.load(f)

    def load_prompt_template(self, prompt_type):
        
        prompt_path = os.path.join(self.prompt_dir, f"{prompt_type}.json")
        with open(prompt_path, "r") as f:
            return json.load(f)

    def generate_instruction(self, prompt_template, context):

        instruction = ""
        for prompt in prompt_template:
            if "{context}" in prompt["content"]:
                instruction += prompt["content"].replace("{context}", context)
            else:
                instruction += prompt["content"]
        return instruction.strip()

    def generate_score_rubric(self, prompt_type):
        
        rubric_data = self.eval_data[prompt_type]["rubric_data"]
        return SCORE_RUBRIC_TEMPLATE.format(**rubric_data)

    def evaluate_entry(self, instruction, response, reference_answer, score_rubric):
        
        feedback, score = self.judge.single_absolute_grade(
            instruction=instruction,
            response=response,
            rubric=score_rubric,
            reference_answer=reference_answer
        )
        return feedback, score

    def save_result(self, prompt_type, entry_id, instruction, response, reference_answer, feedback, score):
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_file = f"{prompt_type}_{timestamp}_{entry_id}.json"
        output_path = os.path.join(self.output_dir, output_file)
        result = {
            "id": entry_id,
            "instruction": instruction,
            "response": response,
            "reference_answer": reference_answer,
            "feedback": feedback,
            "score": score
        }
        with open(output_path, "w") as output_f:
            json.dump(result, output_f, indent=4)
        print(f"Saved evaluation result to {output_path}")

    def process_prompt_type(self, prompt_type):
        
        prompt_data = self.load_prompt_data(prompt_type)
        prompt_template = self.load_prompt_template(prompt_type)
        score_rubric = self.generate_score_rubric(prompt_type)

        for entry in prompt_data["data"]:
            context = entry.get("context", "")
            response = entry.get("response", "")
            reference_answer = entry.get("reference_answer", "")

            if not context or not response:  # Skip empty data
                continue

            instruction = self.generate_instruction(prompt_template, context)
            feedback, score = self.evaluate_entry(instruction, response, reference_answer, score_rubric)
            self.save_result(prompt_type, entry["id"], instruction, response, reference_answer, feedback, score)

    def run(self):
        """Run the evaluation process for all prompt types."""
        prompt_types = ["title", "keywords", "line_summary", "summarization", "whattodo", "chatting"]
        for prompt_type in prompt_types:
            self.process_prompt_type(prompt_type)


if __name__ == "__main__":
    # Initialize directories
    DATA_DIR = "/home/guest/marhaedgh/marhaedgh_backend/evaluation_data"
    OUTPUT_DIR = "/home/guest/marhaedgh/marhaedgh_backend/evaluation_data/stacked_eval_data"

    # Run evaluation
    evaluator = EvalPrometheus(data_dir=DATA_DIR, output_dir=OUTPUT_DIR)
    evaluator.run()

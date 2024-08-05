from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch

# Split input into chunks
chunk_size = 500
max_new_tokens = 50
model_max_length = 1000

# Initialize the tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# problem: each file data can be huge hence split data to chunks is required
# Define a function to split input into manageable chunks
def chunk_input(input_ids, chunk_size):
    return [input_ids[:, i:i+chunk_size] for i in range(0, input_ids.size(1), chunk_size)]

def process_chunks(input_text):
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    input_chunks = chunk_input(input_ids, chunk_size)

    outputs = []
    for chunk in input_chunks:
        attention_mask = torch.ones(chunk.shape, dtype=torch.long)
        output = model.generate(chunk, max_length=min(chunk.shape[1] + max_new_tokens, model_max_length), attention_mask=attention_mask, pad_token_id=tokenizer.eos_token_id)
        outputs.append(output)
    
    return torch.cat(outputs, dim=1)

def generate_instruction_completion_dataset(output_path):
    with open(output_path, 'r') as f:
        # Combine outputs and decode
        output_ids = process_chunks(f.read())
        return tokenizer.decode(output_ids[0], skip_special_tokens=True)
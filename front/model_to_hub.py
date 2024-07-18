


tokenizer = AutoTokenizer.from_pretrained("Rodrigolar/llava-v1.6-mistral-7b")
model = AutoModel.from_pretrained("Rodrigolar/llava-v1.6-mistral-7b")


from transformers import LlavaForConditionalGeneration, LlavaConfig

config = LlavaConfig(vision_config, text_config)
model =  LlavaForConditionalGeneration.from_pretrianed('llava-hf/llava-v1.6-mistral-7b')

model.push_to_hub("nielsr/my-awesome-bert-model")

# reload
model = BertModel.from_pretrained("nielsr/my-awesome-bert-model")

# Create a model or dataset repo from the CLI if needed
# huggingface-cli repo create repo_name --type {model, dataset, space}

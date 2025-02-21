from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch
import pandas as pd
import json
model_name="bhadresh-savani/distilbert-base-uncased-emotion"
tokenizer = AutoTokenizer.from_pretrained(model_name)
pipe = pipeline("text-classification", model=model_name, return_all_scores=True)  


def return_emotions(text):
    # Tokenize with overflow handling for long text
    encoding = tokenizer(
        text,
        truncation=True,
        padding="max_length",
        max_length=500, 
        stride=64,  # Creates overlapping chunks
        return_overflowing_tokens=True,
        return_tensors="pt"
    )

    # Extract input IDs and attention masks for all chunks
    input_ids_chunks = encoding["input_ids"]
    attention_masks = encoding["attention_mask"]

    # Move tensors to the appropriate device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    input_ids_chunks = input_ids_chunks.to(device)
    attention_masks = attention_masks.to(device)

    # Classify each chunk separately
    results = []
    for i in range(len(input_ids_chunks)):
        chunk_result = pipe(
            [tokenizer.decode(input_ids_chunks[i], skip_special_tokens=True)]
        )[0]
        chunk_result =  {dic["label"]: dic["score"] for dic in chunk_result }
        results.append(chunk_result)

    json_text = pd.DataFrame(results).mean().to_json()
    final_score = json.loads(json_text)
    return final_score
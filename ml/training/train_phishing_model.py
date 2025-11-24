# ml/training/train_phishing_model.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import torch

# Cameroon-specific scam examples
data = {
    "text": [
        "Envoie 5000 FCFA sur 699999999 pour débloquer ton prix",
        "Bonjour, comment ça va ?",
        "Ton code MoMo est 123456, ne le partage pas",
        "URGENT: Valide ton compte avant 10 min ou il sera bloqué"
    ],
    "label": [1, 0, 0, 1]  # 1 = phishing
}

dataset = Dataset.from_dict(data)
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-multilingual-cased")

def tokenize(batch):
    return tokenizer(batch["text"], truncation=True, padding=True, max_length=128)

dataset = dataset.map(tokenize, batched=True)
dataset.set_format(type='torch', columns=['input_ids', 'attention_mask', 'label'])

model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-multilingual-cased", num_labels=2)

args = TrainingArguments(
    output_dir="../models/phishing_classifier",
    per_device_train_batch_size=8,
    num_train_epochs=3,
    save_steps=100,
)

trainer = Trainer(model=model, args=args, train_dataset=dataset)
trainer.train()
trainer.save_model("../models/phishing_classifier")
print("Phishing model trained and saved!")
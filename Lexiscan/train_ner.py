import spacy
from spacy.training.example import Example
import random
import os

# Sample labeled data in Spacy format for demonstration purposes
TRAINING_DATA = [
    ("The contract is effective as of January 1, 2025.", {"entities": [(34, 49, "EFFECTIVE_DATE")]}),
    ("This agreement is made between InfoTact Solutions and Acme Corp.", {"entities": [(31, 49, "PARTY"), (54, 63, "PARTY")]}),
    ("The total monetary value is $50,000 for the services.", {"entities": [(28, 35, "MONEY")]}),
    ("Termination date is set for December 31, 2026.", {"entities": [(28, 45, "TERMINATION_DATE")]}),
]

def train_ner_model(model_name=None, output_dir="models/ner_model", n_iter=10):
    """Trains a custom NER model."""
    print("Setting up NER training pipeline...")
    
    if model_name is not None and spacy.util.is_package(model_name):
        nlp = spacy.load(model_name)
        print(f"Loaded model '{model_name}'")
    else:
        nlp = spacy.blank("en")
        print("Created blank 'en' model")

    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner", last=True)
    else:
        ner = nlp.get_pipe("ner")

    # Add labels
    for _, annotations in TRAINING_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    # Disable other pipes during training
    pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
    
    print("Beginning training...")
    with nlp.disable_pipes(*other_pipes):
        if model_name is None:
            optimizer = nlp.begin_training()
        else:
            optimizer = nlp.resume_training()
            
        for itn in range(n_iter):
            random.shuffle(TRAINING_DATA)
            losses = {}
            for text, annotations in TRAINING_DATA:
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                nlp.update([example], drop=0.5, sgd=optimizer, losses=losses)
            print(f"Iteration {itn + 1} Losses: {losses}")

    os.makedirs(output_dir, exist_ok=True)
    nlp.to_disk(output_dir)
    print(f"Model saved to {output_dir}")

if __name__ == "__main__":
    train_ner_model()

import spacy
import os

class NERPipeline:
    def __init__(self, model_dir="models/ner_model"):
        """Initialize the NER model from the standard directory. Fallback to basic spacy model."""
        if os.path.exists(model_dir):
            self.nlp = spacy.load(model_dir)
        else:
            print("Warning: Custom model not found. Using blank model. Run train_ner.py first.")
            self.nlp = spacy.blank("en")

    def extract_entities(self, text):
        """Extract entities from the provided text."""
        doc = self.nlp(text)
        entities = {}
        for ent in doc.ents:
            if ent.label_ not in entities:
                entities[ent.label_] = []
            entities[ent.label_].append(ent.text)
        return entities

if __name__ == "__main__":
    ner = NERPipeline()
    print("NER Pipeline loaded.")

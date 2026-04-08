from dateutil import parser
import re

class RulesEngine:
    def __init__(self):
        pass

    def standardize_date(self, date_string):
        """Standardize date string to ISO 8601 format (YYYY-MM-DD)."""
        try:
            parsed_date = parser.parse(date_string, fuzzy=True)
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            return None

    def validate_entities(self, extracted_entities):
        """
        Validate entities logically.
        For example: Termination date cannot precede Effective Date.
        """
        effective_date_raw = extracted_entities.get("EFFECTIVE_DATE")
        termination_date_raw = extracted_entities.get("TERMINATION_DATE")

        if isinstance(effective_date_raw, list) and len(effective_date_raw) > 0:
            effective_date_raw = effective_date_raw[0]
        if isinstance(termination_date_raw, list) and len(termination_date_raw) > 0:
            termination_date_raw = termination_date_raw[0]

        effective_date = self.standardize_date(effective_date_raw) if effective_date_raw else None
        termination_date = self.standardize_date(termination_date_raw) if termination_date_raw else None

        # Clean entities back into standard formats
        cleaned_entities = extracted_entities.copy()
        if effective_date:
            cleaned_entities["EFFECTIVE_DATE_ISO"] = effective_date
        if termination_date:
            cleaned_entities["TERMINATION_DATE_ISO"] = termination_date

        # Constraint checking
        if effective_date and termination_date:
            if effective_date > termination_date:
                cleaned_entities["WARNING"] = "Termination Date precedes Effective Date"

        # Standardizing Money Format
        monetary_value = extracted_entities.get("MONEY")
        if isinstance(monetary_value, list) and len(monetary_value) > 0:
            monetary_value = monetary_value[0]
        if monetary_value:
            cleaned_money = self.standardize_money(monetary_value)
            cleaned_entities["MONEY_CLEANED"] = cleaned_money

        return cleaned_entities
        
    def standardize_money(self, money_str):
        """Remove commas and redundant signs from money amounts."""
        cleaned = re.sub(r'[^\d.]', '', money_str)
        return cleaned

if __name__ == "__main__":
    re_engine = RulesEngine()
    print("Rules Engine Initialized.")

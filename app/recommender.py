import json
import pandas as pd
from pathlib import Path


# Locate the saved association rules

# Locate the saved association rules
PROJECT_DIR = Path(__file__).resolve().parents[1]
RULES_PATH = PROJECT_DIR / "models" / "rules.json"


def load_rules():
    # Load the rules generated during model training
    with open(RULES_PATH, "r", encoding="utf-8") as file:
        rules = json.load(file)

    df_rules = pd.DataFrame(rules)

    # Restore itemsets to the format used in the notebook
    df_rules["antecedents"] = df_rules["antecedents"].apply(frozenset)
    df_rules["consequents"] = df_rules["consequents"].apply(frozenset)

    return df_rules


def recommend(basket, df_rules, top_n=5):

    basket = set(basket)

    # Find rules that match the customer's basket
    df_matching = df_rules[
        df_rules["antecedents"].apply(
            lambda itemset: itemset.issubset(basket)
        )
    ].copy()

    if df_matching.empty:
        return df_matching

    # Keep rules recommending a single product
    df_matching = df_matching[
        df_matching["consequents"].apply(len) == 1
    ].copy()

    if df_matching.empty:
        return df_matching

    # Exclude products already in the basket
    df_matching = df_matching[
        df_matching["consequents"].apply(
            lambda itemset: itemset.isdisjoint(basket)
        )
    ].copy()

    if df_matching.empty:
        return df_matching

    # Extract the recommended product
    df_matching["product"] = df_matching["consequents"].apply(
        lambda itemset: next(iter(itemset))
    )

    # Rank recommendations by strength
    df_matching = df_matching.sort_values(
        ["lift", "confidence", "support"],
        ascending=False
    )

    # Keep the strongest rule for each product
    df_matching = df_matching.drop_duplicates(
        subset="product",
        keep="first"
    )

    return df_matching.head(top_n)

import json
from pathlib import Path

import pandas as pd
import streamlit as st

from recommender import load_rules, recommend

# --------------------------------------------------
# Application configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Boréal Marché",
    page_icon="🛒",
    layout="wide"
)

PROJECT_DIR = Path(__file__).resolve().parents[1]


# --------------------------------------------------
# Load application data
# --------------------------------------------------

@st.cache_data
def load_products():
    return pd.read_csv(PROJECT_DIR / "data" / "products.csv")


@st.cache_data
def load_saved_rules():
    return load_rules()


@st.cache_data
def load_popularity():
    popularity_path = PROJECT_DIR / "models" / "product_popularity.json"

    with open(popularity_path, "r", encoding="utf-8") as file:
        popularity = json.load(file)

    return pd.DataFrame(popularity)


df_products = load_products()
df_rules = load_saved_rules()
df_popularity = load_popularity()

# Product lookup for basket details
df_product_lookup = df_products.set_index("Item")



# Category icons for product displays
CATEGORY_ICONS = {
    "Boissons": "🥤",
    "Boulangerie": "🥖",
    "Bébé": "🍼",
    "Collations": "🍿",
    "Fromages": "🧀",
    "Fruits et légumes": "🥦",
    "Maison": "🏠",
    "Poissons": "🐟",
    "Produits laitiers": "🥛",
    "Spécialités": "🍽️",
    "Surgelés": "🧊",
    "Viandes": "🥩",
    "Épicerie": "🛒",
}


def get_category_icon(category):
    return CATEGORY_ICONS.get(category, "🏷️")



def show_popular_products(basket):
    # These are popular items, not personalized rule-based recommendations.
    df_available = df_popularity[
        ~df_popularity["Item"].isin(basket)
    ].head(5)

    st.markdown("**⭐ Popular Products**")
    st.caption(
        "Based on overall historical basket frequency, "
        "not your basket's association rules."
    )

    for _, row in df_available.iterrows():
        item_name = row["Item"]
        product = df_product_lookup.loc[item_name]

        category = product["Category"]
        price = float(product["Price"])
        support = float(row["support"])
        icon = get_category_icon(category)

        with st.container(border=True):
            st.markdown(f"**{icon} {item_name}**")
            st.caption(f"{category} · ${price:.2f}")
            st.caption(f"In {support:.1%} of historical baskets")

            if st.button(
                "➕ Add to Basket",
                key=f"popular_add_{item_name}"
            ):
                if item_name not in st.session_state.basket:
                    st.session_state.basket.append(item_name)

                st.rerun()


# --------------------------------------------------
# Initialize session state
# --------------------------------------------------

if "basket" not in st.session_state:
    st.session_state.basket = []


# --------------------------------------------------
# Application header
# --------------------------------------------------

st.title("🛒 Boréal Marché")
st.caption("Smart Grocery Recommendation Engine")

st.success(
    f"Catalogue loaded: {len(df_products)} products | "
    f"Association rules loaded: {len(df_rules):,}"
)

st.divider()


# --------------------------------------------------
# Main application layout
# --------------------------------------------------

col_catalogue, col_basket, col_recommendations = st.columns(
    [1.2, 1, 1.2],
    gap="large"
)


# ==================================================
# ZONE 1 — PRODUCT CATALOGUE
# ==================================================

with col_catalogue:

    st.subheader("🛍️ Product Catalogue")

    # Category filter
    categories = ["All Categories"] + sorted(
        df_products["Category"].dropna().unique().tolist()
    )


    selected_category = st.selectbox(
        "Filter by Category",
        options=categories,
        format_func=lambda category: (
            "🗂️ All Categories"
            if category == "All Categories"
            else f"{get_category_icon(category)} {category}"
        )
    )


    # Product search
    search_term = st.text_input(
        "Search Products",
        placeholder="Search by French or English name"
    )

    # Filter the catalogue
    df_catalogue = df_products.copy()

    if selected_category != "All Categories":
        df_catalogue = df_catalogue[
            df_catalogue["Category"] == selected_category
        ]

    if search_term:
        matches = (
            df_catalogue["Item"].str.contains(
                search_term,
                case=False,
                regex=False,
                na=False
            )
            |
            df_catalogue["Item_EN"].str.contains(
                search_term,
                case=False,
                regex=False,
                na=False
            )
        )

        df_catalogue = df_catalogue[matches]

    # Display search result count
    product_count = len(df_catalogue)
    product_label = "product" if product_count == 1 else "products"

    st.caption(f"{product_count} {product_label} found")

    # Select a product
    selected_product = st.selectbox(
        "Choose a Product",
        options=sorted(df_catalogue["Item"].tolist()),
        format_func=lambda item: (
            f"{get_category_icon(df_product_lookup.loc[item, 'Category'])} "
            f"{item}"
        ),
        disabled=df_catalogue.empty
    )


    # Display selected product details
    if selected_product is not None:

        product = df_product_lookup.loc[selected_product]

        st.caption(
            f"{product['Category']} | "
            f"${float(product['Price']):.2f}"
        )

    # Add product to the basket
    if st.button(
        "➕ Add to Basket",
        disabled=df_catalogue.empty
    ):

        if selected_product not in st.session_state.basket:
            st.session_state.basket.append(selected_product)

        else:
            st.info("This product is already in your basket.")


# ==================================================
# ZONE 2 — SHOPPING BASKET
# ==================================================

with col_basket:

    st.subheader("🛒 Your Basket")

    # Display the number of products in the basket
    basket_count = len(st.session_state.basket)
    item_label = "item" if basket_count == 1 else "items"

    st.caption(f"{basket_count} {item_label} in basket")

    # Clear basket
    if st.button(
        "Clear Basket",
        disabled=not st.session_state.basket
    ):
        st.session_state.basket = []
        st.rerun()

    if st.session_state.basket:
        basket_total = 0.0

        # Display each basket item
        for item_name in st.session_state.basket:

            product = df_product_lookup.loc[item_name]

            category = product["Category"]
            price = float(product["Price"])

            basket_total += price

            with st.container(border=True):

                col_details, col_remove = st.columns(
                    [3, 1],
                    vertical_alignment="center"
                )

                with col_details:
                    icon = get_category_icon(category)
                    st.write(f"**{icon} {item_name}**")
                    st.caption(category)
                    st.write(f"${price:.2f}")

                with col_remove:
                    if st.button(
                        "Remove",
                        key=f"remove_{item_name}"
                    ):
                        st.session_state.basket.remove(item_name)
                        st.rerun()

        st.divider()

        # Basket total
        st.metric(
            label="Basket Total",
            value=f"${basket_total:.2f}"
        )

    else:
        st.info(
            "Your basket is empty. "
            "Add a product to get started."
        )



# ==================================================
# ZONE 3 — PRODUCT RECOMMENDATIONS
# ==================================================

with col_recommendations:
    st.subheader("✨ Recommended for You")

    basket = st.session_state.basket

    if not basket:
        st.info("Your basket is empty. Explore our most popular products.")
        show_popular_products(basket)

    else:
        # Explain products too rare to appear in the saved rule model
        min_support = 0.005  # Matches models/metadata.json

        df_rare_items = df_popularity[
            df_popularity["Item"].isin(basket)
            & (df_popularity["support"] < min_support)
        ]

        for _, rare_item in df_rare_items.iterrows():
            st.info(
                f"**{rare_item['Item']}** appears in only "
                f"{rare_item['support']:.2%} of historical baskets. "
                f"That is below the model's {min_support:.1%} minimum support "
                "threshold, so the product does not appear in any saved "
                "association rule. Other basket items may still trigger rules."
            )

        # Always calculate recommendations for a nonempty basket
        df_recommendations = recommend(basket, df_rules, top_n=5)

        if df_recommendations.empty:
            st.warning(
                "No eligible personalized recommendations were found "
                "for this basket. Here are popular alternatives."
            )
            show_popular_products(basket)

        else:
            st.caption(
                f"{len(df_recommendations)} personalized "
                "recommendations based on your basket"
            )

            for _, rule in df_recommendations.iterrows():
                product_name = rule["product"]
                product = df_product_lookup.loc[product_name]

                category = product["Category"]
                price = float(product["Price"])
                icon = get_category_icon(category)

                support = float(rule["support"])
                confidence = float(rule["confidence"])
                lift = float(rule["lift"])

                # Strength labels based on lift
                if lift >= 5:
                    strength = "Very Strong"
                elif lift >= 3:
                    strength = "Strong"
                elif lift >= 2:
                    strength = "Moderate"
                else:
                    strength = "Weak"

                antecedents = ", ".join(
                    sorted(rule["antecedents"])
                )

                # Recommendation card
                with st.container(border=True):
                    st.markdown(f"#### {icon} {product_name}")
                    st.caption(f"{category} · ${price:.2f}")

                    st.markdown(
                        f"**Association strength:** {strength}"
                    )

                    # Display metrics side by side
                    col_support, col_confidence, col_lift = st.columns(3)

                    with col_support:
                        st.metric("Support", f"{support:.2%}")

                    with col_confidence:
                        st.metric("Confidence", f"{confidence:.2%}")

                    with col_lift:
                        st.metric("Lift", f"{lift:.2f}×")

                    # Explain the actual association rule
                    st.caption(
                        f"Because your basket contains {antecedents}, "
                        f"historically {confidence:.1%} of baskets containing "
                        f"those items also included {product_name}. "
                        f"That is {lift:.2f}× the average frequency of "
                        f"{product_name}."
                    )

                    # Allow the customer to add the recommendation
                    if st.button(
                        "➕ Add recommendation to basket",
                        key=f"rec_add_{product_name}"
                    ):
                        if product_name not in st.session_state.basket:
                            st.session_state.basket.append(product_name)

                        st.rerun()

            st.caption(
                "Strength labels are display categories based on lift, "
                "not measures of certainty or causation."
            )

        # --------------------------------------------------
        # Explainability — Rules that fired
        # --------------------------------------------------

        # Show the underlying rules even when none qualify for top five
        basket_set = set(basket)

        df_fired_rules = df_rules[
            df_rules["antecedents"].apply(
                lambda items: items.issubset(basket_set)
            )
        ].sort_values(
            ["lift", "confidence", "support"],
            ascending=False
        )

        with st.expander(
            f"🔍 Rules that fired ({len(df_fired_rules):,})"
        ):
            st.caption(
                "All rules whose antecedents match your basket are shown here. "
                "Some may recommend multiple items, items already in your basket, "
                "or fall outside the final top five."
            )

            if df_fired_rules.empty:
                st.info(
                    "No saved association rules were triggered by this basket."
                )

            else:
                # Limit the audit display without modifying the original rules
                df_audit = df_fired_rules[
                    [
                        "antecedents",
                        "consequents",
                        "support",
                        "confidence",
                        "lift"
                    ]
                ].head(50).copy()

                # Make itemsets readable
                df_audit["antecedents"] = df_audit["antecedents"].apply(
                    lambda items: ", ".join(sorted(items))
                )

                df_audit["consequents"] = df_audit["consequents"].apply(
                    lambda items: ", ".join(sorted(items))
                )

                # Format metrics for the customer
                df_audit["support"] = df_audit["support"].map(
                    lambda value: f"{value:.2%}"
                )

                df_audit["confidence"] = df_audit["confidence"].map(
                    lambda value: f"{value:.2%}"
                )

                df_audit["lift"] = df_audit["lift"].round(2)

                df_audit = df_audit.rename(columns={
                    "antecedents": "If basket contains",
                    "consequents": "Then suggests",
                    "support": "Support",
                    "confidence": "Confidence",
                    "lift": "Lift",
                })

                st.dataframe(
                    df_audit,
                    hide_index=True,
                    use_container_width=True,
                    height=260
                )

                if len(df_fired_rules) > 50:
                    st.caption(
                        f"Showing the top 50 of "
                        f"{len(df_fired_rules):,} triggered rules."
                    )
# 🛒 Boréal Marché — Grocery Recommendation Engine

**An interactive grocery recommendation application built using Python, Apriori association rules, and Streamlit.**

- **Course:** 420-975-VA — Unsupervised Machine Learning
- **Program:** AI & Data Science — Vanier College
- **Developer:** Matthew Braithwaite
- **Project Version:** 1.0 — November 2026

---

## 1. Project Overview

Boréal Marché is a grocery recommendation application that suggests products based on items already in a customer's shopping basket.

The goal of this project was to analyze historical grocery transactions, discover purchasing patterns using association-rule mining, and turn those patterns into a working recommendation application.

I used the Apriori algorithm to identify frequently purchased product combinations and generated association rules using support, confidence, and lift.

The project includes the complete workflow, from data exploration and preprocessing to model evaluation, saved model artifacts, recommendation logic, application development, and testing.

The final result is an interactive Streamlit application where customers can build a basket, receive recommendations, and understand why those products were suggested.

## 2. Application Features

### Product Catalogue

- Browse 98 grocery products across 13 categories.
- Filter products by category.
- Search using French or English product names.
- View product categories and prices.
- Use category icons for easier navigation.

### Shopping Basket

- Add products from the catalogue or recommendation cards.
- Remove individual products or clear the basket.
- View selected products, prices, and categories.
- Automatically calculate the basket total.
- Maintain basket contents during Streamlit interactions.

The V1 basket stores unique products. Multiple quantities of the same product are planned for a future version.

### Recommendation Engine

- Display up to five personalized product recommendations.
- Rank recommendations using lift, then confidence and support.
- Exclude products already in the basket.
- Prevent duplicate recommendations by keeping the strongest rule for each product.
- Display support, confidence, lift, and an association-strength label.
- Explain recommendations using the products that triggered each rule.

An expandable **Rules that fired** section allows users to inspect the underlying association rules.

### Fallback Recommendations

When the basket is empty or no eligible association rule produces a recommendation, the application displays popular products based on historical purchase frequency.

Products below the minimum support threshold also receive an explanation of why they cannot participate in the saved association rules.

Popular-product suggestions are clearly separated from personalized recommendations.

## 3. Project Architecture

The application separates offline data mining from the customer-facing recommendation process.

```text
Historical Transactions + Product Catalogue
                  |
                  v
       Data Cleaning and Encoding
                  |
                  v
      Apriori Association-Rule Mining
                  |
                  v
        Rule Evaluation and Filtering
                  |
                  v
          Saved JSON Artifacts
                  |
                  v
         Python Recommendation Engine
                  |
                  v
          Streamlit Application
```

### Project Structure

```text
boreal-reco-MatthewBraithwaite/
|
|-- app/
|   |-- recommender.py
|   |-- streamlit_app.py
|
|-- data/
|   |-- products.csv
|   |-- transactionsdata.zip
|
|-- models/
|   |-- rules.json
|   |-- metadata.json
|   |-- product_popularity.json
|
|-- notebooks/
|   |-- 01_mining.ipynb
|
|-- reports/
|   |-- benchmark.md
|
|-- tests/
|   |-- manual-regression.md
|
|-- .streamlit/
|   |-- config.toml
|
|-- .gitignore
|-- README.md
|-- requirements.txt
```

**Main components:**

- `01_mining.ipynb` — Data preparation, Apriori experiments, rule evaluation, seasonal analysis, testing, and model export.
- `recommender.py` — Loads saved rules and generates recommendations.
- `streamlit_app.py` — Customer-facing application.
- `rules.json` — Saved association rules used by the application.
- `metadata.json` — Model configuration, thresholds, and coverage.
- `product_popularity.json` — Product frequencies used for fallback recommendations.
- `benchmark.md` — Performance results and model limitations.
- `manual-regression.md` — Functional and edge-case test documentation.

**Apriori does not run when customers interact with the application.** Rules are generated offline and loaded from JSON during application execution.

## 4. Installation and Execution

### Requirements

- Python 3.14 (tested development version)
- pip
- A web browser
- Git, if cloning the repository

The project was developed and tested on Windows using a Python virtual environment.

### Setup

Clone the repository, once published:

```bash
git clone https://github.com/mbraithwaite87/boreal-reco-MatthewBraithwaite.git
cd boreal-reco-MatthewBraithwaite
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the required packages:

```powershell
python -m pip install -r requirements.txt
```

### Launch the Application

From the project root:

```powershell
python -m streamlit run app/streamlit_app.py
```

Streamlit will display the local application URL in the terminal, normally beginning with:

`http://localhost:8501/`

The application loads the saved recommendation rules and product catalogue automatically.

**Note:** Running the Streamlit application does not require rerunning the mining notebook or loading the original transaction dataset.

### Reproducing the Analysis

To review or reproduce the mining process:

1. Open `notebooks/01_mining.ipynb` using VS Code with Jupyter support.
2. Select the project's Python environment.
3. Ensure the source transaction dataset and product catalogue are available under `data/`.
4. Restart the kernel and run all cells.

The notebook contains the preprocessing, Apriori benchmarks, rule evaluation, seasonal comparisons, and JSON exports.

The availability and redistribution of the original transaction dataset should be confirmed before sharing the repository publicly.

## 5. Model Methodology

### Data Preparation

The dataset contains:

| Description | Value |
|---|---:|
| Shopping baskets | 1,000,000 |
| Transaction-item records | 8,379,837 |
| Unique products | 98 |
| Encoded matrix dimensions | 1,000,000 × 98 |

I converted the transactions into a Boolean basket-product matrix using NumPy and Pandas.

Each row represents a shopping basket, and each column indicates whether a product was purchased.

### Apriori Configuration

| Parameter | Selected Value |
|---|---:|
| Algorithm | Apriori |
| Minimum support | 0.005 (0.5%) |
| Minimum confidence | 0.30 (30%) |
| Lift filter | Greater than 1 |
| Low-memory mode | Enabled |

I tested four minimum support thresholds before selecting the final configuration.

Lower support thresholds discovered more product combinations but increased processing time.

The final model prioritizes rules with lift greater than 1 because these represent associations occurring more frequently than expected from the consequent product's overall frequency.

### Recommendation Selection

When a customer adds products to the basket, the engine:

1. Finds rules whose antecedents are contained in the basket.
2. Keeps rules that recommend one product.
3. Excludes products already in the basket.
4. Sorts candidates by lift, confidence, and support.
5. Keeps the strongest rule for each recommended product.
6. Returns up to five unique recommendations.

The engine considers product presence, not purchase quantity.

## 6. Results and Limitations

### Final Model Results

| Metric | Result |
|---|---:|
| Frequent itemsets | 7,106 |
| Rules before lift filtering | 23,918 |
| Final saved rules | 22,476 |
| Rules with single-product consequents | 10,909 |
| Individually recommendable products | 58 of 98 |
| Potential catalogue coverage | 59.18% |

Potential catalogue coverage means that 58 products can appear individually as the consequent of at least one saved rule.

It does **not** mean that 59.18% of customer baskets receive recommendations.

### Performance Results

Apriori was benchmarked using four minimum support thresholds.

| Minimum Support | Frequent Itemsets | Rules | Time (s) |
|---:|---:|---:|---:|
| 0.05 | 191 | 282 | 5.86 |
| 0.02 | 658 | 2,707 | 10.95 |
| 0.01 | 2,267 | 7,817 | 23.44 |
| 0.005 | 7,106 | 23,918 | 43.63 |

All full-dataset benchmarks completed using `low_memory=True`.

The reported execution times include profiling overhead. Memory measurements represent sampled Python process usage rather than memory exclusively allocated by Apriori.

A full-dataset `MemoryError` using the default setting was not reproduced.

See [Apriori Benchmark Report](reports/benchmark.md) for the detailed measurements, controlled memory comparison, and interpretation.

### Seasonal Analysis

I also mined association rules separately for summer and winter.

| Season | Filtered Rules |
|---|---:|
| Summer — June to August | 52,117 |
| Winter — December to February | 13,876 |
| Rules appearing in both seasonal models | 8,923 |

The results demonstrate that association-rule eligibility and purchasing relationships can vary between seasons.

A rule that meets the required support and confidence thresholds in summer may no longer meet them in winter.

The current application uses the year-round model. Seasonal recommendation models are a planned improvement, not an implemented V1 feature.

### Current Limitations

- Rare products may not meet the minimum support threshold.
- Not every catalogue product can be individually recommended.
- Association rules identify relationships but do not determine customer preferences directly.
- Recommendations use product presence rather than quantities.
- Seasonal models have been analyzed but are not dynamically selected in V1.

## 7. Testing and Quality Assurance

Testing was included throughout development to verify data integrity, model behaviour, application functionality, and edge cases.

### Notebook Verification

The mining notebook was restarted and executed from a clean kernel.

The submitted release-candidate notebook contained 41 sequentially executed code cells with no recorded Python errors.

Verification included Boolean encoding accuracy, saved JSON consistency, rule filtering, catalogue coverage, and recommendation-engine assertions.

### Recommendation Engine Tests

The recommendation function was also tested independently of the notebook.

Tests covered valid recommendations, ranking by lift, duplicate-product handling, exclusion of basket products, and multi-item rule matching.

### Manual Browser Regression

The Streamlit application was tested locally in Chrome, including:

- Catalogue loading, filtering, and bilingual searching.
- Basket add, remove, clear, and total calculations.
- Recommendation presentation and explanations.
- Duplicate recommendation prevention.
- Empty-basket and no-rule fallbacks.
- Rare-product explanations.
- Triggered-rule audit display.

See [Manual Regression Test Suite](tests/manual-regression.md) for test scenarios, expected results, and recorded execution outcomes.

Browser testing was manual. Automated browser tests and a fresh-environment installation remain future verification improvements.

## 8. Responsible AI and Privacy

Although Boréal Marché uses a relatively straightforward recommendation algorithm, transparency and responsible use are still important.

### Recommendation Explainability

Every personalized recommendation displays the association metrics and an explanation identifying the products that triggered the rule.

Support, confidence, and lift help users understand the evidence behind a recommendation.

However, **association does not imply causation**. Products frequently purchased together do not necessarily cause one another to be purchased.

### Coverage and Popularity Bias

Association-rule mining tends to favour frequently purchased products because they are more likely to meet minimum support thresholds.

Rare products may be excluded even when they are relevant to certain customers.

The application addresses this limitation by explaining rare-product exclusions and providing popular-product fallbacks.

These fallbacks are not presented as personalized recommendations.

### Québec Law 25 Considerations

This project was developed as an educational application, not as a production system containing customer accounts.

The current interface uses shopping-basket contents within the Streamlit session to calculate recommendations.

If Boréal Marché were expanded into a real retail application, I would evaluate:

- Whether personal information is being collected and why it is needed.
- Transparency about recommendation and profiling technologies.
- Applicable consent and profiling-activation requirements.
- Data minimization, retention, access controls, and security.
- Privacy impact assessment requirements when introducing personal-data processing.

Québec's Law 25 establishes additional privacy obligations for organizations using technologies that identify, locate, or profile individuals.

This section identifies considerations for future development and does not represent a claim of legal compliance.

Reference: [Commission d'accès à l'information du Québec — Law 25](https://www.cai.gouv.qc.ca/protection-renseignements-personnels/sujets-et-domaines-dinteret/principaux-changements-loi-25)

### Correlation Does Not Mean Causation

One association found in the dataset is:

**Couches → Bière (Diapers → Beer)**

- Support: 3.07%
- Confidence: 36.56%
- Lift: 2.43

This is a well-known type of example in retail analytics.

Although diapers and beer appear together more often than expected,
this does not mean purchasing diapers causes someone to buy beer.

Other factors, such as customer shopping habits or the types of
households purchasing these products, may contribute to the association.

The model identifies purchasing patterns, not cause-and-effect relationships.


## 9. Future Improvements

Boréal Marché V1 provides a functional recommendation application, but several improvements could make it more useful and production-ready.

| Enhancement | Description |
|---|---|
| Seasonal recommendation models | Load summer, winter, or year-round rules depending on the season |
| Dynamic seasonal themes | Change the storefront appearance to match seasonal shopping patterns |
| Individual product icons | Add a specific icon or image for each of the 98 products |
| Quantity management | Support multiple units of the same product and quantity-based totals |
| Recommendation quality evaluation | Measure recommendation usefulness, coverage, and customer engagement |
| Automated testing | Add pytest, browser automation, and GitHub Actions |
| Model monitoring | Track changes in purchasing patterns and schedule rule updates |
| Deployment | Host the application for access outside the local development environment |

I would also investigate whether alternative support thresholds or recommendation approaches could improve coverage for less frequently purchased products.

The longer-term goal is to develop Boréal Marché beyond a classroom project into a more complete, testable, and maintainable recommendation application.

---

**Project Status:** V1 completed, tested, and published on GitHub.
The application runs locally. Public hosting is planned for a future version.
# Boréal Marché — Manual Regression Test Suite

## 1. Test Overview

- **Application:** Boréal Marché V1
- **Test Type:** Manual functional and regression testing
- **Environment:** Local development
- **Operating System:** Windows
- **Browser:** Google Chrome
- **Application URL:** http://localhost:8502/
- **Execution Date:** November 4, 2026
- **Status:** Functional testing reported as passed

### Objective

Verify that the catalogue, shopping basket, recommendation engine, explanation features, and fallback behaviour meet the functional requirements.

The application uses saved association rules and does not execute Apriori during normal use.

## 2. Test Environment and Data

| Component | Configuration |
|---|---|
| Python | 3.14 |
| Streamlit | 1.66.1 |
| Product catalogue | 98 products |
| Saved association rules | 22,476 |
| Recommendation limit | 5 products |
| Minimum support | 0.005 |
| Minimum confidence | 0.30 |
| Lift filter | > 1 |
| Test data | Saved rules and product catalogue |

## 3. Catalogue Tests

| Test ID | Test Scenario | Expected Result | Status |
|---|---|---|---|
| CAT-001 | Load the application | All 98 products load without an error | PASS |
| CAT-002 | Select a product category | Only products in that category appear | PASS |
| CAT-003 | Search for `Charbon` | `Charbon de bois` appears | PASS |
| CAT-004 | Search for `Charcoal` | `Charbon de bois` appears using the English name | PASS |
| CAT-005 | Search for a nonexistent product | Zero products found; Add button disabled | PASS |
| CAT-006 | Reset category and search filters | All 98 products become available | PASS |

## 4. Shopping Basket Tests

| Test ID | Test Scenario | Expected Result | Status |
|---|---|---|---|
| BSK-001 | Add a catalogue product | Product appears with name, category and price | PASS |
| BSK-002 | Add the same product twice | No duplicate entry is created | PASS |
| BSK-003 | Remove an individual product | Only the selected item is removed | PASS |
| BSK-004 | Remove the final product | Empty-basket state appears | PASS |
| BSK-005 | Add multiple products | Basket total equals the sum of product prices | PASS |
| BSK-006 | Remove a product | Basket total and recommendations recalculate | PASS |
| BSK-007 | Clear Basket | All selected products are removed and the total resets | PASS |

## 5. Recommendation Tests

| Test ID | Test Scenario | Expected Result | Status |
|---|---|---|---|
| REC-001 | Add `Charbon de bois` | Up to five personalized recommendations appear | PASS |
| REC-002 | Add a previously recommended product | The product no longer appears in recommendations | PASS |
| REC-003 | Change basket contents | Recommendations update based on the new basket | PASS |
| REC-004 | Inspect a recommendation card | Product name, category, price, support, confidence, lift and strength label are displayed | PASS |
| REC-005 | Inspect recommendation explanation | Explanation identifies triggering products, confidence and lift relative to average frequency | PASS |
| REC-006 | Expand "Rules that fired" | Triggered association rules are displayed with their metrics | PASS |
| REC-007 | Add a product from a recommendation card | Product is added and the recommendations update | PASS |

## 6. Graded Edge-Case Tests — Section 5.3

### EDG-001 — Empty Basket

**Steps:**
1. Clear the shopping basket.
2. Inspect the recommendations panel.

**Expected:** A clear empty-basket message and popular-product suggestions.

**Status:** PASS

### EDG-002 — No Eligible Recommendation

**Steps:**
1. Clear the basket.
2. Add `Foie gras`.
3. Inspect the recommendations panel.

**Expected:** No blank panel. Display a clear message and popular-product fallback suggestions.

**Status:** PASS

### EDG-003 — Product Already in Basket

**Steps:**
1. Add `Charbon de bois`.
2. Confirm `Steak de boeuf` appears as a recommendation.
3. Add `Steak de boeuf` to the basket.

**Expected:** Steak no longer appears in the recommended products. The basket and total update correctly.

**Status:** PASS

### EDG-004 — Duplicate Recommended Product

**Steps:**
1. Test a basket that triggers multiple rules recommending the same product.
2. Compare the selected recommendation against the eligible candidate rules.

**Expected:** Each product appears only once, using the rule with the highest lift.

**Status:** PASS — Verified through notebook assertions and independent candidate-rule comparison. This is not claimed as a browser-automated test.

### EDG-005 — Very Rare Product

**Steps:**
1. Clear the basket.
2. Add `Foie gras`.
3. Inspect the rarity message.
4. Add `Charbon de bois`.

**Expected:** Explain that Foie gras falls below the 0.5% minimum support threshold. Other eligible basket products can still produce recommendations.

**Status:** PASS

## 7. Requirements Traceability

| Rubric Requirement | Covered By |
|---|---|
| 5.2 — Product name, category, price | REC-004 |
| 5.2 — Plain-language explanation | REC-005 |
| 5.2 — Support, confidence, lift | REC-004 |
| 5.2 — Lift-based strength label | REC-004 |
| 5.3 — Empty basket fallback | EDG-001 |
| 5.3 — No-rule fallback | EDG-002 |
| 5.3 — Already selected products excluded | EDG-003 |
| 5.3 — Highest-lift duplicate resolution | EDG-004 |
| 5.3 — Very rare product explanation | EDG-005 |

## 8. Execution Summary

**Manual browser testing:** The developer reported passing functional and regression tests during development on November 4, 2026.

**Backend verification:** Recommendation-engine assertions were also executed independently of Streamlit.

**Known testing limitations:**
- Browser testing is manual, not automated.
- A fresh-environment installation has not yet been verified.
- The quantity-management feature is not implemented; basket entries are unique product identifiers.
- Historical screenshot evidence and execution logs are not yet maintained as a separate test-run archive.

## 9. Final Assessment

Boréal Marché V1 passed its reported functional browser checks and recommendation-engine verification.

The test suite covers the catalogue, basket operations, recommendation presentation, rule traceability, and the five graded edge cases.

Future regression improvements could include automated unit tests with pytest, browser automation with Playwright, and continuous integration through GitHub Actions.
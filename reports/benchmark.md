# Boréal Marché - Apriori Benchmark Report

## 1. Objective

The objective of this benchmark is to evaluate the execution time and memory usage of the Apriori algorithm when processing the Boréal Marché transaction dataset.

I tested four minimum support thresholds to understand how changing the threshold affects the number of frequent itemsets, association rules, and processing time.

I also compared Apriori's `low_memory` settings to investigate their effect on performance and memory consumption.

The goal is to select a configuration that provides useful recommendations while keeping processing requirements manageable.

## 2. Dataset and Configuration

The dataset contains one year of grocery transactions with the following characteristics:

| Description | Value |
|---|---:|
| Shopping baskets | 1,000,000 |
| Transaction-item records | 8,379,837 |
| Unique products | 98 |
| Encoded matrix dimensions | 1,000,000 × 98 |
| Encoded DataFrame memory | 101.09 MiB |

The transaction data was converted into a Boolean basket-product matrix using NumPy and Pandas. Each row represents a shopping basket, and each column indicates whether a product was purchased.

### Apriori Configuration

- **Library:** `mlxtend.frequent_patterns`
- **Algorithm:** Apriori
- **Input:** `df_encoded`
- **Minimum support thresholds:** 0.05, 0.02, 0.01, 0.005
- **Minimum confidence:** 0.30
- **Apriori memory setting:** `low_memory=True`
- **Itemset names:** `use_colnames=True`

Execution time was measured using `time.perf_counter()`.

Memory usage was measured using `memory_profiler.memory_usage()` with a sampling interval of 0.1 seconds.

The recorded peak memory represents the highest sampled memory usage of the Python process during the Apriori call. It includes memory already used by the notebook and other variables, not just memory allocated by Apriori.

The measured execution time includes profiling overhead but excludes initial data loading, Boolean matrix creation, and subsequent association-rule generation.

## 3. Benchmark Results

Apriori was executed against the full one-million-basket dataset using four minimum support thresholds.

| Minimum Support | Frequent Itemsets | Association Rules | Time (seconds) | Peak Memory (MiB) |
|---:|---:|---:|---:|---:|
| 0.05 | 191 | 282 | 5.86 | 1,135.34 |
| 0.02 | 658 | 2,707 | 10.95 | 1,148.36 |
| 0.01 | 2,267 | 7,817 | 23.44 | 1,153.56 |
| 0.005 | 7,106 | 23,918 | 43.63 | 1,147.36 |

All four experiments completed successfully using `low_memory=True`.

Association rules were generated using a minimum confidence of 30%.

The rule counts in this table are measured before applying the final `lift > 1` filter.

## 4. Performance Interpretation

The results show that lowering the minimum support threshold increases the number of frequent itemsets and association rules.

When I reduced minimum support from 5% to 0.5%:

- Frequent itemsets increased from 191 to 7,106.
- Association rules increased from 282 to 23,918, approximately 84.8 times more rules.
- Apriori execution time increased from 5.86 to 43.63 seconds, approximately 7.4 times longer.

This happens because a lower support threshold allows less common product combinations to qualify as frequent itemsets. Apriori must evaluate more candidate combinations, which increases the processing workload.

### Memory Observations

Peak process memory remained between approximately 1,135 and 1,154 MiB across the four full-dataset tests.

However, this does not mean Apriori uses a constant amount of memory.

These measurements include memory already allocated by the Python process. The memory profiler also samples usage at intervals, meaning short memory spikes could be missed.

### Performance Trade-off

A lower support threshold can uncover more product relationships, including combinations that would be excluded at higher thresholds.

However, generating more rules does not automatically improve recommendation quality.

A useful configuration needs to balance:

- Number of discovered rules
- Processing time and memory requirements
- Quality of the associations
- Product coverage
- Relevance to customer shopping behaviour

Based on these results, the lowest tested support threshold provides more opportunities for recommendations, with a higher but manageable measured processing time.

## 5. Memory Investigation and Controlled Comparison

The full-dataset benchmarks used `low_memory=True` to reduce the risk of excessive memory allocation.

To investigate the difference between Apriori's memory configurations, I performed a controlled comparison using the same sample of 1,000 shopping baskets and a minimum support threshold of 0.05.

### Controlled Test Results

| low_memory | Frequent Itemsets | Time (seconds) | Peak Memory (MiB) |
|---|---:|---:|---:|
| False | 193 | 2.53 | 476.38 |
| True | 193 | 2.51 | 469.07 |

Both configurations successfully generated 193 frequent itemsets.

The observed runtime difference was very small. The `low_memory=True` configuration also recorded a slightly lower sampled process-memory peak.

However, this was a small-scale test, and the results do not establish a meaningful performance advantage for either setting.

### Understanding `low_memory`

With `low_memory=False`, Apriori uses a more memory-intensive approach to evaluating candidate itemsets. On large datasets, intermediate candidate combinations can require substantial memory.

With `low_memory=True`, Apriori uses an alternative approach intended to reduce memory requirements, potentially at the cost of longer execution times
# ML Fundamentals Interview Questions

Core machine-learning concepts that aren't LLM-specific — model choice, bias/variance, evaluation, classical algorithms. Distinct from [llm-fundamentals/](../llm-fundamentals/questions.md) (transformer/LLM architecture).

## Q1: When would you reach for a classical ML model (XGBoost / Random Forest) over a deep learning model?

**Answer:**


**Classical ML (XGBoost / Random Forest):**
- **Tabular data:** I would usually prefer XGBoost or Random Forest because they perform very well on structured data.
- **Limited data:** Classical ML is often a better choice when the dataset is small or medium-sized.
- **Interpretability:** I would choose tree-based models when understanding feature importance and explaining predictions is important.
- **Compute and latency:** Classical ML is preferable when I need faster training, lower infrastructure cost, or low-latency inference.

**Deep learning:**
- **Unstructured data:** I would choose deep learning for text, images, audio, or video because it can learn useful representations automatically.
- **Complex patterns:** I would use deep learning when the problem requires learning highly complex representations that are difficult to engineer manually.

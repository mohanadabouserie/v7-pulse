# Noon page read by Claude: test inputs

- `2026-10-11_soft_drinks_popularity.html`: noon.com Egypt Soft Drinks listing, sorted by popularity,
  fetched 11 Oct 2026 with curl over HTTP/2 (plain HTTP/1.1 requests hang).
  - It lists 38 products, one product link each, with no sponsored items.
  - V7 Pink Lemonade is #1 and V7 Pomegranate shows "Only 9 left in stock".
  - It's the input for `tests/test_noon_llm.py`.
- Live runs of `data/noon_llm.py` save each day's page and result under `data/raw/stores/noon_llm/YYYY-MM-DD/`.

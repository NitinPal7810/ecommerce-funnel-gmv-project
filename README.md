# E-commerce Funnel Drop-off & GMV Recovery Analytics

## Project Overview

This project analyses e-commerce customer journeys to identify funnel drop-offs, understand conversion differences across devices and channels, and quantify potential GMV recovery opportunities.

The project combines:

- MySQL for data storage and SQL-based analysis
- Python for analysis and visualization
- Power BI for interactive business reporting
- Synthetic e-commerce session, event, user, and order data

## Business Problem

E-commerce businesses can lose significant revenue when users drop out between product discovery, cart, checkout, payment, and order completion.

This project focuses on:

1. Identifying major funnel drop-off points
2. Comparing conversion performance across devices
3. Measuring cart abandonment
4. Analysing GMV and Average Order Value
5. Estimating potential GMV recovery from abandoned carts
6. Understanding conversion patterns across categories, channels, and time
7. Examining the relationship between session duration and conversion

## Dataset

The project uses a synthetic e-commerce dataset containing:

- 150,000 users
- 500,000 sessions
- 1,225,384 events
- 43,637 orders

The raw CSV files are excluded from GitHub using `.gitignore`.

They can be regenerated using:

```bash
python generate_data.py 

```
## Technology Stack

- Python
- Pandas
- NumPy
- Faker
- MySQL
- SQLAlchemy
- MySQL Connector/Python
- Matplotlib
- Seaborn
- Plotly
- Power BI


## Key Business Results

| Metric | Result |
|---|---:|
| Total Sessions | 500,000 |
| PDP Sessions | 413,403 |
| Add-to-Cart Sessions | 141,151 |
| Checkout Sessions | 72,945 |
| Payment Sessions | 54,248 |
| Orders | 43,637 |
| Overall Conversion | 8.73% |
| GMV | ₹11.52 Cr |
| Average Order Value | ₹2,640.27 |
| Cart Abandonment Rate | 48.32% |

## Funnel Conversion

| Funnel Stage | Conversion |
|---|---:|
| Session → PDP | 82.68% |
| PDP → Add-to-Cart | 34.14% |
| Cart → Checkout | 51.68% |
| Checkout → Payment | 74.37% |
| Payment → Order | 80.44% |

## Device Analysis

The cart-to-checkout conversion was:

- Mobile: 48.73%
- Desktop: 57.14%
- Tablet: 56.60%

The desktop-mobile cart-to-checkout difference is 8.41 percentage points.

The PDP-to-cart conversion was similar between mobile and desktop, while the larger difference appeared at the cart-to-checkout stage. This indicates a potential checkout-stage friction area that could be investigated further through product analytics and A/B testing.

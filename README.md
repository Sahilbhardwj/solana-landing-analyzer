# Solana Transaction Landing Analyzer

A small research tool to measure **transaction landing latency on Solana** and analyze how **priority fees affect execution time**.

This project sends transactions to the Solana devnet, records the latency and estimated slot delay, and then analyzes the results using Python.

---

## Features

- Sends test transactions to Solana
- Measures transaction confirmation latency
- Estimates slot delay
- Tests multiple priority fee levels
- Stores results in CSV format
- Performs statistical analysis and visualization

---

## Project Structure
solana_landing_analyzer
│
├── src/
│ └── main.rs # Rust transaction experiment tool
│
├── analyze_latency.py # Python analysis script
├── latency_results.csv # Experiment results (generated)
├── Cargo.toml # Rust project configuration
└── README.md
---

## Requirements

- Rust
- Cargo
- Python 3
- Python packages:
  - pandas
  - matplotlib

---

## Running the Experiment

Run the Rust program to send transactions and collect latency data:
cargo run


This will generate a dataset:
latency_results.csv

source venv/bin/activate
python analyze_latency.py
The script will:

- print latency statistics
- compute p50 / p95 / p99 latency
- calculate average latency per priority fee
- generate graphs

Graphs will be saved as:
latency_vs_fee.png
latency_distribution.png
slot_delay_distribution.png

---

## What This Measures

The experiment analyzes:

- transaction confirmation latency
- estimated slot delay
- RPC slot lag
- effect of priority fees on execution speed

---

## Purpose

This project was built by me as part of explaining **Solana execution infrastructure and transaction mechanics**, including:

- transaction submission
- slot timing
- priority fees
- latency analysis

---

## License

MIT

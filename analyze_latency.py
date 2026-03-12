import pandas as pd
import matplotlib.pyplot as plt

print("\nLoading dataset...\n")

# Load CSV produced by Rust program
df = pd.read_csv("latency_results.csv")

# ---------------------------------------------------
# Dataset Preview
# ---------------------------------------------------

print("Dataset Preview:\n")
print(df.head())

print("\nTotal transactions:", len(df))

# ---------------------------------------------------
# Basic Latency Statistics
# ---------------------------------------------------

print("\nLatency Statistics (including outliers):\n")
print(df["latency_ms"].describe())

# ---------------------------------------------------
# Percentile Analysis (important for execution infra)
# ---------------------------------------------------

p50 = df["latency_ms"].quantile(0.50)
p95 = df["latency_ms"].quantile(0.95)
p99 = df["latency_ms"].quantile(0.99)

print("\nLatency Percentiles:")
print(f"P50 latency : {p50:.2f} ms")
print(f"P95 latency : {p95:.2f} ms")
print(f"P99 latency : {p99:.2f} ms")

# ---------------------------------------------------
# Remove extreme outliers (> 3000ms)
# ---------------------------------------------------

filtered_df = df[df["latency_ms"] < 3000]

print("\nAfter removing outliers (>3000ms):")
print("Remaining samples:", len(filtered_df))

print("\nFiltered Latency Statistics:\n")
print(filtered_df["latency_ms"].describe())

# ---------------------------------------------------
# Average latency per priority fee
# ---------------------------------------------------

avg_latency = filtered_df.groupby("fee")["latency_ms"].mean()

print("\nAverage latency per fee:\n")
print(avg_latency)

# ---------------------------------------------------
# Average slot delay per priority fee
# ---------------------------------------------------

avg_slot_delay = filtered_df.groupby("fee")["estimated_slot_delay"].mean()

print("\nAverage slot delay per fee:\n")
print(avg_slot_delay)

# ---------------------------------------------------
# Plot: Latency vs Priority Fee
# ---------------------------------------------------

plt.figure(figsize=(8,5))
avg_latency.plot(kind="bar")

plt.title("Average Latency vs Priority Fee")
plt.xlabel("Priority Fee (micro-lamports)")
plt.ylabel("Latency (ms)")
plt.grid(True)

plt.tight_layout()
plt.savefig("latency_vs_fee.png")

print("\nSaved graph: latency_vs_fee.png")

# ---------------------------------------------------
# Plot: Slot Delay Distribution
# ---------------------------------------------------

plt.figure(figsize=(8,5))

filtered_df["estimated_slot_delay"].hist(bins=20)

plt.title("Slot Delay Distribution")
plt.xlabel("Estimated Slot Delay (slots)")
plt.ylabel("Frequency")

plt.grid(True)
plt.tight_layout()
plt.savefig("slot_delay_distribution.png")

print("Saved graph: slot_delay_distribution.png")

# ---------------------------------------------------
# Plot: Latency Distribution
# ---------------------------------------------------

plt.figure(figsize=(8,5))

filtered_df["latency_ms"].hist(bins=25)

plt.title("Latency Distribution")
plt.xlabel("Latency (ms)")
plt.ylabel("Frequency")

plt.grid(True)
plt.tight_layout()
plt.savefig("latency_distribution.png")

print("Saved graph: latency_distribution.png")

print("\nAnalysis complete.\n")
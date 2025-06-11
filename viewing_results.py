import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv("results2.csv")  # <-- Replace with your actual CSV filename

# Ensure episode is numeric
df["episode"] = pd.to_numeric(df["episode"], errors="coerce")
df = df.dropna(subset=["kanji", "episode"])

# Sort by episode
df = df.sort_values("episode")

# First chart: Unique kanji per episode
kanji_per_episode = df.groupby("episode")["kanji"].nunique()

# Second chart: Cumulative unique kanji over time
cumulative_kanji = []
seen_kanji = set()
for ep, group in df.groupby("episode"):
    for k in group["kanji"]:
        seen_kanji.add(k)
    cumulative_kanji.append((ep, len(seen_kanji)))

cumulative_df = pd.DataFrame(cumulative_kanji, columns=["episode", "cumulative_kanji"])

# Plotting
plt.figure(figsize=(12, 6))

# Chart 1: Unique Kanji Per Episode
plt.subplot(1, 2, 1)
plt.plot(kanji_per_episode.index, kanji_per_episode.values, marker='o')
plt.title("Unique Kanji per Episode")
plt.xlabel("Episode")
plt.ylabel("Kanji Count")
plt.grid(True)

# Chart 2: Cumulative Kanji
plt.subplot(1, 2, 2)
plt.plot(cumulative_df["episode"], cumulative_df["cumulative_kanji"], marker='o', color='orange')
plt.title("Cumulative Unique Kanji")
plt.xlabel("Episode")
plt.ylabel("Total Unique Kanji So Far")
plt.grid(True)

plt.tight_layout()
plt.show()
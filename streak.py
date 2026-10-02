"""
GitHub Streak Keeper
Automates daily commits to maintain GitHub contribution streak with clean, meaningful updates.
"""
from datetime import datetime, timezone, timedelta
import os
import random
from pathlib import Path

# Quotes for developers to keep it fun and meaningful
DEV_QUOTES = [
    ("Talk is cheap. Show me the code.", "Linus Torvalds"),
    ("Programs must be written for people to read, and only incidentally for machines to execute.", "Harold Abelson"),
    ("Simplicity is prerequisite for reliability.", "Edsger W. Dijkstra"),
    ("Make it work, make it right, make it fast.", "Kent Beck"),
    ("Clean code always looks like it was written by someone who cares.", "Robert C. Martin"),
    ("First, solve the problem. Then, write the code.", "John Johnson"),
    ("Any fool can write code that a computer can understand. Good programmers write code that humans can understand.", "Martin Fowler"),
    ("Experience is the name everyone gives to their mistakes.", "Oscar Wilde"),
    ("In order to be irreplaceable, one must always be different.", "Coco Chanel"),
    ("Knowledge is power.", "Francis Bacon"),
    ("Before software can be reusable it first has to be usable.", "Ralph Johnson"),
    ("Optimism is an occupational hazard of programming: feedback is the treatment.", "Kent Beck"),
    ("Computers are fast; developers are slow.", "Anonymous"),
    ("Code never lies, comments sometimes do.", "Ron Jeffries"),
    ("The best error message is the one that never shows up.", "Thomas Fuchs"),
    ("Debugging is twice as hard as writing the code in the first place.", "Brian Kernighan"),
    ("Software is like entropy: It is difficult to grasp, weighs nothing, and obeys the Second Law of Thermodynamics; i.e., it always increases.", "Norman Augustine"),
    ("Good code is its own best documentation.", "Steve McConnell"),
    ("Consistency is what transforms average into excellence.", "Tony Robbins"),
    ("Small daily improvements over time lead to stunning results.", "Robin Sharma")
]

BASE_DIR = Path(__file__).parent.resolve()
README_PATH = BASE_DIR / "README.md"
HISTORY_PATH = BASE_DIR / "history.log"

def get_turkey_time():
    utc_now = datetime.now(timezone.utc)
    trt_zone = timezone(timedelta(hours=3))
    return utc_now.astimezone(trt_zone)

def update_history(trt_time):
    date_str = trt_time.strftime("%Y-%m-%d %H:%M:%S TRT")
    entry = f"[{date_str}] Streak keeper heartbeat - keep coding!\n"
    
    if not HISTORY_PATH.exists():
        HISTORY_PATH.write_text(entry, encoding="utf-8")
        total_runs = 1
    else:
        with open(HISTORY_PATH, "a", encoding="utf-8") as f:
            f.write(entry)
        with open(HISTORY_PATH, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
            total_runs = len(lines)
            
    return total_runs

def update_readme(trt_time, total_runs):
    quote_text, quote_author = random.choice(DEV_QUOTES)
    date_str = trt_time.strftime("%d %B %Y, %H:%M:%S (TRT, UTC+3)")
    utc_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # Read last 5 history items
    recent_logs = []
    if HISTORY_PATH.exists():
        with open(HISTORY_PATH, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
            recent_logs = lines[-5:]
            recent_logs.reverse()

    log_markdown = "\n".join([f"- `{item}`" for item in recent_logs]) if recent_logs else "- *Henüz kayıt yok.*"

    readme_content = f"""# 🟢 Daily Streak Keeper

[![Daily Streak Automation](https://github.com/atillacam/daily-streak/actions/workflows/streak.yml/badge.svg)](https://github.com/atillacam/daily-streak/actions/workflows/streak.yml)
![GitHub commit activity](https://img.shields.io/badge/streak-active-brightgreen?style=flat-square&logo=github)
![Total Commits](https://img.shields.io/badge/Total_Updates-{total_runs}-blue?style=flat-square)

GitHub katkı grafiğini (contribution graph / streak) 7/24 aktif ve yeşil tutan bulut tabanlı otomatik iş akışı.

---

### 📊 Durum & İstatistikler
- **Son Güncelleme (TRT):** `{date_str}`
- **Son Güncelleme (UTC):** `{utc_str}`
- **Toplam Otomasyon Güncellemesi:** `{total_runs}`
- **Çalışma Modu:** GitHub Actions (Bulut - Bilgisayar kapalı olsa bile çalışır)

---

### 💡 Günün Notu
> *"{quote_text}"*  
> — **{quote_author}**

---

### 📜 Son Kayıtlar
{log_markdown}

---

<p align="center">
  <sub>Otomatik olarak <a href="https://github.com/features/actions">GitHub Actions</a> tarafından tetiklenmektedir.</sub>
</p>
"""
    README_PATH.write_text(readme_content, encoding="utf-8")

def main():
    trt_time = get_turkey_time()
    total_runs = update_history(trt_time)
    update_readme(trt_time, total_runs)
    print(f"Updated streak keeper! Total runs: {total_runs}, Time: {trt_time.isoformat()}")

if __name__ == "__main__":
    main()

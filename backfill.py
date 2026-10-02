"""
Geçmiş Günleri Yeşillendirme (Backfill Script - Opsiyonel)
Kullanım:
    python backfill.py --days 30          # Son 30 güne 1-3 arası rastgele commit atar
    python backfill.py --start 2026-09-01 # Belirli bir tarihten bugüne doldurur
"""

import argparse
from datetime import datetime, timedelta
import os
import random
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
HISTORY_PATH = BASE_DIR / "history.log"

def create_backfill_commits(start_date: datetime, end_date: datetime, max_per_day: int = 3):
    current = start_date
    total_created = 0
    
    print(f"🚀 {start_date.strftime('%Y-%m-%d')} tarihinden {end_date.strftime('%Y-%m-%d')} tarihine kadar commitler oluşturuluyor...")
    
    while current <= end_date:
        # Hafta sonları veya rastgele günlerde 1-3 commit at
        commits_today = random.randint(1, max_per_day)
        
        for i in range(commits_today):
            # Rastgele bir saat belirle (09:00 - 22:00 arası)
            hour = random.randint(9, 21)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            commit_time = current.replace(hour=hour, minute=minute, second=second)
            time_iso = commit_time.strftime("%Y-%m-%dT%H:%M:%S")
            
            with open(HISTORY_PATH, "a", encoding="utf-8") as f:
                f.write(f"[{time_iso}] Backfill contribution point #{i+1}\n")
                
            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"] = time_iso
            env["GIT_COMMITTER_DATE"] = time_iso
            
            subprocess.run(["git", "add", str(HISTORY_PATH)], cwd=BASE_DIR, env=env, check=True)
            subprocess.run(
                ["git", "commit", "-m", f"chore(backfill): activity on {commit_time.strftime('%Y-%m-%d')}"],
                cwd=BASE_DIR,
                env=env,
                capture_output=True,
                check=True
            )
            total_created += 1
            
        current += timedelta(days=1)
        
    print(f"✅ Toplam {total_created} adet geçmişe dönük commit başarıyla oluşturuldu!")
    print("👉 Şimdi 'git push origin main' yaparak GitHub'a gönderebilirsiniz.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GitHub geçmişini doldurma aracı")
    parser.add_argument("--days", type=int, default=14, help="Kaç gün geriye gidilecek (varsayılan: 14)")
    parser.add_argument("--start", type=str, help="Başlangıç tarihi (YYYY-AA-GG formatında)")
    args = parser.parse_args()
    
    today = datetime.now()
    if args.start:
        start = datetime.strptime(args.start, "%Y-%m-%d")
    else:
        start = today - timedelta(days=args.days)
        
    create_backfill_commits(start, today)

from crewai import Agent, Task, Crew, LLM
import time
import argparse
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Config from env or defaults
MODEL = os.getenv('LLM_MODEL', 'ollama/qwen2.5:14b-instruct-q4_K_M')
BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
INTERVAL_MIN = int(os.getenv('INTERVAL_MIN', '10'))
LOOP_RUNS = int(os.getenv('LOOP_RUNS', '1'))  # 1 for single, -1 for infinite

llm = LLM(
    model=MODEL,
    base_url=BASE_URL,
    api_key="ollama"
)

# Agents (same as before)
supervisor = Agent(role='Supervisor', goal='Koordiniere das Team und schlage neue Themen vor', backstory='Du bist der Chef des InstaContentTeams.', llm=llm, verbose=True)
scout = Agent(role='Trend Scout', goal='Finde aktuelle Instagram-Trends', backstory='Du bist ein scharfer Trend-Beobachter.', llm=llm, verbose=True)
idea_gen = Agent(role='Idea Generator', goal='Erstelle 3-5 konkrete Content-Ideen', backstory='Du bist kreativ.', llm=llm, verbose=True)
writer = Agent(role='Caption Writer', goal='Schreibe ansprechende Captions', backstory='Du bist ein Instagram-Texter.', llm=llm, verbose=True)
hashtag_specialist = Agent(role='Hashtag & SEO Specialist', goal='Füge optimale Hashtags hinzu', backstory='Du bist ein Hashtag-Profi.', llm=llm, verbose=True)
reviewer = Agent(role='Final Reviewer & Polisher', goal='Prüfe alles und gib finale Version frei', backstory='Du bist der strenge Qualitäts-Checker.', llm=llm, verbose=True)

# Tasks
task0 = Task(description='Schlage ein neues, trendiges Instagram-Thema vor (kurz, max. 6 Wörter).', agent=supervisor, expected_output='Ein einzelnes Thema')
task1 = Task(description='Analysiere das Thema "{topic}" und schlage passende Trends vor.', agent=scout, expected_output='Kurze Trend-Zusammenfassung')
task2 = Task(description='Erstelle 3-5 konkrete Instagram-Content-Ideen', agent=idea_gen, expected_output='Liste mit Ideen')
task3 = Task(description='Schreibe für die beste Idee eine fertige Caption (mit Emoji und Call-to-Action)', agent=writer, expected_output='Die Caption')
task4 = Task(description='Füge optimale Hashtags hinzu und optimiere die Caption', agent=hashtag_specialist, expected_output='Optimierte Caption + Hashtags')
task5 = Task(description='Prüfe auf Markenstimme, Grammatik und Engagement. Gib die finale Version.', agent=reviewer, expected_output='FINALER INSTAGRAM-POST')

crew = Crew(agents=[supervisor, scout, idea_gen, writer, hashtag_specialist, reviewer],
            tasks=[task0, task1, task2, task3, task4, task5],
            verbose=True)

log_file = "instagram_content_log.md"

def run_crew(topic='aktuelle Marketing-Trends'):
    result = crew.kickoff(inputs={'topic': topic})
    
    # Extract topic
    topic = result.raw.split("FINALER INSTAGRAM-POST")[0].strip()[-80:] if "FINALER INSTAGRAM-POST" in result.raw else "Automatisch generiert"
    
    # Log
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"\n\n## {datetime.now().strftime('%d.%m.%Y – %H:%M Uhr')}\n")
        f.write(f"**Thema:** {topic}\n\n")
        f.write(f"**Finaler Instagram-Post:**\n{result.raw}\n")
        f.write("---\n")
    
    print(f"✅ Post generated & logged: {log_file}")
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Instagram 5-Agent Crew - Local Content Generator")
    parser.add_argument('--loop', type=int, default=LOOP_RUNS, help='Number of runs (-1 for infinite)')
    parser.add_argument('--interval', type=int, default=INTERVAL_MIN, help='Minutes between runs')
    parser.add_argument('--topic', default='aktuelle Marketing-Trends', help='Initial topic')
    
    args = parser.parse_args()
    
    print(f"🚀 Starting Instagram CrewAI (Model: {MODEL}) | Loop: {args.loop} | Interval: {args.interval}min")
    
    runs = 0
    while True:
        try:
            print(f"\n🔄 Run {runs+1} – {datetime.now().strftime('%H:%M:%S')}")
            run_crew(args.topic)
            runs += 1
            
            if args.loop > 0 and runs >= args.loop:
                break
                
            if args.interval > 0:
                print(f"⏳ Next in {args.interval} min...")
                time.sleep(args.interval * 60)
                
        except KeyboardInterrupt:
            print("\n🛑 Stopped by user.")
            break
        except Exception as e:
            print(f"⚠️ Error: {e} – Retrying in 30s...")
            time.sleep(30)
    
    print("🏁 Done! Check instagram_content_log.md")
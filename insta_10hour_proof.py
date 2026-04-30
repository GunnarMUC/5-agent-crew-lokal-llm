from crewai import Agent, Task, Crew, LLM
import time
from datetime import datetime

# Dein schon installiertes Modell
llm = LLM(
    model="ollama/qwen2.5:14b-instruct-q4_K_M",
    base_url="http://localhost:11434",
    api_key="ollama"
)

# 5 Agenten + expliziter Supervisor für mehr Klarheit
supervisor = Agent(role='Supervisor', goal='Koordiniere das Team und schlage neue Themen vor', backstory='Du bist der Chef des InstaContentTeams.', llm=llm, verbose=True)
scout = Agent(role='Trend Scout', goal='Finde aktuelle Instagram-Trends', backstory='Du bist ein scharfer Trend-Beobachter.', llm=llm, verbose=True)
idea_gen = Agent(role='Idea Generator', goal='Erstelle 3-5 konkrete Content-Ideen', backstory='Du bist kreativ.', llm=llm, verbose=True)
writer = Agent(role='Caption Writer', goal='Schreibe ansprechende Captions', backstory='Du bist ein Instagram-Texter.', llm=llm, verbose=True)
hashtag_specialist = Agent(role='Hashtag & SEO Specialist', goal='Füge optimale Hashtags hinzu', backstory='Du bist ein Hashtag-Profi.', llm=llm, verbose=True)
reviewer = Agent(role='Final Reviewer & Polisher', goal='Prüfe alles und gib finale Version frei', backstory='Du bist der strenge Qualitäts-Checker.', llm=llm, verbose=True)

# Aufgaben
task0 = Task(description='Schlage ein neues, trendiges Instagram-Thema vor (kurz, max. 6 Wörter).', agent=supervisor, expected_output='Ein einzelnes Thema')
task1 = Task(description='Analysiere das Thema "{topic}" und schlage passende Trends vor.', agent=scout, expected_output='Kurze Trend-Zusammenfassung')
task2 = Task(description='Erstelle 3-5 konkrete Instagram-Content-Ideen', agent=idea_gen, expected_output='Liste mit Ideen')
task3 = Task(description='Schreibe für die beste Idee eine fertige Caption (mit Emoji und Call-to-Action)', agent=writer, expected_output='Die Caption')
task4 = Task(description='Füge optimale Hashtags hinzu und optimiere die Caption', agent=hashtag_specialist, expected_output='Optimierte Caption + Hashtags')
task5 = Task(description='Prüfe auf Markenstimme, Grammatik und Engagement. Gib die finale Version.', agent=reviewer, expected_output='FINALER INSTAGRAM-POST')

crew = Crew(agents=[supervisor, scout, idea_gen, writer, hashtag_specialist, reviewer],
            tasks=[task0, task1, task2, task3, task4, task5],
            verbose=True)

print("✅ 10-Stunden-Machbarkeitsbeweis gestartet – läuft jetzt automatisch 10+ Stunden!\n")

log_file = "instagram_content_log.md"

# Dauer-Loop für 10 Stunden
for i in range(60):   # 60 Durchläufe = ca. 10 Stunden bei 10 Min. Pause
    try:
        # Supervisor schlägt neues Thema vor
        print(f"\n🔄 Durchlauf {i+1}/60 – {datetime.now().strftime('%H:%M:%S')}")
        result = crew.kickoff(inputs={'topic': 'aktuelle Marketing-Trends'})
        
        # Extrahiere finales Thema
        topic = result.raw.split("FINALER INSTAGRAM-POST")[0].strip()[-80:] if "FINALER INSTAGRAM-POST" in result.raw else "Automatisch generiert"
        
        # In Markdown-Datei schreiben
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n\n## {datetime.now().strftime('%d.%m.%Y – %H:%M Uhr')}\n")
            f.write(f"**Thema:** {topic}\n\n")
            f.write(f"**Finaler Instagram-Post:**\n{result.raw}\n")
            f.write("---\n")
        
        print(f"✅ Gespeichert in {log_file}")
        
        # 8 Minuten Pause (damit der Mac nicht heiß läuft)
        print("⏳ Nächster Durchlauf in 8 Minuten...\n")
        time.sleep(480)
        
    except Exception as e:
        print(f"⚠️ Kleiner Fehler (wird ignoriert): {e}")
        time.sleep(30)

print("🏁 10-Stunden-Beweis abgeschlossen! Schau in die Datei instagram_content_log.md")

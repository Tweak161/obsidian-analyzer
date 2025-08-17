# Kurzanleitung - Obsidian Vault Analyzer

## In 3 Schritten zum Dashboard:

### 1️⃣ Module installieren (nur beim ersten Mal)
```bash
python run_analysis.py --install
```

### 2️⃣ Analyse starten
```bash
python run_analysis.py
```

### 3️⃣ Dashboard ansehen
Browser öffnet automatisch: http://localhost:5006

---

## Wichtige Befehle

| Was? | Befehl |
|------|--------|
| Erste Installation | `python run_analysis.py --install` |
| Normal starten | `python run_analysis.py` |
| Nur analysieren | `python run_analysis.py --analyze-only` |
| Nur Dashboard | `python run_analysis.py --dashboard-only` |
| Anderen Vault | `python run_analysis.py "C:\Pfad\zum\Vault"` |

## Dashboard-Bereiche

- **Overview**: Statistiken und Übersicht
- **Timeline**: Wann Sie was bearbeitet haben  
- **Important Notes**: Ihre wichtigsten Notizen
- **Orphaned Notes**: Notizen ohne Verbindungen
- **Network Graph**: Interaktive Verbindungs-Grafik
- **Analysis**: Detaillierte Auswertungen

## Bei Problemen

1. Module neu installieren: `python run_analysis.py --install`
2. Terminal/Konsole neu starten
3. Python-Version prüfen: `python --version` (mindestens 3.8)

**Tipp**: Dashboard läuft weiter, bis Sie Strg+C drücken!
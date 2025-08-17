# Obsidian Vault Analyzer - Anleitung

Ein Python-Tool zur Analyse und Visualisierung Ihres Obsidian Vaults mit interaktivem Dashboard.

## 🚀 Schnellstart

### 1. Module installieren

Öffnen Sie ein Terminal im Projektordner und führen Sie aus:

```bash
python run_analysis.py --install
```

Dies installiert automatisch alle benötigten Python-Module:
- obsidiantools (Vault-Analyse)
- networkx (Graphen-Verarbeitung)
- pyvis (Netzwerk-Visualisierung)
- plotly (Diagramme)
- panel (Dashboard-Framework)
- weitere Hilfsbibliotheken

**Hinweis:** Die Installation kann 2-5 Minuten dauern.

### 2. Vault analysieren und Dashboard starten

Nach der Installation starten Sie die Analyse:

```bash
python run_analysis.py
```

Das Programm wird:
1. Ihren Vault scannen (Pfad: `/mnt/c/Users/hess/OneDrive/Dokumente/MyVault`)
2. Alle `.md` und `.excalidraw` Dateien analysieren
3. Ein interaktives Dashboard im Browser öffnen

### 3. Dashboard verwenden

Nach dem Start öffnet sich automatisch Ihr Browser mit dem Dashboard unter:
```
http://localhost:5006
```

Falls sich der Browser nicht automatisch öffnet, können Sie die URL manuell eingeben.

## 📊 Dashboard-Übersicht

### Overview (Übersicht)
- Statistiken zu Ihrem Vault
- Anzahl der Notizen, Verbindungen, verwaiste Notizen
- Verteilung der Dateitypen
- Zuletzt bearbeitete Notizen

### Timeline (Zeitlinie)
- **Erstellungs-Timeline**: Wann wurden Notizen erstellt
- **Bearbeitungs-Historie**: Aktivität über Zeit
- **Aktivitäts-Heatmap**: An welchen Wochentagen/Uhrzeiten Sie arbeiten

### Important Notes (Wichtige Notizen)
- Ranking der wichtigsten Notizen basierend auf:
  - Anzahl eingehender/ausgehender Links
  - PageRank-Algorithmus (Netzwerk-Zentralität)
  - Inhaltsmenge (Wörter, Bilder, Tags)
- Klicken Sie auf Notizen, um sie in Obsidian zu öffnen

### Orphaned Notes (Verwaiste Notizen)
- Liste aller Notizen ohne Verbindungen
- Hilfreich zum Aufräumen oder Verknüpfen isolierter Inhalte

### Network Graph (Netzwerk-Grafik)
- Interaktive Visualisierung aller Notiz-Verbindungen
- Zoom, Verschieben und Hover für Details
- Farbkodierung nach Dateityp

### Analysis (Analyse)
- Verteilung der ausgehenden Links
- Wortanzahl-Statistiken
- Tag-Häufigkeiten

## ⚙️ Weitere Optionen

### Nur Analyse durchführen (ohne Dashboard)
```bash
python run_analysis.py --analyze-only
```
Erstellt nur die Analyse-Datei `vault_analysis.json`

### Nur Dashboard starten (mit vorhandenen Daten)
```bash
python run_analysis.py --dashboard-only
```
Startet das Dashboard mit bereits analysierten Daten

### Anderen Vault-Pfad verwenden
```bash
python run_analysis.py "C:\Pfad\zu\Ihrem\Vault"
```

### Dashboard auf anderem Port starten
```bash
python run_analysis.py --port 8080
```

## 🔧 Fehlerbehebung

### "ModuleNotFoundError"
Führen Sie die Installation erneut aus:
```bash
python run_analysis.py --install
```

### Vault wird nicht gefunden
Überprüfen Sie den Pfad. Das Tool akzeptiert:
- Windows-Pfade: `C:\Users\Name\Vault`
- WSL-Pfade: `/mnt/c/Users/Name/Vault`

### Dashboard öffnet sich nicht
- Prüfen Sie, ob Port 5006 frei ist
- Verwenden Sie einen anderen Port: `--port 8080`
- Öffnen Sie manuell: `http://localhost:5006`

### Große Vaults (1000+ Notizen)
Die erste Analyse kann mehrere Minuten dauern. Der Fortschritt wird im Terminal angezeigt.

## 📁 Ausgabe-Dateien

Nach der Analyse finden Sie:
- `vault_analysis.json`: Alle Analyse-Daten im JSON-Format
- `.cache/`: Cache-Ordner für schnellere Folge-Analysen

## 🛡️ Datenschutz

- Alle Analysen erfolgen lokal auf Ihrem Computer
- Keine Daten werden an externe Server gesendet
- Der Cache enthält nur Metadaten, keine Notiz-Inhalte

## 💡 Tipps

1. **Regelmäßige Analysen**: Führen Sie die Analyse wöchentlich aus, um Trends zu erkennen
2. **Verwaiste Notizen**: Nutzen Sie die Orphaned Notes-Liste zum Aufräumen
3. **Wichtige Notizen**: Die Important Notes zeigen Ihre zentralen Wissensknoten
4. **Zeitlinien**: Erkennen Sie Ihre produktivsten Zeiten in der Heatmap

## 🐛 Probleme melden

Bei Problemen erstellen Sie bitte ein Issue auf GitHub oder kontaktieren Sie den Entwickler.
#!/usr/bin/env python3
"""Generate summaries for all remaining batches"""
import json
from pathlib import Path

def analyze_batch_3():
    return {
        "summaries": [
            {
                "note_id": "800_Ressources/103_PKM/Second Brain, PKMS - LATCH System - How to find Notes",
                "path": "800_Ressources/103_PKM/Second Brain, PKMS - LATCH System - How to find Notes.md",
                "ai_summary": "Explains the LATCH system (Location, Alphabet, Time, Category, Hierarchy) as a framework for organizing and finding notes effectively in personal knowledge management systems.",
                "ai_hashtags": ["#productivity", "#education", "#personal"],
                "ai_keywords": ["LATCH system", "note organization", "information retrieval", "PKM", "second brain", "finding notes", "categorization", "hierarchy", "alphabetical order"]
            },
            {
                "note_id": "800_Ressources/103_PKM/Second Brain, PKMS - Principles",
                "path": "800_Ressources/103_PKM/Second Brain, PKMS - Principles.md",
                "ai_summary": "Core principles for building and maintaining a second brain or personal knowledge management system, focusing on capture, organization, and retrieval strategies.",
                "ai_hashtags": ["#productivity", "#education", "#personal"],
                "ai_keywords": ["PKM principles", "second brain", "knowledge management", "organizational principles", "capture strategies", "information architecture"]
            },
            {
                "note_id": "800_Ressources/103_PKM/Shape your Digital and Physical Environments - They shape your Thinking and therefore your Life (Cathedral Effect)",
                "path": "800_Ressources/103_PKM/Shape your Digital and Physical Environments - They shape your Thinking and therefore your Life (Cathedral Effect).md",
                "ai_summary": "Explores how digital and physical environments influence thinking patterns and life outcomes, referencing the Cathedral Effect where high ceilings promote abstract thinking.",
                "ai_hashtags": ["#productivity", "#psychology", "#personal"],
                "ai_keywords": ["Cathedral Effect", "environment design", "cognitive influence", "digital environment", "physical space", "thinking patterns", "environmental psychology"]
            },
            {
                "note_id": "800_Ressources/103_PKM/The Power of IPs (Intermediate Packets) - Building Blocks to Boost your Productivity",
                "path": "800_Ressources/103_PKM/The Power of IPs (Intermediate Packets) - Building Blocks to Boost your Productivity.md",
                "ai_summary": "Discusses the concept of Intermediate Packets (IPs) as reusable units of work that can be combined and recombined to boost productivity and creative output.",
                "ai_hashtags": ["#productivity", "#creativity", "#personal"],
                "ai_keywords": ["Intermediate Packets", "IPs", "productivity", "building blocks", "reusable content", "creative process", "work units", "modular thinking"]
            },
            {
                "note_id": "800_Ressources/103_PKM/Visual-Note-Taking.excalidraw",
                "path": "800_Ressources/103_PKM/Visual-Note-Taking.excalidraw.md",
                "ai_summary": "An Excalidraw diagram about visual note-taking techniques and methods for better comprehension and retention.",
                "ai_hashtags": ["#productivity", "#education", "#creativity"],
                "ai_keywords": ["visual note-taking", "sketchnotes", "visual thinking", "diagram", "comprehension", "retention", "learning techniques"]
            },
            {
                "note_id": "800_Ressources/104_Buddhism/5 Feinde der Meditation",
                "path": "800_Ressources/104_Buddhism/5 Feinde der Meditation.md",
                "ai_summary": "Describes the five hindrances or enemies of meditation in Buddhist practice that obstruct mental clarity and spiritual progress.",
                "ai_hashtags": ["#meditation", "#spirituality", "#psychology"],
                "ai_keywords": ["meditation hindrances", "five enemies", "Buddhist practice", "mental obstacles", "spiritual barriers", "meditation challenges"]
            },
            {
                "note_id": "800_Ressources/104_Buddhism/5 Freunde der Meditation",
                "path": "800_Ressources/104_Buddhism/5 Freunde der Meditation.md",
                "ai_summary": "Outlines the five friends or supportive factors of meditation that help cultivate a successful and sustained meditation practice.",
                "ai_hashtags": ["#meditation", "#spirituality", "#personal"],
                "ai_keywords": ["meditation supports", "five friends", "Buddhist practice", "meditation aids", "spiritual helpers", "practice factors"]
            },
            {
                "note_id": "800_Ressources/104_Buddhism/Buddhismus - Drei Daseinsmerkmale",
                "path": "800_Ressources/104_Buddhism/Buddhismus - Drei Daseinsmerkmale.md",
                "ai_summary": "Explains the three marks of existence (Trilakshana) in Buddhism: impermanence (anicca), suffering (dukkha), and non-self (anatta).",
                "ai_hashtags": ["#spirituality", "#philosophy", "#meditation"],
                "ai_keywords": ["three marks of existence", "Trilakshana", "impermanence", "suffering", "non-self", "Buddhist philosophy", "anicca", "dukkha", "anatta"]
            },
            {
                "note_id": "800_Ressources/104_Buddhism/Buddhismus 10 Tugenden aka Paramis",
                "path": "800_Ressources/104_Buddhism/Buddhismus 10 Tugenden aka Paramis.md",
                "ai_summary": "Details the ten perfections (Paramis) in Buddhism that practitioners cultivate on the path to enlightenment, including generosity, morality, and wisdom.",
                "ai_hashtags": ["#spirituality", "#philosophy", "#personal"],
                "ai_keywords": ["Paramis", "ten perfections", "Buddhist virtues", "spiritual qualities", "enlightenment path", "generosity", "morality", "wisdom", "patience"]
            },
            {
                "note_id": "800_Ressources/104_Buddhism/MOC - Meditation.excalidraw",
                "path": "800_Ressources/104_Buddhism/MOC - Meditation.excalidraw.md",
                "ai_summary": "A Map of Content organizing meditation-related resources, techniques, and Buddhist concepts in an Excalidraw diagram.",
                "ai_hashtags": ["#meditation", "#spirituality", "#education"],
                "ai_keywords": ["meditation MOC", "Buddhist meditation", "practice map", "meditation resources", "spiritual practices", "mindfulness", "concentration"]
            }
        ]
    }

def analyze_batch_4():
    return {
        "summaries": [
            {
                "note_id": "800_Ressources/104_Buddhism/Metta Sutta",
                "path": "800_Ressources/104_Buddhism/Metta Sutta.md",
                "ai_summary": "The Metta Sutta, a fundamental Buddhist text on loving-kindness meditation and the cultivation of universal compassion for all beings.",
                "ai_hashtags": ["#meditation", "#spirituality", "#personal"],
                "ai_keywords": ["Metta Sutta", "loving-kindness", "compassion", "Buddhist scripture", "meditation text", "universal love", "spiritual practice"]
            },
            {
                "note_id": "800_Ressources/104_Buddhism/Review - Anapana (Breathing Meditation)",
                "path": "800_Ressources/104_Buddhism/Review - Anapana (Breathing Meditation).md",
                "ai_summary": "A review and guide to Anapana meditation, the Buddhist practice of mindfulness of breathing as a foundation for deeper meditation.",
                "ai_hashtags": ["#meditation", "#spirituality", "#health"],
                "ai_keywords": ["Anapana", "breathing meditation", "mindfulness", "breath awareness", "meditation technique", "Buddhist practice", "concentration"]
            },
            {
                "note_id": "800_Ressources/104_Buddhism/S.N. Goenka - 10 Day Vipassana Course.excalidraw",
                "path": "800_Ressources/104_Buddhism/S.N. Goenka - 10 Day Vipassana Course.excalidraw.md",
                "ai_summary": "An Excalidraw diagram outlining the structure and key elements of S.N. Goenka's 10-day Vipassana meditation course.",
                "ai_hashtags": ["#meditation", "#spirituality", "#education"],
                "ai_keywords": ["Vipassana", "S.N. Goenka", "10-day course", "meditation retreat", "insight meditation", "Buddhist practice", "silent retreat"]
            },
            {
                "note_id": "800_Ressources/104_Buddhism/Summary of Pratītyasamutpāda (dependent origination)",
                "path": "800_Ressources/104_Buddhism/Summary of Pratītyasamutpāda (dependent origination).md",
                "ai_summary": "Summarizes the Buddhist concept of dependent origination (Pratītyasamutpāda), explaining how all phenomena arise in dependence upon multiple causes and conditions.",
                "ai_hashtags": ["#spirituality", "#philosophy", "#education"],
                "ai_keywords": ["dependent origination", "Pratītyasamutpāda", "Buddhist philosophy", "causality", "interdependence", "twelve links", "conditional arising"]
            },
            {
                "note_id": "800_Ressources/104_Buddhism/The Noble Eightfold Path.excalidraw",
                "path": "800_Ressources/104_Buddhism/The Noble Eightfold Path.excalidraw.md",
                "ai_summary": "An Excalidraw diagram illustrating the Noble Eightfold Path, Buddhism's practical guide to ethical living and the cessation of suffering.",
                "ai_hashtags": ["#spirituality", "#philosophy", "#personal"],
                "ai_keywords": ["Noble Eightfold Path", "Buddhist ethics", "right understanding", "right action", "spiritual path", "enlightenment", "moral conduct", "wisdom"]
            },
            {
                "note_id": "800_Ressources/105_Dating/BoaP - Fundamentals of Female Dynamics (Michael Knight).excalidraw",
                "path": "800_Ressources/105_Dating/BoaP - Fundamentals of Female Dynamics (Michael Knight).excalidraw.md",
                "ai_summary": "An Excalidraw diagram summarizing concepts from Michael Knight's work on understanding female psychology and dynamics in dating contexts.",
                "ai_hashtags": ["#relationship", "#psychology", "#personal"],
                "ai_keywords": ["dating dynamics", "female psychology", "relationship patterns", "attraction", "social dynamics", "interpersonal relationships"]
            },
            {
                "note_id": "800_Ressources/105_Dating/The rise of lonely single man - YT.excalidraw",
                "path": "800_Ressources/105_Dating/The rise of lonely single man - YT.excalidraw.md",
                "ai_summary": "An Excalidraw diagram analyzing the societal phenomenon of increasing male loneliness and singlehood, based on YouTube content.",
                "ai_hashtags": ["#relationship", "#psychology", "#personal"],
                "ai_keywords": ["male loneliness", "single men", "social isolation", "dating challenges", "modern relationships", "societal trends", "mental health"]
            },
            {
                "note_id": "800_Ressources/106_Trading/A Complete Day Trading System - Kristjan Qullamagie.excalidraw",
                "path": "800_Ressources/106_Trading/A Complete Day Trading System - Kristjan Qullamagie.excalidraw.md",
                "ai_summary": "An Excalidraw diagram outlining Kristjan Qullamagie's complete day trading system, including strategies, risk management, and technical analysis.",
                "ai_hashtags": ["#finance", "#business", "#education"],
                "ai_keywords": ["day trading", "trading system", "Kristjan Qullamagie", "technical analysis", "risk management", "trading strategies", "financial markets"]
            },
            {
                "note_id": "800_Ressources/106_Trading/Economics and Financial Markets.excalidraw",
                "path": "800_Ressources/106_Trading/Economics and Financial Markets.excalidraw.md",
                "ai_summary": "An Excalidraw diagram exploring the relationships between economics and financial markets, including key concepts and market dynamics.",
                "ai_hashtags": ["#finance", "#business", "#education"],
                "ai_keywords": ["economics", "financial markets", "market dynamics", "economic theory", "trading", "investment", "macroeconomics", "market analysis"]
            },
            {
                "note_id": "800_Ressources/106_Trading/MOC - Trading.excalidraw",
                "path": "800_Ressources/106_Trading/MOC - Trading.excalidraw.md",
                "ai_summary": "A Map of Content organizing trading-related resources, strategies, tools, and educational materials in an Excalidraw format.",
                "ai_hashtags": ["#finance", "#business", "#education"],
                "ai_keywords": ["trading MOC", "trading resources", "investment strategies", "financial education", "market analysis", "trading tools", "portfolio management"]
            }
        ]
    }

def analyze_batch_5():
    return {
        "summaries": [
            {
                "note_id": "800_Ressources/106_Trading/Trading - Gesammelte Strategien von Meetup Gruppe",
                "path": "800_Ressources/106_Trading/Trading - Gesammelte Strategien von Meetup Gruppe.md",
                "ai_summary": "A collection of trading strategies gathered from a trading meetup group, including various approaches and techniques shared by community members.",
                "ai_hashtags": ["#finance", "#business", "#education"],
                "ai_keywords": ["trading strategies", "meetup group", "community knowledge", "trading techniques", "collective wisdom", "practical strategies", "peer learning"]
            },
            {
                "note_id": "800_Ressources/106_Trading/Trading Psychology",
                "path": "800_Ressources/106_Trading/Trading Psychology.md",
                "ai_summary": "Explores the psychological aspects of trading, including emotional control, discipline, and mental strategies for successful trading.",
                "ai_hashtags": ["#finance", "#psychology", "#personal"],
                "ai_keywords": ["trading psychology", "emotional control", "discipline", "mental strategies", "risk psychology", "decision making", "behavioral finance"]
            },
            {
                "note_id": "800_Ressources/106_Trading/Trading with Qullamagie - Lesezeichen und Notizen",
                "path": "800_Ressources/106_Trading/Trading with Qullamagie - Lesezeichen und Notizen.md",
                "ai_summary": "Bookmarks and notes related to Qullamagie's trading methods, containing key insights and reference points for his trading approach.",
                "ai_hashtags": ["#finance", "#business", "#education"],
                "ai_keywords": ["Qullamagie", "trading notes", "bookmarks", "trading insights", "reference material", "swing trading", "growth stocks"]
            },
            {
                "note_id": "800_Ressources/106_Trading/Why Day Trading does not work",
                "path": "800_Ressources/106_Trading/Why Day Trading does not work.md",
                "ai_summary": "An analysis of why day trading often fails for most traders, examining statistical evidence and common pitfalls.",
                "ai_hashtags": ["#finance", "#business", "#education"],
                "ai_keywords": ["day trading critique", "trading failures", "statistical evidence", "retail trading", "market efficiency", "trading misconceptions", "risk analysis"]
            },
            {
                "note_id": "800_Ressources/106_Trading/William O'Neil - How to Make Money in Stocks (CANSLIM)",
                "path": "800_Ressources/106_Trading/William O'Neil - How to Make Money in Stocks (CANSLIM).md",
                "ai_summary": "Summary of William O'Neil's CANSLIM investment strategy from 'How to Make Money in Stocks', covering the seven key criteria for stock selection.",
                "ai_hashtags": ["#finance", "#business", "#education"],
                "ai_keywords": ["CANSLIM", "William O'Neil", "stock investing", "growth investing", "technical analysis", "fundamental analysis", "investment strategy"]
            },
            {
                "note_id": "800_Ressources/107_Self_Improvement/12 Rules of Life by Jordan Peterson - Top Takeaways.excalidraw",
                "path": "800_Ressources/107_Self_Improvement/12 Rules of Life by Jordan Peterson - Top Takeaways.excalidraw.md",
                "ai_summary": "An Excalidraw diagram summarizing the key takeaways from Jordan Peterson's '12 Rules for Life', focusing on personal responsibility and self-improvement.",
                "ai_hashtags": ["#personal", "#psychology", "#education"],
                "ai_keywords": ["12 Rules for Life", "Jordan Peterson", "self-improvement", "personal responsibility", "life principles", "psychology", "meaning", "order and chaos"]
            },
            {
                "note_id": "800_Ressources/107_Self_Improvement/30 Day Challange - How to Build a Habit.excalidraw",
                "path": "800_Ressources/107_Self_Improvement/30 Day Challange - How to Build a Habit.excalidraw.md",
                "ai_summary": "An Excalidraw diagram outlining a 30-day challenge framework for building new habits, including strategies and tracking methods.",
                "ai_hashtags": ["#personal", "#productivity", "#health"],
                "ai_keywords": ["30-day challenge", "habit building", "behavior change", "consistency", "tracking progress", "personal development", "habit formation"]
            },
            {
                "note_id": "800_Ressources/107_Self_Improvement/4 Commitments for Life by Don Miguel Ruiz",
                "path": "800_Ressources/107_Self_Improvement/4 Commitments for Life by Don Miguel Ruiz.md",
                "ai_summary": "Summary of Don Miguel Ruiz's 'The Four Agreements', presenting four principles for personal freedom and authentic living based on ancient Toltec wisdom.",
                "ai_hashtags": ["#personal", "#spirituality", "#philosophy"],
                "ai_keywords": ["Four Agreements", "Don Miguel Ruiz", "Toltec wisdom", "personal freedom", "authentic living", "life principles", "spiritual growth"]
            },
            {
                "note_id": "800_Ressources/107_Self_Improvement/Anti Fragility by Nassim Taleb.excalidraw",
                "path": "800_Ressources/107_Self_Improvement/Anti Fragility by Nassim Taleb.excalidraw.md",
                "ai_summary": "An Excalidraw diagram exploring Nassim Taleb's concept of antifragility - systems that gain from disorder and become stronger under stress.",
                "ai_hashtags": ["#personal", "#philosophy", "#business"],
                "ai_keywords": ["antifragility", "Nassim Taleb", "robustness", "disorder", "stress adaptation", "complex systems", "Black Swan", "resilience"]
            },
            {
                "note_id": "800_Ressources/107_Self_Improvement/BoaP - Deep Work by Cal Newport.excalidraw",
                "path": "800_Ressources/107_Self_Improvement/BoaP - Deep Work by Cal Newport.excalidraw.md",
                "ai_summary": "An Excalidraw summary of Cal Newport's 'Deep Work', covering strategies for focused, distraction-free work in an increasingly connected world.",
                "ai_hashtags": ["#productivity", "#career", "#personal"],
                "ai_keywords": ["deep work", "Cal Newport", "focus", "productivity", "distraction-free", "cognitive performance", "professional skills", "attention management"]
            }
        ]
    }

def analyze_batch_6():
    return {
        "summaries": [
            {
                "note_id": "800_Ressources/107_Self_Improvement/BoaP - Der reichste Mann von Babylon",
                "path": "800_Ressources/107_Self_Improvement/BoaP - Der reichste Mann von Babylon.md",
                "ai_summary": "Summary of 'The Richest Man in Babylon', presenting timeless financial wisdom through ancient Babylonian parables about wealth building and money management.",
                "ai_hashtags": ["#finance", "#personal", "#education"],
                "ai_keywords": ["Richest Man in Babylon", "financial wisdom", "wealth building", "money management", "savings", "investment principles", "ancient wisdom", "personal finance"]
            },
            {
                "note_id": "800_Ressources/107_Self_Improvement/BoaP - Finite and Infinite Games by James P. Carse.excalidraw",
                "path": "800_Ressources/107_Self_Improvement/BoaP - Finite and Infinite Games by James P. Carse.excalidraw.md",
                "ai_summary": "An Excalidraw diagram exploring James Carse's concept of finite games (played to win) versus infinite games (played to continue playing) as frameworks for understanding life.",
                "ai_hashtags": ["#philosophy", "#personal", "#psychology"],
                "ai_keywords": ["finite games", "infinite games", "James Carse", "life philosophy", "game theory", "purpose", "competition", "continuation"]
            },
            {
                "note_id": "800_Ressources/107_Self_Improvement/BoaP - Getting Things Done (The Art of Stressfree Productivity) - David Allen.excalidraw",
                "path": "800_Ressources/107_Self_Improvement/BoaP - Getting Things Done (The Art of Stressfree Productivity) - David Allen.excalidraw.md",
                "ai_summary": "An Excalidraw summary of David Allen's GTD methodology, covering the five-step workflow for capturing, clarifying, organizing, reflecting, and engaging with tasks.",
                "ai_hashtags": ["#productivity", "#personal", "#business"],
                "ai_keywords": ["GTD", "Getting Things Done", "David Allen", "productivity system", "task management", "stress-free productivity", "workflow", "organization"]
            },
            {
                "note_id": "800_Ressources/107_Self_Improvement/BoaP - So Good They Can't Ignore You by Cal Newport.excalidraw",
                "path": "800_Ressources/107_Self_Improvement/BoaP - So Good They Can't Ignore You by Cal Newport.excalidraw.md",
                "ai_summary": "An Excalidraw diagram of Cal Newport's career advice book, challenging the 'follow your passion' myth and advocating for skill development and craftsman mindset.",
                "ai_hashtags": ["#career", "#personal", "#education"],
                "ai_keywords": ["career capital", "Cal Newport", "skill development", "craftsman mindset", "passion myth", "deliberate practice", "career advice", "professional growth"]
            },
            {
                "note_id": "800_Ressources/107_Self_Improvement/Book - Breath by James Nestor.excalidraw",
                "path": "800_Ressources/107_Self_Improvement/Book - Breath by James Nestor.excalidraw.md",
                "ai_summary": "An Excalidraw summary of James Nestor's 'Breath', exploring the science and practice of breathing for improved health and performance.",
                "ai_hashtags": ["#health", "#personal", "#science"],
                "ai_keywords": ["breathing", "James Nestor", "respiratory health", "breathwork", "nasal breathing", "health optimization", "ancient practices", "modern science"]
            },
            {
                "note_id": "800_Ressources/107_Self_Improvement/Book - Cant hurt me - David Goggins",
                "path": "800_Ressources/107_Self_Improvement/Book - Cant hurt me - David Goggins.md",
                "ai_summary": "Summary of David Goggins' autobiography 'Can't Hurt Me', detailing his transformation from troubled youth to Navy SEAL and ultra-endurance athlete through mental toughness.",
                "ai_hashtags": ["#personal", "#health", "#psychology"],
                "ai_keywords": ["David Goggins", "mental toughness", "Navy SEAL", "ultra-endurance", "self-discipline", "overcoming adversity", "40% rule", "accountability mirror"]
            },
            {
                "note_id": "800_Ressources/107_Self_Improvement/Choose Yourself - James Altucher.excalidraw",
                "path": "800_Ressources/107_Self_Improvement/Choose Yourself - James Altucher.excalidraw.md",
                "ai_summary": "An Excalidraw diagram of James Altucher's 'Choose Yourself', advocating for self-reliance and entrepreneurial thinking in the modern economy.",
                "ai_hashtags": ["#personal", "#business", "#career"],
                "ai_keywords": ["Choose Yourself", "James Altucher", "self-reliance", "entrepreneurship", "personal economy", "daily practice", "idea muscle", "reinvention"]
            },
            {
                "note_id": "800_Ressources/107_Self_Improvement/Digital Minimalism by Cal Newport",
                "path": "800_Ressources/107_Self_Improvement/Digital Minimalism by Cal Newport.md",
                "ai_summary": "Summary of Cal Newport's 'Digital Minimalism', offering a philosophy and practical strategies for using technology more intentionally to support values and goals.",
                "ai_hashtags": ["#productivity", "#personal", "#technology"],
                "ai_keywords": ["digital minimalism", "Cal Newport", "technology use", "intentional living", "digital declutter", "solitude", "high-quality leisure", "attention economy"]
            },
            {
                "note_id": "800_Ressources/107_Self_Improvement/Dopamine Detox",
                "path": "800_Ressources/107_Self_Improvement/Dopamine Detox.md",
                "ai_summary": "Explores the concept and practice of dopamine detoxing to reset reward systems, reduce addictive behaviors, and increase motivation for meaningful activities.",
                "ai_hashtags": ["#health", "#personal", "#psychology"],
                "ai_keywords": ["dopamine detox", "reward system", "addiction", "motivation", "neuroplasticity", "digital detox", "behavioral reset", "pleasure tolerance"]
            },
            {
                "note_id": "800_Ressources/107_Self_Improvement/Fasting",
                "path": "800_Ressources/107_Self_Improvement/Fasting.md",
                "ai_summary": "Information about various fasting practices, their health benefits, and implementation strategies for physical and mental well-being.",
                "ai_hashtags": ["#health", "#personal", "#spirituality"],
                "ai_keywords": ["fasting", "intermittent fasting", "autophagy", "metabolic health", "longevity", "mental clarity", "spiritual practice", "health optimization"]
            }
        ]
    }

def analyze_batch_7():
    return {
        "summaries": [
            {
                "note_id": "800_Ressources/107_Self_Improvement/Goal Visualisation (Process Simulations beat Outcome simulations)",
                "path": "800_Ressources/107_Self_Improvement/Goal Visualisation (Process Simulations beat Outcome simulations).md",
                "ai_summary": "Explains why visualizing the process of achieving goals is more effective than visualizing outcomes, based on psychological research about motivation and performance.",
                "ai_hashtags": ["#personal", "#psychology", "#productivity"],
                "ai_keywords": ["goal visualization", "process simulation", "outcome simulation", "mental rehearsal", "performance psychology", "motivation", "achievement strategies"]
            },
            {
                "note_id": "800_Ressources/107_Self_Improvement/James Clear Yearly Compass 2023.excalidraw",
                "path": "800_Ressources/107_Self_Improvement/James Clear Yearly Compass 2023.excalidraw.md",
                "ai_summary": "An Excalidraw visualization of James Clear's yearly planning compass for 2023, including goal-setting frameworks and reflection exercises.",
                "ai_hashtags": ["#personal", "#productivity", "#education"],
                "ai_keywords": ["yearly planning", "James Clear", "goal setting", "annual review", "compass framework", "reflection", "personal development", "habit tracking"]
            },
            {
                "note_id": "800_Ressources/107_Self_Improvement/Locus of Control",
                "path": "800_Ressources/107_Self_Improvement/Locus of Control.md",
                "ai_summary": "Explores the psychological concept of locus of control, distinguishing between internal (self-determined) and external (environment-determined) attribution of life events.",
                "ai_hashtags": ["#psychology", "#personal", "#education"],
                "ai_keywords": ["locus of control", "internal control", "external control", "attribution theory", "personal agency", "responsibility", "psychology", "self-efficacy"]
            },
            {
                "note_id": "800_Ressources/107_Self_Improvement/MOC - Self Improvement.excalidraw",
                "path": "800_Ressources/107_Self_Improvement/MOC - Self Improvement.excalidraw.md",
                "ai_summary": "A comprehensive Map of Content organizing self-improvement resources, including books, concepts, strategies, and practical tools for personal development.",
                "ai_hashtags": ["#personal", "#education", "#productivity"],
                "ai_keywords": ["self-improvement MOC", "personal development", "resource map", "growth strategies", "life skills", "learning resources", "improvement framework"]
            },
            {
                "note_id": "800_Ressources/107_Self_Improvement/Never Split The Difference (Chris Voss)",
                "path": "800_Ressources/107_Self_Improvement/Never Split The Difference (Chris Voss).md",
                "ai_summary": "Summary of Chris Voss's negotiation tactics from his FBI hostage negotiator experience, including tactical empathy and calibrated questions.",
                "ai_hashtags": ["#business", "#psychology", "#personal"],
                "ai_keywords": ["negotiation", "Chris Voss", "FBI tactics", "tactical empathy", "calibrated questions", "mirroring", "labeling", "Black Swan method"]
            },
            {
                "note_id": "800_Ressources/107_Self_Improvement/Obsidian Day Planner with Ali Abdaal",
                "path": "800_Ressources/107_Self_Improvement/Obsidian Day Planner with Ali Abdaal.md",
                "ai_summary": "A daily planning system inspired by Ali Abdaal's productivity methods, adapted for use within Obsidian for time-blocking and task management.",
                "ai_hashtags": ["#productivity", "#personal", "#technology"],
                "ai_keywords": ["day planning", "Ali Abdaal", "Obsidian", "time blocking", "productivity system", "daily schedule", "task management", "workflow optimization"]
            },
            {
                "note_id": "800_Ressources/107_Self_Improvement/Quote - At what point is productivity just procrastination",
                "path": "800_Ressources/107_Self_Improvement/Quote - At what point is productivity just procrastination.md",
                "ai_summary": "A thought-provoking quote examining when productivity systems and optimization become forms of procrastination from actual meaningful work.",
                "ai_hashtags": ["#productivity", "#psychology", "#personal"],
                "ai_keywords": ["productivity paradox", "procrastination", "busy work", "meaningful action", "self-reflection", "productivity trap", "action bias"]
            },
            {
                "note_id": "800_Ressources/107_Self_Improvement/Quote - If you only read the books that everyone is reading you will only think what everyone is thinking",
                "path": "800_Ressources/107_Self_Improvement/Quote - If you only read the books that everyone is reading you will only think what everyone is thinking.md",
                "ai_summary": "A quote emphasizing the importance of diverse reading and independent thinking to develop unique perspectives and insights.",
                "ai_hashtags": ["#education", "#personal", "#creativity"],
                "ai_keywords": ["independent thinking", "diverse reading", "originality", "conformity", "intellectual diversity", "unique perspectives", "critical thinking"]
            },
            {
                "note_id": "800_Ressources/107_Self_Improvement/Stoizismus - Übersicht mit Zitaten.excalidraw",
                "path": "800_Ressources/107_Self_Improvement/Stoizismus - Übersicht mit Zitaten.excalidraw.md",
                "ai_summary": "An Excalidraw overview of Stoicism including key concepts and quotes from major Stoic philosophers like Marcus Aurelius, Seneca, and Epictetus.",
                "ai_hashtags": ["#philosophy", "#personal", "#spirituality"],
                "ai_keywords": ["Stoicism", "Marcus Aurelius", "Seneca", "Epictetus", "Stoic philosophy", "virtue ethics", "emotional resilience", "practical wisdom"]
            },
            {
                "note_id": "800_Ressources/107_Self_Improvement/The 5 Second Rule - Mel Robbins",
                "path": "800_Ressources/107_Self_Improvement/The 5 Second Rule - Mel Robbins.md",
                "ai_summary": "Mel Robbins' simple technique of counting down 5-4-3-2-1 to overcome hesitation and take immediate action, breaking the habit of overthinking.",
                "ai_hashtags": ["#personal", "#psychology", "#productivity"],
                "ai_keywords": ["5 second rule", "Mel Robbins", "action trigger", "procrastination", "decision making", "behavioral activation", "momentum", "habit breaking"]
            }
        ]
    }

def analyze_batch_8():
    return {
        "summaries": [
            {
                "note_id": "800_Ressources/107_Self_Improvement/The Feynman Method of Learning",
                "path": "800_Ressources/107_Self_Improvement/The Feynman Method of Learning.md",
                "ai_summary": "Explains Richard Feynman's learning technique of teaching complex concepts in simple terms to identify knowledge gaps and deepen understanding.",
                "ai_hashtags": ["#education", "#personal", "#science"],
                "ai_keywords": ["Feynman method", "learning technique", "teaching", "simplification", "knowledge gaps", "deep understanding", "active learning", "Richard Feynman"]
            },
            {
                "note_id": "800_Ressources/107_Self_Improvement/The power of now by Eckhart Tolle.excalidraw",
                "path": "800_Ressources/107_Self_Improvement/The power of now by Eckhart Tolle.excalidraw.md",
                "ai_summary": "An Excalidraw diagram summarizing Eckhart Tolle's teachings on presence, consciousness, and transcending ego-based thinking to find inner peace.",
                "ai_hashtags": ["#spirituality", "#personal", "#psychology"],
                "ai_keywords": ["Power of Now", "Eckhart Tolle", "presence", "mindfulness", "ego transcendence", "consciousness", "spiritual awakening", "present moment"]
            },
            {
                "note_id": "800_Ressources/107_Self_Improvement/The War Of Art - Steven Pressfield",
                "path": "800_Ressources/107_Self_Improvement/The War Of Art - Steven Pressfield.md",
                "ai_summary": "Steven Pressfield's guide to overcoming creative resistance, identifying the internal forces that prevent us from doing our most important work.",
                "ai_hashtags": ["#creativity", "#personal", "#writing"],
                "ai_keywords": ["War of Art", "Steven Pressfield", "resistance", "creative blocks", "professional mindset", "artistic discipline", "procrastination", "creative work"]
            },
            {
                "note_id": "800_Ressources/107_Self_Improvement/Tony Robbins - Motivational Concepts",
                "path": "800_Ressources/107_Self_Improvement/Tony Robbins - Motivational Concepts.md",
                "ai_summary": "Key motivational concepts from Tony Robbins including state management, the six human needs, and strategies for personal transformation.",
                "ai_hashtags": ["#personal", "#psychology", "#business"],
                "ai_keywords": ["Tony Robbins", "motivation", "state management", "six human needs", "personal transformation", "peak performance", "NLP", "success psychology"]
            },
            {
                "note_id": "800_Ressources/107_Self_Improvement/Yearly Compass.excalidraw",
                "path": "800_Ressources/107_Self_Improvement/Yearly Compass.excalidraw.md",
                "ai_summary": "An Excalidraw template for annual planning and reflection, providing a visual framework for setting yearly goals and tracking progress.",
                "ai_hashtags": ["#personal", "#productivity", "#education"],
                "ai_keywords": ["yearly planning", "annual goals", "compass framework", "reflection", "goal setting", "progress tracking", "life design", "strategic planning"]
            },
            {
                "note_id": "800_Ressources/108_Lifestyle_Business/Gary Keller & Jay Papasan - The ONE Thing.excalidraw",
                "path": "800_Ressources/108_Lifestyle_Business/Gary Keller & Jay Papasan - The ONE Thing.excalidraw.md",
                "ai_summary": "An Excalidraw summary of 'The ONE Thing' concept, focusing on identifying and prioritizing the single most important task that makes everything else easier or unnecessary.",
                "ai_hashtags": ["#productivity", "#business", "#personal"],
                "ai_keywords": ["ONE Thing", "Gary Keller", "Jay Papasan", "focus", "prioritization", "domino effect", "time blocking", "goal achievement"]
            },
            {
                "note_id": "800_Ressources/109_Literatur/Ralph Waldo Emerson - Quote",
                "path": "800_Ressources/109_Literatur/Ralph Waldo Emerson - Quote.md",
                "ai_summary": "A collection of inspiring quotes from Ralph Waldo Emerson on self-reliance, nature, and transcendentalist philosophy.",
                "ai_hashtags": ["#philosophy", "#writing", "#spirituality"],
                "ai_keywords": ["Ralph Waldo Emerson", "transcendentalism", "self-reliance", "nature", "American philosophy", "quotes", "wisdom", "individualism"]
            },
            {
                "note_id": "800_Ressources/109_Literatur/Truth & Beauty by Ann Patchett",
                "path": "800_Ressources/109_Literatur/Truth & Beauty by Ann Patchett.md",
                "ai_summary": "Notes on Ann Patchett's memoir about her friendship with poet Lucy Grealy, exploring themes of friendship, art, and mortality.",
                "ai_hashtags": ["#book", "#writing", "#personal"],
                "ai_keywords": ["Ann Patchett", "Truth & Beauty", "memoir", "friendship", "Lucy Grealy", "writers", "mortality", "artistic life"]
            },
            {
                "note_id": "800_Ressources/110_Career/Career Development Resources",
                "path": "800_Ressources/110_Career/Career Development Resources.md",
                "ai_summary": "A curated collection of resources for career development including books, courses, mentorship strategies, and professional growth tools.",
                "ai_hashtags": ["#career", "#education", "#personal"],
                "ai_keywords": ["career development", "professional growth", "skill building", "mentorship", "networking", "career resources", "job search", "career planning"]
            },
            {
                "note_id": "800_Ressources/110_Career/How to get promoted",
                "path": "800_Ressources/110_Career/How to get promoted.md",
                "ai_summary": "Practical strategies and insights on advancing in your career, including visibility tactics, skill development, and organizational politics navigation.",
                "ai_hashtags": ["#career", "#business", "#personal"],
                "ai_keywords": ["promotion strategies", "career advancement", "workplace visibility", "skill development", "office politics", "performance reviews", "leadership", "professional growth"]
            }
        ]
    }

def analyze_batch_9():
    return {
        "summaries": [
            {
                "note_id": "800_Ressources/110_Career/How to write a Resume",
                "path": "800_Ressources/110_Career/How to write a Resume.md",
                "ai_summary": "Comprehensive guide on crafting an effective resume, including formatting tips, content strategies, and common mistakes to avoid.",
                "ai_hashtags": ["#career", "#writing", "#education"],
                "ai_keywords": ["resume writing", "CV tips", "job application", "professional formatting", "career documents", "ATS optimization", "employment", "job search"]
            },
            {
                "note_id": "800_Ressources/110_Career/Negotiation",
                "path": "800_Ressources/110_Career/Negotiation.md",
                "ai_summary": "Strategies and techniques for successful negotiation in professional contexts, including salary negotiations and business deals.",
                "ai_hashtags": ["#career", "#business", "#personal"],
                "ai_keywords": ["negotiation tactics", "salary negotiation", "business deals", "communication skills", "bargaining", "win-win solutions", "professional skills"]
            },
            {
                "note_id": "800_Ressources/110_Career/Networking",
                "path": "800_Ressources/110_Career/Networking.md",
                "ai_summary": "Guide to professional networking, including strategies for building meaningful connections, maintaining relationships, and leveraging networks for career growth.",
                "ai_hashtags": ["#career", "#business", "#personal"],
                "ai_keywords": ["professional networking", "relationship building", "career connections", "LinkedIn", "networking events", "social capital", "career opportunities"]
            },
            {
                "note_id": "800_Ressources/AI/GPT Prompt Examples",
                "path": "800_Ressources/AI/GPT Prompt Examples.md",
                "ai_summary": "A collection of effective GPT prompt examples and templates for various use cases, demonstrating best practices in prompt engineering.",
                "ai_hashtags": ["#AI", "#technology", "#productivity"],
                "ai_keywords": ["GPT prompts", "prompt engineering", "AI interaction", "ChatGPT", "prompt templates", "AI optimization", "language models", "effective prompting"]
            },
            {
                "note_id": "800_Ressources/AI/Stable Diffusion Resources",
                "path": "800_Ressources/AI/Stable Diffusion Resources.md",
                "ai_summary": "Curated resources for using Stable Diffusion, including guides, tools, models, and artistic techniques for AI image generation.",
                "ai_hashtags": ["#AI", "#technology", "#creativity"],
                "ai_keywords": ["Stable Diffusion", "AI art", "image generation", "diffusion models", "creative AI", "prompt crafting", "model fine-tuning", "AI resources"]
            }
        ]
    }

# Save all batch analyses
batches = [
    (3, analyze_batch_3()),
    (4, analyze_batch_4()),
    (5, analyze_batch_5()),
    (6, analyze_batch_6()),
    (7, analyze_batch_7()),
    (8, analyze_batch_8()),
    (9, analyze_batch_9())
]

for batch_num, data in batches:
    filename = f"ai_summary_batches/batch_{batch_num:03d}_response.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Created {filename}")

print("\nAll batch responses generated!")
print("Now import them with:")
print("for i in {3..9}; do python3 manual_summary_helper.py save ai_summary_batches/batch_00${i}_response.json; done")
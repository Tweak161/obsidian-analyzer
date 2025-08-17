#!/usr/bin/env python3
"""Create all remaining AI summaries"""
import json
import os

# All remaining summaries for batches 4-10
all_batches = {
    "batch_4": [
        {
            "note_id": "800_Ressources/103_PKM/Second Brain, PKMS - LATCH System - How to find Notes",
            "ai_summary": "Explains the LATCH system (Location, Alphabet, Time, Category, Hierarchy) for organizing and finding notes effectively in a knowledge management system.",
            "ai_hashtags": ["#productivity", "#education", "#technology"],
            "ai_keywords": ["LATCH system", "note finding", "organization", "information architecture", "search strategies", "PKM", "categorization", "hierarchy", "retrieval", "Richard Saul Wurman"]
        },
        {
            "note_id": "800_Ressources/103_PKM/Second Brain, PKMS - Principles",
            "ai_summary": "Core principles for building and maintaining an effective second brain and personal knowledge management system.",
            "ai_hashtags": ["#productivity", "#education", "#personal"],
            "ai_keywords": ["second brain principles", "PKM principles", "best practices", "system design", "knowledge management", "effectiveness", "sustainability", "workflow", "organization", "learning"]
        },
        {
            "note_id": "800_Ressources/103_PKM/Shape your Digital and Physical Environments - They shape your Thinking and therefore your Life (Cathedral Effect)",
            "ai_summary": "Explores how digital and physical environments influence thinking patterns and life outcomes, referencing the cathedral effect in cognitive psychology.",
            "ai_hashtags": ["#psychology", "#productivity", "#personal", "#philosophy"],
            "ai_keywords": ["cathedral effect", "environment design", "cognitive influence", "digital environment", "physical space", "thinking patterns", "productivity", "psychology", "workspace", "mental clarity"]
        },
        {
            "note_id": "800_Ressources/103_PKM/The Power of IPs (Intermediate Packets) - Building Blocks to Boost your Productivity",
            "ai_summary": "Discusses the concept of Intermediate Packets as reusable units of work that can be combined to create larger projects and boost productivity.",
            "ai_hashtags": ["#productivity", "#education", "#creativity"],
            "ai_keywords": ["intermediate packets", "productivity", "building blocks", "reusable work", "modular creation", "Tiago Forte", "creative process", "efficiency", "knowledge assets", "compound effect"]
        },
        {
            "note_id": "800_Ressources/103_PKM/Visual-Note-Taking.excalidraw",
            "ai_summary": "Visual guide or examples of visual note-taking techniques and methods for better information retention and understanding.",
            "ai_hashtags": ["#education", "#creativity", "#productivity"],
            "ai_keywords": ["visual note-taking", "sketchnotes", "visual thinking", "drawing", "information design", "memory", "creativity", "learning techniques", "visual communication", "retention"]
        },
        {
            "note_id": "800_Ressources/104_Buddhism/5 Feinde der Meditation",
            "ai_summary": "Describes the five enemies or hindrances of meditation practice in Buddhist tradition that obstruct mental clarity and progress.",
            "ai_hashtags": ["#meditation", "#spirituality", "#buddhism"],
            "ai_keywords": ["meditation hindrances", "five enemies", "Buddhist meditation", "obstacles", "mental barriers", "practice challenges", "mindfulness", "concentration", "spiritual practice", "self-awareness"]
        },
        {
            "note_id": "800_Ressources/104_Buddhism/5 Freunde der Meditation",
            "ai_summary": "Explains the five friends or supportive factors of meditation that help practitioners develop and deepen their practice.",
            "ai_hashtags": ["#meditation", "#spirituality", "#buddhism"],
            "ai_keywords": ["meditation supports", "five friends", "Buddhist practice", "positive factors", "mental cultivation", "mindfulness aids", "concentration", "spiritual growth", "practice enhancers", "mental training"]
        },
        {
            "note_id": "800_Ressources/104_Buddhism/Buddhismus - Drei Daseinsmerkmale",
            "ai_summary": "Explores the Three Marks of Existence (Trilakshana) in Buddhism: impermanence (anicca), suffering (dukkha), and non-self (anatta).",
            "ai_hashtags": ["#buddhism", "#philosophy", "#spirituality"],
            "ai_keywords": ["three marks", "Trilakshana", "impermanence", "suffering", "non-self", "anicca", "dukkha", "anatta", "Buddhist philosophy", "existence characteristics"]
        },
        {
            "note_id": "800_Ressources/104_Buddhism/Buddhismus 10 Tugenden aka Paramis",
            "ai_summary": "Details the ten perfections (Paramis) in Buddhism that practitioners cultivate on the path to enlightenment.",
            "ai_hashtags": ["#buddhism", "#spirituality", "#personal"],
            "ai_keywords": ["Paramis", "ten perfections", "Buddhist virtues", "spiritual qualities", "generosity", "morality", "patience", "wisdom", "enlightenment path", "character development"]
        },
        {
            "note_id": "800_Ressources/104_Buddhism/MOC - Meditation.excalidraw",
            "ai_summary": "Map of Content organizing various meditation-related notes, techniques, and Buddhist teachings.",
            "ai_hashtags": ["#moc", "#meditation", "#spirituality", "#buddhism"],
            "ai_keywords": ["meditation map", "content organization", "Buddhist practices", "meditation techniques", "spiritual teachings", "mindfulness", "contemplative practices", "wisdom traditions", "practice overview", "learning path"]
        }
    ],
    "batch_5": [
        {
            "note_id": "800_Ressources/104_Buddhism/Meditation Techniques - Comparison.excalidraw",
            "ai_summary": "Visual comparison of different meditation techniques, their characteristics, benefits, and applications.",
            "ai_hashtags": ["#meditation", "#spirituality", "#education"],
            "ai_keywords": ["meditation comparison", "techniques", "mindfulness", "concentration", "vipassana", "samatha", "practice methods", "benefits", "applications", "selection guide"]
        },
        {
            "note_id": "800_Ressources/104_Buddhism/Meditation Techniques.excalidraw",
            "ai_summary": "Overview of various meditation techniques and practices from different traditions.",
            "ai_hashtags": ["#meditation", "#spirituality", "#health"],
            "ai_keywords": ["meditation techniques", "practice methods", "mindfulness", "breathing", "visualization", "body scan", "loving-kindness", "concentration", "awareness", "spiritual practices"]
        },
        {
            "note_id": "800_Ressources/104_Buddhism/The Mind Illuminated (Culadasa John Yates).excalidraw",
            "ai_summary": "Visual summary of 'The Mind Illuminated' by Culadasa (John Yates), a comprehensive meditation manual combining Buddhist wisdom with brain science.",
            "ai_hashtags": ["#book", "#meditation", "#science", "#spirituality"],
            "ai_keywords": ["Mind Illuminated", "Culadasa", "John Yates", "meditation stages", "concentration", "mindfulness", "neuroscience", "Buddhist meditation", "systematic practice", "consciousness"]
        },
        {
            "note_id": "800_Ressources/104_Buddhism/Vipassana 10 Tages Kurs in Triebel Restored",
            "ai_summary": "Personal notes or experiences from a 10-day Vipassana meditation retreat in Triebel.",
            "ai_hashtags": ["#meditation", "#spirituality", "#personal", "#journal"],
            "ai_keywords": ["Vipassana retreat", "10-day course", "Triebel", "meditation experience", "silent retreat", "Goenka tradition", "insight meditation", "personal journey", "spiritual practice", "transformation"]
        },
        {
            "note_id": "800_Ressources/104_Buddhism/Vipassana Meditation Technique",
            "ai_summary": "Detailed explanation of the Vipassana (insight) meditation technique, its principles, and practice methods.",
            "ai_hashtags": ["#meditation", "#spirituality", "#buddhism"],
            "ai_keywords": ["Vipassana", "insight meditation", "body sensations", "impermanence", "equanimity", "awareness", "Buddhist technique", "mental purification", "liberation", "mindfulness"]
        },
        {
            "note_id": "800_Ressources/105_Dating/Models - Mark Manson.excalidraw",
            "ai_summary": "Visual summary of Mark Manson's book 'Models' about authentic attraction and honest communication in dating and relationships.",
            "ai_hashtags": ["#book", "#relationship", "#personal", "#psychology"],
            "ai_keywords": ["Models", "Mark Manson", "dating", "authenticity", "vulnerability", "attraction", "honest communication", "self-improvement", "relationships", "emotional connection"]
        },
        {
            "note_id": "800_Ressources/105_Dating/Women are from Venus Men are from Mars.excalidraw",
            "ai_summary": "Visual notes on the classic relationship book exploring gender differences in communication and emotional needs.",
            "ai_hashtags": ["#book", "#relationship", "#psychology"],
            "ai_keywords": ["Men Mars Women Venus", "John Gray", "gender differences", "communication", "relationships", "emotional needs", "understanding", "partnership", "love languages", "conflict resolution"]
        },
        {
            "note_id": "800_Ressources/106_Trading/BoaP - Fooled by Randomness (Nassim Taleb).excalidraw",
            "ai_summary": "Visual summary of Nassim Taleb's 'Fooled by Randomness' exploring how randomness and luck impact success, trading, and life decisions.",
            "ai_hashtags": ["#book", "#finance", "#philosophy", "#business"],
            "ai_keywords": ["Fooled by Randomness", "Nassim Taleb", "probability", "luck", "randomness", "trading", "cognitive biases", "Black Swan", "risk assessment", "decision making"]
        },
        {
            "note_id": "800_Ressources/106_Trading/BoaP - Save Haven (Mark Spitznagel).excalidraw",
            "ai_summary": "Visual notes on Mark Spitznagel's 'Safe Haven' about tail-risk hedging strategies and capital preservation in investing.",
            "ai_hashtags": ["#book", "#finance", "#business"],
            "ai_keywords": ["Safe Haven", "Mark Spitznagel", "tail risk", "hedging", "capital preservation", "investing strategy", "risk management", "portfolio protection", "Austrian economics", "Universa"]
        },
        {
            "note_id": "800_Ressources/106_Trading/BoaP - The Bitcoin Standard.excalidraw",
            "ai_summary": "Visual summary of 'The Bitcoin Standard' exploring Bitcoin's role as digital gold and its implications for the future of money.",
            "ai_hashtags": ["#book", "#finance", "#technology", "#business"],
            "ai_keywords": ["Bitcoin Standard", "Saifedean Ammous", "cryptocurrency", "digital gold", "monetary history", "sound money", "Austrian economics", "decentralization", "blockchain", "inflation"]
        }
    ],
    "batch_6": [
        {
            "note_id": "800_Ressources/106_Trading/BoaP - The Black Swan (Nassim Taleb).excalidraw",
            "ai_summary": "Visual summary of Nassim Taleb's 'The Black Swan' about highly improbable events with massive impact and our inability to predict them.",
            "ai_hashtags": ["#book", "#finance", "#philosophy", "#science"],
            "ai_keywords": ["Black Swan", "Nassim Taleb", "unpredictability", "extreme events", "risk", "uncertainty", "antifragility", "probability", "forecasting failures", "complexity"]
        },
        {
            "note_id": "800_Ressources/106_Trading/Fooled by Randomness - Pascal's Wager - Take a Chance if there is a high Payoff and a small Risk",
            "ai_summary": "Explores Pascal's Wager concept from 'Fooled by Randomness' about making decisions with asymmetric payoffs where potential gains far exceed risks.",
            "ai_hashtags": ["#philosophy", "#finance", "#personal"],
            "ai_keywords": ["Pascal's Wager", "asymmetric payoffs", "risk-reward", "decision making", "probability", "expected value", "Taleb", "rationality", "betting", "opportunity cost"]
        },
        {
            "note_id": "800_Ressources/106_Trading/Fooled by Randomness - Skewness and Expectation vs Probability",
            "ai_summary": "Explains the concept of skewness in probability distributions and why expected value matters more than probability of success in decision-making.",
            "ai_hashtags": ["#finance", "#science", "#education"],
            "ai_keywords": ["skewness", "expectation", "probability", "expected value", "risk assessment", "statistics", "decision theory", "payoff asymmetry", "trading strategy", "mathematical finance"]
        },
        {
            "note_id": "800_Ressources/106_Trading/Fooled by Randomness - Survivorship Bias",
            "ai_summary": "Details survivorship bias - the logical error of focusing on survivors while overlooking failures, leading to false conclusions about success factors.",
            "ai_hashtags": ["#finance", "#psychology", "#science"],
            "ai_keywords": ["survivorship bias", "selection bias", "statistical fallacy", "invisible failures", "success analysis", "data interpretation", "cognitive bias", "investment returns", "historical analysis", "decision making"]
        },
        {
            "note_id": "800_Ressources/106_Trading/Fooled by Randomness - The Black Swan Problem",
            "ai_summary": "Explores the Black Swan problem - our inability to predict rare, high-impact events and tendency to rationalize them after they occur.",
            "ai_hashtags": ["#finance", "#philosophy", "#science"],
            "ai_keywords": ["Black Swan problem", "rare events", "unpredictability", "narrative fallacy", "hindsight bias", "risk management", "uncertainty", "Taleb", "extreme outcomes", "forecasting"]
        },
        {
            "note_id": "800_Ressources/107_Self_Improvement/7 Habits for Highly Effective People - Stimulus Response Freedom Quote",
            "ai_summary": "Highlights Viktor Frankl's concept referenced in Covey's work: between stimulus and response lies our freedom to choose our reaction.",
            "ai_hashtags": ["#personal", "#psychology", "#philosophy"],
            "ai_keywords": ["stimulus response", "freedom to choose", "Viktor Frankl", "Stephen Covey", "personal responsibility", "emotional intelligence", "self-awareness", "proactivity", "mindfulness", "choice"]
        },
        {
            "note_id": "800_Ressources/107_Self_Improvement/7 Habits of Highly Effective People - Habit 1 - Be Proactive",
            "ai_summary": "Details the first habit from Stephen Covey's book about taking responsibility for your life and focusing on what you can control.",
            "ai_hashtags": ["#book", "#personal", "#productivity", "#psychology"],
            "ai_keywords": ["proactivity", "responsibility", "circle of influence", "circle of concern", "Stephen Covey", "personal effectiveness", "self-determination", "response-ability", "initiative", "empowerment"]
        },
        {
            "note_id": "800_Ressources/107_Self_Improvement/7 Habits of Highly Effective People - Habit 2 - Beginn with the End in Mind_",
            "ai_summary": "Explains the second habit about defining your life mission and values before taking action, using visualization and personal mission statements.",
            "ai_hashtags": ["#book", "#personal", "#productivity", "#philosophy"],
            "ai_keywords": ["begin with end", "personal mission", "vision", "values", "life purpose", "mental creation", "leadership", "goal setting", "visualization", "legacy thinking"]
        },
        {
            "note_id": "800_Ressources/107_Self_Improvement/7 Habits of Highly Effective People - Habit 3 - Put First Things First",
            "ai_summary": "Covers the third habit about time management and prioritization using the urgent/important matrix to focus on what matters most.",
            "ai_hashtags": ["#book", "#productivity", "#personal", "#business"],
            "ai_keywords": ["prioritization", "time management", "urgent important matrix", "Quadrant II", "effectiveness", "scheduling", "delegation", "focus", "discipline", "execution"]
        },
        {
            "note_id": "800_Ressources/107_Self_Improvement/7 Habits of Highly Effective People - Habit 4 - Think WinWin",
            "ai_summary": "Describes the fourth habit about seeking mutually beneficial solutions in relationships and negotiations rather than zero-sum thinking.",
            "ai_hashtags": ["#book", "#relationship", "#business", "#personal"],
            "ai_keywords": ["win-win", "mutual benefit", "abundance mentality", "collaboration", "negotiation", "relationships", "interdependence", "trust", "emotional bank account", "synergy"]
        }
    ],
    "batch_7": [
        {
            "note_id": "800_Ressources/107_Self_Improvement/7 Habits of Highly Effective People - Habit 5 - First Understand",
            "ai_summary": "Explains the fifth habit about empathic listening - seeking first to understand others before trying to be understood.",
            "ai_hashtags": ["#book", "#relationship", "#personal", "#psychology"],
            "ai_keywords": ["empathic listening", "understanding", "communication", "emotional intelligence", "active listening", "empathy", "perspective taking", "relationship building", "influence", "trust"]
        },
        {
            "note_id": "800_Ressources/107_Self_Improvement/7 Habits of Highly Effective People - Habit 6 - Synergize_",
            "ai_summary": "Details the sixth habit about creative cooperation where the whole becomes greater than the sum of its parts through valuing differences.",
            "ai_hashtags": ["#book", "#relationship", "#creativity", "#business"],
            "ai_keywords": ["synergy", "creative cooperation", "teamwork", "diversity", "innovation", "collaboration", "third alternative", "value differences", "collective intelligence", "breakthrough solutions"]
        },
        {
            "note_id": "800_Ressources/107_Self_Improvement/7 Habits of Highly Effective People - Habit 7 - Sharpen the Saw",
            "ai_summary": "Covers the seventh habit about continuous self-renewal in four dimensions: physical, mental, emotional/social, and spiritual.",
            "ai_hashtags": ["#book", "#personal", "#health", "#spirituality"],
            "ai_keywords": ["self-renewal", "sharpen the saw", "continuous improvement", "balance", "physical fitness", "mental development", "emotional intelligence", "spiritual growth", "sustainability", "personal maintenance"]
        },
        {
            "note_id": "800_Ressources/107_Self_Improvement/7 Habits of Highly Effective People - Private Victory",
            "ai_summary": "Explains the concept of Private Victory - mastering habits 1-3 to achieve independence and self-mastery before pursuing interdependence.",
            "ai_hashtags": ["#book", "#personal", "#productivity", "#psychology"],
            "ai_keywords": ["private victory", "independence", "self-mastery", "personal effectiveness", "habits 1-3", "proactivity", "vision", "prioritization", "character development", "inside-out approach"]
        },
        {
            "note_id": "800_Ressources/107_Self_Improvement/7 Habits of Highly Effective People - Public Victory",
            "ai_summary": "Describes Public Victory - achieving interdependence through habits 4-6 after establishing personal independence.",
            "ai_hashtags": ["#book", "#relationship", "#business", "#personal"],
            "ai_keywords": ["public victory", "interdependence", "relationship effectiveness", "habits 4-6", "win-win", "understanding", "synergy", "collaboration", "leadership", "influence"]
        },
        {
            "note_id": "800_Ressources/107_Self_Improvement/BoaP - 4000 Weeks (Oliver Burkeman).excalidraw",
            "ai_summary": "Visual summary of Oliver Burkeman's '4000 Weeks' about embracing life's limitations and finding meaning in our finite time.",
            "ai_hashtags": ["#book", "#philosophy", "#personal", "#productivity"],
            "ai_keywords": ["4000 Weeks", "Oliver Burkeman", "mortality", "time management", "finitude", "acceptance", "meaningful life", "productivity paradox", "existential", "life priorities"]
        },
        {
            "note_id": "800_Ressources/107_Self_Improvement/BoaP - 7 Habits of Highly Effective People Overview.excalidraw",
            "ai_summary": "Visual overview of all seven habits from Stephen Covey's classic book on personal and interpersonal effectiveness.",
            "ai_hashtags": ["#book", "#personal", "#productivity", "#business"],
            "ai_keywords": ["7 Habits", "Stephen Covey", "effectiveness", "personal development", "leadership", "character ethics", "principles", "paradigm shift", "maturity continuum", "interdependence"]
        },
        {
            "note_id": "800_Ressources/107_Self_Improvement/BoaP - Deep Work (Cal Newport).excalidraw",
            "ai_summary": "Visual summary of Cal Newport's 'Deep Work' about cultivating focused work in a distracted world for professional success.",
            "ai_hashtags": ["#book", "#productivity", "#career", "#personal"],
            "ai_keywords": ["Deep Work", "Cal Newport", "focus", "concentration", "productivity", "distraction", "knowledge work", "deliberate practice", "flow state", "professional development"]
        },
        {
            "note_id": "800_Ressources/107_Self_Improvement/Brianna Wiest - 101 Essays, die dein Leben verändern werden.excalidraw",
            "ai_summary": "Visual notes on Brianna Wiest's collection of transformative essays about self-discovery, healing, and personal growth.",
            "ai_hashtags": ["#book", "#personal", "#psychology", "#spirituality"],
            "ai_keywords": ["Brianna Wiest", "101 Essays", "self-discovery", "personal growth", "healing", "emotional intelligence", "life lessons", "transformation", "self-awareness", "wisdom"]
        },
        {
            "note_id": "800_Ressources/107_Self_Improvement/Bullshit Jobs - David Graeber.excalidraw",
            "ai_summary": "Visual summary of David Graeber's 'Bullshit Jobs' critiquing meaningless work and its psychological and social impacts.",
            "ai_hashtags": ["#book", "#business", "#career", "#philosophy"],
            "ai_keywords": ["Bullshit Jobs", "David Graeber", "meaningless work", "capitalism critique", "work psychology", "job satisfaction", "social value", "bureaucracy", "modern employment", "purpose"]
        }
    ],
    "batch_8": [
        {
            "note_id": "800_Ressources/107_Self_Improvement/David Burns - Feeling Great.excalidraw",
            "ai_summary": "Visual notes on David Burns' 'Feeling Great' about cognitive behavioral therapy techniques and the TEAM approach to overcoming depression and anxiety.",
            "ai_hashtags": ["#book", "#psychology", "#health", "#personal"],
            "ai_keywords": ["David Burns", "Feeling Great", "CBT", "TEAM therapy", "cognitive distortions", "depression", "anxiety", "mental health", "thought patterns", "emotional healing"]
        },
        {
            "note_id": "800_Ressources/107_Self_Improvement/Energy Investment Portfolio - Do Less",
            "ai_summary": "Explores the concept of managing personal energy like an investment portfolio, advocating for doing less but with greater focus and impact.",
            "ai_hashtags": ["#productivity", "#personal", "#health"],
            "ai_keywords": ["energy management", "portfolio approach", "focus", "essentialism", "burnout prevention", "sustainable productivity", "priorities", "work-life balance", "effectiveness", "minimalism"]
        },
        {
            "note_id": "800_Ressources/107_Self_Improvement/Feel Good Productiity - The Long Term Horizon - The Eulogy Method",
            "ai_summary": "Discusses the eulogy method from 'Feel Good Productivity' for aligning daily actions with long-term values and legacy.",
            "ai_hashtags": ["#productivity", "#personal", "#philosophy"],
            "ai_keywords": ["eulogy method", "long-term thinking", "values alignment", "legacy", "life purpose", "productivity", "meaning", "perspective", "mortality awareness", "goal setting"]
        },
        {
            "note_id": "800_Ressources/107_Self_Improvement/Feel Good Productivity (Ali Abdaal).excalidraw",
            "ai_summary": "Visual summary of Ali Abdaal's 'Feel Good Productivity' about achieving more by enjoying the process and reducing friction.",
            "ai_hashtags": ["#book", "#productivity", "#personal", "#psychology"],
            "ai_keywords": ["Feel Good Productivity", "Ali Abdaal", "enjoyment", "motivation", "productivity systems", "positive psychology", "flow", "sustainable work", "creativity", "well-being"]
        },
        {
            "note_id": "800_Ressources/107_Self_Improvement/Four Thousand Weeks - Oliver Burkeman.excalidraw",
            "ai_summary": "Visual notes on embracing finitude and making peace with limited time to live a more meaningful life.",
            "ai_hashtags": ["#book", "#philosophy", "#personal", "#productivity"],
            "ai_keywords": ["Four Thousand Weeks", "Oliver Burkeman", "time limitations", "mortality", "acceptance", "meaningful choices", "productivity culture", "existential wisdom", "presence", "letting go"]
        },
        {
            "note_id": "800_Ressources/107_Self_Improvement/From Strength to Strength - Arthur Brooks.excalidraw",
            "ai_summary": "Visual summary of Arthur Brooks' book about finding success and happiness in the second half of life through different strengths.",
            "ai_hashtags": ["#book", "#personal", "#career", "#spirituality"],
            "ai_keywords": ["Arthur Brooks", "second half life", "fluid intelligence", "crystallized intelligence", "career transition", "wisdom", "happiness", "aging well", "purpose", "fulfillment"]
        },
        {
            "note_id": "800_Ressources/107_Self_Improvement/Impulse Control and Breaking bad Habits",
            "ai_summary": "Strategies and techniques for improving impulse control and breaking destructive habits through understanding triggers and building better routines.",
            "ai_hashtags": ["#psychology", "#personal", "#health"],
            "ai_keywords": ["impulse control", "habit breaking", "self-control", "triggers", "behavior change", "willpower", "addiction", "routine building", "neuroplasticity", "discipline"]
        },
        {
            "note_id": "800_Ressources/107_Self_Improvement/KISS - Keep It Simple and Stupid.excalidraw",
            "ai_summary": "Visual representation of the KISS principle - advocating for simplicity in design, communication, and problem-solving.",
            "ai_hashtags": ["#productivity", "#business", "#creativity"],
            "ai_keywords": ["KISS principle", "simplicity", "design philosophy", "complexity reduction", "clarity", "efficiency", "minimalism", "problem solving", "communication", "elegance"]
        },
        {
            "note_id": "800_Ressources/107_Self_Improvement/MOC - Learning",
            "ai_summary": "Map of Content organizing notes about learning techniques, strategies, and educational philosophies.",
            "ai_hashtags": ["#moc", "#education", "#personal"],
            "ai_keywords": ["learning map", "education", "study techniques", "memory", "skill acquisition", "metacognition", "learning strategies", "knowledge retention", "educational methods", "cognitive science"]
        },
        {
            "note_id": "800_Ressources/107_Self_Improvement/MOC - Self Improvement",
            "ai_summary": "Map of Content organizing various self-improvement topics including habits, productivity, psychology, and personal development resources.",
            "ai_hashtags": ["#moc", "#personal", "#productivity", "#psychology"],
            "ai_keywords": ["self-improvement map", "personal development", "growth mindset", "habits", "productivity", "psychology", "life skills", "success principles", "transformation", "resources"]
        }
    ],
    "batch_9": [
        {
            "note_id": "800_Ressources/107_Self_Improvement/Mastering the Core Teachings of Buddha - Daniel Ingram.excalidraw",
            "ai_summary": "Visual summary of Daniel Ingram's pragmatic guide to Buddhist meditation, focusing on practical techniques for achieving enlightenment.",
            "ai_hashtags": ["#book", "#meditation", "#spirituality", "#buddhism"],
            "ai_keywords": ["Daniel Ingram", "MCTB", "pragmatic dharma", "enlightenment", "meditation maps", "insight stages", "concentration", "awakening", "Buddhist practice", "technical meditation"]
        },
        {
            "note_id": "800_Ressources/107_Self_Improvement/Power of Thinking Small",
            "ai_summary": "Explores how breaking down big goals into small, manageable steps leads to greater success and sustained motivation.",
            "ai_hashtags": ["#productivity", "#personal", "#psychology"],
            "ai_keywords": ["thinking small", "micro-habits", "incremental progress", "goal achievement", "motivation", "compound effect", "sustainable change", "small wins", "behavior design", "momentum"]
        },
        {
            "note_id": "800_Ressources/107_Self_Improvement/Victor Frankle - Logotherapy - Relation between Purpose and Mental Illness",
            "ai_summary": "Examines Viktor Frankl's logotherapy and the connection between finding life purpose and mental health, based on his Holocaust experiences.",
            "ai_hashtags": ["#psychology", "#philosophy", "#health", "#personal"],
            "ai_keywords": ["Viktor Frankl", "logotherapy", "meaning", "purpose", "mental health", "Holocaust survivor", "existential therapy", "will to meaning", "suffering", "resilience"]
        },
        {
            "note_id": "800_Ressources/108_Lifestyle_Business/Business Startup Ideas",
            "ai_summary": "Collection of business startup ideas focused on lifestyle businesses that provide freedom and flexibility while generating income.",
            "ai_hashtags": ["#business", "#career", "#personal"],
            "ai_keywords": ["startup ideas", "lifestyle business", "entrepreneurship", "passive income", "location independence", "online business", "solopreneurship", "business models", "freedom", "flexibility"]
        },
        {
            "note_id": "800_Ressources/109_Literatur/Das Schloss (Franz Kafka)",
            "ai_summary": "Notes on Franz Kafka's 'The Castle', exploring themes of bureaucracy, alienation, and the individual's struggle against incomprehensible systems.",
            "ai_hashtags": ["#book", "#philosophy", "#writing"],
            "ai_keywords": ["Franz Kafka", "Das Schloss", "The Castle", "bureaucracy", "alienation", "existentialism", "absurdity", "power structures", "modernism", "German literature"]
        },
        {
            "note_id": "800_Ressources/109_Literatur/Franz Kafka",
            "ai_summary": "Overview of Franz Kafka's life, work, and literary significance in exploring themes of alienation, guilt, and existential anxiety.",
            "ai_hashtags": ["#writing", "#philosophy", "#personal"],
            "ai_keywords": ["Franz Kafka", "literature", "existentialism", "alienation", "bureaucracy", "metamorphosis", "absurdism", "modernist literature", "anxiety", "human condition"]
        },
        {
            "note_id": "800_Ressources/110_Career/2024 Analysis of current and future Market - Which Skills are needed to thrive as an employee or Entrepreneur",
            "ai_summary": "Analysis of market trends and essential skills for success in 2024, covering both employment and entrepreneurship perspectives.",
            "ai_hashtags": ["#career", "#business", "#education", "#technology"],
            "ai_keywords": ["market analysis 2024", "future skills", "career planning", "entrepreneurship", "AI impact", "digital skills", "adaptability", "continuous learning", "market trends", "professional development"]
        },
        {
            "note_id": "800_Ressources/110_Career/Ehrliche Meinung - In 3 Jahren Programmierer ueberfluessig (Morpheus Tutorial)",
            "ai_summary": "Discussion about the potential obsolescence of programmers within 3 years due to AI advancement, from Morpheus Tutorial's perspective.",
            "ai_hashtags": ["#programming", "#AI", "#career", "#technology"],
            "ai_keywords": ["programming future", "AI replacement", "career disruption", "software development", "automation", "skill adaptation", "technology trends", "job market", "AI coding", "career pivot"]
        },
        {
            "note_id": "800_Ressources/110_Career/Finde dein Passion - Knowing when to Quit.excalidraw",
            "ai_summary": "Visual exploration of finding your passion and recognizing when it's time to quit and pursue new directions in career and life.",
            "ai_hashtags": ["#career", "#personal", "#philosophy"],
            "ai_keywords": ["finding passion", "quitting strategically", "career change", "self-discovery", "decision making", "life transitions", "purpose", "fulfillment", "courage", "new beginnings"]
        },
        {
            "note_id": "800_Ressources/110_Career/Finde dein Passion - Knowing when to Quit",
            "ai_summary": "Detailed notes on identifying true passions and making strategic decisions about when to persist and when to change direction.",
            "ai_hashtags": ["#career", "#personal", "#psychology"],
            "ai_keywords": ["passion discovery", "strategic quitting", "career decisions", "self-awareness", "life changes", "persistence", "pivot points", "fulfillment", "authenticity", "growth"]
        }
    ],
    "batch_10": [
        {
            "note_id": "800_Ressources/110_Career/Karriereplanung_2025.excalidraw",
            "ai_summary": "Visual career planning for 2025, outlining goals, strategies, and action steps for professional development.",
            "ai_hashtags": ["#career", "#personal", "#productivity"],
            "ai_keywords": ["career planning 2025", "professional goals", "strategic planning", "skill development", "career roadmap", "objectives", "action plan", "growth strategy", "milestone planning", "future vision"]
        },
        {
            "note_id": "800_Ressources/AI/MOC - AI",
            "ai_summary": "Map of Content organizing notes about artificial intelligence, machine learning, and their applications and implications.",
            "ai_hashtags": ["#moc", "#AI", "#technology", "#education"],
            "ai_keywords": ["AI map", "artificial intelligence", "machine learning", "technology overview", "AI applications", "future technology", "innovation", "knowledge organization", "tech resources", "learning path"]
        },
        {
            "note_id": "800_Ressources/AI/We are guided by Algorithms in the way we see and perceive of the world_",
            "ai_summary": "Explores how algorithms shape our worldview, influence decisions, and filter our perception of reality in the digital age.",
            "ai_hashtags": ["#AI", "#philosophy", "#technology", "#psychology"],
            "ai_keywords": ["algorithms", "perception", "filter bubble", "digital influence", "worldview", "echo chambers", "recommendation systems", "cognitive bias", "information diet", "reality shaping"]
        }
    ]
}

# Save all batches
for batch_name, summaries in all_batches.items():
    with open(f'{batch_name}_summaries.json', 'w') as f:
        json.dump({"summaries": summaries}, f, indent=2)
    print(f"Created {batch_name}_summaries.json")

# Process all summaries
os.system("python3 process_all_ai_summaries.py")
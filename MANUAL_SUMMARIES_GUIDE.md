# Manual AI Summaries Guide (No API Key Required)

If you don't want to use an API key, you can generate AI summaries manually through your Claude conversation using the helper script.

## How It Works

1. The script prepares prompts with your note content
2. You paste these prompts into your Claude conversation (like this one)
3. Claude generates summaries for your notes
4. You save Claude's response and import it back

## Step-by-Step Process

### 1. Generate Prompts for Your Notes

```bash
# Generate prompts for 5 notes at a time from 800_Ressources
python3 manual_summary_helper.py generate 800_Ressources 5

# Or process 10 notes at a time
python3 manual_summary_helper.py generate 800_Ressources 10
```

### 2. Copy and Paste

The script will show you prompts like this:
- Copy the entire prompt (between the dashed lines)
- Paste it into your Claude conversation
- Claude will analyze the notes and return JSON with summaries

### 3. Save Claude's Response

When Claude responds with JSON:
1. Copy the JSON response (everything between ```json and ```)
2. Save it to a file (e.g., `summaries.json`)
3. Import the summaries:

```bash
python3 manual_summary_helper.py save summaries.json
```

## Example Workflow

```bash
# Step 1: Generate prompts
$ python3 manual_summary_helper.py generate 800_Ressources 3
Found 15 notes in 800_Ressources without AI summaries

============================================================
BATCH 1 of 5
============================================================

Copy the following prompt and paste it into your Claude conversation:
------------------------------------------------------------
[Prompt will appear here]
------------------------------------------------------------

Press Enter to see the next batch...

# Step 2: Copy the prompt and paste into Claude

# Step 3: Save Claude's JSON response to a file
$ echo '[Claude's JSON response]' > batch1_summaries.json

# Step 4: Import the summaries
$ python3 manual_summary_helper.py save batch1_summaries.json
✓ Successfully updated 3 notes with AI summaries!
```

## Advantages of Manual Method

- **No API key required** - Use your existing Claude conversation
- **Full control** - Review summaries before saving
- **Cost-free** - Uses your regular Claude subscription
- **Flexible** - Can customize prompts or ask for clarification

## Tips

- Process 5-10 notes per batch for best results
- You can ask Claude to revise summaries if needed
- The JSON format must be exact for import to work
- All progress is saved, so you can work in multiple sessions

## Viewing Results

After importing summaries, restart the dashboard:
```bash
python3 run_analysis.py --dashboard-only
```

The AI summaries will appear in the dashboard just like API-generated ones!
import requests
import json
import logging
from config import OLLAMA_ENDPOINT, LLM_MODEL


def generate_summary(transcript):
    prompt = f"""
Here is a transcript to analyze:
<transcript>
{transcript}
</transcript>

You are an AI assistant tasked with summarizing discussions from an Automatic Speech Recognition (ASR) transcript. Your goal is to create concise, easily scannable summaries of each distinct discussion within the transcript.

ASR transcripts may have misheard words, here is a list of common names and terms that may be used in our transcripts but misheard by the processor:
Clara, Eleanor, Rachel, Wally, StarRez, Symplicity Advocate, Infor, SCLogic, TZ Lockers, SBU, Stony Brook University

For each distinct discussion you identify in the transcript, create a summary using the following format:

1. Use a ### header for the discussion title, followed by a brief description
2. Include the following sections, using emojis for quick visual scanning:
   - **SUMMARY:** A one-sentence overview
   - 👥 **WHO:** Number and identities (if inferrable) of participants
   - 🏢 **WHERE:** The setting or context of the discussion
   - ⏱️ **WHEN:** Date and time of the discussion. Use date from filename if not part of discussion.
   - 💬 **WHAT:** Key points, events, or decisions, using bullet points
   - 🔑 **HASHTAGS:** 3-5 important products, terms, or concepts mentioned
   - 📋 **TODO:** 3-5 actionable follow-up items (if applicable, not every discussion results in TODO items).

Identify distinct discussions based on topic changes, speaker transitions, or clear breaks in the conversation. If parts of the transcript are unclear or fragmented, focus on the most coherent and informative sections.

Present your summaries in order, enclosed within <summaries> tags. Use markdown formatting for readability. Here's an example of how a single summary should be structured:


### **SUMMARY:** One-sentence overview of the discussion
#️⃣ **HASHTAGS:** #Term1, #Term2, #Term3
👥 **WHO:** 
- Participant details
🏢 **WHERE:** Setting or context
⏱️ **WHEN:** Date/Time
💬 **WHAT:** 
- Key point 1
- Key point 2
- Key point 3
📋 **TODO:** 
- [ ] Action item 1
- [ ] Action item 2
- [ ] Action item 3

Remember to keep each summary concise and easily scannable, focusing on the most important information. If you encounter unclear or repetitive sections in the transcript, use your best judgment to summarize the main points and note any uncertainties.

"""
    payload = {
        "model": LLM_MODEL,
        "prompt": prompt,
        "stream": False,
        "context_size": 20000
    }
    try:
        response = requests.post(OLLAMA_ENDPOINT, json=payload, timeout=36000)
        response.raise_for_status()
        result = response.json()
        return result.get('response', "")
    except (requests.RequestException, json.JSONDecodeError) as e:
        logging.error(f"Error during LLM processing: {e}")
        return f"Error generating summary: {str(e)}"
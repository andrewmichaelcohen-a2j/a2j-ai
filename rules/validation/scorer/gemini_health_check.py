#!/usr/bin/env python3
"""
Quick Gemini + OpenAI health check before running the v0.2 scorer.
Run from the repo root:  python3 rules/validation/scorer/gemini_health_check.py
"""
import os, sys, json

def check_gemini():
    key = os.environ.get("GOOGLE_API_KEY", "")
    if not key:
        return "NO_KEY", "GOOGLE_API_KEY not set in environment"
    try:
        import google.generativeai as genai
        genai.configure(api_key=key)
        model = genai.GenerativeModel("gemini-2.5-pro")
        resp = model.generate_content("Reply with the single word WORKING and nothing else.")
        text = resp.text.strip() if hasattr(resp, "text") else str(resp)
        if "WORKING" in text.upper():
            return "OK", text
        return "UNEXPECTED", text
    except Exception as e:
        return "ERROR", str(e)

def check_openai():
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key:
        return "NO_KEY", "OPENAI_API_KEY not set in environment"
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        resp = client.chat.completions.create(
            model="gpt-5.5",
            messages=[{"role": "user", "content": "Reply with the single word WORKING and nothing else."}],
            max_completion_tokens=20,
        )
        text = resp.choices[0].message.content.strip()
        # GPT-5.5 is a reasoning model; accept any non-empty response as OK
        if text:
            return "OK", text[:60]
        return "UNEXPECTED", "(empty response)"
    except Exception as e:
        return "ERROR", str(e)

if __name__ == "__main__":
    print("=== API Health Check (pre-score gate) ===\n")
    g_status, g_msg = check_gemini()
    o_status, o_msg = check_openai()

    print(f"Gemini  2.5-pro : {g_status:12s}  {g_msg}")
    print(f"OpenAI  GPT-5.5 : {o_status:12s}  {o_msg}")

    print()
    both_ok = g_status == "OK" and o_status == "OK"
    if both_ok:
        print("✅  DUAL-MODEL-CONSENSUS gate MET — safe to run scorer.")
        print()
        print("Run the Stage 2 v0.2 score with:")
        print("  python3 rules/validation/scorer/ca_notice_scorer.py \\")
        print("    --golden rules/validation/scorer/FROZEN/goldenset_CA_notice_v0.2_20260701.xlsx \\")
        print("    --held-out-only")
        print()
        print("Then run the dev set:")
        print("  python3 rules/validation/scorer/ca_notice_scorer.py \\")
        print("    --golden rules/validation/scorer/FROZEN/goldenset_CA_notice_v0.2_20260701.xlsx \\")
        print("    --non-held-out-only")
    elif o_status == "OK" and g_status != "OK":
        print(f"⛔  Gemini NOT available ({g_status}: {g_msg}).")
        print("    Do NOT run the consensus scorer yet.")
        print("    A GPT-only PRELIMINARY run is permitted with the ⛔ banner — never cite as a result.")
    else:
        print("❌  One or both models unavailable. Do not score.")

    sys.exit(0 if both_ok else 1)

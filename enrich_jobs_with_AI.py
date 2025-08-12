import datetime
import os
import json
import time
from glob import glob
from openai import OpenAI
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector # Allows using XPath/Selectors on raw HTML like Scrapy
from scrapy.crawler import CrawlerProcess

#------------------------------------------------------------------------------------
# add credit for this api key
# put your api key here
# DON'T FORGET TO REMOVE YOUR API KEY BEFORE SHARING THIS CODE
os.environ["OPENAI_API_KEY"] = ""
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#------------------------------------------------------------------------------------


# Get required skills, years and citizenPR
def analyze_job_description(link):
    # --- If the link is empty or None, return blank values ---
    if not link:
        return {"Skills": "", "Years": "", "CitizenPR": ""}

    # Headless Selenium (Colab-compatible)
    service = Service(executable_path='/usr/bin/chromedriver')
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920x1080")
    # options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    d = webdriver.Chrome(service=service, options=options)
    try:
        d.get(link)
        time.sleep(5)
        sel = Selector(text=d.page_source)

        # --- Extract all text from <main> or <article> (where job description usually is) ---
        # if .strip() This filters out any strings that are empty after stripping spaces/newlines.
        # Most OpenAI's models expect a single string prompt, not a list, so we need to join a space between string by using " ".join
        text = " ".join(
            t.strip() for t in sel.xpath("//main//text() | //article//text()").getall() if t.strip()
        )
        # --- Cut the text if it's too long to save tokens ---
        text = text[:12000]

        # Ask OpenAI for compact, structured output (JSON)
        # using JSON when sending data to the API has two big benefits, Easier Parsing and Avoids Unnecessary Words(Save token)
        prompt = f"""
    You are a precise information extractor. Read the job description text below and return a STRICT JSON object with these keys:
    - "Skills": short, comma-separated list of the top required skills (max 8 items)
    - "Years": numeric years of experience required (e.g., "1-2", "3+", or "0")
    - "CitizenPR": "Y" if Canadian citizenship or Canadian permanent residence is explicitly required, otherwise "N".

    Return ONLY JSON, no commentary.

    Job Description:
    {text}
    """.strip()

        jd_model = "gpt-4o-mini"  # --TEST the differences between other models
        resp = client.responses.create(
            model=jd_model,
            input=prompt
        )
        json_data = resp.output_text.strip()

        # Try to parse JSON; if model adds extra text, we still try to recover
        # converts the text into a Python dictionary
        import json, re
        try:
            info = json.loads(json_data)
        except Exception:
            # crude fallback: extract JSON block if any
            m = re.search(r"\{.*\}", json_data, re.S)
            info = json.loads(m.group(0)) if m else {"Skills": "", "Years": "", "CitizenPR": ""}

        # Creates a brand new dictionary — even if info already has these keys, Normalize missing keys
        return {
            "Skills": (info.get("Skills") or "").strip(),
            "Years": (info.get("Years") or "").strip(),
            "CitizenPR": (info.get("CitizenPR") or "").strip()
        }
    except Exception as e:
        return {"Skills": f"(err: {e})", "Years": f"(err: {e})", "CitizenPR": f"(err: {e})"}
    finally:
        d.quit()


def enrich_jobs_with_AI():
    # -- locate the lasted file before enrich ---
    output_dir = "output"
    # Get all .jsonl files in the output dir
    json_files = glob(os.path.join(output_dir, "*.jsonl"))
    if not json_files:
        raise FileNotFoundError("No JSONL files found in the output directory.")
    # Pick the most recently modified file
    latest_file = max(json_files, key=os.path.getctime)
    print(f"Using latest file: {latest_file}")
    # Read the file
    with open(latest_file, encoding="utf-8") as f:
        rawdata = [json.loads(line) for line in f]

    # --- Adding job categories ---
    # Create a list of job titles from the JSONL
    # i["Job_title"] → Gets the value of "Job_title" from that dictionary.
    jobs_title = [i.get("Job_title") for i in rawdata]

    # Build the prompt (send the message to OpenAI)
    # 1. Ask GPT to choose exactly ONE tag from a fixed list
    # 2. Tell it to keep the order the same as our input
    # 3. Tell it to output only tags (one per line, no extra text)
    # 4. Add all job titles to the prompt
    # 5. Add potential categories here.
    prompt = (
            "For each of the following job titles, return exactly ONE tag from this list: "
            "Data, Developer, QA, Analyst, Engineer, IT Support, Design, IT Ops, Microsoft, "
            "Web Design, DevOps, Network, Security, Cloud, Database, IT Management, ML, Others.\n"
            "Return the tags in the same order, one per line, no extra text.\n\n"
            + "\n".join(jobs_title)  # Appends all job titles in titles as separate lines.
    )
    try:
        # Send the request to OpenAI
        model_used = "gpt-5-nano"  # TEST the differences between other models
        resp = client.responses.create(
            model=model_used,
            input=prompt
        )
        # Split GPT's answer into a list of tags (one tag per line)
        # .strip() removes any leading/trailing whitespace
        category = resp.output_text.strip().splitlines()

        # Merge Categories
        for rawdata, category in zip(rawdata, category):
            rawdata["Category"] = category  # Add categories to the job dictionary
            # Call analyze_job_description function here
            details = analyze_job_description(job.get("Link"))
            # Merge these details into the existing job dictionary
            enriched_data = rawdata.update(details)
            yield enriched_data
    except Exception as e:
        print(e)

    # Output enriched files
    os.makedirs(output_dir, exist_ok=True)  # create dir if not exist
    # Get current time string (e.g., 2025-07-14_01-30-00)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    process = CrawlerProcess(settings={
        # The FEEDS setting tells Scrapy where and how to save the scraped data.
        "FEEDS": {
            os.path.join(output_dir, f"Enriched_Result_{timestamp}.jsonl"): {"format": "jsonlines"},
            os.path.join(output_dir, f"Enriched_Result_{timestamp}.csv"): {"format": "csv"},
        },
    })


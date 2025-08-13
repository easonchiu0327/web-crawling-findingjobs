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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from dotenv import load_dotenv

#------------------------------------------------------------------------------------
# DON'T FORGET TO REMOVE YOUR API KEY BEFORE SHARING THIS CODE
# Load environment variables from .env file
# replace your api key here
load_dotenv()
# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#------------------------------------------------------------------------------------
# TEST the differences between other models
category_model = "gpt-5-nano"
job_description_model = "gpt-4o-mini"
#------------------------------------------------------------------------------------

# --- Build ONE shared driver and reuse it-faster
def build_driver():
    path = r'C:\Users\eason\webscraping_online course\chromedriver-win64\chromedriver.exe'
    service = Service(executable_path=path)
    options = Options()
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-sync")
    options.add_argument("--metrics-recording-only")
    options.add_argument("--disable-default-apps")
    options.add_argument("--no-first-run")
    options.add_argument("--disable-notifications")
    # Block images to cut bandwidth
    options.add_experimental_option("prefs", {
        "profile.managed_default_content_settings.images": 2
    })
    # Stop waiting for full load (wait only for DOMContentLoaded)
    options.page_load_strategy = "eager"

    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(15)      # fail fast on slow pages
    driver.set_script_timeout(10)
    return driver

# Get required skills, years and citizenPR
def analyze_job_description(link, driver):
    # --- If the link is empty or None, return blank values ---
    if not link:
        print("There is not link to scrape")
        return {"Skills": "", "Years": "", "CitizenPR": ""}
    try:
        driver.get(link)
        try:
            # use wait instead of sleep
            WebDriverWait(driver, 10).until(
                EC.any_of(
                    EC.presence_of_element_located((By.TAG_NAME, "main")),
                    EC.presence_of_element_located((By.TAG_NAME, "article")),
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
            )
        except (TimeoutException, WebDriverException) as e:
            pass  # parse whatever we have
            print(f"wait failed: {e}")
        sel = Selector(text=driver.page_source)

        # --- Extract all text from <main>, <article> or <body>(where job description usually is) ---
        # Most OpenAI's models expect a single string prompt, not a list, so we need to join a space between string by using " ".join
        text = " ".join(
            t.strip() for t in sel.xpath("//main//text() | //article//text() | //body//text()").getall() if t.strip()
        )
        # --- Cut the text if it's too long to save tokens ---
        # --- Test the result
        text = text[:12000]
        # if page text is too short, skip the model call
        if len(text) < 150:
            print("The text is too short, might be a problem of scraping the text from link")
            return {"Skills": "", "Years": "", "CitizenPR": ""}

        # Ask OpenAI for compact, structured output (JSON)
        # using JSON when sending data to the API has two big benefits, Easier Parsing and Avoids Unnecessary Words(Save token)
        prompt = f"""
    You are a precise information extractor. Read the job description text below and return a STRICT JSON object with these keys:
    - "Skills": short, comma-separated list of the top required skills (max 8 items)
    - "Years": numeric years of experience required
    - "CitizenPR": "Y" if Canadian citizenship or Canadian permanent residence is explicitly required, otherwise "N".

    Return ONLY JSON, no commentary.

    Job Description:
    {text}
    """.strip()

        resp = client.responses.create(
            model=job_description_model,
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

        # Creates a brand-new dictionary — even if info already has these keys, Normalize missing keys
        return {
            "Skills": (info.get("Skills") or "").strip(),
            "Years": str(info.get("Years") or "").strip(), # safe for int
            "CitizenPR": (info.get("CitizenPR") or "").strip()
        }
    except Exception as e:
        print(f"There is problem of loading json{e}/n")
        return {"Skills": f"(err: {e})", "Years": f"(err: {e})", "CitizenPR": f"(err: {e})"}


def enrich_jobs_with_ai():
    # -- load the lasted file before enrich ---
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)  # create dir if not exist
    # Get all .jsonl files in the output dir that are "raw" (not previously enriched results)
    # skip any file whose name starts with "Enriched_Result_
    jsonl_raw_files = [
        f for f in glob(os.path.join(output_dir, "*.jsonl"))
        if not os.path.basename(f).startswith("Enriched_Result_")
    ]
    if not jsonl_raw_files:
        raise FileNotFoundError("No raw JSONL files found in the output directory.")
    # Pick the most recently modified file
    latest_raw_file = max(jsonl_raw_files, key=os.path.getctime)
    print(f"Using latest raw file: {latest_raw_file}")
    # Read the file
    with open(latest_raw_file, encoding="utf-8") as f:
        raw_result = [json.loads(line) for line in f if line.strip()] # skip blank lines
    if not raw_result:
        raise ValueError("Latest JSONL file is empty.")

    # --- Adding job categories ---
    # Create a list of job titles from the JSONL
    # i["Job_title"] → Gets the value of "Job_title" from that dictionary.
    jobs_title = [(i.get("Job_title") or "Unknown") for i in raw_result]

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

    # Send the request to OpenAI once
    try:
        resp = client.responses.create(
            model=category_model,
            input=prompt
        )
        # Split GPT's answer into a list of tags (one tag per line)
        # .strip() removes any leading/trailing whitespace
        categories = (resp.output_text or "").strip().splitlines()
    except Exception as e:
        print(f"OpenAI error while tagging: {e}")
        categories = ["(OpenAI error)"] * len(jobs_title)

    # ------Merge Categories-------

    # build and reuse one driver for all jobs-faster
    driver = build_driver()
    try:
        enriched_data = []
        for raw, category in zip(raw_result, categories):
            out = dict(raw)  # copy so we don't mutate original
            out["Category"] = category.strip()  # Add categories to the job dictionary
            # Call analyze_job_description function here
            try:
                details = analyze_job_description(out.get("Link"), driver)
            except Exception as e:
                details = {"Skills": f"(err: {e})", "Years": "", "CitizenPR": ""}
            # Merge these details into the existing job dictionary
            out.update(details)
            enriched_data.append(out)
            # ---- rate limit per-page AI analysis & page fetch ----
            time.sleep(0.2)
    finally:
        driver.quit() # quit driver here at once

    # Output enriched files
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    enriched_path = os.path.join(output_dir, f"Enriched_Result_{timestamp}.jsonl")
    try:
        with open(enriched_path, "w", encoding="utf-8") as f:
            for rec in enriched_data:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            print(
                f"Enriched JSONL: {enriched_path}, category_model={category_model}, job_description_model={job_description_model}")
    except Exception as e:
        print(f"Failed to write enriched file: {e}")
    return enriched_path

if __name__ == "__main__":
    enrich_jobs_with_ai()


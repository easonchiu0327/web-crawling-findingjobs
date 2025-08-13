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

# Get required skills, years and citizenPR
def analyze_job_description(link):
    # --- If the link is empty or None, return blank values ---
    if not link:
        return {"Skills": "", "Years": "", "CitizenPR": ""}
    # set up selenium
    # --- Setup Selenium Chrome Driver ---
    # the path of where the chrome driver is
    path = r'C:\Users\eason\webscraping_online course\chromedriver-win64\chromedriver.exe'
    service = Service(executable_path=path)
    options = Options()
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(link)
        time.sleep(5)
        sel = Selector(text=driver.page_source)

        # --- Extract all text from <main> or <article> (where job description usually is) ---
        # Most OpenAI's models expect a single string prompt, not a list, so we need to join a space between string by using " ".join
        text = " ".join(
            t.strip() for t in sel.xpath("//main//text() | //article//text()").getall() if t.strip()
        )
        # --- Cut the text if it's too long to save tokens ---
        # --- Test the result
        text = text[:12000]

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
        try:
            info = json.loads(json_data)
            # Creates a brand new dictionary — even if info already has these keys, Normalize missing keys
            return {
                "Skills": (info.get("Skills") or "").strip(),
                "Years": (info.get("Years") or "").strip(),
                "CitizenPR": (info.get("CitizenPR") or "").strip()
            }
        except Exception as e:
            print(e)
            # Fallback if the model didn’t return strict JSON
            return {"Skills": "", "Years": "", "CitizenPR": ""}


    except Exception as e:
        return {"Skills": f"(err: {e})", "Years": f"(err: {e})", "CitizenPR": f"(err: {e})"}
    finally:
        driver.quit()


def enrich_jobs_with_ai():
    # -- load the lasted file before enrich ---
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
        raw_result = [json.loads(line) for line in f]
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
    # Merge Categories
    enriched_data = []
    for raw, category in zip(raw_result, categories):
        out = dict(raw)  # copy so we don't mutate original
        out["Category"] = category.strip()  # Add categories to the job dictionary
        # Call analyze_job_description function here
        try:
            details = analyze_job_description(out.get("Link"))
        except Exception as e:
            details = {"Skills": f"(err: {e})", "Years": "", "CitizenPR": ""}
        # Merge these details into the existing job dictionary
        out.update(details)
        enriched_data.append(out)
        # ---- rate limit per-page AI analysis & page fetch ----
        time.sleep(0.3)

    # Output enriched files
    os.makedirs(output_dir, exist_ok=True)  # create dir if not exist
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    jsonl_path = os.path.join(output_dir, f"Enriched_Result_{timestamp}.jsonl")
    try:
        with open(jsonl_path, "w", encoding="utf-8") as f:
            for rec in enriched_data:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception as e:
        print(e)

    print(f"Enriched JSONL: {jsonl_path}, category_model={category_model}, job_description_model={job_description_model}")
    return jsonl_path


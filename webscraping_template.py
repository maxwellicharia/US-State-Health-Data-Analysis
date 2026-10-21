"""
Web Scraping Module
-------------------
Extracts tabular data from web pages using requests-html and pandas.
"""

from io import StringIO
from pathlib import Path
from typing import Optional
import pandas as pd
from requests_html import HTMLSession
from bs4 import BeautifulSoup

# Define default configuration constants
TARGET_URL: str = (
    "https://www.visualcapitalist.com/mapped-obesity-rates-highest-in-usa/"
)
OUTPUT_FILE: Path = Path("obesity_rates_in_US_States.csv")


def scrape_table(url: str) -> Optional[pd.DataFrame]:
    """
    Fetches a web page, renders client-side JavaScript, and extracts table data into a pandas DataFrame.

    :param url: The target web page URL.
    :return: Extracted pandas DataFrame if table is found, otherwise None.
    """
    session = HTMLSession()
    try:
        response = session.get(url)
        # Execute JavaScript for dynamically rendered tables
        response.html.render(timeout=20)

        soup = BeautifulSoup(response.html.html, "lxml")

        # Class-based selector for resilience against dynamic ID changes
        table = soup.find("table", class_="tablepress") or soup.find("table")

        if table is None:
            print("[!] Error: No matching table found on the page.")
            return None

        # Parse string HTML using StringIO for pandas 2.0+ compatibility
        dfs = pd.read_html(StringIO(str(table)))
        return dfs[0] if dfs else None

    except Exception as exc:
        print(f"[!] An error occurred during extraction: {exc}")
        return None
    finally:
        session.close()


def main() -> None:
    """Main execution function."""
    print(f"[*] Extracting table data from: {TARGET_URL}")
    df = scrape_table(TARGET_URL)

    if df is not None:
        print("\nExtracted Data Sample:")
        print(df.head())

        # Save DataFrame to CSV using Path object
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"\n[+] Data successfully saved to '{OUTPUT_FILE.resolve()}'")
    else:
        print("[-] Process completed with no output generated.")


if __name__ == "__main__":
    main()
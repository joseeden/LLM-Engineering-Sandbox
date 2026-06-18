from pathlib import Path

from dotenv import load_dotenv

from agents import ResearchPlannerAgent, SummaryReportAgent, WebSearchAgent
from database import init_db


BASE_DIR = Path(__file__).resolve().parent
REPORT_FILE = BASE_DIR / "reports" / "summary_report.md"


def main():
    load_dotenv()
    init_db()

    research_plan = ResearchPlannerAgent().run()
    search_results = WebSearchAgent().run(research_plan)
    summary_report = SummaryReportAgent().run(search_results)

    REPORT_FILE.parent.mkdir(exist_ok=True)
    REPORT_FILE.write_text(summary_report, encoding="utf-8")
    print(f"Summary report saved to {REPORT_FILE}")


if __name__ == "__main__":
    main()

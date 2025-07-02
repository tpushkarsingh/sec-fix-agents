# helpers/coverage_tools.py
import re, subprocess, xml.etree.ElementTree as ET
from pathlib import Path

def run_coverage(repo_dir: str) -> float:
    """
    Executes `mvn test jacoco:report` and returns overall line‑coverage %
    """
    subprocess.run(
        ["mvn", "-q", "test", "jacoco:report"],
        cwd=repo_dir,
        check=True
    )
    xml = Path(repo_dir) / "target/site/jacoco/jacoco.xml"
    tree = ET.parse(xml)
    line_rate = float(tree.getroot().attrib["line-rate"])
    return round(line_rate * 100, 1)

def list_low_classes(repo_dir: str, threshold: float = 0.8) -> list[str]:
    """
    Parses jacoco.xml and returns fully‑qualified class names below threshold
    """
    xml = Path(repo_dir) / "target/site/jacoco/jacoco.xml"
    tree = ET.parse(xml)
    ns = {"j": "http://www.eclemma.org/jacoco"}
    low = []
    for pkg in tree.findall(".//package"):
        pkg_name = pkg.attrib["name"].replace("/", ".")
        for cls in pkg.findall("class"):
            rate = float(cls.attrib["line-rate"])
            if rate < threshold:
                name = f"{pkg_name}.{cls.attrib['name'].split('/')[-1]}"
                low.append(name)
    return low

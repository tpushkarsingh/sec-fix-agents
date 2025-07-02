# helpers/pom_tools.py
import xml.etree.ElementTree as ET
from pathlib import Path

def patch_pom_xml(repo_dir: str, fixes: list[dict]) -> None:
    """
    fixes = [
        {"groupId": "org.springframework.security", "artifactId": "spring-security-core", "new": "5.8.9"},
        {"groupId": "com.fasterxml.jackson.core",   "artifactId": "jackson-databind",   "new": "2.17.1"},
    ]
    """
    pom_path = Path(repo_dir) / "pom.xml"
    tree = ET.parse(pom_path)
    root = tree.getroot()

    # Maven POM uses the XML namespace "http://maven.apache.org/POM/4.0.0"
    ns = {"m": "http://maven.apache.org/POM/4.0.0"}

    for fix in fixes:
        xpath = (
            "./m:dependencies/m:dependency"
            f"[m:groupId='{fix['groupId']}'][m:artifactId='{fix['artifactId']}']/m:version"
        )
        version_elem = root.find(xpath, ns)
        if version_elem is not None:
            version_elem.text = fix["new"]

    tree.write(pom_path, encoding="utf-8", xml_declaration=True)

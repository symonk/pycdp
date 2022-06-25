import logging

from pycdp._models import Domain
from pycdp._utils import browser_protocol_data, js_protocol_data

logging.basicConfig(level=logging.DEBUG)


def main() -> int:
    """Main entrypoint; parses the json file into appropriate in memory models and subsequently
    writes them to disk as new python modules in a `devtools` module.
    """
    js_map, browser_map = js_protocol_data(), browser_protocol_data()
    merged = [domain for domain in js_map["domains"] + browser_map["domains"] if "deprecated" not in domain]
    domain_objects = []
    domain_objects.append(Domain.from_json(merged[0]))  # Let's make one work for now, then we can iterate others.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

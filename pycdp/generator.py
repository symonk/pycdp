import logging
import pprint

from pycdp._models import Domain
from pycdp._utils import browser_protocol_data
from pycdp._utils import js_protocol_data

logging.basicConfig(level=logging.DEBUG)


def main() -> int:
    """Main entrypoint; parses the json file into appropriate in memory models and subsequently
    writes them to disk as new python modules in a `devtools` module.
    """
    js_map, browser_map = js_protocol_data(), browser_protocol_data()
    merged_domains = [domain for domain in js_map["domains"] + browser_map["domains"]]
    # Let's just build one object for now.
    domains = [Domain.deserialize(domain) for domain in merged_domains]
    pprint.pprint(domains)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

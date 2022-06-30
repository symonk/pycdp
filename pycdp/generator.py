import argparse
import logging
import pathlib
import pprint
import shutil

from pycdp._models import Domain
from pycdp._utils import browser_protocol_data
from pycdp._utils import js_protocol_data
from pycdp._config import Config
logging.basicConfig(level=logging.DEBUG)


def main(config: Config) -> int:
    """Main entrypoint; parses the json file into appropriate in memory models and subsequently
    writes them to disk as new python modules in a `devtools` module.
    """
    create_domains_directory(config.directory)
    js_map, browser_map = js_protocol_data(), browser_protocol_data()
    merged_domains = [domain for domain in js_map["domains"] + browser_map["domains"]]
    # Let's just build one object for now.
    domains = Domain.deserialize(merged_domains[0])
    pprint.pprint(domains)
    return 0


def create_domains_directory(directory_name: str) -> None:
    """Generate the devtools directory for storing deserialised domain data."""
    folder = pathlib.Path(__file__).parent.joinpath(directory_name)
    shutil.rmtree(folder)
    folder.mkdir(exist_ok=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory",
                        "-d",
                        action="store",
                        default="devtools",
                        help="Directory to write the generated CDP files into")
    raise SystemExit(main(Config(**vars(parser.parse_args()))))

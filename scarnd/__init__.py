import logging
from scarnd.gbif import get_scar_network_datasets, create_gbif_url
from scarnd.github import get_github_issues, create_github_issue
from termcolor import colored


logger = logging.getLogger(__name__)


class ScarNetworkDatasets:

    def __init__(self):

        self.github_issues = get_github_issues()
        self.gbif_datasets = get_scar_network_datasets()

    def normalize_identifier(self, identifier):
        identifier = identifier.replace("https://", "http://")
        if identifier.endswith("/"):
            identifier = identifier[:-1]
        if identifier.startswith("10."):
            identifier = identifier.replace("10.", "https://doi.org/10.")
        return identifier

    def github_has_issue(self, identifiers):
        for identifier in identifiers:
            for issue in self.github_issues:
                if issue["body"] is not None and "URLs" in issue["body"]:
                    for url in issue["body"]["URLs"]:
                        if self.normalize_identifier(identifier) == self.normalize_identifier(url):
                            return True
        return False

    def dataset_is_orphaned(self, gbif_dataset):
        if len([endpoint["url"] for endpoint in gbif_dataset["endpoints"] if endpoint["url"].startswith("https://orphans.gbif.org")]) > 0:
            return True
        return False

    def dataset_has_dwc_endpoint(self, gbif_dataset):
        if len([endpoint["url"] for endpoint in gbif_dataset["endpoints"] if endpoint["type"] == "DWC_ARCHIVE"]) > 0:
            return True
        return False

    def run(self, dry_run=False):
        for gbif_dataset in self.gbif_datasets:
            gbif_url = create_gbif_url(gbif_dataset["key"])

            identifiers = [identifier["identifier"] for identifier in gbif_dataset["identifiers"]]
            if gbif_dataset["doi"] is not None:
                doi_url = self.normalize_identifier(gbif_dataset["doi"])
                if doi_url not in identifiers:
                    identifiers.append(doi_url)

            if not self.dataset_has_dwc_endpoint(gbif_dataset):
                logger.info(colored(f"No IPT URL found for {gbif_url}", "red"))
            else:
                if not self.dataset_is_orphaned(gbif_dataset):
                    logger.info(colored(f"Dataset is not orphaned: {gbif_url}", "blue"))
                    if not self.github_has_issue(identifiers):
                        logger.info(colored(f"Dataset not in GitHub: {gbif_url}", "green"))
                        if not dry_run:
                            create_github_issue(gbif_dataset, identifiers)

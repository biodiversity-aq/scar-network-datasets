# SCAR-network-datasets

This Python package creates issues for datasets added to the [SCAR network](https://www.gbif.org/network/8534dd20-c368-4a1f-bdaf-e6b390710f89) in the GBIF registry.

Since the release of IPT 2.5.2, publishers can select the networks their dataset belongs to in IPT. 

Datasets that are added to the SCAR network appear here: https://www.gbif.org/network/8534dd20-c368-4a1f-bdaf-e6b390710f89 (note that while the dataset appears immediately the occurrence records reprocess so lag behind a little).


## Run

Create `.env` file with environment variables `GITHUB_USER` and `GITHUB_ACCESS_TOKEN`.

```
python -m scarnd
```

## Acknowledgement

This repository is adapted from the [OBIS network datasets](https://github.com/iobis/obis-network-datasets) repository. We acknowledge the contribution of the original [contributors](https://github.com/iobis/obis-network-datasets/graphs/contributors) from the [OBIS network datasets](https://github.com/iobis/obis-network-datasets) repository.

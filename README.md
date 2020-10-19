# CRM20 How does software break ![Sanity Checks](https://github.com/XPerianer/CRM20_How_does_software_break/workflows/Sanity%20Checks/badge.svg)

This repository is to document my work in the SS 2020 Seminar Code Repository Mining.
It contains analysis code, and also documented analysis in the jupyter notebook.

# Installation
The requirements are documented in the `requirements.txt` file, so if you are using `pip`, you can call
```
pip install -r requirements.txt
```
I recommend to create a virtual environment beforehand.

# Structure
The mutation testing datasets were generated with [Mutester](https://github.com/XPerianer/Mutester), a tool I developed to simplify generation of mutation testing data. Four of these datasets are also available in the `data` folder via git lfs. In the [folder specific readme](data/README.md), you can also find some details about the datasets.

A good starting point is the [Jupyter Notebook](./How_Does_Software_Break.ipynb). There you finde a walkthrough of the different aspects that were highlighted during the seminar.

The Notebook makes heavy use of code imported from the `src` folder, that is partitioned in diverse helper modules.

Especially the metric analysis code from the `src` folder is also tested (`test` folder).


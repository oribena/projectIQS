

# Iterative Query Selection Web Platform

The Iterative Query Selection (IQS) Web Platform retrieves information from opaque search engines using the IQS algorithm.
Given a document, the algorithm extracts the optimal short keyword queries thus improving the retrieval quality from opaque search engines.

Visit the [IQS web platform](https://iqs.cs.bgu.ac.il/) at the following URL: https://iqs.cs.bgu.ac.il/.

To watch the IQS promotional video click on the link below: https://www.youtube.com/watch?v=-GWxibc36wY


## Web Platform Overveiw

* Search and retrieve data from Twitter's website using the IQS algorithm.
* Performs comparison experiment between the IQS algorithm and other state of the art algorithm (ALMIK).
* Review past search results on their history page.
* Designed for a wide range of users.

# IQS Python Package

The python packege implements the IQS algorithm 

## Installation

Installation can be done using [pypi](https://pypi.org/project/IQS-algorithm/):

```bash
pip install IQS-algorithm
```
In order to use the package add `from IQS_algorithm import IQS` to your code.

## Python Package Overveiw

* Performs the IQS algorithm on various queries by providing a simple API for accessing all its functionality.
* Modify the quality of the search results from Twitter by setting different parameters. 
* Designed for users with technical background.
* Download the package using pip install IQS-algorithm

## citation

IQS algorithm's creators: Dr. Aviad Elishar, Mr. Maor Reuven and Dr. Rami Puzis

To cite Iterative Query Selection [article](https://www.sciencedirect.com/science/article/abs/pii/S0957417422004432), please use the following bibtex reference:

```
@article{Reuben2022Iterative,
title = {Iterative query selection for opaque search engines with pseudo relevance feedback},
journal = {Expert Systems with Applications},
volume = {201},
pages = {117027},
year = {2022},
issn = {0957-4174},
doi = {https://doi.org/10.1016/j.eswa.2022.117027},
url = {https://www.sciencedirect.com/science/article/pii/S0957417422004432},
author = {Maor Reuben and Aviad Elyashar and Rami Puzis},
keywords = {Query selection, Opaque search engine, Pseudo relevance feedback, Fake news},
}
```

We are Ophir Porat, Ori Ben-Artzy and Mor Zweig, students in the department of Software and Information Systems Engineering at Ben Gurion University of the Negev. These platforms are our final project under the guidance of Dr. Aviad Elishar and Mr. Maor Reuven IQS algorithm's creators.

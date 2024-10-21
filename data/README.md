# Dataset

In this project, we utilize the [The Cystic Fibrosis Database (CF)](https://users.dcc.uchile.cl/~rbaeza/mir2ed/ref.php.html), which is provided by Ricardo Baeza-Yates. You can obtain the dataset in the context of Ricardo's book, "[Modern Information Retrieval](https://users.dcc.uchile.cl/~rbaeza/mir2ed/home.php.html)".

The CF Database consists of 1,239 documents published between 1974 and 1979 that discuss various aspects of cystic fibrosis, along with 100 queries and their corresponding relevant documents.

## Preprocessing

To obtain a list of documents we used [scripts/preprocess.py](../scripts/preprocess.py).
The script loops over all records available in the CF data collection and applies the following steps to preprocess text:

1. Removes ends of line throughout the text (`text.replace("\n", " ")`)
2. Removes extra spaces within the text (`re.sub(" +", " ", text)`)

The following section details the list of attributes we extracted for each document.

## Document Structure

The following snippet shows the document structure for each record and their corresponding .XML tags (in the original dataset).

```json
{
    "abstract": "",    // ABSTRACT | EXTRACT
    "authors": [],     // AUTHORS (AUTHOR)
    "major_subj": [],  // MAJORSUBJ (TOPIC)
    "minor_subj": [],  // MINORSUBJ (TOPIC)
    "id": "",          // RECORDNUM
    "source": "",      // SOURCE
    "title": ""        // TITLE
}
```

## QREL Structure

The following snippet shows the QREL structure for each query and their corresponding .XML tags (in the original dataset).

```json
{
    "query_n": "",     // QueryNumber
    "query_text": [],  // QueryText
    "qrels": [],       // Records (Record)
}
```

The [scripts/preprocess.py](../scripts/preprocess.py) script saves separate .JSON files for each query.



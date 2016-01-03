import pytest
import graphviz
from numpy import nan
import pandas as pd

import wikivision


@pytest.fixture
def simple_revisions():
    return pd.DataFrame({
        'rev_sha1': ['a', 'b', 'c'],
        'parent_sha1': [nan, 'a', 'b'],
    })


def test_to_graph_requires_hashes():
    wikitexts = pd.DataFrame({
        'wikitext': list('abc'),
    })
    with pytest.raises(wikivision.MissingRequiredColumnError):
        wikivision.revisions_to_graph(wikitexts)


def test_to_graph_returns_graphviz_object(simple_revisions):
    simple_graph = wikivision.revisions_to_graph(simple_revisions)
    assert isinstance(simple_graph, graphviz.Digraph)


def test_graph_body_correct_length(simple_revisions):
    simple_graph = wikivision.revisions_to_graph(simple_revisions)

    # calculate expected number of lines in the body of the dot source
    num_nodes = len(simple_revisions)
    num_edges = num_nodes - 1
    expected_body_len = num_nodes + num_edges

    assert len(simple_graph.body), expected_body_len

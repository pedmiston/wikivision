import os

import pytest
from pandas import DataFrame

import wikivision


@pytest.fixture
def db_con(request):
    test_db_name = 'histories-test'
    db_con = wikivision.connect_db(test_db_name)
    def delete_db():
        db_con.close()
        os.remove('{}.sqlite'.format(test_db_name))
    request.addfinalizer(delete_db)
    return db_con

# to_table
# --------

@pytest.fixture
def json_revisions():
    return [
        {'a': [1, 2, 3], 'b': list('abc')},
        {'a': [4, 5, 6], 'b': list('def')},
    ]

def test_to_table(json_revisions):
    revisions = wikivision.to_table(json_revisions)
    assert isinstance(revisions, DataFrame)

def test_column_order(json_revisions):
    columns = ['a', 'b']
    rev_columns = list(reversed(columns))

    revisions = wikivision.to_table(json_revisions, columns=columns)
    rev_revisions = wikivision.to_table(json_revisions, columns=rev_columns)

    assert revisions.columns.tolist() == columns
    assert rev_revisions.columns.tolist() == rev_columns 

def test_adding_keys_to_table(json_revisions):
    id_vars = {
        'slug': 'testing_123',
        'name': 'Testing 123',
    }
    revisions = wikivision.to_table(json_revisions, id_vars=id_vars)
    assert all([v in revisions.columns for v in id_vars])

def test_renaming_table_columns(json_revisions):
    renamer = {'a': 'alpha', 'b': 'beta'}
    revisions = wikivision.to_table(json_revisions, renamer=renamer)
    got = set(revisions.columns)
    want = set(renamer.values())
    assert got == want, "columns weren't renamed properly"

# select_revisions_by_article
# ---------------------------

def _append_test_revisions(article_slug, db_con):
    revisions = DataFrame({'article_slug': [article_slug, ]})
    wikivision.append_revisions(revisions, db_con)

def test_select_revisions_by_article(db_con):
    test_slug = 'test_slug'
    _append_test_revisions(test_slug, db_con)
    revisions = wikivision.select_revisions_by_article(test_slug, db_con)
    assert len(revisions) == 1

def test_select_single_article(db_con):
    slug1 = 'slug1'
    slug2 = 'slug2'

    _append_test_revisions(slug1, db_con)
    _append_test_revisions(slug2, db_con)

    revisions = wikivision.select_revisions_by_article(slug1, db_con)
    assert len(revisions) == 1

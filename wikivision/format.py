import pandas as pd


def tree_format(revisions):
    """ Convert a complete revision history to a tree format. """
    revisions = revisions.copy()
    revisions = drop_repeats(revisions)
    revisions = convert_timestamp_to_datetime(revisions)
    revisions = label_wikitext_id(revisions)
    revisions = label_wikitext_parent_id(revisions)
    tree_data = {'data': revisions.to_dict('records')}
    return tree_data


def drop_repeats(revisions):
    revisions = revisions.copy()
    revisions['is_repeat'] = revisions.wikitext[1:] == revisions.wikitext[:-1]
    revisions.fillna(False, inplace=True)
    return revisions.ix[~revisions.is_repeat].drop('is_repeat', axis=1)


def convert_timestamp_to_datetime(revisions):
    revisions = revisions.copy()
    revisions['timestamp'] = pd.to_datetime(revisions.timestamp)
    revisions.sort_values(by='timestamp', inplace=True)
    return revisions


def label_wikitext_id(revisions):
    revisions = revisions.copy()
    id_map = {wikitext: i for i, wikitext in enumerate(revisions.wikitext.unique())}
    revisions['wikitext_id'] = revisions.wikitext.apply(lambda x: id_map[x])
    return revisions


def label_wikitext_parent_id(revisions):
    revisions = revisions.copy()
    id_map = {wikitext: i for i, wikitext in enumerate(revisions.wikitext.unique())}
    wikitext_parent_ids = []
    wikitexts = revisions.wikitext.tolist()
    for i, wikitext in enumerate(wikitexts):
        if i == 0:
            wikitext_parent_ids.append(-1)
        else:
            parent_wikitext = wikitexts[i-1]
            parent_wikitext_id = id_map[parent_wikitext]
            wikitext_parent_ids.append(parent_wikitext_id)
    revisions['wikitext_parent_id'] = wikitext_parent_ids
    return revisions

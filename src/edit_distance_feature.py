import editdistance

def edit_distance_feature(row_one: [], row_two: []) -> []:

    return list(map(editdistance.eval, row_one, row_two))
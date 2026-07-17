
# ----------------------------------------------------------------------- #
# Dependency check function
# ----------------------------------------------------------------------- #

def dependency_check(df):

    report = {}

    # colonne candidate come ID
    possible_ids = [
        "mouse",
        "subject",
        "sample",
        "patient",
        "id",
        "individual",
        "name" 
    ]

    detected_ids = [
        col for col in df.columns
        if col.lower() in possible_ids
    ]

    report["id_columns"] = detected_ids


    repeated = {}

    for col in detected_ids:

        counts = df[col].value_counts()

        repeated[col] = any(counts > 1)


    report["repeated_measurements"] = repeated


    return report


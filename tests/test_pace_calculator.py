from running_pace_api.pace_calculator import calculate_pace_table, OFFICIAL_DISTANCES
import math

def test_calculate_pace_table():
    min_pace = 180  # 5 minutes per km
    max_pace = 600  # 10 minutes per km
    increment = 2  # 1 minute per km

    expected_number_of_rows = ((max_pace - min_pace) // increment) + 1

    result = calculate_pace_table(min_pace, max_pace, increment)

    # Vérifier que le résultat n'est pas vide
    assert len(result) > 0

    # Vérifier le nombre de lignes
    assert len(result) == expected_number_of_rows

    # Vérifier le contenu de chaque ligne
    for index, pace in enumerate(range(min_pace, max_pace + 1, increment)):
        row = result[index]
        assert row["Pace (sec/km)"] == pace
        for distance in OFFICIAL_DISTANCES:
            expected_time = (distance / 1000) * pace
            assert row[f"{distance}m"] == math.floor(expected_time)

    # Test avec min_pace égal à max_pace
    result_same_pace = calculate_pace_table(min_pace, min_pace, increment)
    assert len(result_same_pace) == 1
    assert result_same_pace[0]["Pace (sec/km)"] == min_pace


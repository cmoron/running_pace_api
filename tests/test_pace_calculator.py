import pytest

from mypacer_api.core.calculator import calculate_pace_table
from mypacer_api.models import OFFICIAL_DISTANCES


def test_calculate_pace_table():
    min_pace = 600  # 10 minutes per km
    max_pace = 180  # 3 minutes per km
    increment = 2  # 2 seconds per km

    expected_number_of_rows = ((min_pace - max_pace) // increment) + 1
    result = calculate_pace_table(min_pace, max_pace, increment, OFFICIAL_DISTANCES)

    # Check result is not empty
    assert len(result) > 0

    # Check lines number
    assert len(result) == expected_number_of_rows

    # Check line content
    # for index, pace in enumerate(range(min_pace, max_pace + 1, increment)):
    for index, pace in enumerate(range(min_pace, max_pace - 1, -increment)):
        speed_km_h = round(3600 / pace, 2)  # Convert pace to speed in km/h
        row = result[index]
        assert row["pace"] == pace
        assert row["speed"] == speed_km_h
        for distance in OFFICIAL_DISTANCES:
            expected_time = (distance / 1000) * pace
            assert row[f"{distance}"] == round(expected_time, 2)

    # Test with min_pace equals to max_pace
    result_same_pace = calculate_pace_table(min_pace, min_pace, increment, [])
    assert len(result_same_pace) == 1
    assert result_same_pace[0]["pace"] == min_pace


def test_calculate_pace_table_errors():
    """Test that calculate_pace_table raises errors for invalid inputs."""
    # Test with non-positive min_pace
    with pytest.raises(ValueError, match="Minimum pace must be positive"):
        calculate_pace_table(0, -10, 1, [])
    with pytest.raises(ValueError, match="Minimum pace must be positive"):
        calculate_pace_table(-10, -20, 1, [])

    # Test with max_pace > min_pace
    with pytest.raises(
        ValueError, match="Minimum pace must be greater than maximum pace"
    ):
        calculate_pace_table(180, 600, 2, [])

    # Test with non-positive increment
    with pytest.raises(ValueError, match="Increment must be positive"):
        calculate_pace_table(600, 180, 0, [])
    with pytest.raises(ValueError, match="Increment must be positive"):
        calculate_pace_table(600, 180, -2, [])

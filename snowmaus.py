import numpy as np

__all__ = ["snowfall", "meltwater_production", "sublimed_snowcover"]


def snowfall(
        precipitation: np.typing.ArrayLike,
        temperature_daily_minimum: np.typing.ArrayLike,
        threshold_temperature_upper: float = 0,
        threshold_temperature_lower: float = -6
) -> np.typing.ArrayLike:
    """Calculate snow accumulation

    :param precipitation: Precipitation
    :type precipitation: np.typing.ArrayLike
    :param temperature_daily_minimum: Daily minimum surface are temperature in degrees Celsius
    :type temperature_daily_minimum: np.typing.ArrayLike
    :param threshold_temperature_upper: Daily minimum temperature threshold above which snowfall
        is impossible, defaults to 0 ˚C
    :type threshold_temperature_upper: float, optional
    :param threshold_temperature_lower: Daily minimum temperature threshold below which all
        precipitation is snowfall, defaults to -6 ˚C
    :type threshold_temperature_lower: float, optional
    :return: Accumulated snow. Unit depends on input `precipitation`
    :rtype: np.typing.ArrayLike
    """
    return np.where(
        temperature_daily_minimum <= threshold_temperature_lower,
        precipitation,
        np.where(
            temperature_daily_minimum < threshold_temperature_upper,
            precipitation * (1 - (temperature_daily_minimum - threshold_temperature_lower)
                             / np.abs(threshold_temperature_upper - threshold_temperature_lower)),
            0
        )
    )


def meltwater_production(
        temperature_daily_minimum: np.typing.ArrayLike,
        temperature_daily_maximum: np.typing.ArrayLike,
        threshold_temperature_minimum: float = -12,
        threshold_temperature_maximum: float = 5,
        melt_rate: float = 0.42  # mm/˚C/day
) -> np.typing.ArrayLike:
    """Calculate meltwater runoff

    :param temperature_daily_minimum: Daily minimum temperature in degrees Celsius
    :type temperature_daily_minimum: np.typing.ArrayLike
    :param temperature_daily_maximum: Daily maximum temperature in degrees Celsius
    :type temperature_daily_maximum: np.typing.ArrayLike
    :param threshold_temperature_minimum: Daily minimum temperature threshold below which melt is
        impossible, defaults to -12 ˚C
    :type threshold_temperature_minimum: float, optional
    :param threshold_temperature_maximum: Daily maximum temperature threshold below which melt is
        impossible, defaults to 5 ˚C
    :type threshold_temperature_maximum: float, optional
    :param melt_rate: Melt rate, defaults to 0.42 mm/˚C/day
    :type melt_rate: float, optional
    :return: Meltwater runoff in mm
    :rtype: np.typing.ArrayLike
    """
    return np.where(
        np.logical_or(
            temperature_daily_minimum <= threshold_temperature_minimum,
            np.logical_and(
                temperature_daily_minimum <= 0,
                temperature_daily_maximum < threshold_temperature_maximum
            )
        ),
        0,
        melt_rate * (temperature_daily_minimum + np.abs(threshold_temperature_minimum))
    )


def sublimed_snowcover(
    snowcover_previous_day: np.typing.ArrayLike,
    threshold_snowcover: float = 20
) -> np.typing.ArrayLike:
    """Calculate sublimed snow

    If the snow cover exceeds `threshold_snowcover`, 1 mm is sublimed on the
    next day.

    :param snowcover_previous_day: Snow cover of the previous day in kg/m²
    :type snowcover_previous_day: np.typing.ArrayLike
    :param threshold_snowcover: Snow cover thickness above which sublimation
        takes place, defaults to 20 kg/m²
    :type threshold_snowcover: float, optional
    :return: Sublimed snow in kg/m²
    :rtype: np.typing.ArrayLike
    """
    return np.where(snowcover_previous_day > threshold_snowcover, 1, 0)

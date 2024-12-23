import numpy as np

__all__ = ["accumulation", "melt"]


def accumulation(
        precipitation: np.typing.ArrayLike,
        temperature_daily_minimum: np.typing.ArrayLike,
        threshold_temperature_upper: np.typing.ArrayLike = 0,
        threshold_temperature_lower: np.typing.ArrayLike = -6
) -> np.typing.ArrayLike:
    """Calculate snow accumulation

    :param precipitation: Precipitation
    :type precipitation: np.typing.ArrayLike
    :param temperature_daily_minimum: Daily minimum surface are temperature in degrees Celsius
    :type temperature_daily_minimum: np.typing.ArrayLike
    :param threshold_temperature_upper: Daily minimum temperature threshold above which snowfall
        is impossible, defaults to 0 ˚C
    :type threshold_temperature_upper: np.typing.ArrayLike, optional
    :param threshold_temperature_lower: Daily minimum temperature threshold below which all
        precipitation is snowfall, defaults to -6 ˚C
    :type threshold_temperature_lower: np.typing.ArrayLike, optional
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


def melt(
        temperature_daily_minimum: np.typing.ArrayLike,
        temperature_daily_maximum: np.typing.ArrayLike,
        threshold_temperature_minimum: np.typing.ArrayLike = -12,
        threshold_temperature_maximum: np.typing.ArrayLike = 5,
        melt_rate: np.typing.ArrayLike = 0.42  # mm/˚C/day
) -> np.typing.ArrayLike:
    """Calculate meltwater runoff

    :param temperature_daily_minimum: Daily minimum temperature in degrees Celsius
    :type temperature_daily_minimum: np.typing.ArrayLike
    :param temperature_daily_maximum: Daily maximum temperature in degrees Celsius
    :type temperature_daily_maximum: np.typing.ArrayLike
    :param threshold_temperature_minimum: Daily minimum temperature threshold below which melt is
        impossible, defaults to -12 ˚C
    :type threshold_temperature_minimum: np.typing.ArrayLike, optional
    :param threshold_temperature_maximum: Daily maximum temperature threshold below which melt is
        impossible, defaults to 5 ˚C
    :type threshold_temperature_maximum: np.typing.ArrayLike, optional
    :param melt_rate: Melt rate, defaults to 0.42 mm/˚C/day
    :type melt_rate: np.typing.ArrayLike, optional
    :return: Meltwater runoff
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

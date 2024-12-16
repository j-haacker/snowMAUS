import numpy as np

__all__ = ["accumulation", "melt"]


def accumulation(
        precipitation: float,
        temperature_daily_minimum: float,
        threshold_temperature_upper: float = 0,
        threshold_temperature_lower: float = -6
) -> float:
    """Calculate snow accumulation

    :param precipitation: Precipitation
    :type precipitation: float
    :param temperature_daily_minimum: Daily minimum surface are temperature in degrees Celsius
    :type temperature_daily_minimum: float
    :param threshold_temperature_upper: Daily minimum temperature threshold above which snowfall
        is impossible, defaults to 0 ˚C
    :type threshold_temperature_upper: float, optional
    :param threshold_temperature_lower: Daily minimum temperature threshold below which all
        precipitation is snowfall, defaults to -6 ˚C
    :type threshold_temperature_lower: float, optional
    :return: Accumulated snow. Unit depends on input `precipitation`
    :rtype: float
    """
    if temperature_daily_minimum <= threshold_temperature_lower:
        return precipitation
    elif temperature_daily_minimum < threshold_temperature_upper:
        return (
            precipitation * (1 - (temperature_daily_minimum - threshold_temperature_lower)
                             / np.abs(threshold_temperature_upper - threshold_temperature_lower))
        )
    return 0.


def melt(
        temperature_daily_minimum: float,
        temperature_daily_maximum: float,
        threshold_temperature_minimum: float = -12,
        threshold_temperature_maximum: float = 5,
        melt_rate: float = 0.42  # mm/˚C/day
) -> float:
    """Calculate meltwater runoff

    :param temperature_daily_minimum: Daily minimum temperature in degrees Celsius
    :type temperature_daily_minimum: float
    :param temperature_daily_maximum: Daily maximum temperature in degrees Celsius
    :type temperature_daily_maximum: float
    :param threshold_temperature_minimum: Daily minimum temperature threshold below which melt is
        impossible, defaults to -12 ˚C
    :type threshold_temperature_minimum: float, optional
    :param threshold_temperature_maximum: Daily maximum temperature threshold below which melt is
        impossible, defaults to 5 ˚C
    :type threshold_temperature_maximum: float, optional
    :param melt_rate: Melt rate, defaults to 0.42 mm/˚C/day
    :type melt_rate: float, optional
    :return: Meltwater runoff
    :rtype: float
    """
    # in the Trnka-2010 paper, it is not defined what should happen
    # in case temperature_daily_minimum > 0 and
    # temperature_daily_minimum < threshold_temperature_lower.
    # this implementation assumes that, then, melt is possible.
    if (
        temperature_daily_minimum <= threshold_temperature_minimum
        or (temperature_daily_minimum <= 0
            and temperature_daily_maximum < threshold_temperature_maximum)
    ):
        return 0.
    return melt_rate * (temperature_daily_minimum + np.abs(threshold_temperature_minimum))

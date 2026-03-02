from zoneinfo import ZoneInfo
from datetime import datetime, timedelta


def get_musician_schedule_in_timezone(musician, customer_timezone):
    """
    Show musician's availability for the next N weeks in customer's timezone

    Args:
        musician: Musician instance (should have availability.time_schedule relationship)
        customer_timezone: String timezone identifier (e.g., 'America/New_York')
        weeks_ahead: Number of weeks to look ahead

    Returns:
        List of available time slots with timezone conversions
    """
    # Map your string day names to weekday integers (0=Monday, 6=Sunday)
    DAY_TO_WEEKDAY = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }

    # Get musician's timezone (adjust field path based on your model)
    # Assuming musician.profile.timezone exists
    musician_tz = ZoneInfo(musician.owner.profile.timezone)
    customer_tz = ZoneInfo(customer_timezone)

    # Get today in musician's timezone
    today = datetime.now(musician_tz).date()
    end_date = today + timedelta(weeks=1)

    # Get all time schedules for this musician
    time_schedules = musician.availability_info.time_schedule.all()

    # Group schedules by day for easier lookup
    schedules_by_day = {}
    for schedule in time_schedules:
        day_name = schedule.day.lower()
        weekday_num = DAY_TO_WEEKDAY.get(day_name)
        if weekday_num is not None:
            if weekday_num not in schedules_by_day:
                schedules_by_day[weekday_num] = []
            schedules_by_day[weekday_num].append(schedule)

    available_slots = []
    current_date = today

    # get the schedule for each day, starting on monday
    for day_of_week in range(7):
        # Get all availability slots for this day
        day_slots = schedules_by_day.get(day_of_week, [])

        for slot in day_slots:
            # Create datetime in musician's timezone
            start_dt = datetime.combine(current_date, slot.start_time).replace(
                tzinfo=musician_tz
            )
            end_dt = datetime.combine(current_date, slot.end_time).replace(
                tzinfo=musician_tz
            )

            # Convert to UTC and customer's timezone
            start_utc = start_dt.astimezone(ZoneInfo("UTC"))
            end_utc = end_dt.astimezone(ZoneInfo("UTC"))
            customer_start = start_dt.astimezone(customer_tz)
            customer_end = end_dt.astimezone(customer_tz)

            available_slots.append(
                # Extra fields not used on the client, for now
                {
                    # "date": current_date.isoformat(),
                    "day": slot.get_day_display(),
                    # "musician_timezone": str(musician_tz),
                    # "musician_start": start_dt.isoformat(),
                    # "musician_end": end_dt.isoformat(),
                    # "customer_timezone": str(customer_tz),
                    "start_time": customer_start.isoformat(),  # customer start
                    "end_time": customer_end.isoformat(),  # customer end
                    # "start_utc": start_utc.isoformat(),
                    # "end_utc": end_utc.isoformat(),
                }
            )

    return available_slots

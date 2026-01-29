from datetime import datetime

def times_conflict(course1, course2):
    # Check if they meet on any common day
    common_days = set(course1.days) & set(course2.days)
    if not common_days:
        return False

    # Check time overlap
    latest_start = max(course1.start_time, course2.start_time)
    earliest_end = min(course1.end_time, course2.end_time)
    return latest_start < earliest_end  # If there's any overlap

def generate_schedules(input_classes, alternatives, times_of_day, schedule_courses):
    from itertools import product

    # Collect all valid options for each required course (incl. alternatives)
    course_options = []

    for base_code in input_classes:
        valid_courses = []

        for course in schedule_courses:
            course_code = f"{course.subject}{course.course_number}"
            if course_code == base_code or course_code in alternatives.get(base_code, []):
                if base_code in times_of_day:
                    preferred_ranges = times_of_day[base_code]
                    match = False
                    for time_range in preferred_ranges:
                        if isinstance(time_range, tuple):
                             # Time range format
                            range_start = datetime.strptime(time_range[0], "%I:%M%p").time()
                            range_end = datetime.strptime(time_range[1], "%I:%M%p").time()

                            # Skip if course is missing valid time
                            if course.start_time is None or course.end_time is None:
                                continue

                            if course.start_time >= range_start and course.end_time <= range_end:
                                match = True
                                break
                        elif isinstance(time_range, str):
                            # Fallback string labels, e.g. "morning"
                            course_hour = course.start_time.hour
                            if (time_range == "morning" and 6 <= course_hour < 12) or \
                                    (time_range == "afternoon" and 12 <= course_hour < 17) or \
                                    (time_range == "evening" and 17 <= course_hour < 22):
                                match = True
                                break
                    if not match:
                        continue

                valid_courses.append(course)

        course_options.append(valid_courses)

    # Generate all combinations (cartesian product)
    all_combos = list(product(*course_options))
    valid_schedules = []

    for combo in all_combos:
        has_conflict = False
        for i in range(len(combo)):
            for j in range(i + 1, len(combo)):
                if times_conflict(combo[i], combo[j]):
                    has_conflict = True
                    break
            if has_conflict:
                break
        if not has_conflict:
            valid_schedules.append(combo)

    # Sort by total average pass rate descending
    sorted_schedules = sorted(valid_schedules, key=lambda sched: sum(c.pass_rate for c in sched) / len(sched), reverse=True)

    return sorted_schedules  # List of tuples of Course objects
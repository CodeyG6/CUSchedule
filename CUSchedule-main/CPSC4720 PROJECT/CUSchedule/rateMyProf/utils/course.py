from datetime import datetime

class Course:
    def __init__(self, subject, course_number, section, course_title, credit_hours, instructor, pass_rate, meeting_days, meeting_time, end_time):
        self.subject = subject
        self.course_number = course_number
        self.section = section
        self.course_title = course_title
        self.credit_hours = credit_hours
        self.instructor = instructor
        self.pass_rate = float(pass_rate)
        self.days = self.parse_days(meeting_days)
        self.start_time = self.parse_time(meeting_time)   # datetime.time
        self.end_time = self.parse_time(end_time)         # datetime.time

    def parse_days(self, day_str):
        day_map = {"M": "Mon", "T": "Tue", "W": "Wed", "R": "Thu", "F": "Fri"}
        if not isinstance(day_str, str):
            return []
        return [day_map[d] for d in day_str if d in day_map]

    def parse_time(self, time_str):
        if not isinstance(time_str, str):
            return None
        # Fix double spaces and strip
        clean_time = time_str.strip().replace("  ", " ").replace(" ", "")
        try:
            return datetime.strptime(clean_time, "%I:%M%p").time()
        except ValueError:
            print(f"Invalid time format: '{time_str}' → '{clean_time}'")
            return None

    def __str__(self):
        return f"{self.subject} {self.course_number} section {self.section} | {self.course_title} | {self.start_time}-{self.end_time} | {self.days} | {self.pass_rate}%"


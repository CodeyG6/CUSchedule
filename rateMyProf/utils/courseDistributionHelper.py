import pandas as pd

from .courseDistribution import CourseDistribution
from .course import Course

class CourseDistributionHelper:
    instructor_stats_df = pd.DataFrame()
    courses_df = pd.DataFrame()
    pass_rate_df = pd.DataFrame()

    @staticmethod
    def get_course_pass_rate(course_subject, course_number):
        CourseDistributionHelper.check_df_imports()

        course = course_subject + ' ' + str(course_number)
        
        if course in CourseDistributionHelper.pass_rate_df['Course'].values:
            pass_rate = CourseDistributionHelper.pass_rate_df[CourseDistributionHelper.pass_rate_df['Course'] == course]['Pass rate'].iloc[0]
            
            return pass_rate

        return -1

    @staticmethod
    def filter_by_pass_rate(df, target_pass_rate):
        for index in range(len(df)):
            remove = True
            
            course_subject = df.iloc[index, 0]
            course_number = df.iloc[index, 1]
            
            pass_rate = CourseDistributionHelper.get_course_pass_rate(course_subject, course_number)
            remove = pass_rate < target_pass_rate

            if remove:
                df = df.drop(index=index)

        return df
    
    def check_df_imports():
        if len(CourseDistributionHelper.pass_rate_df) == 0:
            CourseDistributionHelper.pass_rate_df = pd.read_csv('rateMyProf/utils/Course pass rates.csv')

        if len(CourseDistributionHelper.courses_df) == 0:
            # .csv file hasn't been imported yet
            CourseDistributionHelper.courses_df = pd.read_csv('rateMyProf/utils/classes.csv')

        if len(CourseDistributionHelper.instructor_stats_df) == 0:
            # .csv file hasn't been imported yet
            CourseDistributionHelper.instructor_stats_df = pd.read_csv('rateMyProf/utils/Instructor Stats List.csv')

    @staticmethod
    def find_courses(course_number = -1, honors = False, subject = "", days = "", pass_rate = 0.0, start_time = "", end_time = ""):
        CourseDistributionHelper.check_df_imports()

        if course_number is None or course_number == '':
            course_number = -1

        if subject is None:
            subject = ""

        if days is None:
            days = ""

        if pass_rate is None:
            pass_rate = 0.0

        if start_time is None:
            start_time = ""

        if end_time is None:
            end_time = ""
        
        filtered = CourseDistributionHelper.courses_df

        if course_number != -1:
            filtered = CourseDistributionHelper.get_rows_with_list_match(filtered, [course_number], 'Course Number', case_sensitive=True)
        
        if honors:
            filtered = CourseDistributionHelper.get_rows_with_list_match(filtered, ["Honors"], 'Attributes', case_sensitive=False, match_perfect=False)

        if subject != "":
            filtered = CourseDistributionHelper.get_rows_with_list_match(filtered, [subject], 'Subject')

        if days != "":
            days_list = days.split()
            filtered = CourseDistributionHelper.get_rows_with_list_match(filtered, days_list, 'Meeting 1 Days', case_sensitive=False, match_full_list=True)

        if start_time != "" and end_time != "":
            filtered = CourseDistributionHelper.filter_by_time(filtered, start_time, end_time)

        if pass_rate > 0:
            filtered = CourseDistributionHelper.filter_by_pass_rate(filtered, pass_rate)

        course_list = CourseDistributionHelper.get_course_list_from_df(filtered)

        '''for course in course_list:
            course.print()'''

        return course_list
    
    def filter_by_time(df, start_time, end_time):
        start_time = CourseDistributionHelper.convert_string_to_time_int(start_time)
        end_time = CourseDistributionHelper.convert_string_to_time_int(end_time)

        df_indexes = df.index
        for index in df_indexes:
            course_start_time_string = df.loc[index, 'Meeting 1 Start Time']
            course_end_time_string = df.loc[index, 'Meeting 1 End Time']

            if course_start_time_string == 'N/A' or pd.isna(course_start_time_string) or course_end_time_string == 'N/A' or pd.isna(course_end_time_string):
                df = df.drop(index=index)
            else:
                course_start_time = CourseDistributionHelper.convert_string_to_time_int(course_start_time_string)
                course_end_time = CourseDistributionHelper.convert_string_to_time_int(course_end_time_string)

                if course_start_time < start_time or course_end_time > end_time:
                    df = df.drop(index=index)

        return df

    def convert_string_to_time_int(time):
        time = time.replace("  ", " ")
        new_time = ""

        if len(time) == 7:
            # e.g. 7:00 PM
            new_time = int(time[0:1] + time[2:4])

            if time[5:7] == "PM":
                new_time += 1200

        elif len(time) == 8:
            # e.g. 10:00 PM
            new_time = int(time[0:2] + time[3:5])

            if time[6:8] == "PM" and time[0:1] == "0":
                new_time += 1200
        else:
            print("INVALID TIME " + time)

        return new_time

    def get_course_list_from_df(df):
        course_list = []
        for index in range(len(df)):
            subject = df.iloc[index, 0]
            course_number = df.iloc[index, 1]
            section = df.iloc[index, 2]
            course_title = df.iloc[index, 3]
            credit_hours = df.iloc[index, 4]
            instructor = df.iloc[index, 5]
            pass_rate = CourseDistributionHelper.get_course_pass_rate(subject, course_number)

            meeting_days = df.iloc[index].get('Meeting 1 Days', '')
            meeting_time = df.iloc[index].get('Meeting 1 Start Time', '')
            end_time = df.iloc[index].get('Meeting 1 End Time', '')

            if meeting_time in ('', 'N/A') or end_time in ('', 'N/A'):
                continue

            course_list.append(Course(
            subject, course_number, section,
            course_title, credit_hours, instructor,
            pass_rate, meeting_days, meeting_time, end_time
))

        return course_list

    @staticmethod
    def get_professor_stats(professor_name: str):
        CourseDistributionHelper.check_df_imports()

        name_list = professor_name.split()
        prof_df = CourseDistributionHelper.get_rows_with_list_match(CourseDistributionHelper.instructor_stats_df, name_list, 'Instructor', case_sensitive=False, match_perfect=False, match_full_list=True)
        if len(prof_df) <= 0:
            return CourseDistribution(-1, -1, -1)
        
        return CourseDistribution(prof_df.iloc[0]['A rate'], prof_df.iloc[0]['Pass rate'], prof_df.iloc[0]['Withdraw rate'])
    
    @staticmethod
    def get_professor_courses(professor_name: str):
        CourseDistributionHelper.check_df_imports()
        name_list = professor_name.split()

        course_df = CourseDistributionHelper.get_rows_with_list_match(CourseDistributionHelper.courses_df, name_list, 'Instructor', case_sensitive=False, match_perfect=False, match_full_list=True)
        course_list = CourseDistributionHelper.get_course_list_from_df(course_df)
        
        return course_list
    
    # df - DataFrame to filter
    # input_list - List of target values (e.g. to look for all classes that are either CPSC or ENGR, provide [CPSC, ENGR])
    # category - Column to compare the input_list values to (e.g. "Course")
    # avoid_duplicates_category - Column name to avoid duplicates from (e.g. To only have one of each instructor, provide "Instructor")
    # case_sensitive - Whether the match check should be case sensitive
    # match_perfect - Whether the input list values are the entire target (e.g. course type) or only a substring (e.g. partial instructor name)
    # match_full_list - Whether each input in the input list has to match some value in the column value
    @staticmethod
    def get_rows_with_list_match(df, input_list, category, avoid_duplicates_category = None, case_sensitive = True, match_perfect = True, match_full_list = False):
        avoid_duplicates = avoid_duplicates_category != None
        if not avoid_duplicates:
            # Just prevents error from occurring
            avoid_duplicates_category = category
            
        added_items = []
        df_indexes = df.index
        
        if not match_full_list:
            input_list = CourseDistributionHelper.remove_keywords(input_list)

        for i in df_indexes:
            row_value = df.loc[i, category]
            duplicate_category_item = df.loc[i, avoid_duplicates_category]

            if pd.isnull(row_value):
                remove_item = True
            else:
                if not match_full_list:
                    # Item should be removed unless there is one instance where there is a match
                    remove_item = True
                else:
                    # Item should not be removed unless there is one instance where there is not a match
                    remove_item = False
        
                if not avoid_duplicates or duplicate_category_item not in added_items:
                    # Either duplicates are allowed, or the item has been been added to added_items yet
                    for input_value in input_list:
                        values_match = CourseDistributionHelper.do_values_match(input_value, row_value, case_sensitive, match_perfect)
                        if not match_full_list and values_match:
                            # The values match, and only one input has to match
                            added_items.append(duplicate_category_item)
                            remove_item = False
                            break
                        elif match_full_list and not values_match:
                            # The values do not match, and every input must match
                            remove_item = True
                            break

            if remove_item:
                df = df.drop(index=i)

        return df

    @staticmethod
    def do_values_match(val_1, val_2, case_sensitive, match_perfect):    
        if val_1 == '':
            return False
        
        if not case_sensitive:
            val_1 = val_1.lower()
            val_2 = val_2.lower()

        if match_perfect:
            return val_1 == val_2

        return val_1 in val_2
    @staticmethod
    def load_all_courses():
        CourseDistributionHelper.check_df_imports()
        df = CourseDistributionHelper.courses_df
        return CourseDistributionHelper.get_course_list_from_df(df)

    @staticmethod
    def remove_keywords(input_list):
        keywords = ['to', 'for', '&', 'and', 'of', 'i', 'ii', 'lab', 'intro', 'introduction']
        
        temp_input_list = []
        for input_value in input_list:
            if not isinstance(input_value, str) or input_value.lower() not in keywords:
                temp_input_list.append(input_value)

        return temp_input_list
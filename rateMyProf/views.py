from .forms import ProfessorDataSearch
from .forms import CourseSearch
from .scheduler_utils import generate_schedules

#Rendering RateMyProfessor-related page. 
def home_view(request):
    return render(request, 'rateMyProf/homepage.html')

#Rendering the form for the RMP search
def prof_search(request):
    form = ProfessorDataSearch()
    if request.method == 'POST':
        form = ProfessorDataSearch(request.POST)
        if form.is_valid():
            form.save()
            prof_name = form.cleaned_data['Name']
            prof_stats = CourseDistributionHelper.get_professor_stats(prof_name)
            
            a_rate = prof_stats.a_rate
            pass_rate = prof_stats.pass_rate
            withdrawal_rate = prof_stats.withdrawal_rate

            professor_courses = CourseDistributionHelper.get_professor_courses(prof_name)

            print('Professor courses:')
            for course in professor_courses:
                print(course)

            return render(request, 'rateMyProf/rmpSearchResult.html', 
                          {'name': prof_name,
                          'a_rate': a_rate,
                          'pass_rate': pass_rate,
                          'withdrawal_rate': withdrawal_rate,
                          'prof_courses': professor_courses})
    return render(request, 'rateMyProf/rmpSearch.html',
                    {'form':form})
    
#rendering the search result - need to edit to actually render the fetched data, this is a placeholder
def prof_search_result(request):
    return render(request, 'rateMyProf/rmpSearchResult.html')

#Rendering the form for the course search
def course_search(request):
    form = CourseSearch()
    if request.method == 'POST':
        form = CourseSearch(request.POST)
        if form.is_valid():
            form.save()
            
            course_number = form.cleaned_data['CourseNumber']
            honors = form.cleaned_data['Honors']
            subject = form.cleaned_data['Subject']
            days = form.cleaned_data['MeetingDays']
            pass_rate = form.cleaned_data['PassRate']
            start_time = form.cleaned_data['StartTime']
            end_time = form.cleaned_data['EndTime']
            
            course_list = CourseDistributionHelper.find_courses(course_number, honors, subject, days, pass_rate, start_time, end_time) 
        
            return render(request, 'courseInfo/courseSearchResult.html', {'course_list': course_list})
    return render(request, 'courseInfo/courseSearch.html', 
                    {'form':form})
    
#rendering the search result - need to edit to actually render the fetched data, this is a placeholder
def course_search_result(request):
    return render(request, 'courseInfo/courseSearchResult.html')


from django.shortcuts import render
from .scheduler_utils import generate_schedules
from .utils.courseDistributionHelper import CourseDistributionHelper
from datetime import datetime

def schedule_builder(request):
    if request.method == 'POST':
        input_classes_raw = request.POST.getlist('input_classes')
        alt_classes_raw = request.POST.getlist('alternatives')
        start_times_raw = request.POST.getlist('start_times')
        end_times_raw = request.POST.getlist('end_times')
        pass_rates_raw = request.POST.getlist('pass_rates')

        # Process user input into usable structures
        input_classes = []
        alternatives = {}
        time_preferences = {}

        for idx, course_code in enumerate(input_classes_raw):
            base_code = course_code.strip().replace(" ", "")
            input_classes.append(base_code)

            # Handle alternatives
            raw_alts = alt_classes_raw[idx].strip()
            if raw_alts:
                alt_list = [alt.strip().replace(" ", "") for alt in raw_alts.split(',') if alt.strip()]
                alternatives[base_code] = alt_list

            # Handle time range
            start = start_times_raw[idx]
            end = end_times_raw[idx]
            if start and end:
                time_preferences[base_code] = [(datetime.strptime(start, "%H:%M").strftime("%I:%M%p"),
                                                datetime.strptime(end, "%H:%M").strftime("%I:%M%p"))]

        # Optional pass rate filter — here we filter before calling the schedule generator
        pass_rate_filters = {}
        for idx, rate in enumerate(pass_rates_raw):
            if rate:
                try:
                    pass_rate_filters[input_classes[idx]] = float(rate)
                except ValueError:
                    pass  # skip invalid input

        # Load course data
        all_courses = CourseDistributionHelper.load_all_courses()

        if pass_rate_filters:
            filtered_courses = []
            for course in all_courses:
                code = f"{course.subject}{course.course_number}"
                min_pass = pass_rate_filters.get(code)
                if min_pass is None or course.pass_rate >= min_pass:
                    filtered_courses.append(course)
        else:
            filtered_courses = all_courses

        # Generate recommended schedules
        recommended = generate_schedules(
            input_classes=input_classes,
            alternatives=alternatives,
            times_of_day=time_preferences,
            schedule_courses=filtered_courses
        )

        return render(request, 'scheduleBuilder/schedule_builder_result.html', {
            'recommended': recommended
        })

    return render(request, 'scheduleBuilder/schedule_builder.html')
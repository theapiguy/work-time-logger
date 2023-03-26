from utils import set_work_dict, work_dict, date_time_format, date_format, get_work_log
from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '81c88e9c-f11d-47b8-a8d0-c0ac708a12ea'


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        button_value = request.form['start-stop']
        jira_number = request.form['jira_number']
        if 'work_description' in request.form:
            work_description = request.form['work_description']
        else:
            work_description = ''
        if button_value == 'Start':
            #  Need to reset work_dict and use sessionio in case the browser closes
            ed = 'readonly'
            button_value = 'Stop'
            start_time = datetime.now().strftime(date_time_format)
            message = f"Started timer for {jira_number} at {start_time}"
            set_work_dict(start_time=start_time, button_value=button_value,
                          jira_number=jira_number, ed=ed, elapsed_time='',
                          end_time='', show_work_description=True)
            print(f"In start, getting today's work.")
            today_work = get_work_log(datetime.now().strftime(date_format))
        elif button_value == 'Stop':
            ed = ''
            button_value = 'Start'
            end_time = datetime.now().strftime(date_time_format)
            set_work_dict(end_time=end_time, button_value=button_value,
                          jira_number=jira_number, ed=ed,
                          work_description=work_description, show_work_description=False)
            message = f"Stopped timer for {jira_number} at {end_time}.  Task took {work_dict['elapsed_time']} hours to complete."
            print(f"In Stop, getting today's work.")
            work_dict['jira_number'] = ''
            today_work = get_work_log(datetime.now().strftime(date_format))
        else:
            message = f"Invalid status of {button_value}"

        print(f"Work dict - {work_dict}")
        return render_template('home.html',
                               message=message, work_dict=work_dict, today_work=today_work)
    today_work = get_work_log(datetime.now().strftime(date_format))
    print(f"Work dict - {work_dict}")
    return render_template('home.html', ss_value='Start', work_dict=work_dict, today_work=today_work)


@app.route("/search", methods=["GET", "POST"])
def do_search():
    if request.method == "POST":
        work_date = request.form.get('work_date')
        results = get_work_log(work_date)
        print(f"Search Results for {work_date} - {results}")
        return render_template('report.html', results=results)

    return render_template('report.html')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

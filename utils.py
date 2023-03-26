import sqlite3
from datetime import datetime

work_dict = {
    'start_time': '',
    'end_time': '',
    'button_value': 'Start',
    'elapsed_time': '',
    'ed': '',
    'jira_number': '',
    'work_description': '',
    'show_work_description': False
}
work_dict_valid_keys = work_dict.keys()
date_time_format = '%b %d, %Y %H:%M:%S %p'
date_format = '%Y-%m-%d'

####  Start Database/Table Creation
connection = sqlite3.connect('engineer_worklog.db', check_same_thread=False)
print("Connection established.")
cursor = connection.cursor()
print("Cursor established.")

# Create worklog table
cmd1 = """CREATE TABLE IF NOT EXISTS 
    worklog(log_id INTEGER PRIMARY KEY, start_time DATETIME, 
    end_time DATETIME, ticket_number VARCHAR(25), work_description TEXT(3000))"""

print(f"Executing command - {cmd1}")
cursor.execute(cmd1)
####  End Database/Table Creation


def get_work_dict():
    global work_dict
    return work_dict


def set_work_dict(**kwargs):
    global work_dict
    for work_dict_key in work_dict_valid_keys:
        if work_dict_key in kwargs:
            work_dict[work_dict_key] = kwargs[work_dict_key]

    print(f"set_work_dict = {work_dict}")
    #  Debugging an issue with not writing data
    if work_dict['start_time'] == '' and work_dict['end_time'] != '':
        print(f"End Time but no Start Time for - {work_dict}")
    if work_dict['start_time'] != '' and work_dict['end_time'] != '':
        if work_dict['elapsed_time'] == '':
            #  Calculate elapsed time
            work_dict['elapsed_time'] = get_elapsed_time(work_dict['start_time'], work_dict['end_time'])
            start_time = datetime.strptime(work_dict['start_time'], date_time_format)
            end_time = datetime.strptime(work_dict['end_time'], date_time_format)
            jira_number = work_dict['jira_number']
            work_description = work_dict['work_description']
            start_date = datetime.strptime(work_dict['start_time'], date_time_format).strftime(date_format)
            #  Add to table
            insert_cmd = f'INSERT INTO worklog VALUES (NULL, "{start_time}", ' \
                         f'"{end_time}", "{jira_number}", "{work_description}", "{start_date}")'
            print(f"{insert_cmd} executed.")
            cursor.execute(insert_cmd)
            connection.commit()


def get_elapsed_time(start_time, end_time, fmt=date_time_format):
    date1_obj = datetime.strptime(start_time, fmt)
    date2_obj = datetime.strptime(end_time, fmt)

    elapsed = (date2_obj - date1_obj).seconds
    hours_elapsed = elapsed/3600
    return hours_elapsed


def get_work_log(start_date=None):
    if start_date:
        cmd = f"SELECT * FROM worklog WHERE start_date = '{start_date}'"
        message = f"Results for {start_date}"
    else:
        message = "Results"
        cmd = "SELECT * FROM worklog"

    cursor.execute(cmd)
    results = cursor.fetchall()
    print(message)
    work_log_list = []
    for result in results:
        print(result)
        elapsed_time = get_elapsed_time(result[1], result[2], '%Y-%m-%d %H:%M:%S')
        work_log_dict = {
            "log_id": result[0],
            "start_time": result[1],
            "end_time": result[2],
            "ticket_number": result[3],
            "description": result[4],
            "elapsed_time": elapsed_time
        }
        work_log_list.append(work_log_dict)
    return work_log_list


if __name__ == '__main__':
    # cmd = "ALTER TABLE worklog ADD start_date DATE;"
    # cursor.execute(cmd)
    # print("Updating table")
    # cmd = "UPDATE worklog SET start_date = '2023-03-22' WHERE log_id = '1'"
    # cursor.execute(cmd)
    #
    # cmd = "UPDATE worklog SET start_date = '2023-03-22' WHERE log_id = '2'"
    # cursor.execute(cmd)
    # connection.commit()
    # exit(0)
    # start_time = "2023-03-21 09:13:17"
    # end_time = "2023-03-21 09:28:59"
    # jira_number = "MIS-1234"
    # work_description = "This is a test."
    # insert_cmd = f'INSERT INTO worklog VALUES (NULL, "{start_time}", "{end_time}", "{jira_number}", "{work_description}")'
    # cursor.execute(insert_cmd)
    # cursor.execute(insert_cmd)
    # cursor.execute(insert_cmd)
    # connection.commit()
    # print(f"{insert_cmd} executed.")

    print(f"Getting work log.")
    get_work_log()
    # get_work_log('2023-03-22')
    # get_work_log('2023-03-23')


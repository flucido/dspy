import requests
import pandas as pd
from aeries_connection import *
from warnings import filterwarnings

filterwarnings("ignore", category=UserWarning, message='.*pandas only supports SQLAlchemy connectable.*')


def flatten_json(json_obj, parent_key='', separator='_'):
	flattened = {}
	if isinstance(json_obj, list):
		for i, item in enumerate(json_obj):
			if isinstance(item, dict):
				flattened.update(flatten_json(item, f"{parent_key}{separator}{i}", separator))
	elif isinstance(json_obj, dict):
		for key, value in json_obj.items():
			new_key = f"{parent_key}{separator}{key}" if parent_key else key
			if isinstance(value, dict):
				flattened.update(flatten_json(value, new_key, separator))
			elif isinstance(value, list):
				for i, item in enumerate(value):
					if isinstance(item, dict):
						flattened.update(flatten_json(item, f"{new_key}{separator}{i}", separator))
			else:
				flattened[new_key] = value
	return flattened


def attendance_data_request(sc):
	url = "https://millercreeksd.aeries.net/admin/api/v5/schools/" + str(sc) + "/attendanceHistory/summary"
	
	payload = {}
	headers = {
		'AERIES-CERT': 'b7ee197342d5499f9a00b2564d145a4a',
		'Cookie': 'AWSALB=wfRvbbq98S/vzfrrnSAHR36F/c9DtKnLqPV7v0scRNTdr+Ncdgz/MTqAaLd5FRKjlmsuTeoRrZzM5Os2o1sb'
		          '+oYs1eyTxo/D75rd/h1btwBustKTIv5qZhQ7H9b5; '
		          'AWSALBCORS=wfRvbbq98S/vzfrrnSAHR36F/c9DtKnLqPV7v0scRNTdr+Ncdgz/MTqAaLd5FRKjlmsuTeoRrZzM5Os2o1sb'
		          '+oYs1eyTxo/D75rd/h1btwBustKTIv5qZhQ7H9b5; s=2yscluaxgpsohdsbailddy41 '
	}
	
	response = requests.request("GET", url, headers=headers, data=payload)
	response = response.json()
	
	return response


def student_information_request(stuid, sc):
	url = "https://millercreeksd.aeries.net/admin/api/v5/schools/" + str(sc) + "/students/" + str(stuid)
	
	payload = {}
	headers = {
		'AERIES-CERT': 'b7ee197342d5499f9a00b2564d145a4a',
		'Cookie': 'AWSALB=wfRvbbq98S/vzfrrnSAHR36F/c9DtKnLqPV7v0scRNTdr+Ncdgz/MTqAaLd5FRKjlmsuTeoRrZzM5Os2o1sb'
		          '+oYs1eyTxo/D75rd/h1btwBustKTIv5qZhQ7H9b5; '
		          'AWSALBCORS=wfRvbbq98S/vzfrrnSAHR36F/c9DtKnLqPV7v0scRNTdr+Ncdgz/MTqAaLd5FRKjlmsuTeoRrZzM5Os2o1sb'
		          '+oYs1eyTxo/D75rd/h1btwBustKTIv5qZhQ7H9b5; s=2yscluaxgpsohdsbailddy41 '
	}
	
	response = requests.request("GET", url, headers=headers, data=payload)
	response = response.json()
	
	return response


def student_enrollment_request(stuid):
	url = "https://millercreeksd.aeries.net/admin/api/v5/enrollment/" + str(stuid)
	
	payload = {}
	headers = {
		'AERIES-CERT': 'b7ee197342d5499f9a00b2564d145a4a',
		'Cookie': 'AWSALB=wfRvbbq98S/vzfrrnSAHR36F/c9DtKnLqPV7v0scRNTdr+Ncdgz/MTqAaLd5FRKjlmsuTeoRrZzM5Os2o1sb'
		          '+oYs1eyTxo/D75rd/h1btwBustKTIv5qZhQ7H9b5; '
		          'AWSALBCORS=wfRvbbq98S/vzfrrnSAHR36F/c9DtKnLqPV7v0scRNTdr+Ncdgz/MTqAaLd5FRKjlmsuTeoRrZzM5Os2o1sb'
		          '+oYs1eyTxo/D75rd/h1btwBustKTIv5qZhQ7H9b5; s=2yscluaxgpsohdsbailddy41 '
	}
	
	response = requests.request("GET", url, headers=headers, data=payload)
	response = response.json()
	
	return response


def student_attendance_request(stuid, sc):
	url = "https://millercreeksd.aeries.net/admin/api/v5/schools/" + str(sc) + "/attendanceHistory/summary/" + str(
		stuid)
	
	payload = {}
	headers = {
		'AERIES-CERT': 'b7ee197342d5499f9a00b2564d145a4a',
		'Cookie': 'AWSALB=wfRvbbq98S/vzfrrnSAHR36F/c9DtKnLqPV7v0scRNTdr+Ncdgz/MTqAaLd5FRKjlmsuTeoRrZzM5Os2o1sb'
		          '+oYs1eyTxo/D75rd/h1btwBustKTIv5qZhQ7H9b5; '
		          'AWSALBCORS=wfRvbbq98S/vzfrrnSAHR36F/c9DtKnLqPV7v0scRNTdr+Ncdgz/MTqAaLd5FRKjlmsuTeoRrZzM5Os2o1sb'
		          '+oYs1eyTxo/D75rd/h1btwBustKTIv5qZhQ7H9b5; s=2yscluaxgpsohdsbailddy41 '
	}
	
	response = requests.request("GET", url, headers=headers, data=payload)
	response = response.json()
	
	return response


def student_program_request(stuid, sc):
	url = "https://millercreeksd.aeries.net/admin/api/v5/schools/" + str(sc) + "/students/" + str(stuid) + "/programs"
	
	payload = {}
	headers = {
		'AERIES-CERT': 'b7ee197342d5499f9a00b2564d145a4a',
		'Cookie': 'AWSALB=wfRvbbq98S/vzfrrnSAHR36F/c9DtKnLqPV7v0scRNTdr+Ncdgz/MTqAaLd5FRKjlmsuTeoRrZzM5Os2o1sb'
		          '+oYs1eyTxo/D75rd/h1btwBustKTIv5qZhQ7H9b5; '
		          'AWSALBCORS=wfRvbbq98S/vzfrrnSAHR36F/c9DtKnLqPV7v0scRNTdr+Ncdgz/MTqAaLd5FRKjlmsuTeoRrZzM5Os2o1sb'
		          '+oYs1eyTxo/D75rd/h1btwBustKTIv5qZhQ7H9b5; s=2yscluaxgpsohdsbailddy41 '
	}
	
	response = requests.request("GET", url, headers=headers, data=payload)
	response = response.json()
	
	return response


def student_grade_request(stuid, sc):
	url = "https://millercreeksd.aeries.net/admin/api/v5/schools/" + str(sc) + "/ReportCard/" + str(stuid)
	
	payload = {}
	headers = {
		'AERIES-CERT': 'b7ee197342d5499f9a00b2564d145a4a',
		'Cookie': 'AWSALB=wfRvbbq98S/vzfrrnSAHR36F/c9DtKnLqPV7v0scRNTdr+Ncdgz/MTqAaLd5FRKjlmsuTeoRrZzM5Os2o1sb'
		          '+oYs1eyTxo/D75rd/h1btwBustKTIv5qZhQ7H9b5; '
		          'AWSALBCORS=wfRvbbq98S/vzfrrnSAHR36F/c9DtKnLqPV7v0scRNTdr+Ncdgz/MTqAaLd5FRKjlmsuTeoRrZzM5Os2o1sb'
		          '+oYs1eyTxo/D75rd/h1btwBustKTIv5qZhQ7H9b5; s=2yscluaxgpsohdsbailddy41 '
	}
	
	response = requests.request("GET", url, headers=headers, data=payload)
	response = response.json()
	
	return response


def student_GPA_request(stuid, sc):
	url = "https://millercreeksd.aeries.net/admin/api/v5/schools/" + str(sc) + "/gpas/" + str(stuid)
	
	payload = {}
	headers = {
		'AERIES-CERT': 'b7ee197342d5499f9a00b2564d145a4a',
		'Cookie': 'AWSALB=wfRvbbq98S/vzfrrnSAHR36F/c9DtKnLqPV7v0scRNTdr+Ncdgz/MTqAaLd5FRKjlmsuTeoRrZzM5Os2o1sb'
		          '+oYs1eyTxo/D75rd/h1btwBustKTIv5qZhQ7H9b5; '
		          'AWSALBCORS=wfRvbbq98S/vzfrrnSAHR36F/c9DtKnLqPV7v0scRNTdr+Ncdgz/MTqAaLd5FRKjlmsuTeoRrZzM5Os2o1sb'
		          '+oYs1eyTxo/D75rd/h1btwBustKTIv5qZhQ7H9b5; s=2yscluaxgpsohdsbailddy41 '
	}
	
	response = requests.request("GET", url, headers=headers, data=payload)
	response = response.json()
	
	return response


def student_AD_request(stuid, sc):
	url = "https://millercreeksd.aeries.net/admin/api/v5/schools/" + str(sc) + "/assertivediscipline/" + str(stuid)
	
	payload = {}
	headers = {
		'AERIES-CERT': 'b7ee197342d5499f9a00b2564d145a4a',
		'Cookie': 'AWSALB=wfRvbbq98S/vzfrrnSAHR36F/c9DtKnLqPV7v0scRNTdr+Ncdgz/MTqAaLd5FRKjlmsuTeoRrZzM5Os2o1sb'
		          '+oYs1eyTxo/D75rd/h1btwBustKTIv5qZhQ7H9b5; '
		          'AWSALBCORS=wfRvbbq98S/vzfrrnSAHR36F/c9DtKnLqPV7v0scRNTdr+Ncdgz/MTqAaLd5FRKjlmsuTeoRrZzM5Os2o1sb'
		          '+oYs1eyTxo/D75rd/h1btwBustKTIv5qZhQ7H9b5; s=2yscluaxgpsohdsbailddy41 '
	}
	
	response = requests.request("GET", url, headers=headers, data=payload)
	response = response.json()
	
	return response


def student_test_data_request(stuid):
	url = "https://millercreeksd.aeries.net/admin/api/v5/students/" + str(stuid) + "/tests"
	
	payload = {}
	headers = {
		'AERIES-CERT': 'b7ee197342d5499f9a00b2564d145a4a',
		'Cookie': 'AWSALB=3cQa'
		          '/WQv8fNHqEWg9DDIQtZxwjYxj2vwVvNHuGRtkR04f6U7K'
		          'inDb8MM3OTHDp3F9Ws6gMhEPoj6Wt7IlFqotkFx8qRx1N9'
		          'ZCH5Q0KyralLiYPYY5srE+eg5rgFL; AWSALBCORS=3cQa/WQ'
		          'v8fNHqEWg9DDIQtZxwjYxj2vwVvNHuGRtkR04f6U7KinDb8MM3O'
		          'THDp3F9Ws6gMhEPoj6Wt7IlFqotkFx8qRx1N9ZCH5Q0KyralLiYPYY5srE+eg5rgFL '
	}
	
	response = requests.request("GET", url, headers=headers, data=payload)
	response = response.json()
	return response


def student_information_return(stuid, sc):
	json_data = student_information_request(stuid, sc)
	
	flattened_json = [flatten_json(item) for item in json_data]
	df = pd.DataFrame(flattened_json)
	
	data_list = []
	data_list.extend(df['StudentID'])
	data_list.extend(df['StateStudentID'])
	
	if df.loc[0, 'SchoolCode'] == 12:
		data_list += ['Lucas Valley']
	if df.loc[0, 'SchoolCode'] == 14:
		data_list.extend += ['Mary E. Silvira']
	if df.loc[0, 'SchoolCode'] == 16:
		data_list += ['MillerCreek']
	if df.loc[0, 'SchoolCode'] == 19:
		data_list += ['Vallecito']
	
	data_list.extend(df['FirstName'])
	data_list.extend(df['LastName'])
	data_list.extend(df['Gender'])
	data_list.extend(df['Grade'])
	data_list.extend(df['Birthdate'])
	
	if df.loc[0, 'EthnicityCode'] == 'Y':
		data_list += ['Hispanic']
	elif df.loc[0, 'EthnicityCode'] == 'N' and int(df.loc[0, 'RaceCode1']) == 100:
		data_list += ['American Indian or Alaska']
	elif df.loc[0, 'EthnicityCode'] == 'N' and int(df.loc[0, 'RaceCode1']) == 700:
		data_list += ['White']
	elif df.loc[0, 'EthnicityCode'] == 'N' and int(df.loc[0, 'RaceCode1']) == 600:
		data_list += ['Black or African American']
	elif df.loc[0, 'EthnicityCode'] == 'N' and int(df.loc[0, 'RaceCode1']) == 400:
		data_list += ['Filipino']
	elif df.loc[0, 'EthnicityCode'] == 'N' and (
			int(df.loc[0, 'RaceCode1']) >= 299 or int(df.loc[0, 'RaceCode1']) >= 399):
		data_list += ['Native Hawaiian or Pacific Islander']
	elif df.loc[0, 'EthnicityCode'] == 'N' and int(df.loc[0, 'RaceCode2']) > 0:
		data_list += ['Multi Racial']
	else:
		data_list += ['Unknown']
	
	data_list.extend(df['LanguageFluencyCode'])
	
	df2 = pd.DataFrame(columns=['Student ID',
	                            'SSID',
	                            'School',
	                            'First Name',
	                            'Last Name',
	                            'Gender',
	                            'Grade',
	                            'Birthdate',
	                            'Race',
	                            'Language Fluency'])
	df2.loc[0] = data_list
	# print(df2)
	
	return df2


def student_enrollment_return(stuid):
	json_data = student_enrollment_request(stuid)
	
	flattened_json = [flatten_json(item) for item in json_data]
	df = pd.DataFrame(flattened_json)
	df2 = pd.DataFrame(columns=['School Code', 'Academic Year', 'Grade', 'Enter Date', 'Leave Date'])
	df2['School Code'] = df['SchoolCode']
	df2['Academic Year'] = df['AcademicYear']
	df2['Grade'] = df['Grade']
	df2['Enter Date'] = df['EnterDate']
	df2['Leave Date'] = df['LeaveDate']
	
	return df2


def school_code(stuid):
	df = student_enrollment_return(stuid)
	
	sc = df.iloc[0]['School Code']
	return sc


def student_attendance_return(stuid, sc):
	json_data = student_attendance_request(stuid, sc)
	flattened_json = [flatten_json(item) for item in json_data]
	df = pd.DataFrame(flattened_json)
	
	rows = len(df.columns)
	
	rows = int(((rows - 1) / 23))
	
	data_list1 = []
	data_list2 = []
	
	for x in range(rows):
		
		for i in range(10):
			index = (14 + i) + 23 * x
			data_list1.append(df.iloc[0, index])
		data_list2.append(data_list1[:])
		data_list1.clear()
	
	df2 = pd.DataFrame(data_list2, columns=['School Year',
	                                        'School Code',
	                                        'Days Enrolled',
	                                        'Days Present',
	                                        'Days Absence',
	                                        'Days Excused',
	                                        'Days Unexcused',
	                                        'Days Tardy',
	                                        'Days Of Truancy',
	                                        'Days Suspension'])
	df2['Percent Absent'] = (df2['Days Present'] / df2['Days Enrolled']) * 100
	df2['Percent Absent'] = df2['Percent Absent'].round(2)
	
	# print(df2)
	return df2


def student_program_return(stuid, sc):
	json_data = student_program_request(stuid, sc)
	flattened_json = [flatten_json(item) for item in json_data]
	df = pd.DataFrame(flattened_json)
	df2 = pd.DataFrame(columns=['Program Code', 'Program Description', 'Start Date', 'End Date'])
	df2['Program Code'] = df['ProgramCode']
	df2['Program Desciption'] = df['ProgramDescription']
	df2['Start Date'] = df['EligibilityStartDate']
	df2['End Date'] = df['EligibilityEndDate']
	
	return df2


def student_grade_return(stuid, sc):
	json_data = student_grade_request(stuid, sc)
	flattened_json = [flatten_json(item) for item in json_data]
	df = pd.DataFrame(flattened_json)
	return df


def student_GPA_return(stuid, sc):
	json_data = student_GPA_request(stuid, sc)
	flattened_json = [flatten_json(item) for item in json_data]
	df = pd.DataFrame(flattened_json)
	return df


def student_AD_return(stuid, sc):
	json_data = student_AD_request(stuid, sc)
	flattened_json = [flatten_json(item) for item in json_data]
	df = pd.DataFrame(flattened_json)
	return df


def student_test_data_return(stuid):
	# returns student test scores as a list of data frames
	
	test_data = student_test_data_request(stuid)
	
	json_data = test_data
	flattened_json = [flatten_json(item) for item in json_data]
	
	test_data_frames = []
	
	df = pd.DataFrame(flattened_json)
	
	df_star_ELA = df[(df['TestID'] == 'STAR') & (df['TestingAdministration'] != "") & (df['TestPart'] == '1')]
	df_star_ELA.reset_index(inplace=True)
	test_data_frames.append(df_star_ELA)
	
	df_star_MATH = df[(df['TestID'] == 'STAR') & (df['TestingAdministration'] != "") & (df['TestPart'] == '2')]
	df_star_MATH.reset_index(inplace=True)
	test_data_frames.append(df_star_MATH)
	
	df_sbac_ELA = df[(df['TestID'] == 'SBAC') & (df['TestPart'] == '1')]
	df_sbac_ELA.reset_index(inplace=True)
	test_data_frames.append(df_sbac_ELA)
	
	df_sbac_MATH = df[(df['TestID'] == 'SBAC') & (df['TestPart'] == '2')]
	df_sbac_MATH.reset_index(inplace=True)
	test_data_frames.append(df_sbac_MATH)
	
	return test_data_frames


def student_data(stuid):
	sc = school_code(stuid)
	
	student_information_df = [student_information_return(stuid, sc), student_enrollment_return(stuid),
	                          student_attendance_return(stuid, sc), student_program_return(stuid, sc),
	                          student_GPA_return(stuid, sc), student_grade_return(stuid, sc),
	                          student_AD_return(stuid, sc)]
	
	return student_information_df


def race_lable(row):
	if row['EthnicityCode'] == 'Y':
		return 'Hispanic'
	if row['EthnicityCode'] == 'N' and int(row['RaceCode1']) == 100:
		return 'American Indian or Alaska'
	if row['EthnicityCode'] == 'N' and int(row['RaceCode1']) == 700:
		return 'White'
	if row['EthnicityCode'] == 'N' and int(row['RaceCode1']) == 600:
		return 'Black or African American'
	if row['EthnicityCode'] == 'N' and (199 <= int(row['RaceCode1']) <= 299):
		return 'Asian'
	if ['EthnicityCode'] == 'N' and int(row['RaceCode1']) == 400:
		return 'Filipino'
	if row['EthnicityCode'] == 'N' and (299 <= int(row['RaceCode1']) <= 399):
		return 'Native Hawaiian or Pacific Islander'
	if row['EthnicityCode'] == 'N' and row['RaceCode2'] != "":
		return 'Multi Racial'
	return 'Unknown'


def student_demographics(schoolcode):
	json_data = student_information_request("", schoolcode)
	
	flattened_json = [flatten_json(item) for item in json_data]
	df = pd.DataFrame(flattened_json)
	
	df['Race'] = df.apply(race_lable, axis=1)
	
	df = df[~df['InactiveStatusCode'].str.contains("I|N")]
	
	df.to_csv("school_data.csv")
	
	return df


def school_attendance_data(schoolcode):
	json_data = attendance_data_request(schoolcode)
	
	flattened_json = [flatten_json(item) for item in json_data]
	df = pd.DataFrame(flattened_json)
	# use test csv to avid repeted API calls
	# df = pd.read_csv("attendance_data_test_database.csv")
	
	data_list1 = []
	data_list2 = []
	for row in range(len(df)):
		# print(row)
		for column in range(len(df.columns)):
			# print(column, end= " ")
			if df.iloc[row, column] == '2023-2024':
				
				data_list1.append(df.iloc[row, 0])
				for i in range(10):
					data_list1.append(df.iloc[row, column + i])
				data_list2.append(data_list1[:])
				data_list1.clear()
	
	df2 = pd.DataFrame(data_list2,
	                   columns=["StudentID", "SchoolYear", "SchoolCode", "DaysEnrolled", "DaysPresent", "DaysAbsence",
	                            "DaysExcused", "DaysUnexcused", "DaysTardy", "DaysOfTruancy", "Days Suspended"])
	df2['Percent Absent'] = (df2['DaysPresent'] / df2['DaysEnrolled']) * 100
	df2['Percent Absent'] = df2['Percent Absent'].round(2)
	
	# df2.to_csv("attendance_data.csv")
	return df2


def school_data(schoolcode):
	school_data = []
	
	df_demo = student_demographics(schoolcode)
	df_att = school_attendance_data(schoolcode)
	
	race_list = ['White', 'Black or African American', 'Hispanic', 'Asian',
	             'American Indian or Alaska', 'Filipino',
	             'Native Hawaiian or Pacific Islander', 'Multi Racial']
	school_data_list = [df_demo.shape[0], df_demo['Gender'].value_counts()['F'], df_demo['Gender'].value_counts()['M']]
	try:
		school_data_list.append(df_demo['Grade'].value_counts()[3])
	except KeyError:
		school_data_list.append(0)
	try:
		school_data_list.append(df_demo['Grade'].value_counts()[4])
	except KeyError:
		school_data_list.append(0)
	try:
		school_data_list.append(df_demo['Grade'].value_counts()[5])
	except KeyError:
		school_data_list.append(0)
	try:
		school_data_list.append(df_demo['Grade'].value_counts()[6])
	except KeyError:
		school_data_list.append(0)
	try:
		school_data_list.append(df_demo['Grade'].value_counts()[7])
	except KeyError:
		school_data_list.append(0)
	try:
		school_data_list.append(df_demo['Grade'].value_counts()[8])
	except KeyError:
		school_data_list.append(0)
	
	for i in range(len(race_list)):
		if df_demo['Race'].eq(race_list[i]).any():
			school_data_list.append(df_demo['Race'].value_counts()[race_list[i]])
		else:
			school_data_list.append(0)
	
	school_data_list.append(df_demo['LanguageFluencyCode'].value_counts()["L"])
	school_data_list.append(df_demo['LanguageFluencyCode'].value_counts()["R"])
	
	df2 = pd.DataFrame(columns=['Total', 'Male,', 'Female', '3rd', '4th', '5th', '6th', '7th', '8th',
	                            'White', 'Black or African American', 'Hispanic', 'Asian',
	                            'American Indian or Alaska', 'Filipino',
	                            'Native Hawaiian or Pacific Islander', 'Multi Racial',
	                            'El', 'REFP'])
	df2.loc[0] = school_data_list
	
	school_data.append(df2)
	
	# df2.to_csv('school_stats.csv')
	
	# print(df2)
	
	df3 = df_demo.merge(df_att, on='StudentID')
	df3.drop_duplicates(subset=["StudentID"], keep='first', inplace=True)
	
	chron_abs = [len(df3[(df3["Percent Absent"] <= 90)]),
	             len(df3[(df3["Percent Absent"] <= 90) & (df3["Gender"] == "M")]),
	             len(df3[(df3["Percent Absent"] <= 90) & (df3["Gender"] == "F")]),
	             len(df3[(df3["Percent Absent"] <= 90) & (df3["Grade"] == 3)]),
	             len(df3[(df3["Percent Absent"] <= 90) & (df3["Grade"] == 4)]),
	             len(df3[(df3["Percent Absent"] <= 90) & (df3["Grade"] == 5)]),
	             len(df3[(df3["Percent Absent"] <= 90) & (df3["Grade"] == 6)]),
	             len(df3[(df3["Percent Absent"] <= 90) & (df3["Grade"] == 7)]),
	             len(df3[(df3["Percent Absent"] <= 90) & (df3["Grade"] == 8)])]
	
	for i in range(len(race_list)):
		if df3['Race'].eq(race_list[i]).any():
			chron_abs.append(len(df3[(df3["Percent Absent"] <= 90) & (df3["Race"] == race_list[i])]))
		else:
			chron_abs.append(0)
	chron_abs.append(len(df3[(df3["Percent Absent"] <= 90) & (df3["LanguageFluencyCode"] == "L")]))
	chron_abs.append(len(df3[(df3["Percent Absent"] <= 90) & (df3["LanguageFluencyCode"] == "R")]))
	
	df4 = pd.DataFrame(columns=['Total', 'Male,', 'Female', '3rd', '4th', '5th', '6th', '7th', '8th',
	                            'White', 'Black or African American', 'Hispanic', 'Asian',
	                            'American Indian or Alaska', 'Filipino',
	                            'Native Hawaiian or Pacific Islander', 'Multi Racial',
	                            'El', 'REFP'])
	df4.loc[0] = chron_abs
	
	
	df4['Total'] = df4['Total'] / df2['Total'] * 100
	df4['Male,'] = df4['Male,'] / df2['Male,'] * 100
	df4['Female'] = df4['Female'] / df2['Female'] * 100
	df4['6th'] = df4['3rd'] / df2['3rd'] * 100
	df4['6th'] = df4['4th'] / df2['4th'] * 100
	df4['6th'] = df4['5th'] / df2['5th'] * 100
	df4['6th'] = df4['6th'] / df2['6th'] * 100
	df4['7th'] = df4['7th'] / df2['7th'] * 100
	df4['8th'] = df4['8th'] / df2['8th'] * 100
	df4['White'] = df4['White'] / df2['White']
	df4['Black or African American'] = df4['Black or African American'] / df2['Black or African American'] * 100
	df4['Hispanic'] = df4['Hispanic'] / df2['Hispanic'] * 100
	df4['Asian'] = df4['Asian'] / df2['Asian'] * 100
	df4['American Indian or Alaska'] = df4['American Indian or Alaska'] / df2['American Indian or Alaska'] * 100
	df4['Filipino'] = df4['Filipino'] / df2['Filipino'] * 100
	df4['Native Hawaiian or Pacific Islander'] = df4['Native Hawaiian or Pacific Islander'] / df2['Native Hawaiian or ' \
	                                                                                              'Pacific Islander'] \
	                                             * 100
	df4['Multi Racial'] = df4['Multi Racial'] / df2['Multi Racial'] * 100
	df4['El'] = df4['El'] / df2['El'] * 100
	df4['REFP'] = df4['REFP'] / df2['REFP'] * 100
	
	school_data.append(df4)
	#print(df4)
	# df4.to_csv("attendanc_percentages.csv")
	return school_data


def school_test_data(SC, test, part):
	demo = student_demographics(SC)
	
	STAR_TEST_LIST_DF = pd.read_sql_query("""SELECT DISTINCT tst.TA FROM tst
	WHERE tst.ID = '""" + str(test) + """' AND tst.TA != '' """, aeries_connection())
	STAR_TEST_LIST_DF = STAR_TEST_LIST_DF[::-1]
	STAR_TEST_LIST = STAR_TEST_LIST_DF.TA.values.tolist()
	
	STAR_READING_DF_LIST = []
	data_totals = []
	df4 = pd.DataFrame(columns=['TA',
	                            'Total T',
	                            'Total P',
	                            'Male T',
	                            'Male P',
	                            'Female T',
	                            'Female P',
	                            '3rd T',
	                            '3rd P',
	                            '4th T',
	                            '4th P',
	                            '5th T',
	                            '5th P',
	                            '6th T',
	                            '6th P',
	                            '7th T',
	                            '7th P',
	                            '8th T',
	                            '8th P',
	                            'White T',
	                            'White P',
	                            'Black or African American T',
	                            'Black or African American P',
	                            'Hispanic T',
	                            'Hispanic P',
	                            'Asian T',
	                            'Asian P',
	                            'American Indian or Alaska T',
	                            'American Indian or Alaska P',
	                            'Filipino T',
	                            'Filipino P',
	                            'Native Hawaiian or Pacific Islander T',
	                            'Native Hawaiian or Pacific Islander P',
	                            'Multi Racial T',
	                            'Multi Racial P',
	                            'El T',
	                            'El P',
	                            'REFP T',
	                            'REFP P'])
	#print(STAR_TEST_LIST)
	for i in range(len(STAR_TEST_LIST)):
		data = pd.read_sql_query(
			"""SELECT PID,ID,TA,GR,SS,PC,OT FROM tst WHERE tst.ID = '""" + test + """' AND tst.TA = '"""
			+ STAR_TEST_LIST[i] + """' AND tst.pt = """ + str(part) + """""", aeries_connection())
		df3 = pd.merge(demo, data, left_on='StudentID', right_on='PID')
		STAR_READING_DF_LIST.append(df3)
		
		# STAR_READING_DF_LIST[i].to_csv(str(i) + str(STAR_TEST_LIST[i]) + "Star_reading_school_data.csv")
		
		data_totals.append(STAR_TEST_LIST[i])
		data_totals.append(STAR_READING_DF_LIST[i].shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("PC >= 40").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Gender == 'F'").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Gender == 'F' & PC >= 40").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Gender == 'M' ").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Gender == 'M' & PC >= 40").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Grade == 3").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Grade == 3 & PC >= 40").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Grade == 4").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Grade == 4 & PC >= 40").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Grade == 5").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Grade == 5 & PC >= 40").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Grade == 6").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Grade == 6 & PC >= 40").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Grade == 7").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Grade == 7 & PC >= 40").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Grade == 8").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Grade == 8 & PC >= 40").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Race == 'White'").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Race == 'White'& PC >= 40").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Race == 'Black or African American'").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Race == 'Black or African American' & PC >= 40").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Race == 'Hispanic'").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Race == 'Hispanic' & PC >= 40").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Race == 'Asian'").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Race == 'Asian' & PC >= 40").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Race == 'American Indian or Alaska'").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Race == 'American Indian or Alaska' & PC >= 40").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Race == 'Filipino'").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Race == 'Filipino' & PC >= 40").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Race == 'Native Hawaiian or Pacific Islander'").shape[0])
		data_totals.append(
			STAR_READING_DF_LIST[i].query("Race == 'Native Hawaiian or Pacific Islander' & PC >= 40").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Race == 'Multi Racial'").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("Race == 'Multi Racial' & PC >= 40").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("LanguageFluencyCode == 'L'").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("LanguageFluencyCode == 'L' & PC >= 40").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("LanguageFluencyCode == 'R'").shape[0])
		data_totals.append(STAR_READING_DF_LIST[i].query("LanguageFluencyCode == 'R' & PC >= 40").shape[0])
		
		df4.loc[i] = data_totals
		data_totals.clear()
		
		df5 = pd.DataFrame(columns=['TA', 'Total', 'Male', 'Female', '3rd', '4th', '5th', '6th', '7th', '8th',
		                            'White', 'Black or African American', 'Hispanic', 'Asian',
		                            'American Indian or Alaska', 'Filipino',
		                            'Native Hawaiian or Pacific Islander', 'Multi Racial',
		                            'El', 'REFP'])
		df5['TA'] = df4['TA']
		df5['Total'] = (df4['Total P'] / df4['Total T'] * 100).round(2)
		df5['Male'] = (df4['Male P'] / df4['Male T'] * 100).round(2)
		df5['Female'] = (df4['Female P'] / df4['Female T'] * 100).round(2)
		df5['3rd'] = (df4['3rd P'] / df4['3rd T'] * 100).round(2)
		df5['4th'] = (df4['4th P'] / df4['4th T'] * 100).round(2)
		df5['5th'] = (df4['5th P'] / df4['5th T'] * 100).round(2)
		df5['6th'] = (df4['6th P'] / df4['6th T'] * 100).round(2)
		df5['7th'] = (df4['7th P'] / df4['7th T'] * 100).round(2)
		df5['8th'] = (df4['8th P'] / df4['8th T'] * 100).round(2)
		df5['White'] = (df4['White P'] / df4['White T'] * 100).round(2)
		df5['Black or AfricanA American'] = (df4['Black or African American P'] / df4[
			'Black or African American T'] * 100).round(2)
		df5['Hispanic'] = (df4['Hispanic P'] / df4['Hispanic T'] * 100).round(2)
		df5['Asian'] = (df4['Asian P'] / df4['Asian T'] * 100).round(2)
		df5['American Indian or Alaska Native'] = (
				df4['American Indian or Alaska P'] / df4['American Indian or Alaska T']).round(2)
		df5['Filipino'] = (df4['Filipino P'] / df4['Filipino T'] * 100).round(2)
		df5['Native Hawaiian or Pacific Isalnder'] = (df4['Native Hawaiian or Pacific Islander P'] / df4[
			'Native Hawaiian or Pacific Islander P'] * 100).round(2)
		df5['Multi Racial'] = (df4['Multi Racial P'] / df4['Multi Racial T'] * 100).round(2)
		df5['El'] = (df4['El P'] / df4['El T'] * 100).round(2)
		df5['REFP'] = (df4['REFP P'] / df4['REFP T'] * 100).round(2)
	
	# df5.to_csv("Star_data.csv")
	df5 = df5.fillna(0)
	return df5


def star_test_data(SC):
	test_data_df_list = [school_test_data(SC, "STAR", 1), school_test_data(SC, "STAR", 2)]
	
	# print(test_data_df_list[0])
	# print(test_data_df_list[1])
	# print(test_data_df_list[2])
	# print(test_data_df_list[3])
	
	return test_data_df_list

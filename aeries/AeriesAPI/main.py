from APIfunctions import *

student_ID = 45993

SC = school_code(student_ID)

student_data = student_data(student_ID)
student_test_data = student_test_data_return(student_ID)


schoolcode = 12

school_data = school_data(schoolcode)

star_test_data = star_test_data(schoolcode)


#student_data[0].to_csv(str(student_ID) + "_information.csv")
#student_data[1].to_csv(str(student_ID) + "_enrollment.csv")
#student_data[2].to_csv(str(student_ID) + "_attendance.csv")
#student_data[3].to_csv(str(student_ID) + "_programs.csv")
#student_data[4].to_csv(str(student_ID) + "_gpa.csv")
#student_data[5].to_csv(str(student_ID) + "_grades.csv")
#student_data[6].to_csv(str(student_ID) + "_discipline.csv")
#student_test_data[0].to_csv(str(student_ID) + "_STAR_ELA.csv")
#student_test_data[1].to_csv(str(student_ID) + "_STAR_MATH.csv")
#student_test_data[2].to_csv(str(student_ID) + "_SBAC_ELA.csv")
#student_test_data[3].to_csv(str(student_ID) + "_SBAC_MATH.csv")

#school_data[0].to_csv(str(schoolcode) + " demographics.csv")
#school_data[1].to_csv(str(schoolcode) + " attendance.csv")

#star_test_data[0].to_csv(str(schoolcode) + ' Star_Reading.csv')
#star_test_data[1].to_csv(str(schoolcode) + ' Star_math.csv')
#test_data[2].to_csv(str(schoolcode) + ' SBAC_Reading.csv')
#test_data[3].to_csv(str(schoolcode) + ' SBAC_math.csv')


json = star_test_data[0].to_json()

print(json)

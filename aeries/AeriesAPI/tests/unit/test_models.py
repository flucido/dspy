import pytest
from src.models.student import Student
from src.models.school import School
from src.models.report import Report

def test_student_model():
    """Test Student model creation and methods."""
    student = Student(id=1, name="John Doe", grade="10", school_id=1, email="john@example.com", phone="123-456-7890")
    
    assert student.id == 1
    assert student.name == "John Doe"
    assert student.grade == "10"
    assert student.school_id == 1
    assert student.email == "john@example.com"
    assert student.phone == "123-456-7890"
    
    # Test to_dict method
    student_dict = student.to_dict()
    assert isinstance(student_dict, dict)
    assert student_dict["id"] == 1
    assert student_dict["name"] == "John Doe"
    
    # Test from_dict method
    new_student = Student.from_dict(student_dict)
    assert new_student.id == student.id
    assert new_student.name == student.name

def test_school_model():
    """Test School model creation and methods."""
    school = School(id=1, name="Test School", address="123 Main St", phone="123-456-7890")
    
    assert school.id == 1
    assert school.name == "Test School"
    assert school.address == "123 Main St"
    assert school.phone == "123-456-7890"
    
    # Test to_dict method
    school_dict = school.to_dict()
    assert isinstance(school_dict, dict)
    assert school_dict["id"] == 1
    assert school_dict["name"] == "Test School"
    
    # Test from_dict method
    new_school = School.from_dict(school_dict)
    assert new_school.id == school.id
    assert new_school.name == school.name

def test_report_model():
    """Test Report model creation and methods."""
    report = Report(id=1, name="Test Report", description="A test report", type="summary")
    
    assert report.id == 1
    assert report.name == "Test Report"
    assert report.description == "A test report"
    assert report.type == "summary"
    
    # Test to_dict method
    report_dict = report.to_dict()
    assert isinstance(report_dict, dict)
    assert report_dict["id"] == 1
    assert report_dict["name"] == "Test Report"
    
    # Test from_dict method
    new_report = Report.from_dict(report_dict)
    assert new_report.id == report.id
    assert new_report.name == report.name
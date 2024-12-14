from django.db import models
from django.contrib.auth.models import User


# Lecturer model
class Lecturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    University = models.CharField(max_length=100 ,null=True)
    Department = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.lecturer_name


# Student model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    University = models.CharField(max_length=100, null=True)
    Index_number = models.CharField(max_length=100, null=True)
    

    def __str__(self):
        return self.student_name


# Model representing a module
class Module(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True)  # Unique code for the module
    description = models.TextField(blank=True, null=True)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, related_name="modules")  
    
    def __str__(self):
        return f"{self.name} ({self.code})"

# Model representing an assignment within a module
class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField()
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="assignments")

    def __str__(self):
        return f"{self.title} - {self.module.name}"

# Model representing files uploaded by the lecturer for an assignment
class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="assignments/%Y/%m/%d/")  # Path where files will be stored
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for {self.assignment.title} uploaded at {self.uploaded_at}"

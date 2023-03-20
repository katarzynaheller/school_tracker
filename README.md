# SCHOOL TRACKER
RESTful app for tracking child's activity in educational institution built with Django REST Framework.

## Purpose:
App's purpose is to improve communication between parent and teacher. Included features provide ability to track calendar of events, meals, behaviour and overall summary. Can be extended to track marks, exams etc. (depending on needs)

## Custom permissions for different users:
App was designed with custom permissions for three different types of users: parent, teacher, admin(superuser). Parents can view details about ONLY own child, but teacher can view and edit. 
Each user (parent/teacher) is added by superuser (no signup option) and can log in on webpage. Superuser and teacher (as is_staff member) has own admin view. 


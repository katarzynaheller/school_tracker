# SCHOOL TRACKER
RESTful app for tracking child's activity in educational institution built with Django REST Framework.


## Purpose:
Project's purpose is to improve communication between parent and teacher. Included features provide ability to send/receive message to/from a teacher, track calendar of events, behaviour and overall summary. Funtionalities can be adjusted to the type of insitution. For example: meals can be tracked for nursery but marks/exams for school.

## Custom permissions for different users:
App was designed with custom permissions for three different types of users: parent, teacher, admin(superuser). Restrictions are implemented on different layers. For example:
- ChildDetailView: parents can view details about ONLY own child,
- ChildListView: teacher can access list view of his assigned group's members,
- MessageCreateView: sender can choose a child he is related to,
- MessageDetailView/MessageListView: user can access messages about child he is related to.
- ...

Each user (parent/teacher) is added by superuser (no signup option) and can log in on webpage. Superuser and teacher (as is_staff member) has own admin view. 

### Chats app:
Chats app is designed to send and track messages about a child. For security and data protection reasons several restrictions needed to be implemented. Parent can access only messages about his child/children. Teacher can view messages about children who are assigned to his group. Messages play role in complement everyday communication - when something needs to be discussed or mentioned. Here parent can also inform about absence or teacher about emergency situation.

CreateAPIView

DetailAPIView

ListAPIView

### Schedules app:

### Members app: 


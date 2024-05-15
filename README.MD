
# SQL Diagram Project

## Team Members
- Abdulrahman Alsaleh
- Michael Nair
- Lennart Martens

## Course
- Professor Taylor 
- CSCI 2541w (May 5)

## Project Overview
This project involves the creation and analysis of an SQL diagram. The diagram can be accessed [here](https://drawsql.app/teams/testing-84/diagrams/our-final-project).

## Normalization
Our SQL schema is in the Third Normal Form (3NF) because it meets the requirements of the First, Second, and Third Normal Forms:

1. **First Normal Form (1NF)**:
   - Each column in a table is atomic, meaning it cannot be further subdivided.
   - In our schema, each column contains only one value, satisfying 1NF.

2. **Second Normal Form (2NF)**:
   - The table is in 1NF, and all non-key attributes are fully dependent on the primary key.
   - All tables have a primary key defined, and non-key attributes depend only on the primary key, meeting 2NF.

3. **Third Normal Form (3NF)**:
   - The table is in 2NF, and all non-key attributes are not transitively dependent on the primary key.
   - Our schema removes transitive dependencies. For example, the "enrollment" table is split into "enrollment" and "sections" to eliminate transitive dependencies. The "students" table separates student-specific data from the "users" table.

## Visual Overview

### Log In Page
all images can be found in the pdf

### Alumni Dashboard
- View transcript page
- Edit info page

### Student Dashboard
(Note: The difference between Ph.D. and master's is that Ph.D. students can submit a thesis, and the requirements differ on the graduation requirements page.)
- Advising
- Advising hold
- Graduation requirements
- Form 1 (advising hold)
- Thesis (only visible to Ph.D. students)
- Register

### Graduate Secretary Dashboard
- Review applicants
- View current students
- View all students

### Admin Dashboard
- View users

### CAC Dashboard
- Review applications

### Applicant Dashboard
- Start application
- View application
- Add recommendations

### Faculty Dashboard
- View registration
- View my students

## Design Justification
To integrate our three projects, we used a dashboard framework allowing users to navigate between each web page individually created. This approach ensures that no page contains too much information.

### Process
1. **Identify User Types and Overlapping Needs**:
   - We identified all user types and their required web pages from phase one of our projects.

2. **Create Dashboards**:
   - We built dashboards for each user type, enabling easy and quick navigation between features and pages.

3. **Applicant Account**:
   - After creating an account, applicants can log in, see the progress of their application, and edit some information.

4. **Student Enrollment**:
   - Accepted applicants have their user type switched to Ph.D. or MS student, with their dashboard updating accordingly.

5. **Alumni Dashboard**:
   - Graduated students have a dashboard similar to students but with view-only permissions.

6. **Faculty/Advisor Integration**:
   - Faculty can view their classes, students, and advisees, and accept or decline forms from their dashboard.

7. **Graduate Secretary Dashboard**:
   - Graduate secretaries can see any student or applicant, manage applications, and assign grades or advisors.

## Work Breakdown
- **Lennart Martens**: Everything on APPS, routing errors, and styling.
- **Michael Nair**: Everything on REGS, admin controls, and styling.
- **Abdulrahman Alsaleh**: Everything on ADS, extra features, and styling.

## Extra Features
1. **Messaging**:
   - Users can message others with similar user types (e.g., alumni to alumni, master student to master student).

2. **Transcript Download**:
   - Users, faculty members, admin, and GS can download transcripts as PDFs.

3. **Internal Mailing**:
   - Users can send mail using the receiver's ID, with an ID lookup feature available.

### Screenshots
- Extra features include user messaging, transcript downloads, and internal mailing options.

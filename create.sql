-- Active: 1681758777577@@s23-group1.cxkvxjzjtgkl.us-east-1.rds.amazonaws.com@3306@university
use university;

SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
  uid CHAR(8) NOT NULL,
  user_type ENUM("applicant", "student_ms", "student_phd", "alumni", "faculty", "reviewer", "GS", "CAC", "admin") NOT NULL,
  fname VARCHAR(32) NOT NULL,
  minit CHAR,
  lname VARCHAR(32) NOT NULL,
  password VARCHAR(32) NOT NULL,
  address VARCHAR(64),
  birthday DATE,
  phone_no CHAR(10),
  ssn CHAR(9),
  email VARCHAR(32),
  PRIMARY KEY(uid)
);

DROP TABLE IF EXISTS applications;
CREATE TABLE applications (
  status ENUM("incomplete", "complete", "under review", "accept", "accept with aid", "reject") NOT NULL,
  uid CHAR(8),
  semester ENUM("fall", "spring", "summer"),
  s_year YEAR,
  degree_type ENUM("MS", "Phd"),
  prior_bac_deg_name VARCHAR(10),
  prior_bac_deg_gpa FLOAT(4),
  prior_bac_deg_major VARCHAR(20),
  prior_bac_deg_year YEAR,
  prior_bac_deg_university VARCHAR(20),
  GRE_verbal INT(10),
  GRE_year YEAR,
  GRE_quatitative INT(10),
  GRE_analytical_writing FLOAT(4),
  TOEFL_score INT(10),
  TOEFL_date YEAR,
  interest VARCHAR(50),
  experience VARCHAR(50),
  prior_ms_deg_name VARCHAR(10),
  prior_ms_deg_gpa FLOAT(4),
  prior_ms_deg_major VARCHAR(20),
  prior_ms_deg_year YEAR,
  prior_ms_deg_university VARCHAR(20),
  recieved_transcript BOOLEAN NOT NULL,
  PRIMARY KEY(uid,semester,s_year),
  FOREIGN KEY(uid) 
    REFERENCES users(uid) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS reviews;
CREATE TABLE reviews (
  review_id CHAR(8),
  student_id CHAR(8),
  p_semester ENUM("fall", "spring", "summer"),
  p_year YEAR,
  rev_rating ENUM("1", "2", "3", "4"),
  deficiency_course VARCHAR(50),
  reason_reject ENUM("A", "B", "C", "D", "E"),
  GAS_comment VARCHAR(100),
  decision ENUM("Reject", "Admit", "Admit with aid"),
  recom_advisor VARCHAR(30),
  PRIMARY KEY(review_id,student_id,p_year,p_semester),
  FOREIGN KEY(review_id)
    REFERENCES users(uid) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY(student_id,p_semester,p_year)
    REFERENCES applications(uid,semester,s_year) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS recommendations;
CREATE TABLE recommendations (
  uid CHAR(8),
  letterID ENUM("1", "2", "3"),
  contents VARCHAR(600),
  recommenderName VARCHAR(20),
  recommenderAffil VARCHAR(20),
  recommenderEmail VARCHAR(20),
  PRIMARY KEY(uid, letterID),
  FOREIGN KEY(uid)
    REFERENCES users(uid) ON DELETE CASCADE ON UPDATE CASCADE
  );

DROP TABLE IF EXISTS enrollment;
CREATE TABLE enrollment (
  student_uid CHAR(8) NOT NULL,
  cid VARCHAR(4) NOT NULL,
  section_id VARCHAR(8),
  grade ENUM("A", "A-", "B+", "B", "B-", "C+", "C", "F","IP") NOT NULL,
  finalized BOOL,
  PRIMARY KEY(student_uid, cid, section_id),
  FOREIGN KEY(student_uid) 
      REFERENCES users(uid) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY(cid, section_id) 
      REFERENCES sections(cid, section_id) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS sections;
CREATE TABLE sections (
  cid VARCHAR(4) NOT NULL,
  section_id VARCHAR(8),
  professor_uid CHAR(8) NOT NULL,
  year YEAR NOT NULL,
  semester ENUM("fall", "spring", "summer") NOT NULL,
  day CHAR NOT NULL,
  timeslot INTEGER NOT NULL,
  PRIMARY KEY(cid, section_id),
  FOREIGN KEY(cid)
    REFERENCES classes(cid) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY(professor_uid)
    REFERENCES users(uid) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS form1;
CREATE TABLE form1 (
  student_uid CHAR(8) NOT NULL,
  cid VARCHAR(4) NOT NULL,
  PRIMARY KEY(student_uid, cid),
  FOREIGN KEY(student_uid) REFERENCES users(uid) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY(cid) REFERENCES classes(cid) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS students;
CREATE TABLE students(
    s_id        CHAR(8) NOT NULL,
    Major       VARCHAR(50) not null,
    graduated   ENUM("yes", "no", "pending") NOT NULL,
    advisor_id  CHAR(8) not NULL,
    thesis      VARCHAR(8),
    thesis_text VARCHAR(500),
    form1       BOOLEAN not null,
    advising_hold       BOOLEAN not null,
    graduation_year int,

    PRIMARY KEY (s_id),
    Foreign Key (s_id) REFERENCES users(uid) ON DELETE CASCADE ON UPDATE CASCADE,
    Foreign Key (advisor_id) REFERENCES users(uid) ON DELETE CASCADE ON UPDATE CASCADE

);
DROP TABLE IF EXISTS classes;
CREATE TABLE classes (
  cid VARCHAR(4) NOT NULL,
  dept ENUM("CSCI", "ECE", "MATH") NOT NULL,
  class_number INTEGER NOT NULL,
  title VARCHAR(32) NOT NULL,
  credit_hours INTEGER,
  PRIMARY KEY(cid)
);

DROP TABLE IF EXISTS prereqs;
CREATE TABLE prereqs (
  class_cid VARCHAR(4) NOT NULL,
  prereq_cid VARCHAR(4) NOT NULL,
  PRIMARY KEY(class_cid, prereq_cid),
  FOREIGN KEY(class_cid)
    REFERENCES classes(cid) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (prereq_cid)
    REFERENCES classes(cid) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS messages;
CREATE TABLE messages (
  uid CHAR(8) NOT NULL,
  message VARCHAR(100) NOT NULL,
  DATE DATETIME NOT NULL,
  FOREIGN KEY(uid)
    REFERENCES users(uid) ON DELETE CASCADE ON UPDATE CASCADE
);
DROP TABLE IF EXISTS mail;
CREATE TABLE mail (
  uid CHAR(8) NOT NULL,
  message VARCHAR(100) NOT NULL,
  reciever CHAR(8) NOT NULL,
  DATE DATETIME NOT NULL,
  FOREIGN KEY(uid)
    REFERENCES users(uid) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY(reciever)
    REFERENCES users(uid) ON DELETE CASCADE ON UPDATE CASCADE
);
DROP TABLE IF EXISTS advising_hold;
CREATE TABLE advising_hold (
  student_uid CHAR(8) NOT NULL,
  cid VARCHAR(4) NOT NULL,
  PRIMARY KEY(student_uid, cid),
  FOREIGN KEY(student_uid) REFERENCES users(uid),
  FOREIGN KEY(cid) REFERENCES classes(cid)
);

SET FOREIGN_KEY_CHECKS=1;
INSERT INTO users (uid, user_type, fname, lname, PASSWORD) VALUES ("10", "GS", "firstname", "lastname", "GS");
INSERT INTO users (uid, user_type, fname, lname, PASSWORD) VALUES ("999", "faculty", "tacher", "lastname", "teacher");
INSERT INTO users (uid, user_type, fname, lname, PASSWORD) VALUES ("9999", "faculty", "teacher2", "teacher2", "teacher");

SELECT uid FROM users;
INSERT INTO users (uid, user_type, fname, lname, PASSWORD) VALUES ("9", "student_ms", "firstname", "lastname", "test");
INSERT INTO students(s_id, advisor_id ,Major, graduated, form1) VALUES ("9", "999" ,"CSCI", "no", 1);

-- required stuff for regs
INSERT INTO users(uid, user_type, fname, lname, password) values ("90000001", "faculty", "Bhagirath", "Narahari", "advisor");
insert into users(uid , user_type, fname, lname, password) values ("90000003", "faculty", "Brian", "Choi", "pass");
insert into users(uid , user_type, fname, lname, password) values ("90000004", "GS", "Michael", "Nair", "pass");
-- each semester has choi teaching 6212 and Narahari teaching 6461
-- more at bottom of doc

-- extra teachers to fill out course catalog
INSERT INTO users(uid, user_type, fname, lname, password) values ("11110000", "faculty", "first", "dummy", "pass");
INSERT INTO users(uid, user_type, fname, lname, password) values ("22220000", "faculty", "second", "dummy", "pass");
INSERT INTO users(uid, user_type, fname, lname, password) values ("33330000", "faculty", "third", "dummy", "pass");
INSERT INTO users(uid, user_type, fname, lname, password) values ("44440000", "faculty", "fourth", "dummy", "pass");


-- add classes
INSERT INTO classes VALUES (1,'CSCI',6221,'SW Paradigms',3);
INSERT INTO classes VALUES (2,'CSCI',6461,'Computer Architecture',3);
INSERT INTO classes VALUES (3,'CSCI',6212,'Algorithms',3);
INSERT INTO classes VALUES (4,'CSCI',6220,'Machine Learning',3);
INSERT INTO classes VALUES (5,'CSCI',6232,'Networks 1',3);
INSERT INTO classes VALUES (6,'CSCI',6233,'Networks 2',3);
INSERT INTO classes VALUES (7,'CSCI',6241,'Database 1',3);
INSERT INTO classes VALUES (8,'CSCI',6242,'Database 2',3);
INSERT INTO classes VALUES (9,'CSCI',6246,'Compilers',3);
INSERT INTO classes VALUES (10,'CSCI',6260,'Multimedia',3);
INSERT INTO classes VALUES (11,'CSCI',6251,'Cloud Computing',3);
INSERT INTO classes VALUES (12,'CSCI',6254,'SW Engineering',3);
INSERT INTO classes VALUES (13,'CSCI',6262,'Graphics 1',3);
INSERT INTO classes VALUES (14,'CSCI',6283,'Security 1',3);
INSERT INTO classes VALUES (15,'CSCI',6284,'Cryptography',3);
INSERT INTO classes VALUES (16,'CSCI',6286,'Network Security',3);
INSERT INTO classes VALUES (17,'CSCI',6325,'Algorithms 2',3);
INSERT INTO classes VALUES (18,'CSCI',6339,'Embedded Systems',3);
INSERT INTO classes VALUES (19,'CSCI',6384,'Cryptography 2',3);
INSERT INTO classes VALUES (20,'ECE',6241,'Communication Theory',3);
INSERT INTO classes VALUES (21,'ECE',6242,'Information Theory',2);
INSERT INTO classes VALUES (22,'MATH',6210,'Logic',2);


-- add prereqs
INSERT INTO prereqs VALUES (6,5);
INSERT INTO prereqs VALUES (8,7);
INSERT INTO prereqs VALUES (9,2);
INSERT INTO prereqs VALUES (9,3);
INSERT INTO prereqs VALUES (11,2);
INSERT INTO prereqs VALUES (12,1);
INSERT INTO prereqs VALUES (14,3);
INSERT INTO prereqs VALUES (15,3);
INSERT INTO prereqs VALUES (16,14);
INSERT INTO prereqs VALUES (16,5);
INSERT INTO prereqs VALUES (17,3);
INSERT INTO prereqs VALUES (18,2);
INSERT INTO prereqs VALUES (18,3);
INSERT INTO prereqs VALUES (19,15);


-- add sections
-- 2023 1
INSERT INTO sections VALUES ('1','1','11110000',2023,1,'M',1);
INSERT INTO sections VALUES ('2','2','90000001',2023,1,'T',1);
INSERT INTO sections VALUES ('3','3','90000003',2023,1,'W',1);
INSERT INTO sections VALUES ('5','4','11110000',2023,1,'M',3);
INSERT INTO sections VALUES ('6','5','11110000',2023,1,'T',3);
INSERT INTO sections VALUES ('7','6','11110000',2023,1,'W',3);
INSERT INTO sections VALUES ('8','7','11110000',2023,1,'R',3);
INSERT INTO sections VALUES ('9','8','22220000',2023,1,'T',1);
INSERT INTO sections VALUES ('11','9','22220000',2023,1,'M',3);
INSERT INTO sections VALUES ('12','10','22220000',2023,1,'M',1);
INSERT INTO sections VALUES ('10','11','22220000',2023,1,'R',3);
INSERT INTO sections VALUES ('13','12','22220000',2023,1,'W',3);
INSERT INTO sections VALUES ('14','13','22220000',2023,1,'T',3);
INSERT INTO sections VALUES ('15','14','33330000',2023,1,'M',3);
INSERT INTO sections VALUES ('16','15','33330000',2023,1,'W',3);
INSERT INTO sections VALUES ('19','16','33330000',2023,1,'W',1);
INSERT INTO sections VALUES ('20','17','44440000',2023,1,'M',3);
INSERT INTO sections VALUES ('21','18','44440000',2023,1,'T',3);
INSERT INTO sections VALUES ('22','19','44440000',2023,1,'W',3);
INSERT INTO sections VALUES ('18','20','44440000',2023,1,'R',2);

-- 2023 2
INSERT INTO sections VALUES ('1','21','11110000',2023,2,'M',1);
INSERT INTO sections VALUES ('2','22','90000001',2023,2,'T',1);
INSERT INTO sections VALUES ('3','23','90000003',2023,2,'W',1);
INSERT INTO sections VALUES ('5','24','11110000',2023,2,'M',3);
INSERT INTO sections VALUES ('6','25','11110000',2023,2,'T',3);
INSERT INTO sections VALUES ('7','26','11110000',2023,2,'W',3);
INSERT INTO sections VALUES ('8','27','11110000',2023,2,'R',3);
INSERT INTO sections VALUES ('9','28','22220000',2023,2,'T',1);
INSERT INTO sections VALUES ('11','29','22220000',2023,2,'M',3);
INSERT INTO sections VALUES ('12','30','22220000',2023,2,'M',1);
INSERT INTO sections VALUES ('10','31','22220000',2023,2,'R',3);
INSERT INTO sections VALUES ('13','32','22220000',2023,2,'W',3);
INSERT INTO sections VALUES ('14','33','22220000',2023,2,'T',3);
INSERT INTO sections VALUES ('15','34','33330000',2023,2,'M',3);
INSERT INTO sections VALUES ('16','35','33330000',2023,2,'W',3);
INSERT INTO sections VALUES ('19','36','33330000',2023,2,'W',1);
INSERT INTO sections VALUES ('20','37','44440000',2023,2,'M',3);
INSERT INTO sections VALUES ('21','38','44440000',2023,2,'T',3);
INSERT INTO sections VALUES ('22','39','44440000',2023,2,'W',3);
INSERT INTO sections VALUES ('18','40','44440000',2023,2,'R',2);

-- 2023 3
INSERT INTO sections VALUES ('1','41','11110000',2023,3,'M',1);
INSERT INTO sections VALUES ('2','42','90000001',2023,3,'T',1);
INSERT INTO sections VALUES ('3','43','90000003',2023,3,'W',1);
INSERT INTO sections VALUES ('5','44','11110000',2023,3,'M',3);
INSERT INTO sections VALUES ('6','45','11110000',2023,3,'T',3);
INSERT INTO sections VALUES ('7','46','11110000',2023,3,'W',3);
INSERT INTO sections VALUES ('8','47','11110000',2023,3,'R',3);
INSERT INTO sections VALUES ('9','48','22220000',2023,3,'T',1);
INSERT INTO sections VALUES ('11','49','22220000',2023,3,'M',3);
INSERT INTO sections VALUES ('12','50','22220000',2023,3,'M',1);
INSERT INTO sections VALUES ('10','51','22220000',2023,3,'R',3);
INSERT INTO sections VALUES ('13','52','22220000',2023,3,'W',3);
INSERT INTO sections VALUES ('14','53','22220000',2023,3,'T',3);
INSERT INTO sections VALUES ('15','54','33330000',2023,3,'M',3);
INSERT INTO sections VALUES ('16','55','33330000',2023,3,'W',3);
INSERT INTO sections VALUES ('19','56','33330000',2023,3,'W',1);
INSERT INTO sections VALUES ('20','57','44440000',2023,3,'M',3);
INSERT INTO sections VALUES ('21','58','44440000',2023,3,'T',3);
INSERT INTO sections VALUES ('22','59','44440000',2023,3,'W',3);
INSERT INTO sections VALUES ('18','60','44440000',2023,3,'R',2);

-- 2024 1
INSERT INTO sections VALUES ('1','61','11110000',2024,1,'M',1);
INSERT INTO sections VALUES ('2','62','90000001',2024,1,'T',1);
INSERT INTO sections VALUES ('3','63','90000003',2024,1,'W',1);
INSERT INTO sections VALUES ('5','64','11110000',2024,1,'M',3);
INSERT INTO sections VALUES ('6','65','11110000',2024,1,'T',3);
INSERT INTO sections VALUES ('7','66','11110000',2024,1,'W',3);
INSERT INTO sections VALUES ('8','67','11110000',2024,1,'R',3);
INSERT INTO sections VALUES ('9','68','22220000',2024,1,'T',1);
INSERT INTO sections VALUES ('11','69','22220000',2024,1,'M',3);
INSERT INTO sections VALUES ('12','70','22220000',2024,1,'M',1);
INSERT INTO sections VALUES ('10','71','22220000',2024,1,'R',3);
INSERT INTO sections VALUES ('13','72','22220000',2024,1,'W',3);
INSERT INTO sections VALUES ('14','73','22220000',2024,1,'T',3);
INSERT INTO sections VALUES ('15','74','33330000',2024,1,'M',3);
INSERT INTO sections VALUES ('16','75','33330000',2024,1,'W',3);
INSERT INTO sections VALUES ('19','76','33330000',2024,1,'W',1);
INSERT INTO sections VALUES ('20','77','44440000',2024,1,'M',3);
INSERT INTO sections VALUES ('21','78','44440000',2024,1,'T',3);
INSERT INTO sections VALUES ('22','79','44440000',2024,1,'W',3);
INSERT INTO sections VALUES ('18','80','44440000',2024,1,'R',2);

-- 2024 2
INSERT INTO sections VALUES ('1','81','11110000',2024,2,'M',1);
INSERT INTO sections VALUES ('2','82','90000001',2024,2,'T',1);
INSERT INTO sections VALUES ('3','83','90000003',2024,2,'W',1);
INSERT INTO sections VALUES ('5','84','11110000',2024,2,'M',3);
INSERT INTO sections VALUES ('6','85','11110000',2024,2,'T',3);
INSERT INTO sections VALUES ('7','86','11110000',2024,2,'W',3);
INSERT INTO sections VALUES ('8','87','11110000',2024,2,'R',3);
INSERT INTO sections VALUES ('9','88','22220000',2024,2,'T',1);
INSERT INTO sections VALUES ('11','89','22220000',2024,2,'M',3);
INSERT INTO sections VALUES ('12','90','22220000',2024,2,'M',1);
INSERT INTO sections VALUES ('10','91','22220000',2024,2,'R',3);
INSERT INTO sections VALUES ('13','92','22220000',2024,2,'W',3);
INSERT INTO sections VALUES ('14','93','22220000',2024,2,'T',3);
INSERT INTO sections VALUES ('15','94','33330000',2024,2,'M',3);
INSERT INTO sections VALUES ('16','95','33330000',2024,2,'W',3);
INSERT INTO sections VALUES ('19','96','33330000',2024,2,'W',1);
INSERT INTO sections VALUES ('20','97','44440000',2024,2,'M',3);
INSERT INTO sections VALUES ('21','98','44440000',2024,2,'T',3);
INSERT INTO sections VALUES ('22','99','44440000',2024,2,'W',3);
INSERT INTO sections VALUES ('18','100','44440000',2024,2,'R',2);

-- 2024 3
INSERT INTO sections VALUES ('1','101','11110000',2024,3,'M',1);
INSERT INTO sections VALUES ('2','102','90000001',2024,3,'T',1);
INSERT INTO sections VALUES ('3','103','90000003',2024,3,'W',1);
INSERT INTO sections VALUES ('5','104','11110000',2024,3,'M',3);
INSERT INTO sections VALUES ('6','105','11110000',2024,3,'T',3);
INSERT INTO sections VALUES ('7','106','11110000',2024,3,'W',3);
INSERT INTO sections VALUES ('8','107','11110000',2024,3,'R',3);
INSERT INTO sections VALUES ('9','108','22220000',2024,3,'T',1);
INSERT INTO sections VALUES ('11','109','22220000',2024,3,'M',3);
INSERT INTO sections VALUES ('12','110','22220000',2024,3,'M',1);
INSERT INTO sections VALUES ('10','111','22220000',2024,3,'R',3);
INSERT INTO sections VALUES ('13','112','22220000',2024,3,'W',3);
INSERT INTO sections VALUES ('14','113','22220000',2024,3,'T',3);
INSERT INTO sections VALUES ('15','114','33330000',2024,3,'M',3);
INSERT INTO sections VALUES ('16','115','33330000',2024,3,'W',3);
INSERT INTO sections VALUES ('19','116','33330000',2024,3,'W',1);
INSERT INTO sections VALUES ('20','117','44440000',2024,3,'M',3);
INSERT INTO sections VALUES ('21','118','44440000',2024,3,'T',3);
INSERT INTO sections VALUES ('22','119','44440000',2024,3,'W',3);
INSERT INTO sections VALUES ('18','120','44440000',2024,3,'R',2);




-- ADS enrollments (need to change advisor id for data) (ADD NARAHARI)

-- Narahari created above since he teaches classes

INSERT INTO users(uid, user_type, fname, lname, password) values ("90000002", "faculty", "Gabriel", "Parmer", "advisor");

insert into users(uid , user_type, fname, lname, password) values ("55555555", "student_ms", "Paul", "McCartney", "student");

insert into students(s_id ,Major, graduated, advisor_id) values ("55555555", "Computer Science", "no", "90000001");
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("55555555", "1", "1", "A", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("55555555", "3", "3", "A", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("55555555", "2", "2", "A", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("55555555", "5", "4", "A", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("55555555", "6", "5", "A", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("55555555", "7", "6", "B", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("55555555", "9", "8", "B", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("55555555", "13", "12", "B", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("55555555", "14", "13", "B", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("55555555", "8", "7", "B", 1);



insert into users(uid , user_type, fname, lname, password) values ("66666666", "student_ms", "George", "Harrison", "student");

insert into students(s_id ,Major, graduated, advisor_id) values ("66666666", "Computer Science", "no", "90000002");

insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("66666666", "21", "18", "C", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("66666666", "1", "1", "B", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("66666666", "2", "2", "B", 1);

insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("66666666", "3", "3", "B", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("66666666", "5", "4", "B", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("66666666", "6", "5", "B", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("66666666", "7", "6", "B", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("66666666", "8", "7", "B", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("66666666", "14", "13", "B", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("66666666", "15", "14", "B", 1);


insert into users(uid , user_type, fname, lname, password) values ("10000000", "student_phd", "Ringo", "Starr", "student");
insert into students(s_id ,Major, graduated, advisor_id) values ("10000000", "Computer Science", "no", "90000002");

insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("10000000", "1", "1", "A", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("10000000", "2", "2", "A", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("10000000", "3", "3", "A", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("10000000", "5", "4", "A", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("10000000", "6", "5", "A", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("10000000", "7", "6", "A", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("10000000", "8", "7", "A", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("10000000", "9", "8", "A", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("10000000", "10", "11", "A", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("10000000", "11", "9", "A", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("10000000", "12", "10", "A", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("10000000", "13", "12", "A", 1);

insert into users(uid , user_type, fname, lname, password) values ("77777777", "alumni", "Eric", "Clapton", "student");
insert into students(s_id ,Major, graduated, advisor_id, graduation_year) values ("77777777", "Computer Science", "yes", "90000002", 2014);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("77777777", "1", "1", "B", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("77777777", "3", "3", "B", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("77777777", "2", "2", "B", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("77777777", "5", "4", "B", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("77777777", "6", "5", "B", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("77777777", "7", "6", "B", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("77777777", "8", "7", "B", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("77777777", "16", "15", "A", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("77777777", "15", "14", "A", 1);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("77777777", "14", "13", "A", 1);

-- more requirements for regs starting state
insert into users(uid , user_type, fname, lname, password) values ("88888888", "student_ms", "Billie", "Holiday", "pass");
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("88888888", "2", "42", "IP", 0);
insert into enrollment(student_uid, cid, section_id, grade, finalized) values ("88888888", "3", "43", "IP", 0);
insert into users(uid , user_type, fname, lname, password) values ("99999999", "student_ms", "Diana", "Krall", "pass");

-- APPS starting state
INSERT INTO users(uid, user_type, fname, lname, ssn, password) VALUES ('12312312', 'applicant', 'John', 'Lennon', '111111111', 'pass');
INSERT INTO users(uid, user_type, fname, lname, ssn, password) VALUES ('66666665', 'applicant', 'Ringo', 'Jr', '222111111', 'pass');
INSERT INTO users(uid, user_type, fname, lname, ssn, password) VALUES ('98798798', 'reviewer', 'Tim', 'Wood', '987987987', 'pass');
INSERT INTO users(uid, user_type, fname, lname, ssn, password) VALUES ('87687687', 'reviewer', 'Rachel', 'Heller', '876876876', 'pass');

INSERT INTO applications(uid, semester, s_year, degree_type, status, prior_bac_deg_year, prior_bac_deg_name, prior_bac_deg_gpa, prior_bac_deg_major, prior_bac_deg_university, interest, experience) 
VALUES ('12312312', 'fall', 2023, 'MS', 'complete', 2022, 'BS', 4.0, 'CS', 'GWU', 'Quantum computing', 'none');
INSERT INTO applications(uid, semester, s_year, degree_type, status) VALUES ('66666665', 'fall', 2023, 'MS', 'incomplete');
INSERT INTO users(uid, user_type, fname, lname, password) VALUES ('12349876', 'admin', 'James', 'Taylor', 'rolyat');
INSERT INTO users(uid, user_type, fname, lname, ssn, password) VALUES ('76576576', 'CAC', 'Hellen', 'Keller', '765765765', 'pass');

INSERT INTO recommendations(uid, letterID, contents, recommenderName, recommenderAffil, recommenderEmail) VALUES ('12312312', '1', 'Cool dude', 'Jimmy', 'Friend', 'jimmy@gmail.com');
INSERT INTO recommendations(uid, letterID, contents, recommenderName, recommenderAffil, recommenderEmail) VALUES ('12312312', '2', 'Nice guy', 'Jack', 'Friend', 'jack@gmail.com');
INSERT INTO recommendations(uid, letterID, contents, recommenderName, recommenderAffil, recommenderEmail) VALUES ('12312312', '3', 'Pretty deece', 'John', 'Friend', 'john@gmail.com');
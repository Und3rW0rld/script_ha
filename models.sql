-- Limpiar las tablas en orden inverso al de creación para evitar errores de restricciones de claves foráneas
DROP TABLE IF EXISTS academic_file_record CASCADE;
DROP TABLE IF EXISTS academic_file_block CASCADE;
DROP TABLE IF EXISTS block_type CASCADE;
DROP TABLE IF EXISTS academic_file_period CASCADE;
DROP TABLE IF EXISTS study_plan_subject_period CASCADE;
DROP TABLE IF EXISTS period CASCADE;
DROP TABLE IF EXISTS study_plan_subject CASCADE;
DROP TABLE IF EXISTS typology CASCADE;
DROP TABLE IF EXISTS subject CASCADE;
DROP TABLE IF EXISTS uab CASCADE;
DROP TABLE IF EXISTS faculty CASCADE;
DROP TABLE IF EXISTS university_site CASCADE;
DROP TABLE IF EXISTS academic_file CASCADE;
DROP TABLE IF EXISTS student_admission CASCADE;
DROP TABLE IF EXISTS student CASCADE;
DROP TABLE IF EXISTS study_plan CASCADE;
DROP TABLE IF EXISTS curricular_program CASCADE;
DROP TABLE IF EXISTS curricular_area CASCADE;
DROP TABLE IF EXISTS study_level CASCADE;
DROP TABLE IF EXISTS admission_start_node CASCADE;
DROP TABLE IF EXISTS admission_subaccess CASCADE;
DROP TABLE IF EXISTS admission_access CASCADE;
DROP TABLE IF EXISTS school_type CASCADE;
DROP TABLE IF EXISTS municipality CASCADE;
DROP TABLE IF EXISTS state CASCADE;

-- Crear el schema si no existe
CREATE SCHEMA IF NOT EXISTS academic_history;

-- Usar el schema creado
SET search_path TO academic_history;

-- Limpiar la función y el trigger
DROP TRIGGER IF EXISTS trigger_update_students ON student;
DROP FUNCTION IF EXISTS update_timestamp;


-- 📌 Tabla: State (debe crearse antes de Municipality)
CREATE TABLE state (
    id_state UUID PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL
);

-- 📌 Tabla: Municipality (antes de Student Admission)
CREATE TABLE municipality (
    id_municipality UUID PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    id_state UUID REFERENCES state(id_state)
);

-- 📌 Tabla: School Type (antes de Student Admission)
CREATE TABLE school_type (
    id_school_type UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    academic_mode VARCHAR(50)
);

-- 📌 Tabla: Admission Access (antes de Student Admission)
CREATE TABLE admission_access (
    id_admission_access UUID PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL
);

-- 📌 Tabla: Admission Subaccess (antes de Student Admission)
CREATE TABLE admission_subaccess (
    id_admission_subaccess UUID PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL
);

-- 📌 Tabla: Admission Start Node (antes de Student Admission)
CREATE TABLE admission_start_node (
    id_admission_start_node UUID PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL
);

-- 📌 Tabla: Study Level (antes de Study Plan)
CREATE TABLE study_level (
    id_study_level UUID PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL
);

-- 📌 Tabla: Curricular Area (antes de Curricular Program)
CREATE TABLE curricular_area (
    id_curricular_area UUID PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL
);

-- 📌 Tabla: Curricular Program (antes de Study Plan)
CREATE TABLE curricular_program (
    id_curricular_program UUID PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    snies VARCHAR(20),
    id_curricular_area UUID REFERENCES curricular_area(id_curricular_area)
);

-- 📌 Tabla: University Site (antes de Faculty y Study Plan)
CREATE TABLE university_site (
    id_university_site UUID PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL
);

-- 📌 Tabla: Faculty (antes de UAB)
CREATE TABLE faculty (
    id_faculty UUID PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    id_university_site UUID REFERENCES university_site(id_university_site)
);

-- 📌 Tabla: UAB (antes de Subjects)
CREATE TABLE uab (
    id_uab UUID PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    id_faculty UUID REFERENCES faculty(id_faculty)
);

-- 📌 Tabla: Study Plan (antes de Student Admission)
CREATE TABLE study_plan (
    id_study_plan UUID PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    credits INT,
    agreement VARCHAR(50),
    id_study_level UUID REFERENCES study_level(id_study_level),
    id_curricular_program UUID REFERENCES curricular_program(id_curricular_program),
    id_faculty UUID REFERENCES faculty(id_faculty)
);

-- 📌 Tabla: Students (antes de Student Admission y Academic File)
CREATE TABLE student (
    id_student UUID PRIMARY KEY,
    legal_id_type VARCHAR(10),
    legal_id VARCHAR(20) UNIQUE NOT NULL,
    given_name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    birth_date DATE,
    legal_sex CHAR(1),
    gender VARCHAR(20),
    code VARCHAR(20) UNIQUE,
    username VARCHAR(50) UNIQUE,
    institutional_email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50),
    updated_by VARCHAR(50)
);

-- Crear Trigger para actualizar `updated_at`
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_students
BEFORE UPDATE ON student
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- 📌 Tabla: Student Admission (ahora sí puede crearse sin error)
CREATE TABLE student_admission (
    id_student_admission UUID PRIMARY KEY,
    id_student UUID REFERENCES student(id_student),
    id_municipality UUID REFERENCES municipality(id_municipality),
    social_stratum INT,
    id_school_type UUID REFERENCES school_type(id_school_type),
    school_graduation_year INT,
    pbm FLOAT,
    admission_score FLOAT,
    total_standard_score FLOAT,
    convocation VARCHAR(20),
    opening VARCHAR(20),
    id_admission_access UUID REFERENCES admission_access(id_admission_access),
    id_admission_subaccess UUID REFERENCES admission_subaccess(id_admission_subaccess),
    id_admission_start_node UUID REFERENCES admission_start_node(id_admission_start_node),
    id_study_plan UUID REFERENCES study_plan(id_study_plan)
);

-- 📌 Tabla: Academic File (después de Students)
CREATE TABLE academic_file (
    id_academic_file UUID PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    id_student UUID REFERENCES student(id_student),
    id_study_plan UUID REFERENCES study_plan(id_study_plan),
    id_student_admission UUID REFERENCES student_admission(id_student_admission)
);

-- 📌 Tabla: Subjects (después de UAB)
CREATE TABLE subject (
    id_subject UUID PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    credits INT,
    id_uab UUID REFERENCES uab(id_uab)
);

-- 📌 Tabla: Topology (antes de ser referenciada en Study Plan - Subject)
CREATE TABLE typology (
    id_typology UUID PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL
);

-- 📌 Tabla: Study Plan - Subject (después de Study Plan y Subject)
CREATE TABLE study_plan_subject (
    id_study_plan_subject UUID PRIMARY KEY,
    id_study_plan UUID REFERENCES study_plan(id_study_plan),
    id_subject UUID REFERENCES subject(id_subject),
    id_typology UUID REFERENCES typology(id_typology)
);

-- 📌 Tabla: Period (antes de ser referenciada en Study Plan Subject - Period)
CREATE TABLE period (
    id_period UUID PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL
);


-- 📌 Tabla: Study Plan Subject - Period (después de Study Plan Subject)
CREATE TABLE study_plan_subject_period (
    id_study_plan_subject_period UUID PRIMARY KEY,
    id_study_plan_subject UUID REFERENCES study_plan_subject(id_study_plan_subject),
    id_period UUID REFERENCES period(id_period),
    subject_group VARCHAR(50),
    activity_group VARCHAR(50),
    activity VARCHAR(50),
    principal_activity VARCHAR(50)
);

-- 📌 Tabla: Academic File Period (academic_file_period)
CREATE TABLE academic_file_period (
    id_academic_file_period UUID PRIMARY KEY,
    id_academic_file UUID REFERENCES academic_file(id_academic_file),
    id_period UUID REFERENCES period(id_period),
    cumulative_period_enroll INT,
    period_gpa FLOAT,
    cumulative_gpa FLOAT,
    enrolled_credits INT,
    studied_credits INT,
    approved_credits INT,
    cancelled_credits INT,
    failed_subjects INT,
    mandatory_core INT,
    mandatory_field INT,
    elective INT,
    optional_core INT,
    leveling INT,
    optional_field INT,
    degree_project INT,
    total_credit_quota INT,
    additional_credit_quota INT,
    available_credit_quota INT,
    study_credit_quota INT,
    dual_degree_credit_quota INT
);

-- 📌 Tabla: Block Type (academic_file_block_type)
CREATE TABLE block_type (
  id_block_type UUID PRIMARY KEY,
  code VARCHAR UNIQUE NOT NULL,
  description TEXT
);

-- 📌 Tabla: Academic file block (academic_file_block)
CREATE TABLE academic_file_block (
  id_academic_file_block UUID PRIMARY KEY,
  id_academic_file_period UUID REFERENCES academic_file_period(id_academic_file_period),
  id_block_type UUID REFERENCES block_type(id_block_type),
  block_date DATE,
  is_active BOOLEAN
);

-- 📌 Tabla: Academic File Record (academic_file_record)
CREATE TABLE academic_file_record (
    id_academic_file_record UUID PRIMARY KEY,
    id_academic_file_period UUID REFERENCES academic_file_period(id_academic_file_period),
    id_study_plan_subject_period UUID REFERENCES study_plan_subject_period(id_study_plan_subject_period),
    ind VARCHAR(10),
    type VARCHAR(20),
    alphabetical_score VARCHAR(10),
    score FLOAT,
    cancelled VARCHAR(10),
    blocked VARCHAR(10),
    closed VARCHAR(10),
    with_academic_validity VARCHAR(10),
    total_study_times INT
);
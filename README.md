
# Academic History Data Loader (Proyecto HA)

Este script permite cargar toda la estructura de datos del esquema `academic_history` (HA) junto a las dependencias de seguridad (`security`) y transversales (`transversal`).

La ejecución debe realizarse siguiendo el **orden específico** de carpetas para garantizar la correcta resolución de claves foráneas y relaciones entre entidades.

---

## 📁 Estructura del Proyecto

Puedes encontrar los scripts organizados por entidad en carpetas individuales. Un ejemplo de la estructura es:

```
├── Municipality/
├── Period/
├── SchoolType/
├── State/
├── Student/
├── StudentAdmission/
├── StudyLevel/
├── StudyPlan/
├── StudyPlanSubject/
├── StudyPlanSubjectPeriod/
├── Subject/
├── Typology/
├── Uab/
├── UniversitySite/
├── constants.py
├── models.sql
```

---

## 🧾 Orden de ejecución recomendado junto con la instrucción select para su posterior prueba/visualización

1. `State`  
   `SELECT * FROM academic_history.state;`

2. `Municipality`  
   `SELECT * FROM academic_history.municipality;`

3. `SchoolType`  
   `SELECT * FROM academic_history.school_type;`

4. `AdmissionAccess`  
   `SELECT * FROM academic_history.admission_access;`

5. `AdmissionSubaccess`  
   ⚠️ Se regeneraron manualmente algunos códigos.  
   `SELECT * FROM academic_history.admission_subaccess;`

6. `AdmissionStartNode`  
   ⚠️ Se encontraron códigos duplicados en campos que deberían ser únicos.  
   `SELECT * FROM academic_history.admission_start_node;`

7. `StudyLevel`  
   `SELECT * FROM academic_history.study_level;`

8. `CurricularAreas`  
   ❌ No se recibió la data.  
   Se crea un área curricular comodín.  
   `SELECT * FROM academic_history.curricular_area;`

9. `CurricularPrograms`  
   ✅ Depende de las áreas curriculares.  
   `SELECT * FROM academic_history.curricular_program;`

10. `UniversitySite`  
    `SELECT * FROM academic_history.university_site;`

11. `Faculty`  
    `SELECT * FROM academic_history.faculty;`

12. `Uab`  
    ⚠️ Los códigos de UAB no están presentes en las facultades.  
    `SELECT * FROM academic_history.uab;`

13. `StudyPlan`  
    `SELECT * FROM academic_history.study_plan;`

14. `Student`  
    Se ejecuta `main.py`. Incluye creación en:
    - `academic_history.student`
    - `security.secur_user`
    - `security.secur_person`
    - `security.secur_user_level_role`  

    ⚠️ Muchos estudiantes no tenían `username` (campo obligatorio). Fueron exportados a un `.txt`.

    ⚠️ Asegúrate de tener el siguiente registro para los tipos de documento:
    ```sql
    INSERT INTO transversal.trans_type_legal_id
    ("name", abbreviation, is_of_legal_age, created_by, updated_by)
    VALUES
    ('OTRO', 'OT', false, 'e11a3bf5-3ea4-44bd-8aae-0b67beb67b1d', 'e11a3bf5-3ea4-44bd-8aae-0b67beb67b1d');
    ```

    Verifica:
    ```sql
    SELECT * FROM academic_history.student;
    SELECT * FROM security.secur_user;
    SELECT * FROM security.secur_person;
    ```

15. `StudentAdmission`  
    ⚠️ No incluye `total_standart_score`.  
    `SELECT * FROM academic_history.student_admission;`

16. `AcademicFile`  
    `SELECT * FROM academic_history.academic_file;`

17. `Subject`  
    ⚠️ No hay campo para vincular directamente con `UAB`, se usa `"99999"` como valor por defecto.  
    `SELECT * FROM academic_history.subject;`

18. `Typology`  
    `SELECT * FROM academic_history.typology;`

19. `StudyPlanSubject`  
    `SELECT * FROM academic_history.study_plan_subject;`

20. `Period`  
    `SELECT * FROM academic_history.period;`

21. `StudyPlanSubjectPeriod`  
    ⚠️ Verificar manejo de los grupos.  
    `SELECT * FROM academic_history.study_plan_subject_period;`

22. `AcademicFilePeriod` El academic file period se genera en el siguiente paso 
    ⚠️ Algunos créditos se asumen como `0` por ausencia de datos.  
    `SELECT * FROM academic_history.academic_file_period;`

22. `AcademicFilePeriod`, `BlockType`, `AcademicFileBlock` (se ejecutan juntos)  
    ```sql
    SELECT * FROM academic_history.academic_file_period;
    SELECT * FROM academic_history.block_type;
    SELECT * FROM academic_history.academic_file_block;
    ```

23. `AcademicFileRecord`  
    ⚠️ No hay archivos `.csv`. Se provee el archivo `.py` con la lógica para generar las queries.

---

## ⚠️ Nota Importante sobre la data

Durante la revisión de los archivos CSV y la ejecución de scripts:

- Se detectaron **códigos duplicados en campos que deben ser únicos** (como códigos de nodos de admisión, planes de estudio, estudiantes, etc.).
- Se recomienda realizar una validación previa sobre los campos únicos antes de ejecutar los inserts masivos.
- Se han aplicado `ON CONFLICT DO NOTHING` en la mayoría de inserts para prevenir errores por duplicidad, pero esto **puede ocultar datos incorrectos o redundantes si no se revisan previamente**.
- Se debe ejecutar el archivo .py en la carpeta correspondiente a la entidad, a menos que exista un main.py que crea varias entidades a la vez
---

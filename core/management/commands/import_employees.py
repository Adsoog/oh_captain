import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from apps.accounts.models import CaptainUser
from apps.rrhh.models.employee_models import Employee
from core.models import Department, Area

class Command(BaseCommand):
    help = "Importar empleados desde un archivo Excel y asignarlos a áreas, departamentos y grupos."

    def handle(self, *args, **kwargs):
        # Ruta del archivo Excel
        file_path = os.path.join(os.path.dirname(__file__), 'BD_COLABORADORES_PROCESADO.xlsx')
        print(f"Ruta del archivo: {file_path}")

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"El archivo '{file_path}' no existe."))
            return

        # Leer el archivo Excel
        data = pd.read_excel(file_path)

        # 1ª PASADA: Crear usuarios y empleados
        for _, row in data.iterrows():
            username = row['USUARIO']
            password = str(row['DNI'])

            # Concatenar nombres y apellidos correctamente
            first_name = f"{row['PRIMER_NOMBRE']} {row['SEGUNDO_NOMBRE']}".strip()
            last_name = f"{row['APELLIDO_PATERNO']} {row['APELLIDO_MATERNO']}".strip()

            # Asegurar que los campos no sean NaN
            first_name = first_name if first_name != "nan" else ""
            last_name = last_name if last_name != "nan" else ""

            # Crear o actualizar usuario
            user, _ = CaptainUser.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'is_active': True,
                    'user_type': CaptainUser.UserType.EMPLOYEE,
                }
            )
            if not user.check_password(password):
                user.set_password(password)
                user.save()

            # Crear o actualizar empleado sin asignar aún área y departamento
            Employee.objects.update_or_create(
                user=user,
                defaults={
                    'dni': row['DNI'],
                    'first_name': row['PRIMER_NOMBRE'],
                    'second_name': row['SEGUNDO_NOMBRE'] if pd.notna(row['SEGUNDO_NOMBRE']) else "",
                    'paternal_surname': row['APELLIDO_PATERNO'],
                    'maternal_surname': row['APELLIDO_MATERNO'] if pd.notna(row['APELLIDO_MATERNO']) else "",
                    'position': row['CARGO'],
                    'headquarters': row['SEDE'],
                    'area': None,
                    'department': None
                }
            )

        self.stdout.write(self.style.SUCCESS("Usuarios y empleados creados o actualizados."))

        # 2ª PASADA: Asignar área, departamento y grupos
        for _, row in data.iterrows():
            username = row['USUARIO']
            user = CaptainUser.objects.get(username=username)
            employee = Employee.objects.get(user=user)

            # Asignar área
            area_name = str(row['AREA']).strip() if pd.notna(row['AREA']) else None
            if area_name and area_name.lower() != "nan":
                area, _ = Area.objects.get_or_create(name=area_name)
                employee.area = area

                # Crear grupo basado en área
                area_group, _ = Group.objects.get_or_create(name=f"AREA_{area.name.upper()}")
                user.groups.add(area_group)

            # Asignar departamento
            department_name = str(row['DEPARTAMENTO']).strip() if pd.notna(row['DEPARTAMENTO']) else None
            if department_name and department_name.lower() != "nan":
                cod = department_name.replace(" ", "_").upper()
                department, _ = Department.objects.get_or_create(name=department_name, defaults={'cod': cod})
                employee.department = department

                # Crear grupo basado en departamento
                dept_group, _ = Group.objects.get_or_create(name=f"DEP_{department.name.upper()}")
                user.groups.add(dept_group)

            # Guardar cambios en empleado
            employee.save()

            # Asignar al grupo "Observadores" (todos los empleados lo tienen)
            observadores_group, _ = Group.objects.get_or_create(name="Observadores")
            user.groups.add(observadores_group)

        self.stdout.write(self.style.SUCCESS("Áreas, departamentos y grupos asignados correctamente."))
        
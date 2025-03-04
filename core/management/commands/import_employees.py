import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from apps.accounts.models import CaptainUser
from apps.rrhh.models.employee_models import Employee
from core.models import Department, Area

class Command(BaseCommand):
    help = 'Import employees from xls file and add groups dynamically'

    def handle(self, *args, **kwargs):
        # Ajusta el nombre del archivo según tu carpeta
        file_path = os.path.join(os.path.dirname(__file__), 'BD_COLABORADORES_PROCESADO_SIN_TILDES.xlsx')
        print(f"Ruta del archivo: {file_path}")

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"El archivo '{file_path}' no existe."))
            return

        data = pd.read_excel(file_path)

        # 1ª pasada: crear usuarios y empleados (básicos)
        for _, row in data.iterrows():
            username = row['USUARIO']
            password = str(row['DOI'])
            first_name = row['NOMBRE']
            last_name = row['APELLIDO']

            # Crear/actualizar usuario
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

            # Crear/actualizar empleado sin área ni departamento todavía
            Employee.objects.update_or_create(
                user=user,
                defaults={
                    'dni': row['DOI'],
                    'position': row['CARGO'],
                    'headquarters': row['SEDE'],
                }
            )

        self.stdout.write(self.style.SUCCESS('Usuarios y empleados creados o actualizados.'))

        # 2ª pasada: asignar área, departamento y grupos
        for _, row in data.iterrows():
            username = row['USUARIO']
            user = CaptainUser.objects.get(username=username)
            employee = Employee.objects.get(user=user)

            # Asignar área
            area_name = row['AREA']
            if pd.notna(area_name) and isinstance(area_name, str) and area_name.strip():
                area, _ = Area.objects.get_or_create(name=area_name.strip())
                employee.area = area
            else:
                employee.area = None  # o deja lo que tuviera antes

            # Asignar departamento
            department_name = row['DEPARTAMENTO']
            if pd.notna(department_name) and isinstance(department_name, str) and department_name.strip():
                department_name_clean = department_name.strip()
                cod = department_name_clean.replace(" ", "_").upper()

                # Creamos u obtenemos el Department, asignando el cod
                department, created = Department.objects.get_or_create(
                    name=department_name_clean,
                    defaults={
                        'cod': cod
                    }
                )
                if created:
                    print(f"Departamento creado: {department.name} (cod={department.cod})")
                else:
                    print(f"Departamento encontrado: {department.name} (cod={department.cod})")

                employee.department = department
            else:
                self.stdout.write(
                    self.style.WARNING(f"Departamento inválido para usuario {username}: {department_name}")
                )
                employee.department = None

            # Guardar la asignación al Empleado
            employee.save()

            # Asignar grupos según departamento (si existe) y área (si existe)
            if employee.department:
                dept_group, _ = Group.objects.get_or_create(name=employee.department.name.upper())
                user.groups.add(dept_group)

            if employee.area:
                area_group, _ = Group.objects.get_or_create(name=employee.area.name.upper())
                user.groups.add(area_group)

            # Agregar al grupo Observadores (todo empleado pertenece)
            observadores_group, _ = Group.objects.get_or_create(name="Observadores")
            user.groups.add(observadores_group)

        self.stdout.write(self.style.SUCCESS('Áreas, departamentos y grupos asignados correctamente.'))


import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from apps.accounts.models import CaptainUser
from apps.rrhh.models.employee_models import Employee
from core.models import Department, Area

class Command(BaseCommand):
    help = 'Import employees from xls file and add groups dynamically'

    def handle(self, *args, **kwargs):
        # Ajusta el nombre del archivo según tu carpeta
        file_path = os.path.join(os.path.dirname(__file__), 'BD_COLABORADORES_PROCESADO_SIN_TILDES.xlsx')
        print(f"Ruta del archivo: {file_path}")

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"El archivo '{file_path}' no existe."))
            return

        data = pd.read_excel(file_path)

        # 1ª pasada: crear usuarios y empleados (básicos)
        for _, row in data.iterrows():
            username = row['USUARIO']
            password = str(row['DOI'])
            first_name = row['NOMBRE']
            last_name = row['APELLIDO']

            # Crear/actualizar usuario
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

            # Crear/actualizar empleado sin área ni departamento todavía
            Employee.objects.update_or_create(
                user=user,
                defaults={
                    'dni': row['DOI'],
                    'position': row['CARGO'],
                    'headquarters': row['SEDE'],
                }
            )

        self.stdout.write(self.style.SUCCESS('Usuarios y empleados creados o actualizados.'))

        # 2ª pasada: asignar área, departamento y grupos
        for _, row in data.iterrows():
            username = row['USUARIO']
            user = CaptainUser.objects.get(username=username)
            employee = Employee.objects.get(user=user)

            # Asignar área
            area_name = row['AREA']
            if pd.notna(area_name) and isinstance(area_name, str) and area_name.strip():
                area, _ = Area.objects.get_or_create(name=area_name.strip())
                employee.area = area
            else:
                employee.area = None  # o deja lo que tuviera antes

            # Asignar departamento
            department_name = row['DEPARTAMENTO']
            if pd.notna(department_name) and isinstance(department_name, str) and department_name.strip():
                department_name_clean = department_name.strip()
                cod = department_name_clean.replace(" ", "_").upper()

                # Creamos u obtenemos el Department, asignando el cod
                department, created = Department.objects.get_or_create(
                    name=department_name_clean,
                    defaults={
                        'cod': cod
                    }
                )
                if created:
                    print(f"Departamento creado: {department.name} (cod={department.cod})")
                else:
                    print(f"Departamento encontrado: {department.name} (cod={department.cod})")

                employee.department = department
            else:
                self.stdout.write(
                    self.style.WARNING(f"Departamento inválido para usuario {username}: {department_name}")
                )
                employee.department = None

            # Guardar la asignación al Empleado
            employee.save()

            # Asignar grupos según departamento (si existe) y área (si existe)
            if employee.department:
                dept_group, _ = Group.objects.get_or_create(name=employee.department.name.upper())
                user.groups.add(dept_group)

            if employee.area:
                area_group, _ = Group.objects.get_or_create(name=employee.area.name.upper())
                user.groups.add(area_group)

            # Agregar al grupo Observadores (todo empleado pertenece)
            observadores_group, _ = Group.objects.get_or_create(name="Observadores")
            user.groups.add(observadores_group)

        self.stdout.write(self.style.SUCCESS('Áreas, departamentos y grupos asignados correctamente.'))
        
from django.shortcuts import render, get_object_or_404, redirect
from apps.rrhh.forms.hierarchy_forms import EmployeeHierarchyForm
from apps.rrhh.models.employee_models import Employee

def employee_hierarchy(request):
    employees = Employee.objects.all().order_by('tree_id', 'lft')
    return render(request, 'rrhh/hierarchy/employee_hierarchy_list.html', {'employees': employees})

def assign_hierarchy(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        parent_id = request.POST.get('parent_id')
        if parent_id:
            parent = Employee.objects.get(id=parent_id)
            employee.parent = parent
            employee.save()
            print(f"Jefe asignado a {employee.first_name} {employee.paternal_surname}: {parent.first_name} {parent.paternal_surname}")
        else:
            employee.parent = None
            employee.save()
            print(f"Jefe eliminado para {employee.first_name} {employee.paternal_surname}")

        return redirect('employee_hierarchy')

    employees = Employee.objects.exclude(id=employee_id)
    return render(request, 'rrhh/hierarchy/assign_hierarchy.html', {'employee': employee, 'employees': employees})

def get_direct_subordinates(employee):
    # Obtener solo los subordinados directos (sin entrar en jerarquías más profundas)
    return list(employee.get_children())

def get_indirect_subordinates(employee):
    # Obtener subordinados indirectos (subordinados de los subordinados directos)
    direct_subordinates = get_direct_subordinates(employee)
    indirect_subordinates = []
    for subordinate in direct_subordinates:
        indirect_subordinates.extend(get_direct_subordinates(subordinate))
    return indirect_subordinates

def get_bosses(employee):
    bosses = []
    if employee.parent:
        bosses.append(employee.parent)
        # Obtener los jefes superiores recursivamente
        bosses.extend(get_bosses(employee.parent))
    return bosses

def get_same_level_colleagues(employee):
    # Obtener subordinados directos del jefe directo (padre)
    if employee.parent:
        return [subordinate for subordinate in get_direct_subordinates(employee.parent) if subordinate != employee]
    return []


def employee_hierarchy_detail(request, employee_id):
    # Obtener el empleado por su ID
    employee = get_object_or_404(Employee, id=employee_id)

    # Obtener todos los jefes superiores (recursivamente)
    all_bosses = get_bosses(employee)

    # Separar el jefe directo (el primer jefe en la lista) y los jefes superiores
    direct_boss = all_bosses[0] if all_bosses else None
    superior_bosses = all_bosses[1:]

    # Obtener subordinados directos e indirectos
    direct_subordinates = get_direct_subordinates(employee)
    indirect_subordinates = get_indirect_subordinates(employee)

    # Obtener compañeros de mismo nivel
    same_level_colleagues = get_same_level_colleagues(employee)

    # Pasar la información a la plantilla
    return render(request, 'rrhh/hierarchy/employee_hierarchy_detail.html', {
        'employee': employee,
        'direct_boss': direct_boss,
        'superior_bosses': superior_bosses,
        'direct_subordinates': direct_subordinates,
        'indirect_subordinates': indirect_subordinates,
        'same_level_colleagues': same_level_colleagues,
    })

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.utils import timezone
from apps.commercial.models.proforma_models import Proforma, Equipment
from apps.planning.models.workorder_models import WorkOrder


@receiver(post_save, sender=Proforma)
def initial_work_order(sender, instance, created, **kwargs):
    print(f"Se activó la señal post_save para Proforma id={instance.id}")
    if created:
        print("La Proforma fue creada, no se procesa la orden de trabajo.")
    else:
        if instance.status == 'accepted':
            print(f"La Proforma id={instance.id} está en estado 'accepted'")
            if not instance.work_orders.exists():
                orden = WorkOrder.objects.create(
                    proforma=instance,
                    planned_date=timezone.now()
                )
                orden.equipments.set(instance.equipments.all())
                orden.save()
                print(f"Orden de trabajo creada para Proforma id={instance.id}")
            else:
                print(f"Ya existe una orden de trabajo para la Proforma id={instance.id}")
        else:
            print("Pues valio madres")


@receiver(m2m_changed, sender=WorkOrder.equipments.through)
def reasignar_equipos_removidos(sender, instance, action, pk_set, **kwargs):
    if action == 'post_remove' and pk_set:
        equipos_removidos = Equipment.objects.filter(pk__in=pk_set)
        nueva_orden = WorkOrder.objects.create(
            proforma=instance.proforma,
            planned_date=timezone.now()
        )
        nueva_orden.equipments.set(equipos_removidos)
        nueva_orden.save()

@receiver(post_save, sender=Equipment)
@receiver(post_save, sender=AdditionalCost)
@receiver(post_delete, sender=Equipment)
@receiver(post_delete, sender=AdditionalCost)
def update_proforma_total(sender, instance, **kwargs):
    if instance.proforma and not getattr(instance, 'skip_update', False):
        instance.proforma.save()
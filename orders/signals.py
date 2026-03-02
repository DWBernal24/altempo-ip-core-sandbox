from django.db import transaction
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver

from core.models import Notification
from utils.email import send_email_basic

from .models import Order


def sendEmailNotification(
    instance: Order,
    event: str,
    redirect_link: str = "",
    values: dict = None,
    detail: str = "",
):
    """
    Send notification to user with values for frontend translation.

    Args:
      instance: Order instance
      event: Notification type constant
      redirect_link: URL for notification redirect
      values: Dictionary of values to be used in frontend translation
      detail: Additional detail text
    """
    if values is None:
        values = {}

    # Add common order values
    values.update(
        {
            "order_number": instance.order_number or "",
            "order_id": str(instance.id),
        }
    )

    notification = Notification.objects.create(
        title="",  # Title will be translated in frontend
        message="",  # Message will be translated in frontend
        type=event,
        user=instance.user_profile.user,
        redirect_link=redirect_link,
        values=values,
        detail=detail,
    )
    notification.save()


@receiver(pre_save, sender=Order)
def order_pre_save(sender, instance: Order, **kwargs):
    """
    Antes de guardar: compara el status previo vs el nuevo.
    Guarda en atributos temporales para usarlos en post_save.
    """
    # Si no hay PK, es creación (todavía no existe en DB)
    if not instance.pk:
        # En tu modelo, save() pone un default "CONCEPT_DEFINED" si no viene status.
        # Queremos notificar también el status inicial tras crear.
        instance._was_created = True
        instance._old_status = None
        instance._new_status = (
            instance.status
        )  # puede llegar vacío aquí; el default se aplica en save()
        return

    # Actualización: cargar el anterior para comparar
    try:
        old = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        instance._was_created = True
        instance._old_status = None
        instance._new_status = instance.status
        return

    instance._was_created = False
    instance._old_status = old.status
    instance._new_status = instance.status
    instance._status_changed = old.status != instance.status


@receiver(post_save, sender=Order)
def order_post_save(sender, instance: Order, created: bool, **kwargs):
    """
    Después de guardar: dispara efectos una vez confirmado el commit.
    - Si es creación: emite evento de status inicial.
    - Si es actualización con cambio de status: emite evento de transición.
    """
    was_created = getattr(instance, "_was_created", created)
    old_status = getattr(instance, "_old_status", None)
    new_status = getattr(instance, "_new_status", instance.status)
    status_changed = getattr(instance, "_status_changed", False)

    def fire_events():
        # Aquí coloca tu lógica real: encolar tareas, enviar notificaciones, webhooks, etc.
        # Ejemplos (reemplaza los prints por tus integraciones):
        if was_created:
            sendEmailNotification(
                instance=instance,
                event=Notification.BRIEF_INITIATED,
                redirect_link=f"/orders/{instance.order_number}/briefing",
                values={},
            )
            # ejemplo: notify_initial_status(instance.id, new_status)
        elif status_changed:
            print(
                f"[ORDER EVENT] Order {instance.id} status: {old_status} -> {new_status}"
            )
            if new_status == "MUSICIANS_SELECTED":
                sendEmailNotification(
                    instance=instance,
                    event=Notification.TALENT_RECOMMENDED,
                    redirect_link=f"/orders/{instance.order_number}/musicians",
                    values={},
                )

            if new_status in ("LOGISTICS_PROPOSAL_ACCEPTED", "REJECTED"):
                sendEmailNotification(
                    instance=instance,
                    event=Notification.STRATEGY_ADJUSTMENT_REQUESTED,
                    redirect_link=f"/orders/{instance.order_number}/strategy",
                    values={"status": new_status},
                )

            if new_status == "ORDER_CONFIRMED":
                sendEmailNotification(
                    instance=instance,
                    event=Notification.MUSICIANS_CONFIRMED,
                    redirect_link=f"/orders/{instance.order_number}/scouting",
                    values={},
                )

            if new_status == "CHECKLIST_IN_PROGRESS":
                sendEmailNotification(
                    instance=instance,
                    event=Notification.PROGRESS_TRACKING_ACTIVE,
                    redirect_link=f"/orders/{instance.order_number}/progress",
                    values={},
                )
            if new_status == "EVENT_EXECUTING":
                sendEmailNotification(
                    instance=instance,
                    event=Notification.EVENT_REMINDER_SENT,
                    redirect_link=f"/orders/{instance.order_number}/event",
                    values={},
                )
            if new_status == "POST_EVENT_FEEDBACK_PENDING":
                sendEmailNotification(
                    instance=instance,
                    event=Notification.POST_EVENT_SURVEY_SENT,
                    redirect_link=f"/orders/{instance.order_number}/feedback",
                    values={},
                )

            # ejemplo: notify_status_transition(instance.id, old_status, new_status)
            # ejemplo: crear historial:
            # OrderStatusHistory.objects.create(order=instance, from_status=old_status, to_status=new_status)

    # Dispara sólo cuando el commit se confirma (evita correr si luego hay rollback)
    transaction.on_commit(fire_events)

import logging
from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from .models import *
from .services import *

logger = logging.getLogger(__name__)

@shared_task
def cancel_timed_out_takeaway_orders():
    timeout_limit = timezone.now() - timedelta(minutes=30)

    expired_order_ids = (
        Order.objects.filter(
            fulfillment_mode="TAKEAWAY",
            order_status="OUT_FOR_PICKUP",
            out_for_pickup_at__isnull=False,
            out_for_pickup_at__lte=timeout_limit,
        ).values_list("id", flat=True))

    cancelled_count = 0
    failed_count = 0

    for order_id in expired_order_ids.iterator():
        try:
            cancelled = OrderService.cancel_timed_out_order(order_id)

            if cancelled:
                cancelled_count += 1
                logger.info("Timed-out takeaway order cancelled. Database order ID: %s",order_id,)

        except Exception:
            failed_count += 1
            logger.exception("Failed to cancel timed-out takeaway order. Database order ID: %s",order_id,)

    return {
        "cancelled_orders": cancelled_count,
        "failed_orders": failed_count,
    }

    # for order_id in expired_order_ids.iterator():
    #     if OrderService.cancel_timed_out_order(order_id):
    #         cancelled_count += 1

    # return {"cancelled_orders": cancelled_count}
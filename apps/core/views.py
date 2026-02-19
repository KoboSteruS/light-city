"""
Представления приложения core.
"""

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


@staff_member_required
def admin_undo_last_action(request):
    """
    Отмена последнего действия в админке (откат последней ревизии текущего пользователя).
    """
    from reversion.models import Revision

    # Последняя ревизия, созданная текущим пользователем
    revision = (
        Revision.objects.filter(user=request.user)
        .order_by('-date_created')
        .first()
    )

    if not revision:
        messages.warning(
            request,
            _('Нет сохранённых действий для отмены.')
        )
        return redirect('admin:index')

    try:
        revision.revert()
        messages.success(
            request,
            _('Последнее действие успешно отменено.')
        )
    except Exception as e:
        messages.error(
            request,
            _('Не удалось отменить действие: %(error)s') % {'error': str(e)}
        )

    return redirect('admin:index')

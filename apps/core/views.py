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
    Отмена последнего действия в админке: откат к состоянию *до* последнего
    сохранения (применяем предыдущую ревизию, а не последнюю).
    """
    from reversion.models import Revision

    # Две последние ревизии: [последняя, предпоследняя]
    revisions = list(
        Revision.objects.filter(user=request.user)
        .order_by('-date_created')[:2]
    )

    if len(revisions) < 2:
        messages.warning(
            request,
            _('Нет предыдущего действия для отмены (нужна минимум одна сохранённая правка).')
        )
        return redirect('admin:index')

    # Откатываемся к предпоследней ревизии (состояние до последнего сохранения)
    previous_revision = revisions[1]

    try:
        previous_revision.revert()

        # Удаляем последнюю запись из «Последние действия», чтобы отменённое действие там не отображалось
        from django.contrib.admin.models import LogEntry
        last_log = (
            LogEntry.objects.filter(user_id=request.user.pk)
            .order_by('-action_time')
            .first()
        )
        if last_log:
            last_log.delete()

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

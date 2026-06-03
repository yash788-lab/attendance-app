from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime

from models.communication import Announcement, Event, Poll, PollOption, PollVote
from models.academic import Class
from services.communication_service import CommunicationService
from services.notification_service import NotificationService
from database import db
from . import admin_bp
from utils.decorators import admin_required


# ── Announcements ─────────────────────────────────────────────────────────────

@admin_bp.route('/admin/cms')
@login_required
@admin_required
def admin_cms():
    announcements = CommunicationService.get_all_announcements()
    events = CommunicationService.get_all_events()
    polls = Poll.query.order_by(Poll.created_at.desc()).all()
    classes = Class.query.order_by(Class.name).all()
    return render_template(
        'admin/cms.html',
        announcements=announcements,
        events=events,
        polls=polls,
        classes=classes,
    )


@admin_bp.route('/admin/cms/announcement/add', methods=['POST'])
@login_required
@admin_required
def admin_add_announcement():
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    target_role = request.form.get('target_role', 'all')
    target_class_id = request.form.get('target_class_id', type=int)
    is_pinned = request.form.get('is_pinned') == 'on'

    if not title or not content:
        flash('Title and content are required.', 'error')
        return redirect(url_for('admin.admin_cms'))

    CommunicationService.create_announcement(
        title=title,
        content=content,
        created_by_user_id=current_user.id,
        target_role=target_role,
        target_class_id=target_class_id,
        is_pinned=is_pinned,
    )
    # Trigger in-app notification
    NotificationService.notify_announcement(title=title, message=content[:200])
    flash(f'Announcement "{title}" posted and users notified.', 'success')
    return redirect(url_for('admin.admin_cms'))


@admin_bp.route('/admin/cms/announcement/<int:ann_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_announcement(ann_id):
    CommunicationService.delete_announcement(ann_id)
    flash('Announcement deleted.', 'success')
    return redirect(url_for('admin.admin_cms'))


# ── Events ────────────────────────────────────────────────────────────────────

@admin_bp.route('/admin/cms/event/add', methods=['POST'])
@login_required
@admin_required
def admin_add_event():
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    event_date_str = request.form.get('event_date', '').strip()
    location = request.form.get('location', '').strip()

    if not title or not event_date_str:
        flash('Title and date are required.', 'error')
        return redirect(url_for('admin.admin_cms'))

    try:
        event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
    except ValueError:
        flash('Invalid date format.', 'error')
        return redirect(url_for('admin.admin_cms'))

    CommunicationService.create_event(
        title=title,
        description=description,
        event_date=event_date,
        location=location,
        created_by_user_id=current_user.id,
    )
    flash(f'Event "{title}" added.', 'success')
    return redirect(url_for('admin.admin_cms'))


@admin_bp.route('/admin/cms/event/<int:event_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_event(event_id):
    CommunicationService.delete_event(event_id)
    flash('Event deleted.', 'success')
    return redirect(url_for('admin.admin_cms'))


# ── Polls ─────────────────────────────────────────────────────────────────────

@admin_bp.route('/admin/cms/poll/add', methods=['POST'])
@login_required
@admin_required
def admin_add_poll():
    question = request.form.get('question', '').strip()
    options = request.form.getlist('options')
    expires_at_str = request.form.get('expires_at', '').strip()

    if not question or len([o for o in options if o.strip()]) < 2:
        flash('Question and at least 2 options are required.', 'error')
        return redirect(url_for('admin.admin_cms'))

    expires_at = None
    if expires_at_str:
        try:
            expires_at = datetime.strptime(expires_at_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            pass

    CommunicationService.create_poll(
        question=question,
        options_text=options,
        created_by_user_id=current_user.id,
        expires_at=expires_at,
    )
    flash('Poll created.', 'success')
    return redirect(url_for('admin.admin_cms'))


@admin_bp.route('/admin/cms/poll/<int:poll_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_poll(poll_id):
    CommunicationService.delete_poll(poll_id)
    flash('Poll deleted.', 'success')
    return redirect(url_for('admin.admin_cms'))

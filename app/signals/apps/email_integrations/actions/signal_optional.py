# SPDX-License-Identifier: MPL-2.0
# Copyright (C) 2021 - 2023 Gemeente Amsterdam
import typing

from signals.apps.email_integrations.actions.abstract import AbstractAction
from signals.apps.email_integrations.models import EmailTemplate
from signals.apps.email_integrations.rules import SignalOptionalRule
from signals.apps.signals.models import Signal


class SignalOptionalAction(AbstractAction):
    rule: typing.Callable[[Signal], bool] = SignalOptionalRule()

    key: str = EmailTemplate.SIGNAL_STATUS_CHANGED_OPTIONAL
    subject: str = 'Meer over uw melding {formatted_signal_id}'

    note: str = 'De statusupdate is per e-mail verzonden aan de melder'

    def get_additional_context(self, signal: Signal, dry_run: bool = False) -> dict:
        return {
            'afhandelings_text': signal.status.text
        }

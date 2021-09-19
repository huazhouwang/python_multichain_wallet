from typing import Any

from wallet.lib.basic.functional.require import require_not_none
from wallet.lib.hardware.callbacks import base, helper


class AndroidCallback(base.BaseCallback):
    def notify_handler(self, code: int):
        self.android_handler.sendEmptyMessage(code)

    @property
    def android_handler(self) -> Any:
        return require_not_none(
            helper.get_value_of_agent("handler"), f"Please configure 'handler' for {helper.AGENT} first"
        )

def initialize():
    import logging.config

    from common.conf import settings

    # prepare logging
    logging.config.dictConfig(settings.LOGGING)

    # database migrating
    from common.basic.orm.database import db
    from common.basic.orm.migrate import manager as migrate_manager

    migrate_manager.migrating(db)

    # connect ticker signal here before start
    # example ticker.signals.ticker_signal.connect(my_ticker_callback)
    from common.basic import ticker
    from common.price import manager as price_manager
    from common.transaction import manager as transaction_manager

    ticker.signals.ticker_signal.connect(price_manager.on_ticker_signal)
    ticker.signals.ticker_signal.connect(transaction_manager.on_ticker_signal)

    # start ticker
    ticker.start_default_ticker(seconds=60)  # every 1 min


def terminate():
    from common.basic import ticker

    ticker.cancel_default_ticker()


def reset_runtime():
    import os

    from common.basic.orm import database

    terminate()
    database.db.close()
    os.remove(database.db.database)
    initialize()

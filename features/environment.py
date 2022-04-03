from utilities.logging import LOG


def before_all(context):
    LOG.info("Starting test execution")
    context.log = LOG

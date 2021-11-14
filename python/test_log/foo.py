import logging
# 如果是最新调用这个logging.info
# 会先basicConfig()，渲染配置，导致后面的basicConfig失效。
# 所以如果先在模块代码info，会进行初始化，相当于已经配置了。会导致import 当前模块的代码的外层的basicConfig，直接跳过配置。所以会导致配置无效
# logging.info('info: hi logging')

logger = logging.getLogger(__name__)
# 默认logger的info不输出，格式也是默认的
logger.info('info：Hi, init----')
# warning级别输出
logger.warning('warning： Hi, init----')


def foo():
    # 经过其他渲染后，logger的root的配置发生变更，可以输出，格式也变成新的
    logger.info('Hi, foo')
    logging.info('Hi, foo logging')


class Bar(object):
    def bar(self):
        logger.info('Hi, bar')
        logger.info('Hi, bar')
        logging.info('Hi, bar logging')

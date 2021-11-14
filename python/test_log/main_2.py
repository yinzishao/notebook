import logging
# 提前进行logger的创建，模块的日志按照原始root的配置
import foo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Start reading database')
# read database here
records = {'john': 55, 'tom': 66}
logger.debug('Records: %s', records)
logger.info('Updating records ...')

# 经过上面的渲染，更改了foo里面的logger的配置，所以调用函数可以输出info的basic格式
foo.foo()
bar = foo.Bar()
bar.bar()
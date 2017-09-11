import sys
import os
import logging
import logging.handlers
import traceback

try:
    import bpy
except:
    pass


"""
import logging
#import logging.handlers
import valog

# ロガー
valog.init_logger('Blender', level=logging)

# ハンドラ
#handler = valog.logging.StreamHandler(stream=None)
handler = valog.logging.handlers.RotatingFileHandler(file_path, maxBytes=0, backupCount=0, encoding=None, delay=0)

# フォーマット
# format: %(name)s, %(levelname)s
formatter = logging.Formatter('[%(asctime)s] %(message)s')
handler.setFormatter(formatter)

# ハンドラ追加
valog.logger.addHandler(handler)

# ハンドラ除去
valog.logger.removeHandler(handler)
handler.close()

# handler.baseFilename
"""

"""
logging.Formatter書式
%(name)s     ロガー (ログ記録チャネル) の名前
%(levelno)s     メッセージのログ記録レベルを表す数字 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
%(levelname)s     メッセージのログ記録レベルを表す文字列 (“DEBUG”, “INFO”, “WARNING”, “ERROR”, “CRITICAL”)
%(pathname)s     ログ記録の呼び出しが行われたソースファイルの全パス名 (取得できる場合)
%(filename)s     パス名中のファイル名部分
%(module)s     モジュール名 (ファイル名の名前部分)
%(funcName)s     ログ記録の呼び出しを含む関数の名前
%(lineno)d     ログ記録の呼び出しが行われたソース行番号 (取得できる場合)
%(created)f     LogRecord が生成された時刻 (time.time() の返した値)
%(relativeCreated)d     LogRecord が生成された時刻の logging モジュールが読み込まれた時刻に対するミリ秒単位での相対的な値。
%(asctime)s     LogRecord が生成された時刻を人間が読める書式で表したもの。デフォルトでは “2003-07-08 16:49:45,896” 形式 (コンマ以降の数字は時刻のミリ秒部分) です
%(msecs)d     LogRecord が生成された時刻の、ミリ秒部分
%(thread)d     スレッド ID (取得できる場合)
%(threadName)s     スレッド名 (取得できる場合)
%(process)d     プロセス ID (取得できる場合)
%(message)s     レコードが発信された際に処理された msg % args の結果
"""

"""
レベル
logging.DEBUG
logging.INFO
logging.WARNING
logging.ERROR
logging.CRITICAL
logger.debug("debug message")
logger.info("info message")
logger.warning("warning message")
logger.error("error message")
logger.critical("critical message")
"""


LOG_FILENAME = 'logging_rotatingfile_example.log'
MAX_BYTES = 200 * 1000
BACKUP_COUNT = 5

# blender用
BLENDER_LOGGER_NAME = 'bpy'
WRITE_TEXT_HANDLER_NAME = 'write_text'
RECORD_LOG_HANDLER_NAME = 'record_log'


###############################################################################
# logger
###############################################################################
"""
def get_logger(name, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    return logger
"""
"""def init_logger(name, level=logging.DEBUG):
    global logger
    if not logger:
        logger = get_logger(name, level)
    return logger
"""
# NOTSETは使える？
level_dict = {#logging.NOTSET: logging.NOTSET,
              logging.DEBUG: logging.DEBUG,
              logging.INFO: logging.INFO,
              logging.WARNING: logging.WARNING,
              logging.ERROR: logging.ERROR,
              logging.CRITICAL: logging.CRITICAL,
              #'NOTSET': logging.NOTSET,
              'DEBUG': logging.DEBUG,
              'INFO': logging.INFO,
              'WARNING': logging.WARNING,
              'ERROR': logging.ERROR,
              'CRITICAL': logging.CRITICAL,
              #'notset': logging.NOTSET,
              'debug': logging.DEBUG,
              'info': logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL}


###############################################################################
# 例外
###############################################################################
def excepthook(hook=True, logger_name=''):
    """例外を端末に表示し、logger.error()も行う"""
    class ExceptHook:
        def __init__(self, logger_name=''):
            self.logger_name = logger_name  # 後に変更可能
        def __call__(self, type, value, tb):
            msg = ''.join(traceback.format_exception(type, value, tb))
            print(msg)
            logger = logging.getLogger(self.logger_name)
            #logger.setLevel(logging.DEBUG)
            logger.error(msg)
    if hook:
        sys.excepthook = ExceptHook(logger_name)
    else:
        sys.excepthook = sys.__excepthook__


###############################################################################
# printラッパ
###############################################################################
def print_wrapper():
    """ログに送り、通常のprintも行う
    e.g.
    print = print_wrapper()
    print('message', end='', level='error')
    """
    class PrintWrapper():
        default_level = logging.DEBUG
        
        def __init__(self, logger_name=BLENDER_LOGGER_NAME, level=''):
            self.logger_name = logger_name
            if level:
                self.level = level
            else:
                self.level = self.default_level
        def __call__(self, msg='', *args, **kw):
            # 辞書のlogger,logger_name,levelはここで使うので注意する
            kw2 = dict(kw)
            if 'logger_name' in kw2:
                logger = logging.getLogger(kw2.pop('logger_name'))
            elif 'logger' in kw2:
                logger = kw2.pop('logger')
            else:
                logger = logging.getLogger(self.logger_name)
            
            if 'level' in kw2:
                level = kw2.pop('level')
            else:
                level = self.level
            if level in level_dict:
                logger.log(level_dict[level], msg, *args, **kw2)
            else:
                logger.log(self.default_level, msg, *args, **kw2)

            print(msg, *args, **kw2)
            
    return PrintWrapper()


###############################################################################
# blender専用
###############################################################################
def get_blender_text(name):
    if name in bpy.data.texts:
        return bpy.data.texts[name]
    else:
        return bpy.data.texts.new(name)


class WriteBlenderText:
    """インスタンスをlogging.StreamHandlerに渡す"""
    
    def __init__(self, text_name):
        self.text_name = text_name

    def write(self, string):
        text = get_blender_text(self.text_name)
        text.write(string)
    
    def flush(self):
        pass


def verbose_update_func(self, context):
    """ハンドラのフォーマットの設定。logconf.verboseに設定する"""
    logconf = context.window_manager.logconf
    logger = logging.getLogger(BLENDER_LOGGER_NAME)

    for handler in logger.handlers:
        if handler.name in (WRITE_TEXT_HANDLER_NAME, RECORD_LOG_HANDLER_NAME):
            if logconf.verbose:
                fmt = '%(asctime)s %(levelname)s ' + \
                      '%(module)s %(funcName)s %(message)s'
                formatter = logging.Formatter(fmt)
            else:
                formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)


def record_log_update_func(self, context):
    """ファイル出力ハンドラの更新。logconf.record_log,
    logconf.log_file_pathに設定する
    """
    logconf = context.window_manager.logconf
    logger = logging.getLogger(BLENDER_LOGGER_NAME)
    
    # 一旦ハンドラを削除
    for handler in logger.handlers[:]:
        if handler.name == RECORD_LOG_HANDLER_NAME:
            logger.removeHandler(handler)  # handler: hdlr
            handler.close()
    
    # 有効な場合、新規作成して追加
    if True:  # テキスト出力オペレータが起動中でないといけない。
        if logconf.record_log and logconf.log_file_path:
            path = bpy.path.abspath(logconf.log_file_path)
            handler = logging.handlers.RotatingFileHandler(
                          path, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
            handler.name = RECORD_LOG_HANDLER_NAME
            if logconf.verbose:
                fmt = '%(asctime)s %(levelname)s ' + \
                      '%(module)s %(funcName)s %(message)s'
                formatter = logging.Formatter(fmt)
                handler.setFormatter(formatter)
            handler.setLevel(logging.DEBUG)  # デフォルトではNOTSET
            logger.addHandler(handler)
            verbose_update_func(self, context)

###############################################################################
# テスト
###############################################################################
class StdOut:
    def write(self, string):
        sys.__stdout__.write('StdOut class\n')
        sys.__stdout__.write(string)
    
    def flush(self):
        pass

class ExceptHook:
    def __call__(self, type, value, tb):
        msg = ''.join(traceback.format_exception(type, value, tb))
        print('ExceptHook', msg)

def _main():
    """import test
    x = test.hoge
    x()
    y = test.piyo
    yi = y()
    yi()
    """
    #Logger.exception(msg[, *args])
    #レベル ERROR のメッセージをこのロガーで記録します。引数は debug() と同じように解釈されます。
    #例外情報がログメッセージに追加されます。このメソッドは例外ハンドラからのみ呼び出されます。
    
    
    logger = logging.getLogger('main')
    #print(dir(logger))
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(
                  LOG_FILENAME, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
    #print(dir(handler))
    #handler.name = 'ppppppp'
    #print(handler.get_name())
    
    fmt = '%(asctime)s %(name)s %(levelname)s %(message)s'
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    
    logger2 = logging.getLogger('main.child')
    #logger2.setLevel(logging.NOTSET)
    #logger2.setLevel(logging.ERROR)
    logger2.setLevel(logging.INFO)
    handler2 = logging.handlers.RotatingFileHandler(
                   LOG_FILENAME, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
    formatter2 = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s [fm2]')
    handler2.setFormatter(formatter2)
    #handler2.setLevel(logging.NOTSET)
    logger2.addHandler(handler2)
    
    
    """
    logger2 = logging.getLogger('example.piyo')
    logger2.setLevel(logging.DEBUG)
    handler2 = logging.handlers.RotatingFileHandler(
                   LOG_FILENAME, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
    formatter2 = logging.Formatter()
    handler2.setFormatter(formatter2)
    logger2.addHandler(handler2)
    """
    logger.info('#######################')
    logger.debug('hoge')
    logger2.info('piyo')
    
    #sys.stdout = StdOut()
    #sys.excepthook = ExceptHook()
    
    #excepthook(True, 'example.hoge')
    #logger.debug('hoge')
    #raise TypeError


if __name__ == '__main__':
    _main()

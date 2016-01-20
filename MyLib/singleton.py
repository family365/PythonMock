
class SingletonBase(object):
    '''
    1. must be derived from object
    2. the attribute '_instance' must be prefix with single '_',
        double '__' means private variable, hasattr will not detect that var, so in that case hasattr method will alway return False

    Another way to implement singleton. This method must be called in some place obviously; __new__ method is implicit
    user will use the same instance to hand their work
         
    @staticmethod
    def getInstance():
        if ConfigLoader.__instance is None:
            ConfigLoader.objLocker.acquire()
            if ConfigLoader.__instance is None:
                ConfigLoader.__instance=ConfigLoader()

            ConfigLoader.objLocker.release()

        return ConfigLoader.__instance
    '''
    def __new__(cls, *args, **kargs):
        if not hasattr(cls, '_instance'):
            cls._instance=super(SingletonBase, cls).__new__(cls, args, kargs)
            return cls._instance 



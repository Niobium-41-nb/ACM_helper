"""
ACM_helper - 由 vanadium-23 开发的ACM竞赛辅助工具包

一个模块化的ACM竞赛辅助工具库，提供各种实用功能。
"""

__version__ = "0.1.0"
__author__ = "vanadium-23(Niobium-41-nb)"

# 动态导入机制 - 按需导入模块，避免未使用的模块影响性能
def _import_utils():
    """动态导入utils模块"""
    from . import utils
    return utils

def _import_core():
    """动态导入core模块"""
    try:
        from . import core
        return core
    except ImportError:
        return None

# 包初始化配置
_CONFIG = {
    'debug': False,
    'auto_import': True
}

# 延迟导入的模块缓存
_module_cache = {}

def get_module(module_name):
    """
    动态获取模块
    
    Args:
        module_name: 模块名称，如 'utils', 'core'
    
    Returns:
        模块对象或None
    """
    if module_name in _module_cache:
        return _module_cache[module_name]
    
    try:
        module = __import__(f'ACM_helper.{module_name}', fromlist=[module_name])
        _module_cache[module_name] = module
        return module
    except ImportError:
        return None

def get_class(class_path):
    """
    动态获取类
    
    Args:
        class_path: 类路径，如 'utils.Make_Test_Cases_Cpp'
    
    Returns:
        类对象或None
    """
    try:
        module_path, class_name = class_path.rsplit('.', 1)
        module = get_module(module_path)
        if module and hasattr(module, class_name):
            return getattr(module, class_name)
        return None
    except (ValueError, AttributeError):
        return None

# 自动导出当前已知的功能
try:
    from .utils import Make_Test_Cases_Cpp
    __all__ = ['Make_Test_Cases_Cpp']
except ImportError:
    __all__ = []

# 配置管理函数
def set_debug(enabled):
    """设置调试模式"""
    _CONFIG['debug'] = enabled
    if enabled:
        print(f"ACM_helper {__version__} 调试模式已启用")
    else:
        print("调试模式已禁用")

def get_config():
    """获取当前配置"""
    return _CONFIG.copy()

def version_info():
    """显示版本信息"""
    return f"ACM_helper {__version__} by {__author__}"

# 工具函数快捷访问（可选）
def make_test_cases(L, R, std_cpp_path="std.cpp", gen_cpp_path="gen.cpp"):
    """
    生成测试用例的快捷函数
    
    等同于: Make_Test_Cases_Cpp.generate_test_cases(L, R, std_cpp_path, gen_cpp_path)
    """
    utils = _import_utils()
    if hasattr(utils, 'Make_Test_Cases_Cpp'):
        return utils.Make_Test_Cases_Cpp.generate_test_cases(L, R, std_cpp_path, gen_cpp_path)
    else:
        raise ImportError("Make_Test_Cases_Cpp 类未找到")

def create_zip_archive():
    """创建压缩文件的快捷函数"""
    utils = _import_utils()
    if hasattr(utils, 'Make_Test_Cases_Cpp'):
        return utils.Make_Test_Cases_Cpp.create_zip_archive()
    else:
        raise ImportError("Make_Test_Cases_Cpp 类未找到")

# 包初始化信息
def _print_welcome():
    """显示欢迎信息"""
    if _CONFIG['debug']:
        print(f"ACM_helper {__version__} 已加载 - 由 {__author__} 开发")
        available_modules = []
        for module in ['utils', 'core']:
            if get_module(module):
                available_modules.append(module)
        if available_modules:
            print(f"可用模块: {', '.join(available_modules)}")

# 执行初始化
_print_welcome()

# 异常类
class ACMHelperError(Exception):
    """ACM_helper包的基础异常类"""
    pass

class ModuleNotFoundError(ACMHelperError):
    """模块未找到异常"""
    pass

class FunctionNotFoundError(ACMHelperError):
    """功能未找到异常"""
    pass
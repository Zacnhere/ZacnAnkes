from importlib import import_module

from Teiko.modules import loadModule


async def loadPlugins():
    modules = loadModule()
    for mod in modules:
        imported_module = import_module(f"Teiko.modules.{mod}")
    print(f"[TEIKO]: Succesfull startted all!!")

#!/usr/bin/env python3
"""
Simple test script for nemotek-counters library

This script tests that the package imports work correctly and
that the main classes can be instantiated.
"""

def test_imports():
    """Test that all imports work correctly"""
    print("Testing package imports...")
    
    try:
        # Test main package import
        import nemotek_counters
        print("✅ Main package import successful")
        
        # Test manufacturer imports
        from nemotek_counters import carlo_gavazzi, contrel, diris, lovato, redz, schneider
        print("✅ All manufacturer modules imported successfully")
        
        # Test Carlo Gavazzi EM530 (the implemented one)
        from nemotek_counters.carlo_gavazzi import em530
        from nemotek_counters.carlo_gavazzi.em530 import (
            ConfiguracaoContador,
            ConfiguracaoModbus,
            GestorErrosModbus,
            ColectorDadosEM530
        )
        print("✅ Carlo Gavazzi EM530 classes imported successfully")
        
        # Test empty modules can be imported
        from nemotek_counters.contrel import ud3h
        from nemotek_counters.diris import a10
        from nemotek_counters.lovato import dmg800, dmg210, dmg6
        from nemotek_counters.redz import lkm144
        from nemotek_counters.schneider import iem3250, iem3155
        print("✅ All empty modules imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def test_class_instantiation():
    """Test that the main classes can be instantiated"""
    print("\nTesting class instantiation...")
    
    try:
        from nemotek_counters.carlo_gavazzi.em530 import (
            ConfiguracaoContador,
            ConfiguracaoModbus,
            GestorErrosModbus,
            ColectorDadosEM530
        )
        
        # Test configuration classes
        config_contador = ConfiguracaoContador(
            id_contador=1,
            id_unidade=100,
            nome_contador="Teste",
            id_empresa="Teste"
        )
        print("✅ ConfiguracaoContador instantiated successfully")
        
        config_modbus = ConfiguracaoModbus()
        print("✅ ConfiguracaoModbus instantiated successfully")
        
        # Test error manager
        gestor_erros = GestorErrosModbus("Teste", "Teste")
        print("✅ GestorErrosModbus instantiated successfully")
        
        # Test main collector (without connecting)
        colector = ColectorDadosEM530(config_contador, config_modbus)
        print("✅ ColectorDadosEM530 instantiated successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Class instantiation error: {e}")
        return False


def test_package_structure():
    """Test the package structure is correct"""
    print("\nTesting package structure...")
    
    try:
        import nemotek_counters
        
        # Check version info
        print(f"✅ Package version: {nemotek_counters.__version__}")
        print(f"✅ Package author: {nemotek_counters.__author__}")
        
        # Check that __all__ contains expected modules
        expected_modules = ['carlo_gavazzi', 'contrel', 'diris', 'lovato', 'redz', 'schneider']
        for module in expected_modules:
            if module in nemotek_counters.__all__:
                print(f"✅ Module '{module}' found in __all__")
            else:
                print(f"❌ Module '{module}' missing from __all__")
                return False
                
        return True
        
    except Exception as e:
        print(f"❌ Package structure error: {e}")
        return False


def main():
    """Run all tests"""
    print("Nemotek Counters Library - Test Suite")
    print("=" * 40)
    
    tests = [
        ("Import Tests", test_imports),
        ("Class Instantiation Tests", test_class_instantiation),
        ("Package Structure Tests", test_package_structure)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 40)
    print("Test Results Summary:")
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print(f"\nOverall: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
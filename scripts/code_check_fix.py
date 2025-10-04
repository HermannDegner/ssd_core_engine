#!/usr/bin/env python3
"""
SSD Code Check & Fix Script
全体コードチェックと修正スクリプト
"""

import os
import re
import glob

def fix_import_errors():
    """インポートエラーを一括修正"""
    
    # 修正対象のファイルパターン
    python_files = glob.glob("*.py")
    
    # 除外ファイル
    exclude_files = {"__init__.py", "test_*.py", "demo_*.py", "detailed_territory_test.py"}
    
    fixed_files = []
    
    for filepath in python_files:
        if os.path.basename(filepath) in exclude_files:
            continue
            
        print(f"🔍 チェック中: {filepath}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 相対インポートパターンを検出
            relative_import_pattern = r'from \.([a-zA-Z_]+) import'
            
            if re.search(relative_import_pattern, content):
                print(f"  📝 修正が必要: {filepath}")
                
                # ImportError例外処理内の相対インポートを絶対インポートに変更
                content = re.sub(
                    r'except ImportError:\s*\n.*?from \.([a-zA-Z_]+) import',
                    lambda m: f"except ImportError:\n    import sys\n    import os\n    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\n    from {m.group(1)} import",
                    content,
                    flags=re.MULTILINE | re.DOTALL
                )
                
                # パターンマッチング修正
                fixes = [
                    (r'from \.ssd_types import', 'from ssd_types import'),
                    (r'from \.ssd_meaning_pressure import', 'from ssd_meaning_pressure import'),
                    (r'from \.ssd_alignment_leap import', 'from ssd_alignment_leap import'),
                    (r'from \.ssd_decision import', 'from ssd_decision import'),
                    (r'from \.ssd_prediction import', 'from ssd_prediction import'),
                    (r'from \.ssd_utils import', 'from ssd_utils import'),
                    (r'from \.ssd_territory import', 'from ssd_territory import'),
                    (r'from \.ssd_engine import', 'from ssd_engine import'),
                ]
                
                # except ImportError内部でのみ修正を適用
                lines = content.split('\n')
                in_except_block = False
                indent_level = 0
                
                for i, line in enumerate(lines):
                    if 'except ImportError:' in line:
                        in_except_block = True
                        indent_level = len(line) - len(line.lstrip())
                    elif in_except_block:
                        current_indent = len(line) - len(line.lstrip()) if line.strip() else indent_level + 4
                        if line.strip() and current_indent <= indent_level:
                            in_except_block = False
                        elif in_except_block:
                            for pattern, replacement in fixes:
                                if re.search(pattern, line):
                                    lines[i] = re.sub(pattern, replacement, line)
                
                content = '\n'.join(lines)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                fixed_files.append(filepath)
                print(f"  ✅ 修正完了: {filepath}")
            else:
                print(f"  ✅ OK: {filepath}")
                
        except Exception as e:
            print(f"  ❌ エラー: {filepath} - {e}")
    
    return fixed_files

def test_imports():
    """インポートテスト"""
    test_modules = [
        'ssd_types',
        'ssd_meaning_pressure', 
        'ssd_alignment_leap',
        'ssd_decision',
        'ssd_prediction',
        'ssd_utils',
        'ssd_territory',
        'ssd_engine'
    ]
    
    results = {}
    
    for module in test_modules:
        try:
            exec(f"import {module}")
            results[module] = "✅ OK"
        except Exception as e:
            results[module] = f"❌ {str(e)[:50]}..."
    
    return results

def check_code_quality():
    """コード品質チェック"""
    issues = []
    
    python_files = glob.glob("*.py")
    exclude_files = {"__init__.py", "test_*.py", "demo_*.py", "detailed_territory_test.py"}
    
    for filepath in python_files:
        if os.path.basename(filepath) in exclude_files:
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        # 品質チェック項目
        
        # 1. 長すぎるファイル（500行以上）
        if len(lines) > 500:
            issues.append(f"📏 {filepath}: 長すぎるファイル ({len(lines)}行)")
        
        # 2. 長すぎる行（100文字以上）
        for i, line in enumerate(lines, 1):
            if len(line) > 100:
                issues.append(f"📏 {filepath}:{i}: 長すぎる行 ({len(line)}文字)")
                if len(issues) > 20:  # 上位20件まで
                    break
        
        # 3. デバッグprint文
        debug_prints = [i+1 for i, line in enumerate(lines) if re.search(r'print\s*\(.*[🏘️🔍🎯📊✨🎊]', line)]
        if debug_prints:
            issues.append(f"🖨️ {filepath}: デバッグprint文 (行: {debug_prints[:5]})")
        
        # 4. TODO/FIXME/NOTEコメント
        todos = [i+1 for i, line in enumerate(lines) if re.search(r'#\s*(TODO|FIXME|NOTE|XXX)', line, re.IGNORECASE)]
        if todos:
            issues.append(f"📝 {filepath}: TODO/FIXME (行: {todos})")
    
    return issues

def main():
    """メイン実行"""
    print("🔬 SSD Core Engine - 全体コードチェック")
    print("=" * 50)
    
    # 1. インポート修正
    print("\n1️⃣ インポートエラー修正")
    fixed_files = fix_import_errors()
    if fixed_files:
        print(f"修正したファイル: {len(fixed_files)}個")
        for f in fixed_files:
            print(f"  - {f}")
    else:
        print("修正が必要なファイルはありませんでした")
    
    # 2. インポートテスト
    print(f"\n2️⃣ インポートテスト")
    import_results = test_imports()
    for module, result in import_results.items():
        print(f"  {module}: {result}")
    
    # 3. コード品質チェック  
    print(f"\n3️⃣ コード品質チェック")
    issues = check_code_quality()
    if issues:
        print(f"発見された問題: {len(issues)}個")
        for issue in issues[:10]:  # 上位10件表示
            print(f"  - {issue}")
        if len(issues) > 10:
            print(f"  ... 他 {len(issues)-10}個の問題")
    else:
        print("コード品質の問題は見つかりませんでした")
    
    # 4. サマリー
    print(f"\n📊 チェック結果サマリー")
    success_imports = sum(1 for result in import_results.values() if "✅" in result)
    total_imports = len(import_results)
    
    print(f"✅ インポート成功率: {success_imports}/{total_imports} ({success_imports/total_imports*100:.1f}%)")
    print(f"📝 修正されたファイル: {len(fixed_files)}個")
    print(f"⚠️ 品質問題: {len(issues)}個")
    
    if success_imports == total_imports and len(issues) == 0:
        print(f"\n🎊 全体コードチェック完了！すべて正常です")
    else:
        print(f"\n⚠️ いくつかの問題が残っています。上記を確認してください")

if __name__ == "__main__":
    main()
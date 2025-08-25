"""
統合テスト実行スクリプト
MVCパターンの協調動作を検証
"""

import unittest
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# GUI環境のチェック
try:
    import tkinter as tk
    GUI_AVAILABLE = True
    test_root = tk.Tk()
    test_root.withdraw()
    test_root.destroy()
except Exception as e:
    GUI_AVAILABLE = False
    print(f"⚠️  GUI環境が利用できません: {e}")

if GUI_AVAILABLE:
    from model import PasswordGenerator, PasswordSettings
    from controller import PasswordGeneratorController


class HeadlessPasswordGeneratorView:
    """統合テスト用のGUI表示しないView"""
    
    def __init__(self):
        """ヘッドレスビューの初期化"""
        self.root = tk.Tk()
        self.root.withdraw()
        
        self.password_visible = False
        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.length_var = tk.IntVar(value=8)
        
        self.current_password = ""
        self.on_generate_callback = None
        self.on_copy_callback = None
        self.last_status = "準備完了"
        self.last_error = None
    
    def get_settings(self):
        """現在のUI設定値を取得"""
        return {
            "use_uppercase": self.uppercase_var.get(),
            "use_lowercase": self.lowercase_var.get(),
            "use_digits": self.digits_var.get(),
            "use_symbols": self.symbols_var.get(),
            "length": self.length_var.get()
        }
    
    def display_password(self, password: str):
        """生成されたパスワードを保存"""
        self.current_password = password
        self.last_status = f"パスワード生成完了 ({len(password)}文字)"
    
    def show_error(self, message: str):
        """エラーメッセージを保存"""
        self.last_error = message
        self.last_status = "エラーが発生しました"
    
    def show_success(self, message: str):
        """成功メッセージを保存"""
        self.last_status = message
    
    def set_callbacks(self, on_generate, on_copy):
        """コールバック関数を設定"""
        self.on_generate_callback = on_generate
        self.on_copy_callback = on_copy
    
    def run(self):
        """何もしない（テスト用）"""
        pass
    
    def destroy(self):
        """ウィンドウを破棄"""
        if self.root:
            self.root.destroy()


class TestMVCIntegration(unittest.TestCase):
    """MVC統合テスト"""
    
    def setUp(self):
        """テスト前準備"""
        if not GUI_AVAILABLE:
            self.skipTest("GUI環境が利用できません")
        
        # テスト用コントローラー作成
        self.controller = PasswordGeneratorController()
        # 通常のViewをHeadlessViewに置き換え
        self.controller.view.destroy()
        self.controller.view = HeadlessPasswordGeneratorView()
        self.controller.view.set_callbacks(
            on_generate=self.controller.on_generate,
            on_copy=self.controller.on_copy
        )
    
    def tearDown(self):
        """テスト後クリーンアップ"""
        if hasattr(self, 'controller') and self.controller:
            self.controller.cleanup()
    
    def test_mvc_initialization(self):
        """MVC各層の初期化テスト"""
        self.assertIsInstance(self.controller.model, PasswordGenerator)
        self.assertIsInstance(self.controller.view, HeadlessPasswordGeneratorView)
        self.assertIsNotNone(self.controller.view.on_generate_callback)
        self.assertIsNotNone(self.controller.view.on_copy_callback)
    
    def test_password_generation_flow(self):
        """パスワード生成フロー統合テスト"""
        # 設定変更
        self.controller.view.uppercase_var.set(True)
        self.controller.view.lowercase_var.set(True)
        self.controller.view.digits_var.set(False)
        self.controller.view.symbols_var.set(False)
        self.controller.view.length_var.set(12)
        
        # パスワード生成実行
        self.controller.on_generate()
        
        # 結果確認
        password = self.controller.view.current_password
        self.assertEqual(len(password), 12)
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(c.islower() for c in password))
        self.assertFalse(any(c.isdigit() for c in password))
    
    def test_error_handling_integration(self):
        """エラーハンドリング統合テスト"""
        # 全文字種を無効化
        self.controller.view.uppercase_var.set(False)
        self.controller.view.lowercase_var.set(False)
        self.controller.view.digits_var.set(False)
        self.controller.view.symbols_var.set(False)
        
        # パスワード生成実行
        self.controller.on_generate()
        
        # エラー確認
        self.assertEqual(self.controller.view.current_password, "")
        self.assertIsNotNone(self.controller.view.last_error)


def run_all_tests():
    """全テスト実行"""
    if not GUI_AVAILABLE:
        print("❌ GUI環境が利用できないため、統合テストをスキップします")
        return False
    
    print("🧪 統合テスト実行開始")
    print("=" * 60)
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestMVCIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("=" * 60)
    
    if result.wasSuccessful():
        print("✅ 統合テスト完了 - 全テストパス！")
        return True
    else:
        print("❌ 統合テスト失敗")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
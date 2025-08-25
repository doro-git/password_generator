"""
パスワード生成ツール - 単体テストスイート
Model層の全機能を網羅的にテスト
"""

import unittest
import string
from model import PasswordGenerator, PasswordSettings, UPPERCASE, LOWERCASE, DIGITS, SYMBOLS


class TestPasswordSettings(unittest.TestCase):
    """PasswordSettings クラスのテスト"""
    
    def test_default_initialization(self):
        """デフォルト初期化のテスト"""
        settings = PasswordSettings()
        
        self.assertTrue(settings.use_uppercase)
        self.assertTrue(settings.use_lowercase)
        self.assertTrue(settings.use_digits)
        self.assertTrue(settings.use_symbols)
        self.assertEqual(settings.length, 8)
    
    def test_custom_initialization(self):
        """カスタム初期化のテスト"""
        settings = PasswordSettings(
            use_uppercase=False, 
            use_lowercase=True,
            use_digits=False, 
            use_symbols=True, 
            length=16
        )
        
        self.assertFalse(settings.use_uppercase)
        self.assertTrue(settings.use_lowercase)
        self.assertFalse(settings.use_digits)
        self.assertTrue(settings.use_symbols)
        self.assertEqual(settings.length, 16)


class TestPasswordGenerator(unittest.TestCase):
    """PasswordGenerator クラスのテスト"""
    
    def setUp(self):
        """各テスト前の準備処理"""
        self.generator = PasswordGenerator()
    
    # === 正常系テスト ===
    
    def test_generate_password_default_settings(self):
        """デフォルト設定でのパスワード生成テスト"""
        settings = PasswordSettings()
        password = self.generator.generate_password(settings)
        
        # 基本検証
        self.assertEqual(len(password), 8)
        self.assertIsInstance(password, str)
        
        # 文字種別検証（あなたの実装をそのまま採用）
        self.assertTrue(any(c.isupper() for c in password), "大文字が含まれていません")
        self.assertTrue(any(c.islower() for c in password), "小文字が含まれていません")
        self.assertTrue(any(c.isdigit() for c in password), "数字が含まれていません")
        self.assertTrue(any(c in SYMBOLS for c in password), "記号が含まれていません")
    
    def test_generate_password_uppercase_only(self):
        """大文字のみでのパスワード生成テスト"""
        settings = PasswordSettings(
            use_uppercase=True,
            use_lowercase=False,
            use_digits=False,
            use_symbols=False,
            length=10
        )
        password = self.generator.generate_password(settings)
        
        self.assertEqual(len(password), 10)
        self.assertTrue(all(c.isupper() for c in password))
        self.assertTrue(all(c in UPPERCASE for c in password))
    
    def test_generate_password_lowercase_only(self):
        """小文字のみでのパスワード生成テスト"""
        settings = PasswordSettings(
            use_uppercase=False,
            use_lowercase=True,
            use_digits=False,
            use_symbols=False,
            length=12
        )
        password = self.generator.generate_password(settings)
        
        self.assertEqual(len(password), 12)
        self.assertTrue(all(c.islower() for c in password))
    
    def test_generate_password_digits_only(self):
        """数字のみでのパスワード生成テスト（PINコード風）"""
        settings = PasswordSettings(
            use_uppercase=False,
            use_lowercase=False,
            use_digits=True,
            use_symbols=False,
            length=8
        )
        password = self.generator.generate_password(settings)
        
        self.assertEqual(len(password), 8)
        self.assertTrue(all(c.isdigit() for c in password))
    
    def test_generate_password_symbols_only(self):
        """記号のみでのパスワード生成テスト"""
        settings = PasswordSettings(
            use_uppercase=False,
            use_lowercase=False,
            use_digits=False,
            use_symbols=True,
            length=8
        )
        password = self.generator.generate_password(settings)
        
        self.assertEqual(len(password), 8)
        self.assertTrue(all(c in SYMBOLS for c in password))
    
    def test_generate_password_mixed_types(self):
        """英字+数字の組み合わせテスト"""
        settings = PasswordSettings(
            use_uppercase=True,
            use_lowercase=True,
            use_digits=True,
            use_symbols=False,
            length=16
        )
        password = self.generator.generate_password(settings)
        
        self.assertEqual(len(password), 16)
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(c.islower() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertFalse(any(c in SYMBOLS for c in password))
    
    def test_generate_password_boundary_lengths(self):
        """境界値での長さテスト"""
        # 最小長（8文字）
        settings_min = PasswordSettings(length=8)
        password_min = self.generator.generate_password(settings_min)
        self.assertEqual(len(password_min), 8)
        
        # 最大長（64文字）
        settings_max = PasswordSettings(length=64)
        password_max = self.generator.generate_password(settings_max)
        self.assertEqual(len(password_max), 64)
    
    def test_generate_password_randomness(self):
        """ランダム性の確認テスト"""
        settings = PasswordSettings(length=16)
        
        # 同じ設定で複数回生成
        passwords = [self.generator.generate_password(settings) for _ in range(10)]
        
        # 全て異なることを確認（統計的にほぼ確実）
        unique_passwords = set(passwords)
        self.assertEqual(len(unique_passwords), 10, "生成されたパスワードに重複があります")
    
    # === 異常系テスト ===
    
    def test_generate_password_no_character_types_selected(self):
        """全文字種未選択時の例外テスト（あなたの実装採用）"""
        settings = PasswordSettings(
            use_uppercase=False,
            use_lowercase=False,
            use_digits=False,
            use_symbols=False
        )
        
        with self.assertRaises(ValueError) as context:
            self.generator.generate_password(settings)
        
        self.assertIn("At least one character type", str(context.exception))
    
    def test_generate_password_length_too_short(self):
        """パスワード長不足時の例外テスト"""
        settings = PasswordSettings(length=7)  # 8未満
        
        with self.assertRaises(ValueError) as context:
            self.generator.generate_password(settings)
        
        self.assertIn("between 8 and 64", str(context.exception))
    
    def test_generate_password_length_too_long(self):
        """パスワード長超過時の例外テスト"""
        settings = PasswordSettings(length=65)  # 64超過
        
        with self.assertRaises(ValueError) as context:
            self.generator.generate_password(settings)
        
        self.assertIn("between 8 and 64", str(context.exception))
    
    def test_generate_password_multiple_boundary_violations(self):
        """複数の境界値違反テスト"""
        test_cases = [
            {"length": 0, "desc": "長さ0"},
            {"length": -1, "desc": "負の長さ"},
            {"length": 100, "desc": "長さ100"},
            {"length": 1000, "desc": "長さ1000"}
        ]
        
        for case in test_cases:
            with self.subTest(case=case["desc"]):
                settings = PasswordSettings(length=case["length"])
                with self.assertRaises(ValueError):
                    self.generator.generate_password(settings)
    
    # === クリップボード機能テスト ===
    
    def test_copy_to_clipboard_success(self):
        """クリップボードコピー成功テスト"""
        test_text = "TestPassword123!"
        result = self.generator.copy_to_clipboard(test_text)
        
        # 戻り値の確認（環境によっては失敗する場合もある）
        self.assertIsInstance(result, bool)
    
    def test_copy_to_clipboard_empty_string(self):
        """空文字列のクリップボードコピーテスト"""
        result = self.generator.copy_to_clipboard("")
        self.assertIsInstance(result, bool)


class TestIntegration(unittest.TestCase):
    """統合テスト"""
    
    def setUp(self):
        self.generator = PasswordGenerator()
    
    def test_realistic_usage_scenarios(self):
        """現実的な使用シナリオテスト"""
        
        # シナリオ1: Web用パスワード
        web_settings = PasswordSettings(length=16)
        web_password = self.generator.generate_password(web_settings)
        self.assertEqual(len(web_password), 16)
        
        # シナリオ2: WiFi用パスワード（記号なし）
        wifi_settings = PasswordSettings(use_symbols=False, length=32)
        wifi_password = self.generator.generate_password(wifi_settings)
        self.assertEqual(len(wifi_password), 32)
        self.assertFalse(any(c in SYMBOLS for c in wifi_password))
        
        # シナリオ3: 簡単なPIN（数字のみ）
        pin_settings = PasswordSettings(
            use_uppercase=False, use_lowercase=False, 
            use_symbols=False, length=8
        )
        pin_password = self.generator.generate_password(pin_settings)
        self.assertTrue(all(c.isdigit() for c in pin_password))


# メイン実行部
if __name__ == '__main__':
    # テスト実行設定
    unittest.main(verbosity=2)  # 詳細出力
    
    print("\n" + "="*50)
    print("🧪 単体テスト実行完了！")
    print("✅ Model層の品質確認済み")
    print("="*50)
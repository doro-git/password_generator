"""
パスワード生成ツール - Model層
セキュアなパスワード生成とバリデーション機能を提供
"""

import secrets
import string
from typing import Optional

# 使用可能文字の定義
UPPERCASE = string.ascii_uppercase  # A-Z
LOWERCASE = string.ascii_lowercase  # a-z  
DIGITS = string.digits              # 0-9
SYMBOLS = '!@#$%^&*()_+-=[]{}|;:,.<>?'

# 設定制約値
MIN_LENGTH = 8
MAX_LENGTH = 64


class PasswordSettings:
    """パスワード生成設定を管理するデータクラス"""
    
    def __init__(self, 
                 use_uppercase: bool = True,
                 use_lowercase: bool = True, 
                 use_digits: bool = True,
                 use_symbols: bool = True,
                 length: int = 8):
        """
        パスワード生成設定の初期化
        
        Args:
            use_uppercase: 大文字を使用するか
            use_lowercase: 小文字を使用するか
            use_digits: 数字を使用するか  
            use_symbols: 記号を使用するか
            length: パスワード長（8-64文字）
        """
        self.use_uppercase = use_uppercase
        self.use_lowercase = use_lowercase
        self.use_digits = use_digits
        self.use_symbols = use_symbols
        self.length = length
    
    def __str__(self) -> str:
        """設定内容を文字列で表現（デバッグ用）"""
        return (f"PasswordSettings(uppercase={self.use_uppercase}, "
                f"lowercase={self.use_lowercase}, digits={self.use_digits}, "
                f"symbols={self.use_symbols}, length={self.length})")


class PasswordGenerator:
    """セキュアなパスワード生成を行うクラス"""
    
    def __init__(self):
        """パスワードジェネレーターの初期化"""
        self._random = secrets.SystemRandom()
    
    def generate_password(self, settings: PasswordSettings) -> str:
        """
        設定に基づいてセキュアなパスワードを生成
        
        Args:
            settings: パスワード生成設定
            
        Returns:
            str: 生成されたパスワード文字列
            
        Raises:
            ValueError: 設定が無効な場合
        """
        # バリデーション
        self._validate_settings(settings)
        
        # Step 1: 各文字種から最低1文字ずつ選択（保証文字）
        guaranteed_chars = self._get_guaranteed_characters(settings)
        
        # Step 2: 残りの文字をランダム選択
        remaining_length = settings.length - len(guaranteed_chars)
        all_chars = self._build_character_pool(settings)
        random_chars = [self._random.choice(all_chars) 
                       for _ in range(remaining_length)]
        
        # Step 3: 全文字を結合してシャッフル
        password_chars = guaranteed_chars + random_chars
        self._random.shuffle(password_chars)
        
        return ''.join(password_chars)
    
    def _validate_settings(self, settings: PasswordSettings) -> None:
        """設定値のバリデーション"""
        # 文字種が一つも選択されていない場合
        if not any([settings.use_uppercase, settings.use_lowercase, 
                   settings.use_digits, settings.use_symbols]):
            raise ValueError("At least one character type must be selected.")
        
        # パスワード長の範囲チェック
        if not (MIN_LENGTH <= settings.length <= MAX_LENGTH):
            raise ValueError(f"Password length must be between {MIN_LENGTH} "
                           f"and {MAX_LENGTH} characters.")
    
    def _get_guaranteed_characters(self, settings: PasswordSettings) -> list:
        """各文字種から最低1文字ずつ選択"""
        guaranteed = []
        
        if settings.use_uppercase:
            guaranteed.append(self._random.choice(UPPERCASE))
        if settings.use_lowercase:
            guaranteed.append(self._random.choice(LOWERCASE))
        if settings.use_digits:
            guaranteed.append(self._random.choice(DIGITS))
        if settings.use_symbols:
            guaranteed.append(self._random.choice(SYMBOLS))
            
        return guaranteed
    
    def _build_character_pool(self, settings: PasswordSettings) -> str:
        """使用可能な全文字のプールを構築"""
        pool = ''
        
        if settings.use_uppercase:
            pool += UPPERCASE
        if settings.use_lowercase:
            pool += LOWERCASE
        if settings.use_digits:
            pool += DIGITS
        if settings.use_symbols:
            pool += SYMBOLS
            
        return pool

    def copy_to_clipboard(self, text: str) -> bool:
        """
        テキストをクリップボードにコピー
        
        Args:
            text: コピーするテキスト
            
        Returns:
            bool: コピー成功/失敗
        """
        try:
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()  # ウィンドウを非表示
            root.clipboard_clear()
            root.clipboard_append(text)
            root.update()  # クリップボードを更新
            root.destroy()
            return True
        except Exception as e:
            print(f"Clipboard copy failed: {e}")
            return False


# テスト用コード（実行例）
if __name__ == "__main__":
    # 基本テスト
    generator = PasswordGenerator()
    
    # テストケース1: デフォルト設定
    settings1 = PasswordSettings()
    password1 = generator.generate_password(settings1)
    print(f"デフォルト設定: {password1} (長さ: {len(password1)})")
    
    # テストケース2: 英字のみ
    settings2 = PasswordSettings(use_digits=False, use_symbols=False, length=12)
    password2 = generator.generate_password(settings2)
    print(f"英字のみ12文字: {password2}")
    
    # テストケース3: 数字のみ（PINコード風）
    settings3 = PasswordSettings(use_uppercase=False, use_lowercase=False, 
                                use_symbols=False, length=8)
    password3 = generator.generate_password(settings3)
    print(f"数字のみ8桁: {password3}")
    
    print("\n✅ Model層の実装完了！")
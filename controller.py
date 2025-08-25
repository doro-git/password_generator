"""
パスワード生成ツール - Controller層
Model層とView層を協調させるコントローラー
"""

from model import PasswordGenerator, PasswordSettings
from view import PasswordGeneratorView
from typing import Optional


class PasswordGeneratorController:
    """MVCパターンのController層 - ModelとViewを協調"""
    
    def __init__(self):
        """コントローラーの初期化"""
        # Model層の初期化
        self.model = PasswordGenerator()
        
        # View層の初期化
        self.view = PasswordGeneratorView()
        
        # View層にコールバック関数を設定
        self.view.set_callbacks(
            on_generate=self.on_generate,
            on_copy=self.on_copy
        )
    
    def run(self):
        """アプリケーションの実行開始"""
        self.view.run()
    
    def on_generate(self):
        """パスワード生成要求の処理"""
        try:
            # View から設定を取得
            settings_dict = self.view.get_settings()
            
            # PasswordSettings オブジェクトに変換
            settings = PasswordSettings(
                use_uppercase=settings_dict["use_uppercase"],
                use_lowercase=settings_dict["use_lowercase"],
                use_digits=settings_dict["use_digits"],
                use_symbols=settings_dict["use_symbols"],
                length=settings_dict["length"]
            )
            
            # Model でパスワード生成
            password = self.model.generate_password(settings)
            
            # View に結果を表示
            self.view.display_password(password)
            
        except ValueError as e:
            # バリデーションエラーの処理
            if "character type" in str(e):
                error_msg = "文字種を最低1つは選択してください"
            elif "length" in str(e):
                error_msg = "パスワード長は8～64文字で設定してください"
            else:
                error_msg = str(e)
            
            self.view.show_error(error_msg)
            
        except Exception as e:
            # 予期しないエラーの処理
            self.view.show_error(f"パスワード生成中にエラーが発生しました: {str(e)}")
    
    def on_copy(self, password: str):
        """クリップボードコピー要求の処理"""
        try:
            success = self.model.copy_to_clipboard(password)
            
            if success:
                self.view.show_success("パスワードをクリップボードにコピーしました")
            else:
                self.view.show_error("クリップボードへのコピーに失敗しました")
                
        except Exception as e:
            self.view.show_error(f"コピー中にエラーが発生しました: {str(e)}")
    
    def cleanup(self):
        """リソースのクリーンアップ"""
        if self.view:
            self.view.destroy()


# テスト用のメイン実行
if __name__ == "__main__":
    print("🎮 Controller層テスト開始")
    
    try:
        app = PasswordGeneratorController()
        print("✅ Controller初期化完了")
        app.run()
        
    except KeyboardInterrupt:
        print("\n👋 ユーザーによる終了")
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("🔚 Controller終了")
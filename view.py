"""
パスワード生成ツール - View層（修正版）
tkinterを使用したGUIインターフェース
"""

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Dict, Callable, Any


class PasswordGeneratorView:
    """パスワード生成ツールのGUI表示クラス"""
    
    def __init__(self):
        """ビューの初期化"""
        self.root = None
        self.password_visible = False  # パスワード表示状態
        
        # tkinter変数は setup_ui() で初期化する
        self.uppercase_var = None
        self.lowercase_var = None
        self.digits_var = None
        self.symbols_var = None
        self.length_var = None
        
        # 現在のパスワード
        self.current_password = ""
        
        # コールバック関数（Controller層から設定される）
        self.on_generate_callback: Callable = None
        self.on_copy_callback: Callable = None
        
        # UI初期化（この時点でrootが作成され、その後変数を初期化）
        self.setup_ui()
    
    def setup_ui(self):
        """ウィジェット配置とレイアウト構築"""
        # メインウィンドウを最初に作成
        self.root = tk.Tk()
        self.root.title("パスワード生成ツール v1.0")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # ここでtkinter変数を初期化（rootが存在する状態で）
        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.length_var = tk.IntVar(value=8)
        
        # スタイル設定
        style = ttk.Style()
        style.theme_use('clam')  # モダンなテーマ
        
        # メインフレーム
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # === 設定セクション ===
        settings_frame = ttk.LabelFrame(main_frame, text="📝 設定", padding="10")
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 文字種別セクション
        char_types_frame = ttk.Frame(settings_frame)
        char_types_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(char_types_frame, text="文字種別:").pack(anchor=tk.W)
        
        # チェックボックス（変数が初期化された後で作成）
        checkboxes_frame = ttk.Frame(char_types_frame)
        checkboxes_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.uppercase_check = ttk.Checkbutton(
            checkboxes_frame, text="大文字(A-Z)", 
            variable=self.uppercase_var
        )
        self.lowercase_check = ttk.Checkbutton(
            checkboxes_frame, text="小文字(a-z)", 
            variable=self.lowercase_var
        )
        self.digits_check = ttk.Checkbutton(
            checkboxes_frame, text="数字(0-9)", 
            variable=self.digits_var
        )
        self.symbols_check = ttk.Checkbutton(
            checkboxes_frame, text="記号(!@#$...)", 
            variable=self.symbols_var
        )
        
        # 2x2 グリッド配置
        self.uppercase_check.grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        self.lowercase_check.grid(row=0, column=1, sticky=tk.W)
        self.digits_check.grid(row=1, column=0, sticky=tk.W, padx=(0, 20))
        self.symbols_check.grid(row=1, column=1, sticky=tk.W)
        
        # 長さ設定
        length_frame = ttk.Frame(settings_frame)
        length_frame.pack(fill=tk.X)
        
        ttk.Label(length_frame, text="長さ:").pack(side=tk.LEFT)
        self.length_spinbox = ttk.Spinbox(
            length_frame, from_=8, to=64, width=10,
            textvariable=self.length_var
        )
        self.length_spinbox.pack(side=tk.LEFT, padx=(10, 0))
        ttk.Label(length_frame, text="(8-64文字)").pack(side=tk.LEFT, padx=(10, 0))
        
        # === 生成セクション ===
        generate_frame = ttk.LabelFrame(main_frame, text="⚙️ 生成", padding="10")
        generate_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.generate_button = ttk.Button(
            generate_frame, text="🔄 パスワード生成",
            command=self._on_generate_clicked
        )
        self.generate_button.pack()
        
        # === 結果セクション ===
        result_frame = ttk.LabelFrame(main_frame, text="📋 結果", padding="10")
        result_frame.pack(fill=tk.X)
        
        # パスワード表示
        ttk.Label(result_frame, text="生成されたパスワード:").pack(anchor=tk.W)
        
        password_display_frame = ttk.Frame(result_frame)
        password_display_frame.pack(fill=tk.X, pady=(5, 10))
        
        self.password_entry = ttk.Entry(
            password_display_frame, 
            state="readonly",
            font=("Consolas", 12)  # 等幅フォント
        )
        self.password_entry.pack(fill=tk.X)
        
        # アクションボタン
        action_buttons_frame = ttk.Frame(result_frame)
        action_buttons_frame.pack(fill=tk.X)
        
        self.display_button = ttk.Button(
            action_buttons_frame, text="👁 表示",
            command=self._on_toggle_visibility
        )
        self.copy_button = ttk.Button(
            action_buttons_frame, text="📋 コピー",
            command=self._on_copy_clicked
        )
        self.regenerate_button = ttk.Button(
            action_buttons_frame, text="🔄 再生成",
            command=self._on_generate_clicked
        )
        
        # ボタンを等間隔配置
        self.display_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.copy_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        self.regenerate_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # === ステータスバー ===
        self.status_var = tk.StringVar(value="準備完了")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, pady=(10, 0))
    
    def get_settings(self) -> Dict[str, Any]:
        """現在のUI設定値を取得"""
        return {
            "use_uppercase": self.uppercase_var.get(),
            "use_lowercase": self.lowercase_var.get(),
            "use_digits": self.digits_var.get(),
            "use_symbols": self.symbols_var.get(),
            "length": self.length_var.get()
        }
    
    def display_password(self, password: str):
        """生成されたパスワードを表示"""
        self.current_password = password
        
        # Entry を一時的に編集可能にして更新
        self.password_entry.config(state="normal")
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        
        # 表示状態に応じてshowプロパティを設定
        if self.password_visible:
            self.password_entry.config(show="", state="readonly")
        else:
            self.password_entry.config(show="*", state="readonly")
        
        self.status_var.set(f"パスワード生成完了 ({len(password)}文字)")
    
    def show_error(self, message: str):
        """エラーメッセージをダイアログで表示"""
        messagebox.showerror("エラー", message)
        self.status_var.set("エラーが発生しました")
    
    def show_success(self, message: str):
        """成功メッセージを表示"""
        self.status_var.set(message)
        # 3秒後にステータスをリセット
        self.root.after(3000, lambda: self.status_var.set("準備完了"))
    
    def set_callbacks(self, on_generate: Callable, on_copy: Callable):
        """Controller層からのコールバック関数を設定"""
        self.on_generate_callback = on_generate
        self.on_copy_callback = on_copy
    
    def run(self):
        """GUIアプリケーションを開始"""
        self.root.mainloop()
    
    def destroy(self):
        """ウィンドウを閉じる"""
        if self.root:
            self.root.destroy()
    
    # === プライベートメソッド（イベントハンドラ） ===
    
    def _on_generate_clicked(self):
        """生成ボタンクリック時の処理"""
        if self.on_generate_callback:
            self.on_generate_callback()
        else:
            self.show_error("生成機能が設定されていません")
    
    def _on_copy_clicked(self):
        """コピーボタンクリック時の処理"""
        if not self.current_password:
            self.show_error("コピーするパスワードがありません")
            return
            
        if self.on_copy_callback:
            self.on_copy_callback(self.current_password)
        else:
            self.show_error("コピー機能が設定されていません")
    
    def _on_toggle_visibility(self):
        """表示切り替えボタンクリック時の処理"""
        if not self.current_password:
            return
            
        self.password_visible = not self.password_visible
        
        # ボタンテキストを更新
        if self.password_visible:
            self.display_button.config(text="🙈 非表示")
        else:
            self.display_button.config(text="👁 表示")
        
        # パスワード表示を更新
        self.display_password(self.current_password)


# テスト用コード
if __name__ == "__main__":
    # View単体でのテスト実行
    def dummy_generate():
        print("生成ボタンが押されました")
        view.display_password("TestPassword123!")
    
    def dummy_copy(password):
        print(f"コピー: {password}")
        view.show_success("クリップボードにコピーしました")
    
    view = PasswordGeneratorView()
    view.set_callbacks(dummy_generate, dummy_copy)
    
    print("🎨 View層テスト開始")
    print("設定値:", view.get_settings())
    view.run()